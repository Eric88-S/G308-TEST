import matplotlib.pyplot as plt
import numpy as np


def draw_map(grid, start, end):
    plt.imshow(grid.array, cmap='gray_r', origin='upper')
    plt.gca().add_patch(plt.Rectangle((start[1] - 0.5, start[0] - 0.5), 1, 1, color='blue'))
    plt.gca().add_patch(plt.Rectangle((end[1] - 0.5, end[0] - 0.5), 1, 1, color='blue'))
    plt.grid(True, color='black', linewidth=1, linestyle='dotted')
    plt.xticks(np.arange(grid.rows))
    plt.yticks(np.arange(grid.cols))
    for i, j in grid.obstacle:
        plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='black'))


def draw_path(path,color='red',label=None):
        xs=[p[1] for p in path]
        ys=[p[0] for p in path]

        plt.plot(xs,ys)
        plt.scatter(xs,ys,c='red')