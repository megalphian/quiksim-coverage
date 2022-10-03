from input_manager import get_nodes_from_file
from simulator import SimManager

from visualizer import plot_nodes
from image_utils import convert_rgb_to_bw

from PIL import Image

base_dir = '52119'

nodes = get_nodes_from_file(base_dir + '/' + 'serialized_nodes.txt')
original_env = convert_rgb_to_bw(Image.open(base_dir + '/' + 'original_map.png'))
observed_env = convert_rgb_to_bw(Image.open(base_dir + '/' + 'observed_map.png'))

import matplotlib.pyplot as plt
plt.imshow(observed_env)

sim_manager = SimManager(nodes, original_env)

t_paths, _, initial_cost = sim_manager.connect_and_evaluate_nodes(nodes)
print("Initial Path cost:", initial_cost)

plot_nodes(sim_manager.env.current_iop, nodes, t_paths)

nodes, t_paths, t_costs, total_cost = sim_manager.replan_path_for_gt(observed_env, nodes)

print("Total Replanned Cost:", total_cost)

plot_nodes(sim_manager.env.current_iop, nodes, t_paths)

sim_manager.env.current_iop.save('final_iop.png')

### DESIGN NOTES

# Inputs:
# Parameters:
# Sensor model
# Lin and Ang velocity

# Use grid planner to choose path from one point to another
# Add the estimate to each motion -> even teleport motion
# Cost: length/velocity + turn angle/ angular velocity


