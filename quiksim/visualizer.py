from PIL import Image

import matplotlib.pyplot as plt

def plot_initial_nodes(original_env, nodes):
    fig, ax = plt.subplots()
    ax.imshow(original_env)
    path_x = list()
    path_y = list()

    for node in nodes:
        path = node.get_path()
        path_x += [pt[0] for pt in path]
        path_y += [pt[1] for pt in path]
        
    ax.plot(path_x, path_y)
    
    plt.show()
