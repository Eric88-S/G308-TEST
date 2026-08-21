from A_star import a_star_search
from A_star import reconstruct_path
from create_grid import create_grid
from visualization import draw_map
from visualization import  draw_path
import matplotlib.pyplot as plt
from BFS_grid import bfs_search
import time

def main():
    grid = create_grid(20,20,0.3,(1,1),(18,18))

    start_timeA = time.perf_counter()
    came_from,cost=a_star_search(grid,(1,1),(18,18))
    path1=reconstruct_path(came_from,(1,1),(18,18))
    end_timeA = time.perf_counter()
    print(f'A*耗时{end_timeA-start_timeA}')

    start_timeB = time.perf_counter()
    came_from=bfs_search(grid,(1,1),(18,18))
    path2=reconstruct_path(came_from,(1,1),(18,18))
    end_timeB = time.perf_counter()
    print(f'bfs耗时{end_timeB-start_timeB}')

    draw_map(grid,(1,1),(18,18))
    draw_path(path1,color='red',label='A*')
    draw_path(path2,color='blue',label='bfs')
    plt.show()

if __name__ == '__main__':
    main()