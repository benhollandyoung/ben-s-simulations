# What about implementing Sandpile but using NetworkX??


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# Problem is the laplacian, not correctly setup


def create_sandpile(n):
    G = nx.grid_2d_graph(n, n)

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
    
    for node in sink_nodes: #removes all the sink nodes into one, and redirects edges from sink nodes to one sink node
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
        self.sinkIndex = 0
        for i, node in enumerate(self.G.nodes()):
            if node == 'sink':
                sinkIndex = i
        self.laplacian = nx.laplacian_matrix(self.G).toarray()
        self.laplacian = np.delete(self.laplacian, (self.sinkIndex), axis=0)
        self.laplacian_reduced = np.delete(self.laplacian, (self.sinkIndex), axis=1)


    def cartToMatrix(self, point):
        x = point[0]
        y = point[1]
        return (self.radius-y,self.radius+x)

    def matrixToCart(self, point):
        x = point[0]
        y = point[1]
        return (y-self.radius, self.radius-x)
    


    #input uses cartesian point    

    # Create np.array of grains from G.nodes(), note which index the desired point is at, then create reduced laplacian
    # create new np.array based off of paper, then reassign the grain attribute 
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

    
    def addAt(self,point):
        newNode = self.cartToMatrix(point)
        self.G.nodes()[newNode]['grains'] += 1
    def removeAt(self,point):
        newNode = self.cartToMatrix(point)
        self.G.nodes()[newNode]['grains'] -= 1

    def unstable(self):
        return [self.matrixToCart(node) for node in self.G.nodes if self.G.degree[node] <= self.G.nodes[node]['grains']  ]

    def stabilise(self):
        unstableVertices = self.unstable()
        while len(unstableVertices) != 0:
            for entry in unstableVertices:
                point = (entry[0], entry[1])
                self.topple(point)
            unstableVertices = self.unstable()
    
    

n = 5

sandpile = Sandpile(n)
for _ in range(10):
    sandpile.addAt((0,0))
print(sandpile.laplacian_reduced)

sandpile.stabilise()

def mToC(point, radius):
    x = point[0] 
    y = point[1]
    return (y-radius, radius-x)



#pos = {(x, y): (x, y) for x, y in sandpile.G.nodes()}
data = nx.get_node_attributes(sandpile.G, 'grains') 
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
    newPoint = mToC((x, y), n // 2)
    plt.text(newPoint[0], newPoint[1], str(value), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))


ax = plt.gca()
ax.set_xlim([-1 - n//2, n//2 + 1])
ax.set_ylim([-1 - n//2, n//2 + 1])

# Set plot title and labels
plt.title('Plot of Coordinates with # of grains')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.yscale
#plt.grid(True)
plt.show()

print(data)





