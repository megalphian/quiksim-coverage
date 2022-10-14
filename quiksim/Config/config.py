from enum import Enum

class DriveType(Enum):
    acceleration_based = 0
    velocity_based = 1

class VisGraphConfig:
    def __init__(self):

        self.erosion_kernel_size = 11
        self.dilation_kernel_size = 3

class DynamicsConfig:

    def __init__(self):
        self.drive_type = DriveType.velocity_based
        self.lin_vel_m = 1 # ms-1
        self.lin_acc_m = 0.5 # ms-2

        self.px_per_m = 20

        self.ang_vel = 30 # deg s-1
        # self.ang_vel = math.inf # deg s-1

    def get_lin_vel(self):
        return self.lin_vel_m * self.px_per_m

    def get_lin_acc(self):
        return self.lin_acc_m * self.px_per_m