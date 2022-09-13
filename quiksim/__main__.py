class Cell:
    def __init__(self, bottom_left, top_right):
        self.bottom_left = bottom_left
        self.top_right = top_right

        self.centroid = ((bottom_left.x + top_right.x)/2, (bottom_left.y + top_right.y)/2)

        self.occupied = False

class Environment:
    def __init__(self):
        self.cells = None

class Robot:
    def __init__(self, seed_env):
        self.orientation = 0 # radians
        self.current_cell = None
        self.env_state = seed_env

        self.coverage_time = 0

    def move(self, to_cell, to_orientation):
        self.current_cell = to_cell

class PlanStep:
    def __init__(self) -> None:
        self.cell = None
        self.orientation = None

class SimManager:
    def __init__(self):
        # We have 2 environments, (i) intiial and (ii) ground truth
        # The initial can be used to create the robot's env representation
        # The ground truth will dictate the robot's observations.
        self.seed_env = Environment()
        self.gt_env = Environment()
        self.robot = Robot(self.seed_env)

    def execute_plan(self, plan_steps):
        # plan_steps: PlanStep[]

        for step in plan_steps:
            self.execute_step(step)

    def execute_step(self, step):
        self.robot.move(step.cell, step.orientation)





### DESIGN NOTES


# Inputs:
# Ranks, Cells, Path
# Parameters:
# Sensor model
# Lin and Ang velocity

# Use grid planner to choose path from one point to another
# Add the estimate to each motion -> even teleport motion
# Cost: length/velocity + turn angle/ angular velocity


