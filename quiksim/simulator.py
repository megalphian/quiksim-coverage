from robot import Robot

from PIL import Image

from matplotlib import pyplot as plt

class Environment:
    def __init__(self, base_env_img, cells):
        self.cells = cells
        self.iop = self.generateIOP(base_env_img, cells)

    def generateIOP(self, base_env_img, cells):
        iop = Image.new('1', (base_env_img.width, base_env_img.height), (0))
        iop_px = iop.load()

        for cell in cells:
            for x in range(int(cell.bottom_left[0]), int(cell.top_right[0])):
                for y in range(int(cell.bottom_left[1]), int(cell.top_right[1])):
                    iop_px[x,y] = 255

        return iop
    
    def update_gt(self, gt_map):
        iop_px = self.iop.load()
        gt_map_px = gt_map.load()

        first_cell = self.cells[0]
        px_per_cell = abs(int(first_cell.bottom_left[0]) - int(first_cell.top_right[0])) * abs(int(first_cell.bottom_left[1]) - int(first_cell.top_right[1]))

        for cell in self.cells:
            blocked_px_per_cell = 0
            for x in range(int(cell.bottom_left[0]), int(cell.top_right[0])):
                for y in range(int(cell.bottom_left[1]), int(cell.top_right[1])):
                    if(gt_map_px[x,y] == 0):
                        blocked_px_per_cell += 1
            
            if(blocked_px_per_cell/px_per_cell >= 0.6):
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

    def replan_path_for_gt(self, observed_env, nodes):
        self.env.update_gt(observed_env)


    def execute_plan(self, plan_steps):
        # plan_steps: PlanStep[]

        for step in plan_steps:
            self.execute_step(step)

    def execute_step(self, step):
        self.robot.move(step.cell, step.orientation)