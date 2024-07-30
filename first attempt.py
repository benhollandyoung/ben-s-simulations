#In this file I will simulate an abelian sandpile model on an nxn grid
import numpy as np 

#Use an np array to store the n^2 - those outside the radius of 1 points, 
#the degrees are usually 4 but will sometimes be 2, since we have a multigraph there's no faffing about on the boundary of the circle
#use a lambda to store the mobius transformation


#use an nxn array to store the state, set all sink grains to -1
#to fix the laplacian set all sink vertices to 0, so that nothing is done
#for non sink-vertices use the normal degree or -1 (since we have a grid and not a multigraph)

#MAYBE USE https://github.com/kivyfreakt/sandpile


#Size of grid
n = 15
#Our coordinate system will be a 0 indexed, row and column system
def coordToPlace(at: (int,int)) -> int:
    return (at[0] * n) + at[1] + 1

def placeToCoord(at: int) -> (int,int):
    return (at - 1 / n, at-1 % n)


def coordValid(at: (int,int)) -> bool:
    return (i-n/2)**2 + (j-n/2)**2 < (n/2)**2



#Constructing initial sandpile configuration

config = np.zeros((n,n))


for i in range(n):
    for j in range(n):
        if not coordValid((i,j)):
            config[i,j] = None
#print(config)

config = config.ravel()


laplacian = np.zeros((n**2,n**2))

for i in range(n**2):
    for j in range(n**2):
        if config[i] == None or config[j] == None:
            laplacian[i,j] = None
        else:
            if i == j:
                laplacian[i,j] = 2
            else:
                laplacian[i,j] = -1
    

            
            
#Create topple at x function
def topple(at: (int,int)):
    global config 
    place = coordToPlace(at)
    config -= laplacian[place,:]


topple((3,5))
config = config.reshape(n,n)
print(config)