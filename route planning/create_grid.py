import random
import numpy as np


class grid:#创建类
    def __init__(self,rows,cols,obstacle):
        self.rows = rows
        self.cols = cols
        self.obstacle = obstacle
        self.array = np.zeros((rows,cols),dtype=int)
        for x,y in obstacle:
            self.array[x,y]=1#让障碍物为1方便可视化

    def neighbors(self,current):#遍历周围上下左右的格子
        x,y=current
        neighbors = [(1,0),(0,1),(-1,0),(0,-1)]#当前基础上的行动范围    
        next=[]
        for dx,dy in neighbors:
            nx=x+dx
            ny=y+dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if (nx,ny) not in self.obstacle:
                    next.append((nx,ny))#找可能有的路径
        return next

    def copy(self):
        return self.array.copy()#复制地图


def create_grid(rows:int,cols:int,obstacle_rate=0.3,start=(0,0),end=None):
    if end is None:
        end=(rows-1,cols-1)
    array=np.zeros((rows,cols),dtype=int)
    total_cells=rows*cols
    obstacle_count=int(total_cells*obstacle_rate)#障碍数



    forbidden_cell={start,end}
    all_points=[(i,j) for i in range(rows) for j in range(cols) if (i,j)not in forbidden_cell]
    obs_pos=random.sample(all_points,obstacle_count)#随机选障碍数

    return grid(rows,cols,set(obs_pos))

if __name__=='__main__':
    g=create_grid(20,20,0.3,(1,1),(18,18))
    print(g.array)
