from robot import Robot

class Environment:
    def __init__(self):
        self.cells = None

class PlanStep:
    def __init__(self) -> None:
        self.cell = None
        self.orientation = None

class SimManager:
    def __init__(self, init_nodes):
        # We have 2 environments, (i) intiial and (ii) ground truth
        # The initial can be used to create the robot's env representation
        # The ground truth will dictate the robot's observations.
        self.init_nodes = init_nodes
        self.cells = [cell for node in init_nodes for cell in node.cells]

        print(len(self.cells))
        
        self.seed_env = Environment()
        self.gt_env = Environment()
        self.robot = Robot(self.seed_env)

    def execute_plan(self, plan_steps):
        # plan_steps: PlanStep[]

        for step in plan_steps:
            self.execute_step(step)

    def execute_step(self, step):
        self.robot.move(step.cell, step.orientation)