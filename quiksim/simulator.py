from robot import Robot
from node import replan_lm_nodes, Reconnection_Strategy, get_blocked_lm_nodes

from PathPlanner.main import PathPlanner
from config import DynamicsConfig

from PIL import Image

import itertools

class Environment:
    def __init__(self, base_env_img, cells):
        self.cells = cells
        self.initial_iop = self.generateIOP(base_env_img, cells)
        self.current_iop = self.initial_iop.copy()

    def generateIOP(self, base_env_img, cells):
        iop = Image.new('1', (base_env_img.width, base_env_img.height), (0))
        iop_px = iop.load()

        for cell in cells:
            for x in range(int(cell.bottom_left[0]), int(cell.top_right[0])):
                for y in range(int(cell.bottom_left[1]), int(cell.top_right[1])):
                    iop_px[x,y] = 255
        return iop
    
    def update_gt(self, gt_map):
        iop_px = self.current_iop.load()
        gt_map_px = gt_map.load()

        first_cell = self.cells[0]
        px_per_cell = abs(round(first_cell.bottom_left[0]) - round(first_cell.top_right[0])) * abs(round(first_cell.bottom_left[1]) - round(first_cell.top_right[1]))

        for cell in self.cells:
            blocked_px_per_cell = 0
            for x in range(round(cell.bottom_left[0]), round(cell.top_right[0])):
                for y in range(round(cell.bottom_left[1]), round(cell.top_right[1])):
                    if(gt_map_px[x,y] == 0):
                        blocked_px_per_cell += 1
            
            if(blocked_px_per_cell/px_per_cell > 0):
                cell.occupied = True
                for x in range(int(cell.bottom_left[0]), int(cell.top_right[0])):
                    for y in range(int(cell.bottom_left[1]), int(cell.top_right[1])):
                        iop_px[x,y] = 0

class PlanStep:
    def __init__(self) -> None:
        self.cell = None
        self.orientation = None

class SimManager:
    def __init__(self, init_nodes, base_env):
        # We have 2 environments, (i) intiial and (ii) ground truth
        # The initial can be used to create the robot's env representation
        # The ground truth will dictate the robot's observations.
        self.init_nodes = init_nodes
        self.cells = [cell for node in init_nodes for cell in node.cells]
        
        self.env = Environment(base_env, self.cells)
        self.robot = Robot(self.env)

        self.dynamics = DynamicsConfig()

    def replan_path_for_gt(self, observed_env, nodes):
        self.env.update_gt(observed_env)

        # Get blocked nodes and replan
        lm_paths, node_groups = get_blocked_lm_nodes(nodes, self.env.initial_iop)
        repaired_paths = []
        for path in lm_paths:
            repaired_paths.append(replan_lm_nodes(path, Reconnection_Strategy.preserve_tour))
            # repaired_paths.append(replan_lm_nodes(path))

        start_id = 0
        grouped_nodes = []

        for group in node_groups:
            pre_repair = list(range(start_id,group[0]))
            grouped_nodes.append([nodes[i] for i in pre_repair])
            grouped_nodes.append([nodes[i] for i in group])
            start_id = group[-1] + 1

        post_repair = list(range(start_id,len(nodes)))
        grouped_nodes.append([nodes[i] for i in post_repair])

        for i in range(len(lm_paths)):
            grouped_nodes[2*i + 1] = repaired_paths[i]

        nodes = list(itertools.chain.from_iterable(grouped_nodes))
        t_paths, t_costs, total_cost = self.connect_and_evaluate_nodes(nodes)

        return nodes, t_paths, t_costs, total_cost

    def connect_and_evaluate_nodes(self, nodes):
        path_planner = PathPlanner(self.env.current_iop, dyn_config=self.dynamics)

        t_paths, t_costs = path_planner.plan_transitions(nodes)

        total_node_cost = sum([node.get_length() for node in nodes]) / self.dynamics.get_lin_vel()
        total_cost = sum([cost[1] for cost in t_costs]) + total_node_cost

        return t_paths, t_costs, total_cost


    def execute_plan(self, plan_steps):
        # plan_steps: PlanStep[]

        for step in plan_steps:
            self.execute_step(step)

    def execute_step(self, step):
        self.robot.move(step.cell, step.orientation)