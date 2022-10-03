from PathPlanner.main import PathPlanner

from enum import Enum
import math

class Cell:
    def __init__(self, bottom_left, top_right, dir_x, dir_y):
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.dir_x = dir_x
        self.dir_y = dir_y

        self.cell_vec = [self.dir_x, self.dir_y]

        self.centroid = ((bottom_left[0] + top_right[0])/2, (bottom_left[1] + top_right[1])/2)

        self.occupied = False

class Node:
    def __init__(self, cells):
        
        assert(len(cells) > 0)
        self.cells = cells

        dir_x = cells[0].dir_x
        dir_y = cells[0].dir_y
        
        # Sort cells by the 
        if(dir_y == 0):
            is_reverse = dir_x == -1
            self.cells = sorted(self.cells, key=lambda x: x.centroid[0], reverse=is_reverse)
        elif(dir_x == 0):
            is_reverse = dir_y == -1
            self.cells = sorted(self.cells, key=lambda x: x.centroid[1], reverse=is_reverse)

    @classmethod
    def from_rawcells(cls, dir_x, dir_y, raw_cell_list):
        cells = list()
        for c in raw_cell_list:
            cell = Cell(c[0], c[1], dir_x, dir_y)
            cells.append(cell)
        return cls(cells)

    def get_path(self):
        return [cell.centroid for cell in self.cells]

    def get_length(self):
        path = self.get_path()
        start_pt = path[0]
        end_pt = path[-1]

        length = math.sqrt((end_pt[1] - start_pt[1])**2 + (end_pt[0] - start_pt[0])**2)

        return length

def get_blocked_lm_nodes(nodes, iop):
    path_planner = PathPlanner(iop)

    blocked_node_groups = list()
    blocked_lm_paths = list()

    last_lm_path = None
    last_group = []

    for i in range(len(nodes)):
        if(any([cell.occupied for cell in nodes[i].cells])):
            if(last_lm_path is None):
                last_lm_path = [nodes[i]]
                last_group.append(i)
            else:
                _, cost = path_planner.plan_path(last_lm_path[-1].cells[-1], nodes[i].cells[0])
                if(cost[0] <= 2 * 16):
                    last_lm_path.append(nodes[i])
                    last_group.append(i)
                else:
                    blocked_lm_paths.append(last_lm_path.copy())
                    blocked_node_groups.append(last_group.copy())

                    last_lm_path = [nodes[i]]
                    last_group = [i]
    if(last_lm_path):
        blocked_lm_paths.append(last_lm_path.copy())
        blocked_node_groups.append(last_group.copy())

    return blocked_lm_paths, blocked_node_groups

class Reconnection_Strategy(Enum):
    preserve_tour = 0
    cover_individual = 1

def split_nodes(nodes, recon_strat = Reconnection_Strategy.preserve_tour):
    new_nodes = list()

    is_even = (len(nodes) % 2) == 0

    for node in nodes:
        sub_nodes = [node]
        cell_occ = [cell.occupied for cell in node.cells]
        occ_cells = [-1]
        
        if(any(cell_occ)):
            for i in range(len(cell_occ)):
                if(cell_occ[i]):
                    occ_cells.append(i)

        occ_cells.append(len(cell_occ))

        cell_groups = []
        for i in range(len(occ_cells)-1):
            cell_slice = node.cells[occ_cells[i]+1:occ_cells[i+1]]
            if(len(cell_slice) > 0):
                cell_groups.append(cell_slice)
        
        node.cells = cell_groups[0] if len(cell_groups) > 1 else []
        for i in range(1, len(cell_groups)):
            new_node = Node(cell_groups[i])
            sub_nodes.append(new_node)

        new_nodes += sub_nodes

    if(recon_strat == Reconnection_Strategy.cover_individual):
        sided_nodes = [[new_nodes[0]], []]

        same_side_ct = 0
        side = 1
        for i in range(1, len(new_nodes) - is_even):
            if(same_side_ct >= 2):
                side = 0 if side == 1 else 1
                same_side_ct = 0
            sided_nodes[side].append(new_nodes[i])
            same_side_ct += 1
        
        temp_nodes = sided_nodes[0] + sided_nodes[1]
        if(is_even):
            temp_nodes += [new_nodes[-1]]
        
        new_nodes = temp_nodes
    
    return new_nodes
