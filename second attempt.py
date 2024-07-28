#Use nxn grid with n even and be able to convert between normal coordinates and numpy default 
#Create a degree function to just check whether points are in the unit disc or not
#To topple add to the 4 neighbours individually if they're not in the sink


n = 4
grid = np.zeros(n,n)

def cartesianToNumpy(x,y):
    return abs(x+n/2), abs(y-n/2)

def numpyToCartesian(x,y):
    #fix this

#gotta fix this