from GTSPPlanning.gtsp_file_prop import GTSPFileProperties

class GTSPSolver:

    def solve_GTSP_for_nodes(self, nodes, transition_graph):
        gtsp_prop = GTSPFileProperties()
        gtsp_prop.file_name = 'RankTouring'
        gtsp_prop.file_type = 'AGTSP'
        gtsp_prop.comment = 'GTSP file instance for Rank and Cell touring'
        gtsp_prop.edge_weight_type = 'EXPLICIT'
        gtsp_prop.edge_weight_format = 'FULL_MATRIX'