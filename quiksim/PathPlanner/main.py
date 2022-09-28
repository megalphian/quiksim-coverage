from PathPlanner.visibilityGraphPlanner import VisibilityGraphPlanner, create_cost_strategy

from PathPlanner.plannerUtils import DriveType

class VisGraphConfig:
    def __init__(self):

        self.erosion_kernel_size = 11
        self.dilation_kernel_size = 3

class DynamicsConfig:

    def __init__(self):
        self.drive_type = DriveType.acceleration_based
        self.lin_vel_m = 1 # ms-1
        self.lin_acc_m = 0.5 # ms-2

        self.px_per_m = 20

        self.ang_vel = 30 # deg s-1
        # self.ang_vel = math.inf # deg s-1

    def get_lin_vel(self):
        return self.lin_vel_m * self.px_per_m

    def get_lin_acc(self):
        return self.lin_acc_m * self.px_per_m

class PathPlanner:

    def __init__(self, iop, config=VisGraphConfig()):
        self.vg_planner = VisibilityGraphPlanner(iop, config)

        self.dyn_config = DynamicsConfig()

    def plan_path(self, from_cell, to_cell):
        from_pt = from_cell.centroid
        to_pt = to_cell.centroid

        cost_strategy = create_cost_strategy(self.dyn_config, from_cell.cell_vec, to_cell.cell_vec)

        path = self.vg_planner.planning(from_pt[0], from_pt[1], to_pt[0], to_pt[1])
        cost = self.vg_planner.calculate_cost(path, cost_strategy)

        return (path, cost)