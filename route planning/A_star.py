from queue import PriorityQueue


def heuristic(now, end):
    """曼哈顿距离启发函数。

    网格上只能上下左右走，所以从 now 到 end 的最短步数至少是 |dx| + |dy|。
    因此能保证 A* 找到的路径是最短的。
    """
    x1, y1 = now
    x2, y2 = end
    distance = abs(x1 - x2) + abs(y1 - y2)
    return distance


def a_star_search(grid, start, end):
    # frontier：优先队列(最小堆)，按 f = g + h 从小到大弹出。
    # 队列里每个元素是 (f值, 节点)，f 小的先被取出来。
    frontier = PriorityQueue()
    frontier.put((0, start))            # 起点 f = 0

    # came_from：记录每个节点是从哪个节点走过来的，最后用来回溯路径。
    # cost_so_far：记录从起点到每个节点的最小实际代价 g。
    came_from = {}
    cost_so_far = {}
    came_from[start] = None             # 起点没有前驱
    cost_so_far[start] = 0              # 起点到自己的代价是 0

    while not frontier.empty():
        # 弹出 f 最小的节点 —— A* 的核心：
        # 不是像 BFS 那样按距离一层层扩，而是优先探索"总代价估计最小"的方向。
        current = frontier.get()[1]

        # 已经到达终点，搜索结束
        if current == end:
            break

        # 遍历当前节点的上下左右四个邻居
        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + 1    # 每走一步代价 +1

            # 只有两种情况需要处理这个邻居：
            #   1) 它还没被访问过；
            #   YOLO) 找到了一条比之前更短的到达它的路。
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost                 # 更新 g
                priority = new_cost + heuristic(next, end)   # f = g + h
                frontier.put((priority, next))               # 加入待探索队列
                came_from[next] = current                    # 记录前驱

    return came_from, cost_so_far


def reconstruct_path(came_from, start, end):
    """从终点沿 came_from 一路回溯到起点，返回 (起点 -> 终点) 的路径列表。"""
    if end not in came_from:        # 终点从来没被访问到，说明没有路
        return None

    current = end
    path = [current]
    while current != start:         # 一直往回走，直到回到起点
        current = came_from[current]
        path.append(current)
    path.reverse()                  # 回溯得到的是"终点->起点"，反转成"起点->终点"
    return path
