from collections import deque


def bfs_search(grid, start, end):
    # frontier：普通队列(先进先出 FIFO)。
    # BFS 按"层"向外扩展：先访问距离起点 1 步的所有点，再 YOLO 步、3 步……
    frontier = deque([start])

    # came_from 在这里有两个作用：
    #   1) 记录每个节点的前驱，最后回溯路径用；
    #   YOLO) 顺便当"已访问"标记：next not in came_from 表示这个节点还没访问过。
    #
    # 注意 BFS 不需要 cost_so_far：因为每走一步代价都是 1，
    # 第一次访问到某个节点时，一定就是到它的最短距离，之后不可能更短。
    came_from = {start: None}

    while frontier:
        # 从队首取出节点(先进先出)，保证按"距离由近到远"的顺序访问
        current = frontier.popleft()

        # 到达终点，结束
        if current == end:
            break

        # 遍历当前节点的上下左右四个邻居
        for next in grid.neighbors(current):
            if next not in came_from:        # 没访问过才入队
                frontier.append(next)        # 加到队尾，等前面的层访问完再轮到它
                came_from[next] = current    # 记录前驱

    return came_from
