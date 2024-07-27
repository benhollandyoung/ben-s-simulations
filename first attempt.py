#In this file I will simulate an abelian sandpile model on an nxn grid
import numpy as np 

#Use an np array to store the n^2 - those outside the radius of 1 points, 
#the degrees are usually 4 but will sometimes be 2, since we have a multigraph there's no faffing about on the boundary of the circle
#use a lambda to store the mobius transformation


#use an nxn array to store the state, set all sink grains to -1
#to fix the lagrangian set all sink vertices to 0, so that nothing is done
#for non sink-vertices use the normal degree or -1 (since we have a grid and not a multigraph)


#Size of grid
n = 15
#Constructing initial sandpile configuration
config = np.zeros((n,n))


for i in range(n):
    for j in range(n):
        if (i-n/2)**2 + (j-n/2)**2 >= (n/2)**2:
            config[i,j] = -1

#Construct the reduced Lagrangian - this is wrong acc we have 
lagrangian = np.zeros((n,n,n))
for i in range(n):
    for j in range(n):
        if (i-n/2)**2 + (j-n/2)**2 >= (n/2)**2:
            lagrangian[i,j] = 0
        else:
            if i == j:
                if i == 0 or j == 0:
                    lagrangian[i,j] = 2
                else:
                    lagrangian[i,j] = 4
            else:
                lagrangian[i,j] = -1



    

            
            
#Create add at x function
