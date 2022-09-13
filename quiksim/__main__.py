from input_manager import get_nodes_from_file
from simulator import SimManager

nodes = get_nodes_from_file('serialized_nodes.txt')
sim_manager = SimManager(nodes)

### DESIGN NOTES

# Inputs:
# Parameters:
# Sensor model
# Lin and Ang velocity

# Use grid planner to choose path from one point to another
# Add the estimate to each motion -> even teleport motion
# Cost: length/velocity + turn angle/ angular velocity


