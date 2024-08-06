import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_sandpile(n):
    G = nx.grid_2d_graph(n, n)
    
    center = (n // 2, n // 2)
    radius = n // 2
    sink = 'sink'
    G.add_node(sink)

    inside_nodes = [] # in the disc
    sink_nodes = [] # in the sink

    for node in G.nodes():
        G.nodes[node]['grains'] = 0
        if node == sink:
            continue
        if np.linalg.norm(np.array(node) - np.array(center)) <= radius: # check in the disc
            inside_nodes.append(node)
        else:
            sink_nodes.append(node)
    
    for node in sink_nodes: # redirects edges from sink nodes to one sink node
        neighbors = list(G.neighbors(node))
        for neighbor in neighbors:
            if neighbor in inside_nodes:
                G.add_edge(sink, neighbor)
        G.remove_node(node)

    # Recalculate degrees to ensure correctness
    for node in G.nodes():
        if node != sink:
            G.nodes[node]['degree'] = len(list(G.neighbors(node)))

    return G

# Parameters
n = 10
sink_position = (n, -n)

# Step 1: Create the graph
G = create_sandpile(n)

# Step 2: Compute positions for the nodes
pos = nx.spring_layout(G)

# Step 3: Set the position of the 'sink' node manually
pos['sink'] = sink_position

# Step 4: Draw the graph
plt.figure(figsize=(12, 12))

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# Draw edges
nx.draw_networkx_edges(G, pos, width=2)

# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

# Highlight the sink node
nx.draw_networkx_nodes(G, pos, nodelist=['sink'], node_color='r', node_size=1000)

# Step 5: Display the graph
plt.title("NetworkX Graph with Sink Node at Fixed Position")
plt.show()
