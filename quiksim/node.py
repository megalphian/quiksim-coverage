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
    def __init__(self, dir_x, dir_y, cells_list):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.cells = list()

        for c in cells_list:
            cell = Cell(c[0], c[1], dir_x, dir_y)
            self.cells.append(cell)
        
        # Sort cells by the 
        if(dir_y == 0):
            is_reverse = dir_x == -1
            self.cells = sorted(self.cells, key=lambda x: x.centroid[0], reverse=is_reverse)
        elif(dir_x == 0):
            is_reverse = dir_y == -1
            self.cells = sorted(self.cells, key=lambda x: x.centroid[1], reverse=is_reverse)

    def get_path(self):
        return [cell.centroid for cell in self.cells]
