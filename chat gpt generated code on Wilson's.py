# Generate a random walk on a disc sandpile on an nxn grid

# Starting from code from Chat GPT

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


# Apply this to the constructed Sandpile graph 

def random_walk(G, start, end_set):
    """Perform a random walk on G starting from 'start' until a vertex in 'end_set' is reached."""
    path = [start]
    current = start
    while current not in end_set:
        neighbors = list(G.neighbors(current))
        current = random.choice(neighbors)
        path.append(current)
    return path

def loop_erased_random_walk(G, start, end_set):
    """Perform a loop-erased random walk."""
    path = random_walk(G, start, end_set)
    # Loop erasure process
    seen = set()
    le_path = []
    for vertex in path:
        if vertex in seen:
            # Erase the loop
            idx = le_path.index(vertex)
            le_path = le_path[:idx+1]
        else:
            le_path.append(vertex)
            seen.add(vertex)
    return le_path

def wilson_algorithm(G, root):
    """Generate a uniformly random spanning tree of G using Wilson's algorithm starting from root."""
    T = nx.Graph()
    T.add_node(root)
    vertices = list(G.nodes())
    vertices.remove(root)
    random.shuffle(vertices)
    
    for vertex in vertices:
        le_path = loop_erased_random_walk(G, vertex, set(T.nodes))
        T.add_edges_from([(le_path[i], le_path[i+1]) for i in range(len(le_path)-1)])
    
    return T

# Create the grid graph
n = 10  # Define the size of the grid
G = nx.grid_2d_graph(n, n)

# Convert 2D grid positions to 1D for simplicity
pos = {(x, y): (x, y) for x, y in G.nodes()}
G = nx.convert_node_labels_to_integers(G)
root = 0  # Choose the root node

# Generate the spanning tree using Wilson's algorithm
T = wilson_algorithm(G, root)

# Plot the resulting spanning tree
plt.figure(figsize=(8, 8))
nx.draw(T, pos=pos, with_labels=False, node_size=50, node_color="blue")
plt.title("Spanning Tree using Wilson's Algorithm")
plt.show()
