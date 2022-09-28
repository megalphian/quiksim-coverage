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

    def execute_plan(self, plan_steps):
        # plan_steps: PlanStep[]

        for step in plan_steps:
            self.execute_step(step)

    def execute_step(self, step):
        self.robot.move(step.cell, step.orientation)