from PIL import Image

import matplotlib.pyplot as plt

from PathPlanner.main import PathPlanner

def plot_nodes(iop, nodes, t_paths):
    fig, ax = plt.subplots()
    ax.imshow(iop)

    for i in range(len(nodes)):
        path_i = nodes[i].get_path()

        path_x = [pt[0] for pt in path_i]
        path_y = [pt[1] for pt in path_i]

        try:
            t_path = t_paths[i]

            if(t_path is not None):
                for i in range(1, len(t_path)):
                    path_x.append(t_path[i][0])
                    path_y.append(t_path[i][1])
            else:
                print('Missed transition!')
        except:
            pass

        ax.plot(path_x, path_y)
