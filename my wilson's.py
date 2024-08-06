# This is my attempt at implement Wilson's algorithm, inspired by the ChatGPT version

# use node attributes for # of grains

import networkx as nx
import numpy as np


G = nx.Graph()

#create a "sandpile" graph 
G.add_node(0, grains=1, coord = (1,2))
G.add_node(1, grains=1, coord = (1,2))

#iterate over -n <= i <= n, and -n <= i <= j: and add a node at valid points, with 0 grains
