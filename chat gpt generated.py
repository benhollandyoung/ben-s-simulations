import networkx as nx
import numpy as np

def create_disc_graph(n, radius):
    G = nx.grid_2d_graph(n, n)

    center = (n // 2, n // 2)
    new_node = 'sink'
    G.add_node(new_node)

    inside_nodes = []
    outside_nodes = []

    for node in G.nodes():
        if node == new_node:
            continue
        if np.linalg.norm(np.array(node) - np.array(center)) <= radius:
            print(node)
            inside_nodes.append(node)
        else:
            outside_nodes.append(node)
    
    for node in outside_nodes:
        for neighbor in G.neighbors(node):
            if neighbor in inside_nodes:
                G.add_edge(new_node, neighbor)
        G.remove_node(node)

    return G

# Parameters
n = 21  # Grid size (n x n)
radius = 10  # Radius of the disc

G = create_disc_graph(n, radius)

# Visualize the graph
import matplotlib.pyplot as plt

pos = {node: (node[1], -node[0]) for node in G.nodes() if node != 'outside'}
pos['outside'] = (n, -n)

nx.draw(G, pos, with_labels=True, node_size=100, font_size=8)
plt.show()
