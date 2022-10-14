import matplotlib.pyplot as plt

class ColourScheme:
    horizontalColour = '#e66101'
    verticalColour = '#5e3c99'
    transitionColour = '#58c565'
    robotEdgeColour = '#C3423F'
    robotFaceColour = '#FDE74C'

    finalPathColour = 'blue'

def plot_nodes(iop, nodes, t_paths, base_img = None):
    fig, ax = plt.subplots()
    if(base_img is None):
        base_img = iop
    ax.imshow(base_img)

    for i in range(len(nodes)):
        path_i = nodes[i].get_path()

        path_x = [pt[0] for pt in path_i]
        path_y = [pt[1] for pt in path_i]

        color = ColourScheme.horizontalColour if nodes[i].dir_y == 0 else ColourScheme.verticalColour 

        ax.plot(path_x, path_y, color=color)

        try:
            t_path = t_paths[i]

            if(t_path is not None):
                t_path_x = [t_pt[0] for t_pt in t_path]
                t_path_y = [t_pt[1] for t_pt in t_path]

                ax.plot(t_path_x, t_path_y, color=ColourScheme.transitionColour)
            else:
                print('Missed transition!')
        except:
            pass
