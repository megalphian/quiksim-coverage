from PathPlanner.visibilityGraphPlanner import VisibilityGraphPlanner, create_cost_strategy

from Config.config import VisGraphConfig, DynamicsConfig

class PathPlanner:

    def __init__(self, iop, 
                    vg_config = VisGraphConfig(), 
                    dyn_config=DynamicsConfig()):

        self.iop = iop

        self.vg_config = vg_config
        self.dyn_config = dyn_config

        self.vg_planner = VisibilityGraphPlanner(self.iop, self.vg_config)

    def plan_path(self, from_cell, to_cell):
        from_pt = from_cell.centroid
        to_pt = to_cell.centroid

        cost_strategy = create_cost_strategy(self.dyn_config, from_cell.cell_vec, to_cell.cell_vec)

        path = self.vg_planner.planning(from_pt[0], from_pt[1], to_pt[0], to_pt[1])
        cost = self.vg_planner.calculate_cost(path, cost_strategy)

        return (path, cost)

    def _refresh_vg(self):
        self.vg_planner = VisibilityGraphPlanner(self.iop, self.vg_config)

    def plan_transitions(self, nodes):
        
        # Assuming the node list is NOT cyclic (first node != last node)
        if(nodes[0] == nodes[-1]):
            raise ValueError("plan_transitions: The node list received is cyclic. Something wrong!")

        t_paths = []
        t_costs = []

        self._refresh_vg()
        
        for i in range(len(nodes)):
            next_id = (i+1) % len(nodes)

            t_path, cost = self.plan_path(nodes[i].cells[-1], nodes[next_id].cells[0])
            
            t_paths.append(t_path)
            t_costs.append(cost)

        return t_paths, t_costs

    def connect_and_evaluate_nodes(self, nodes):
        
        # Assuming the node list is NOT cyclic (first node != last node)
        if(nodes[0] == nodes[-1]):
            raise ValueError("connect_and_evaluate_nodes: The node list received is cyclic. Something wrong!")

        t_paths, t_costs = self.plan_transitions(nodes)

        total_node_length = sum([node.get_length() for node in nodes])
        total_node_cost = sum([node.get_time_to_cover(self.dyn_config) for node in nodes])

        total_cost = sum([cost[1] for cost in t_costs]) + total_node_cost
        total_length = (sum([cost[0] for cost in t_costs]) + total_node_length) / self.dyn_config.px_per_m

        print(total_node_cost)
        print(sum([cost[1] for cost in t_costs]))

        return t_paths, t_costs, total_cost, total_length