class Robot:
    def __init__(self, seed_env):
        self.orientation = 0 # radians
        self.current_cell = None
        self.env_state = seed_env

        self.coverage_time = 0

    def move(self, to_cell, to_orientation):
        self.current_cell = to_cell