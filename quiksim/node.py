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

def split_nodes(nodes):
    new_nodes = list()
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
        
        node.cells = cell_groups[0]
        for i in range(1, len(cell_groups)):
            new_node = Node(cell_groups[i])
            sub_nodes.append(new_node)

        new_nodes += sub_nodes
    
    return new_nodes
