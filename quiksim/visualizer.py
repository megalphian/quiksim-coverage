from PIL import Image

import matplotlib.pyplot as plt

from PathPlanner.main import PathPlanner

def plot_initial_nodes(iop, nodes):
    path_planner = PathPlanner(iop)

    fig, ax = plt.subplots()
    ax.imshow(iop)
    path_x = list()
    path_y = list()

    for i in range(len(nodes)-1):
        path_i = nodes[i].get_path()

        path_x += [pt[0] for pt in path_i]
        path_y += [pt[1] for pt in path_i]

        t_path, cost = path_planner.plan_path(nodes[i].cells[-1], nodes[i+1].cells[0])

        for i in range(1, len(t_path)-1):
            path_x.append(t_path[i][0])
            path_y.append(t_path[i][1])

        # print(cost)
    
    path_i = nodes[-1].get_path()

    path_x += [pt[0] for pt in path_i]
    path_y += [pt[1] for pt in path_i]
        
    ax.plot(path_x, path_y)
    
    plt.show()
