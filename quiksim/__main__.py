class Cell:
    def __init__(self, bottom_left, top_right):
        self.bottom_left = bottom_left
        self.top_right = top_right

        self.centroid = ((bottom_left.x + top_right.x)/2, (bottom_left.y + top_right.y)/2)

class Environment:
    def __init__(self):
        self.cells = None

class Robot:
    def __init__(self, environment):
        self.orientation = 0 # radians
        self.current_cell = None
        self.environment = environment
    
    



### DESIGN NOTES
# We have 2 environments, (i) intiial and (ii) ground truth
# The initial can be used to create the robot's env representation
# The ground truth will dictate the robot's observations.

# Inputs:
# Ranks, Cells, Path
# Parameters:
# Sensor model
# Lin and Ang velocity

# Use grid planner to choose path from one point to another
# Add the estimate to each motion -> even teleport motion
# Cost: length/velocity + turn angle/ angular velocity


