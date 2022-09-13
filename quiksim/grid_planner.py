"""
Base Source: https://github.com/AtsushiSakai/PythonRobotics/blob/master/PathPlanning/Dijkstra/dijkstra.py
Base author: Atsushi Sakai(@Atsushi_twi)

Modified by Megnath Ramesh for this specific application
"""

import matplotlib.pyplot as plt
import math

def getAvgPxValue(img_px, i, j):
    # Only applicable for b/w images
        return img_px.getpixel((i,j))

class Node:
    def __init__(self, x, y, cost, parent_index):
        self.x = x  # index of grid
        self.y = y  # index of grid
        self.cost = cost
        self.parent_index = parent_index  # index of previous Node

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(
            self.cost) + "," + str(self.parent_index)

    @staticmethod
    def verify_node(node, bounds, occupancy_grid):
        px = node.x
        py = node.y

        if px < bounds[0]:
            return False
        if py < bounds[2]:
            return False
        if px > bounds[1]:
            return False
        if py > bounds[3]:
            return False

        if getAvgPxValue(occupancy_grid, px, py) == 0:
            return False

        return True


class DijkstraPlanner:

    def __init__(self, preprocessed_map, planning_resolution):
        """
        Initialize map for Dijkstra planning
        resolution: grid resolution [m]
        rr: robot radius[m]
        """

        self.occupancy_grid = preprocessed_map.rect_contraction

        self.bounds = preprocessed_map.parent_map.bounds

        self.planning_resolution = planning_resolution
        self.motion = self.get_motion_model()

    def planning(self, sx, sy):
        """
        dijkstra path search
        input:
            s_x: start x position [m]
            s_y: start y position [m]
        output:
            planned_set: a dict of the shortest paths from the start to every point in the map
        """

        start_node = Node(sx, sy, 0.0, -1)

        open_set = dict()
        planned_set = dict()
        open_set[(start_node.x, start_node.y)] = start_node

        while len(open_set) != 0:
            c_id = min(open_set, key=lambda o: open_set[o].cost)
            current = open_set.pop(c_id)

            # Add it to the closed set
            planned_set[c_id] = current.cost

            # expand search grid based on motion model
            for move_x, move_y, move_cost in self.motion:
                node = Node(current.x + (move_x * self.planning_resolution),
                                 current.y + (move_y * self.planning_resolution),
                                 current.cost + move_cost, c_id)
                n_id = (node.x, node.y)

                if n_id in planned_set:
                    continue

                if not Node.verify_node(node, self.bounds, self.occupancy_grid):
                    continue

                if n_id not in open_set:
                    open_set[n_id] = node  # Discover a new node
                else:
                    if open_set[n_id].cost >= node.cost:
                        # This path is the best until now. record it!
                        open_set[n_id] = node

        return planned_set

    @staticmethod
    def get_motion_model():
        # dx, dy, cost
        motion = [[1, 0, 1],
                  [0, 1, 1],
                  [-1, 0, 1],
                  [0, -1, 1],
                #   [-1, -1, math.sqrt(2)],
                #   [-1, 1, math.sqrt(2)],
                #   [1, -1, math.sqrt(2)],
                #   [1, 1, math.sqrt(2)]
                ]

        return motion