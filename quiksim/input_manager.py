import json
from node import Node

def get_nodes_from_file(filename):
    serialized_nodes = list()

    with open(filename, encoding='utf-8') as file:
        j = json.load(file)
    
    for node_raw in j:
        node = Node.from_rawcells(node_raw[0], node_raw[1], node_raw[2])
        serialized_nodes.append(node)

    return serialized_nodes
        

# We need the initial plan
# We then need the iop and the ground truth map

# Plan in cell format (order of cells and their dimensions)
# Ground truth map
# Check if the cells are occupied or not
