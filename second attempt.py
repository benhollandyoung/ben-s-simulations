import numpy as np

# Initial setup of nxn grid
n = 5
m = n // 2
#n odd is more useful as I have an origin

grid = np.zeros((n,n))





# Converting to and from cartesian coordinates 
        
def cartToMatrix(point):
    x = point[0]
    y = point[1]
    
    return (m-y,m+x)

def matrixToCart(point):
    x = point[0]
    y = point[1]
    return (y-m, m-x)



# Setting invalid points to -1
for i in range(n):
    for j in range(n):
        point = (i,j)
        x, y = matrixToCart(point)
        if x**2 + y**2 > m**2:
            grid[i,j] = -1

# Return degree of a vertex, using matrix coordinates
def degree(point):
    x,y = matrixToCart(point)
    if abs(x) == m or abs(y) == m:
        return 2 #1 valid neighbour + sink
    elif abs(x) == m - 1 and abs(y) == m - 1:
        return 3 #2 valid neighbours + sink
    else:
        return 4 #4 valid neighbours, no sink
# QUESTION: Should I count the sink only once or several times?


# Add/remove at certain coordinate, using matrix coordinates         
    
def addAt(point):
    x, y = point[0], point[1]
    grid[x,y] += 1
def removeAt(point):
    x, y = point[0], point[1]
    grid[x,y] -= 1





# Topple at certain coordinate, using matrix coordinates ADD THE UNSTABLE RETURN ARRAY
def toppleAt(point):
    x, y = point[0], point[1]
    sinkNeighb = 0
    for i in [-1,1]:
        if x + i < n and x + i >= 0 :
            newPoint = (x+i, y)
            if grid[newPoint[0],newPoint[1]] != -1:
                removeAt(point)
                addAt(newPoint)
            else:
                sinkNeighb += 1


    for i in [-1,1]:
        if y + i < n and y + i >= 0 :
            newPoint = (x, y+i)
            if grid[newPoint[0],newPoint[1]] != -1:
                removeAt(point)
                addAt(newPoint)
            else:
                sinkNeighb += 1
    # To only count the sink as one vertex in the degree
    if sinkNeighb > 0:
        removeAt(point)


# For now, use a brute-force method to find the unstable vertices i.e. creating mask, and then scan through that always toppling the first one that is True
# This will be slow but should work for now

# Returns a list of the unstable vertices in matrix coordinates format, not tuples in 2d-array format

def unstable():
    arr = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            if grid[i,j] != -1:
                arr[i,j] = grid[i,j] >= degree((i,j))
            else:
                arr[i,j] = False
    return np.argwhere(arr == 1)

# Stabilises the grid through toppling
def stabilise():
    unstableVertices = unstable()
    while len(unstableVertices) != 0:
        for entry in unstableVertices:
            point = (entry[0], entry[1])
            toppleAt(point)
        unstableVertices = unstable()

addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((-1,1)))
addAt(cartToMatrix((-1,1)))
addAt(cartToMatrix((-1,1)))
addAt(cartToMatrix((-1,1)))
addAt(cartToMatrix((-2,0)))
addAt(cartToMatrix((-2,0)))
addAt(cartToMatrix((-2,0)))
addAt(cartToMatrix((-2,0)))
addAt(cartToMatrix((0,-2)))
addAt(cartToMatrix((0,-2)))
addAt(cartToMatrix((0,-2)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))
addAt(cartToMatrix((1,0)))

print(grid)
stabilise()
print(grid)
