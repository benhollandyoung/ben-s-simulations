# What about implementing Sandpile but using NetworkX??


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


# Creates the multigraph - need multiple edges between vertices compatibility
def gridMultigraph(n):
    G = nx.MultiGraph()
    
    # Adding nodes
    for i in range(n):
        for j in range(n):
            G.add_node((i, j))
    
    # Adding edges
    for i in range(n):
        for j in range(n):
            if i > 0:
                G.add_edge((i-1, j), (i, j))  # Vertical edge
            if j > 0:
                G.add_edge((i, j-1), (i, j))  # Horizontal edge
    
    return G

# Creates the sandpile and configures it
def create_sandpile(n):
    #G = nx.grid_2d_graph(n, n)
    G = gridMultigraph(n)

    center = (n // 2, n // 2)
    radius = n // 2
    sink = 'sink'
    G.add_node(sink)

    inside_nodes = [] #in the disc
    sink_nodes = [] #in the sink

    for node in G.nodes():
        G.nodes[node]['grains'] = 0
        if node == sink:
            continue
        if np.linalg.norm(np.array(node) - np.array(center)) <= radius: #checkin in the disc
            inside_nodes.append(node)
        else:
            sink_nodes.append(node)
    
    #removes all the sink nodes into one, and redirects edges from sink nodes to one sink node
    for node in sink_nodes: 
        for neighbour in G.neighbors(node):
            if neighbour in inside_nodes:
                G.add_edge(neighbour, sink)
        G.remove_node(node)

    return G

class Sandpile:
    def __init__(self, n):
        self.n = n
        self.G = create_sandpile(n)
        self.radius = n // 2
        self.sinkIndex = len(self.G.nodes) - 1
        self.laplacian = nx.laplacian_matrix(self.G).toarray()
        self.laplacian = np.delete(self.laplacian, (self.sinkIndex), axis=0)
        self.laplacian_reduced = np.delete(self.laplacian, (self.sinkIndex), axis=1)

    # Converts between cartesian and matrix coordinates
    def cartToMatrix(self, point):
        x = point[0]
        y = point[1]
        return (self.radius-y,self.radius+x)

    def matrixToCart(self, point):
        x = point[0]
        y = point[1]
        return (y-self.radius, self.radius-x)
    
    # Topples at point, input in cartesian
    def topple(self, point):
        newNode = self.cartToMatrix(point)
        targetNodeIndex = 0
        grains = np.array([])
        for i, node in enumerate(self.G.nodes()):
            if node == newNode:
                targetNodeIndex = i
                grains = np.append(grains, self.G.nodes[node]['grains'])
            elif node == "sink":
                continue
            else:
                grains = np.append(grains, self.G.nodes[node]['grains'])
        

        # toppling from survey paper
        grains = grains - self.laplacian_reduced[targetNodeIndex, :]


        for i, node in enumerate(self.G.nodes()):
            if node == 'sink':
                continue
            else:
                self.G.nodes[node]['grains'] = int(grains[i])

    # Adds and removes grains from vertices, input in cartesian
    def addAt(self,point, num = 1):
        for _ in range(num):
            newNode = self.cartToMatrix(point)
            self.G.nodes()[newNode]['grains'] += 1
    def removeAt(self,point, num = 1):
        for _ in range(num):
            newNode = self.cartToMatrix(point)
            self.G.nodes()[newNode]['grains'] -= 1

    # Returns list of unstable vertices
    def unstable(self):
        return [self.matrixToCart(node) for node in self.G.nodes if self.G.degree[node] <= self.G.nodes[node]['grains']  ]

    # Stabilises the sandpile from current state
    def stabilise(self):
        unstableVertices = self.unstable()
        while len(unstableVertices) != 0:
            for entry in unstableVertices:
                point = (entry[0], entry[1])
                self.topple(point)
            unstableVertices = self.unstable()
    
    def set(self,config):
        for node in self.G.nodes:
            if node != 'sink':
                self.G.nodes[node]['grains'] = config[node]


    # Plotting using matplotlib
    def plot(self):
        data = nx.get_node_attributes(self.G, 'grains') 
        del data['sink']

        # Extract coordinates and values
        coordinates = list(data.keys())
        values = list(data.values())

        # Split coordinates into x and y components
        x_coords, y_coords = zip(*coordinates)

        # Create a scatter plot
        plt.figure(figsize=(10, 10))

        # Annotate the plot with values
        for (x,y) , value in data.items():
            newPoint = self.matrixToCart((x, y))
            if value < 5:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))
            elif value < 30:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='black', bbox=dict(facecolor='yellow', alpha=0.5))
            elif value < 50:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='orange', alpha=0.5))
            else:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='red', alpha=0.5))


        ax = plt.gca()
        ax.set_xlim([-1 - n//2, n//2 + 1])
        ax.set_ylim([-1 - n//2, n//2 + 1])

        # Set plot title and labels
        plt.title('Plot of Coordinates with # of grains')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.yscale
        plt.show()

# Creating the sandpile and configurating it
n = 5
sandpile = Sandpile(n)




# Random walk generator from start point to end_set
def random_walk_until(G,start, end_set):
    # random walk until end_set
    walk = [start]
    current = start
    while current not in end_set:
        neigbhs = list(G.neighbors(current))
        current = random.choice(neigbhs)
        walk.append(current)
    return walk, current




# Loop-erase a path

#LERW   
def loop_erased_random_walk(G, start, end_set):
    path, end = random_walk_until(G, start, end_set)
    #print(path)
    seen = set()
    newPath = []
    for node in path:
        if node in seen:
            idx = newPath.index(node)
             # remove newPath[idx + 1:] from seen
            for item in newPath[idx + 1:]:
                seen.remove(item)
            newPath = newPath[:idx+1]
           
        else:
            newPath.append(node)
            seen.add(node)

    return newPath, end


# plotting a loop-erased RW
def test():

        walk, end = loop_erased_random_walk(sandpile.G, (10,10), ['sink'])

        # Extract coordinates and values
        coordinates = walk

        # Create a scatter plot
        plt.figure(figsize=(10, 10))

        # Annotate the plot with values
        for point in walk:
            if point != 'sink':
                newPoint = sandpile.matrixToCart(point)
            
                plt.text(newPoint[0], newPoint[1], "0", fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))


        ax = plt.gca()
        ax.set_xlim([-1 - n//2, n//2 + 1])
        ax.set_ylim([-1 - n//2, n//2 + 1])

        # Set plot title and labels
        plt.title('Plot of Coordinates with distance')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.yscale
        plt.show()



# Wilson's algorithm - do this adding with a graph to get your uniform spanning tree and return that
def wilson_algorithm(G):
    # Start t0 = {sink}
    # Run RW from v1 until it hits t0, loop-erase it, attach to t0 to create t1
    # Run RW from v2 until it hits t1, loop-erase it, attach to t1 to create t2
    # Finish when we've exhausted the vertices
    # Create new directed graph as I go along, calculate the distance from sink as a node attribute, it is distance to its hitpoint + distance from hitpoint to sink, 
    # also store the node from G as a node attribute
    # another node attribute is the parent node which all have except the sink.
    # return the directed graph and have another graph transform it into the sandpile config using the distances with burning bijection
    # instead of t0, t1, etc just have current path and path (the main one to connect to)


    #first draft, still need to implement distances from sink 
    multi_d_graph = nx.DiGraph()
    multi_d_graph.add_node('sink', distance = 0)


    for node in G.nodes:
        if node != 'sink':
            rw, endNode = loop_erased_random_walk(G, node, multi_d_graph.nodes)
            rw.reverse()
            n = len(rw)
            if n > 1:
                multi_d_graph.add_node(rw[1], distance = multi_d_graph.nodes[endNode]["distance"]+1)
                multi_d_graph.add_edge(endNode,rw[1])

                for i in range(1,n):

                    multi_d_graph.add_node(rw[i], distance = multi_d_graph.nodes[rw[i-1]]["distance"]+1)
                    multi_d_graph.add_edge(rw[i-1],rw[i])



    return multi_d_graph


wilsons = wilson_algorithm(sandpile.G)


# some plotting functions
def plot(tree):
        data = nx.get_node_attributes(tree, 'distance') 
        del data['sink']

        # Extract coordinates and values
        coordinates = list(data.keys())
        values = list(data.values())

        # Split coordinates into x and y components
        x_coords, y_coords = zip(*coordinates)

        # Create a scatter plot
        plt.figure(figsize=(10, 10))

        # Annotate the plot with values
        for (x,y) , value in data.items():
            newPoint = sandpile.matrixToCart((x, y))
            if value < 5:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))
            elif value < 30:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='black', bbox=dict(facecolor='yellow', alpha=0.5))
            elif value < 50:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='orange', alpha=0.5))
            else:
                plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='red', alpha=0.5))


        ax = plt.gca()
        ax.set_xlim([-1 - n//2, n//2 + 1])
        ax.set_ylim([-1 - n//2, n//2 + 1])

        # Set plot title and labels
        plt.title('Plot of Coordinates with distance')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.yscale
        plt.show()

def plot2(tree):
    pos = nx.spring_layout(tree)

    nx.draw_networkx_nodes(tree, pos)
    nx.draw_networkx_labels(tree, pos)
    nx.draw_networkx_edges(tree, pos, edge_color='r', arrows = True)

    plt.show()


def plot3(tree):
    pos = nx.spring_layout(tree)  # You can use other layouts like nx.shell_layout, nx.kamada_kawai_layout, etc.

    # Draw the graph
    nx.draw(tree, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=20)

    # Display the graph
    plt.show()

plot3(wilsons)



# take a uniform spanning tree and turn into a recurrent sandpile config.
def treeToSandpile(sandpile):
    tree = wilson_algorithm(sandpile.G)
    G = sandpile.G
    # iterate through the nodes, except for the sink
    # create a dictionary storing the number of grains we should place
    # for each node, for every neighbour at distance 1 less, reduce the height, starting at degree in G, starting 
    positions = {}
    for node in tree.nodes:
        nodeDist = tree.nodes[node]['distance']
        if node != 'sink':
            #goal is to set positions[node] = #of grains at pos node
            height = G.degree(node) - 1 #the max it could possibly be
            found = False
            for neighb in G.neighbors(node):
                dist = tree.nodes[neighb]['distance']
                if dist + 1 < nodeDist:
                    height -= 1
                if dist+1 == nodeDist: # burnt in the previous step
                    if len(list(tree.successors(node))) > 0 and list(tree.successors(node))[0]  == neighb: # the chosen one in the ordering
                        found = True
                    if found:
                        height -= 1
            positions[node] = height
    return positions
#config = treeToSandpile(sandpile)
#sandpile.set(config)
#sandpile.plot()