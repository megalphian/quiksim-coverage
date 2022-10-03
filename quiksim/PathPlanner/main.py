from PathPlanner.visibilityGraphPlanner import VisibilityGraphPlanner, create_cost_strategy

from config import VisGraphConfig, DynamicsConfig

class PathPlanner:

    def __init__(self, iop, 
                    vgconfig = VisGraphConfig(), 
                    dyn_config=DynamicsConfig()):
        self.vg_planner = VisibilityGraphPlanner(iop, vgconfig)

        self.dyn_config = dyn_config

    def plan_path(self, from_cell, to_cell):
        from_pt = from_cell.centroid
        to_pt = to_cell.centroid

        cost_strategy = create_cost_strategy(self.dyn_config, from_cell.cell_vec, to_cell.cell_vec)

        path = self.vg_planner.planning(from_pt[0], from_pt[1], to_pt[0], to_pt[1])
        cost = self.vg_planner.calculate_cost(path, cost_strategy)

        return (path, cost)

    def plan_transitions(self, nodes):
        t_paths = []
        t_costs = []
        
        for i in range(len(nodes)-1):
            t_path, cost = self.plan_path(nodes[i].cells[-1], nodes[i+1].cells[0])
            
            t_paths.append(t_path)
            t_costs.append(cost)
        
        t_path, cost = self.plan_path(nodes[-1].cells[-1], nodes[0].cells[0])
            
        t_paths.append(t_path)
        t_costs.append(cost)

        return t_paths, t_costs