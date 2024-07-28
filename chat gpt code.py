#Using some ChatGPT generated code - ignore this not useful.

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

def initialize_grid(radius, grid_size):
    y, x = np.ogrid[-grid_size:grid_size, -grid_size:grid_size]
    mask = x**2 + y**2 <= radius**2
    grid = np.zeros((2*grid_size, 2*grid_size), dtype=int)
    return grid, mask

def add_sand(grid, mask, num_grains):
    indices = np.where(mask)
    for _ in range(num_grains):
        idx = np.random.choice(len(indices[0]))
        grid[indices[0][idx], indices[1][idx]] += 1

def topple(grid, mask):
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    while True:
        unstable = (grid > 3) & mask
        if not unstable.any():
            break
        topple_amount = convolve(unstable.astype(int), kernel, mode='constant')
        grid += topple_amount
        grid[~mask] = 0  # Reset cells outside the unit disc to 0

def plot_sandpile(grid, mask):
    plt.imshow(np.ma.masked_where(~mask, grid), cmap='viridis', extent=(-1, 1, -1, 1))
    plt.colorbar(label='Number of Grains')
    plt.title('Abelian Sandpile on a Unit Disc')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Parameters
radius = 50
grid_size = 100
num_grains = 10000

# Initialize grid and mask
grid, mask = initialize_grid(radius, grid_size)

# Add sand grains
add_sand(grid, mask, num_grains)

# Topple until stable
topple(grid, mask)

# Plot the result
plot_sandpile(grid, mask)
