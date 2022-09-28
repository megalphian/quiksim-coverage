from tracemalloc import start
from input_manager import get_nodes_from_file
from simulator import SimManager

from visualizer import plot_nodes
from image_utils import convert_rgb_to_bw

from node import split_nodes, Reconnection_Strategy, get_blocked_lm_nodes

from PIL import Image

import itertools

base_dir = 'Map-9'

nodes = get_nodes_from_file(base_dir + '/' + 'serialized_nodes.txt')
original_env = convert_rgb_to_bw(Image.open(base_dir + '/' + 'original_map.png'))
observed_env = convert_rgb_to_bw(Image.open(base_dir + '/' + 'observed_map-multi.png'))

sim_manager = SimManager(nodes, original_env)
# plot_nodes(sim_manager.env.iop, nodes)

sim_manager.replan_path_for_gt(observed_env, nodes)
# plot_nodes(sim_manager.env.iop, nodes)

# Get blocked nodes and replan
lm_paths, node_groups = get_blocked_lm_nodes(nodes, sim_manager.env.iop)
repaired_paths = []
for path in lm_paths:
    repaired_paths.append(split_nodes(path, Reconnection_Strategy.cover_individual))
    # repaired_paths.append(split_nodes(path))

start_id = 0
grouped_nodes = []

for group in node_groups:
    pre_repair = list(range(start_id,group[0]))
    grouped_nodes.append([nodes[i] for i in pre_repair])
    grouped_nodes.append([nodes[i] for i in group])
    start_id = group[-1] + 1

post_repair = list(range(start_id,len(nodes)))
grouped_nodes.append([nodes[i] for i in post_repair])

for i in range(len(lm_paths)):
    grouped_nodes[2*i + 1] = repaired_paths[i]

nodes = list(itertools.chain.from_iterable(grouped_nodes))
plot_nodes(sim_manager.env.iop, nodes)
### DESIGN NOTES

# Inputs:
# Parameters:
# Sensor model
# Lin and Ang velocity

# Use grid planner to choose path from one point to another
# Add the estimate to each motion -> even teleport motion
# Cost: length/velocity + turn angle/ angular velocity


