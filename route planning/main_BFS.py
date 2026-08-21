from BFS_grid import bfs_search
from A_star import reconstruct_path
from create_grid import create_grid
from visualization import draw_map
from visualization import  draw_path
import matplotlib.pyplot as plt

def main():
    grid = create_grid(20, 20, 0.3, (1, 1), (18, 18))
    came_from = bfs_search(grid, (1, 1), (18, 18))
    path = reconstruct_path(came_from, (1, 1), (18, 18))
    draw_map(grid, (1, 1), (18, 18))
    draw_path(path)
    plt.show()


if __name__ == '__main__':
    main()