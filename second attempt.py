import numpy as np

n = 5
m = n // 2
#n odd is more useful as I have an origin

grid = np.zeros((n,n))





# Be able to use cartesian coordinates 
        
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

# Add/remove at certain coordinate, using matrix coordinates

def addAt(point):
    x, y = point[0], point[1]
    grid[x,y] += 1
def removeAt(point):
    x, y = point[0], point[1]
    grid[x,y] -= 1

# Return degree of a vertex, using matrix coordinates
def degree(point):
    x,y = matrixToCart(point)
    if x == m or y == m:
        return 1
    elif abs(x) == m - 1 and abs(y) == m - 1:
        return 2
    else:
        return 4




# Topple at certain coordinate, using matrix coordinates ADD THE UNSTABLE RETURN ARRAY
def toppleAt(point):
    x, y = point[0], point[1]
    unstable = []
    for i in [-1,1]:
        if x + i < n and x + i >= 0 :
            newPoint = (x+i, y)
            if grid[newPoint[0],newPoint[1]] != -1:
                removeAt(point)
                addAt(newPoint)
                if grid[newPoint[0],newPoint[1]] >= degree(newPoint):
                    unstable.append(newPoint)


    for i in [-1,1]:
        if y + i < n and y + i >= 0 :
            newPoint = (x, y+i)
            if grid[newPoint[0],newPoint[1]] != -1:
                removeAt(point)
                addAt(newPoint)
                if grid[newPoint[0],newPoint[1]] >= degree(newPoint):
                    unstable.append(newPoint)
    return unstable
            
            
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
toppleAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
addAt(cartToMatrix((0,0)))
toppleAt(cartToMatrix((0,0)))
print(grid)

    #return the unstable points 