class Cell:
    def __init__(self, bottom_left, top_right):
        self.bottom_left = bottom_left
        self.top_right = top_right

        self.centroid = ((bottom_left[0] + top_right[0])/2, (bottom_left[1] + top_right[1])/2)

        self.occupied = False

class Node:
    def __init__(self, dir_x, dir_y, cells_list):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.cells = list()

        for c in cells_list:
            cell = Cell(c[0], c[1])
            self.cells.append(cell)
