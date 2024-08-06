# Creating a class Sandpile with the following functionality, user works with cartesian coords
# Add/remove at point
# Access to the current configuration, -1s to be ignored
# Topple at point
# Stabilise 

import numpy as np 

class Sandpile:
    def __init__(self, n, initial):

        self.n = n
        self.grid = initial
        self.m = n // 2
        # Setting invalid points to -1
        for i in range(self.n):
            for j in range(self.n):
                point = (i,j)
                x, y = self.matrixToCart(point)
                if x**2 + y**2 > self.m**2:
                    self.grid[i,j] = -1

    # Switching between coordinates
    def cartToMatrix(self, point):
        x = point[0]
        y = point[1]
    
        return (self.m-y,self.m+x)

    def matrixToCart(self, point):
        x = point[0]
        y = point[1]
        return (y-self.m, self.m-x)
    

    # Return degree of a vertex, using matrix coordinates
    def degree(self,point):
        x,y = self.matrixToCart(point)
        if abs(x) == self.m or abs(y) == self.m:
            return 2 #1 valid neighbour + sink
        elif abs(x) == self.m - 1 and abs(y) == self.m - 1:
            return 3 #2 valid neighbours + sink
        else:
            return 4 #4 valid neighbours, no sink
    # QUESTION: Should I count the sink only once or several times?
        
    # Add/remove at certain coordinate, using matrix coordinates         
    def addAt(self,point):
        x, y = point[0], point[1]
        self.grid[x,y] += 1
    def removeAt(self,point):
        x, y = point[0], point[1]
        self.grid[x,y] -= 1

    # Topple at certain coordinate, using matrix coordinates 
    def toppleAt(self,point):
        x, y = point[0], point[1]
        sinkNeighb = 0
        for i in [-1,1]:
            if x + i < self.n and x + i >= 0 :
                newPoint = (x+i, y)
                if self.grid[newPoint[0],newPoint[1]] != -1:
                    self.removeAt(point)
                    self.addAt(newPoint)
                else:
                    sinkNeighb += 1


        for i in [-1,1]:
            if y + i < self.n and y + i >= 0 :
                newPoint = (x, y+i)
                if self.grid[newPoint[0],newPoint[1]] != -1:
                    self.removeAt(point)
                    self.addAt(newPoint)
                else:
                    sinkNeighb += 1
        # To only count the sink as one vertex in the degree
        if sinkNeighb > 0:
            self.removeAt(point)

    # Returns a list of the unstable vertices in matrix coordinates format, not tuples in 2d-array format

    def unstable(self):
        arr = np.zeros((self.n,self.n))
        for i in range(0,self.n):
            for j in range(0,self.n):
                if self.grid[i,j] != -1:
                    arr[i,j] = self.grid[i,j] >= self.degree((i,j))
                else:
                    arr[i,j] = False
        return np.argwhere(arr == 1)

    # Stabilises the grid through toppling
    def stabilise(self):
        unstableVertices = self.unstable()
        while len(unstableVertices) != 0:
            for entry in unstableVertices:
                point = (entry[0], entry[1])
                self.toppleAt(point)
            unstableVertices = self.unstable()

    

sandpile = Sandpile(15, np.zeros((15,15)) )
sandpile
sandpile.addAt(sandpile.cartToMatrix((0,0)))
sandpile.addAt(sandpile.cartToMatrix((0,0)))
sandpile.addAt(sandpile.cartToMatrix((0,0)))
sandpile.addAt(sandpile.cartToMatrix((0,0)))
sandpile.addAt(sandpile.cartToMatrix((0,0)))
sandpile.addAt(sandpile.cartToMatrix((0,0)))
sandpile.addAt(sandpile.cartToMatrix((0,0)))
sandpile.addAt(sandpile.cartToMatrix((0,0)))

sandpile.stabilise()
print(sandpile.grid)