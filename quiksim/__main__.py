from input_manager import get_nodes_from_file
from simulator import SimManager

from visualizer import plot_initial_nodes

from PIL import Image

base_dir = 'Map-9'

nodes = get_nodes_from_file(base_dir + '/' + 'serialized_nodes.txt')
original_env = Image.open(base_dir + '/' + 'original_map.png')
observed_env = Image.open(base_dir + '/' + 'observed_map.png')

sim_manager = SimManager(nodes)

plot_initial_nodes(observed_env, nodes)

### DESIGN NOTES

# Inputs:
# Parameters:
# Sensor model
# Lin and Ang velocity

# Use grid planner to choose path from one point to another
# Add the estimate to each motion -> even teleport motion
# Cost: length/velocity + turn angle/ angular velocity


