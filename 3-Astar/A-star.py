import heapq  # 导入堆队列模块,用于优先队列实现
import numpy as np  # 导入numpy用于数组操作
import matplotlib.pyplot as plt  # 导入matplotlib用于可视化
import matplotlib.colors as mcolors  # 导入颜色模块
import imageio  # 导入imageio用于生成GIF动画
import os  # 导入os模块用于文件操作

# 可视化并保存为图片帧
def visualize_grid_to_file(grid, path=None, visited=None, filename='frame.png'):
    rows, cols = len(grid), len(grid[0])  # 获取网格的行数和列数
    fig, ax = plt.subplots()  # 创建matplotlib画布和坐标轴
    cmap = mcolors.ListedColormap(['white', 'black'])  # 创建颜色映射:白色表示可通行,黑色表示障碍
    bounds = [-0.5, 0.5, 1.5]  # 设置颜色边界
    norm = mcolors.BoundaryNorm(bounds, cmap.N)  # 创建标准化对象

    ax.imshow(grid, cmap=cmap, norm=norm)  # 显示网格
    ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5)  # 添加网格线
    ax.set_xticks([])  # 移除x轴刻度
    ax.set_yticks([])  # 移除y轴刻度

    if visited:  # 如果有已访问的节点
        for (x, y) in visited:
            ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='blue', alpha=0.3))  # 用蓝色标记已访问节点

    if path:  # 如果有路径
        for (x, y) in path:
            ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='red', alpha=0.5))  # 用红色标记路径

    plt.savefig(filename)  # 保存图片
    plt.close()  # 关闭图形

# A* 搜索算法实现 + 生成GIF动画
def astar_with_gif(grid, start, goal, gif_name='astar.gif'):
    def h(pos):  # 启发式函数:计算曼哈顿距离
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    open_set = []  # 初始化开放列表
    heapq.heappush(open_set, (h(start), 0, start))  # 将起点加入开放列表
    came_from = {}  # 用于记录路径
    g_score = {start: 0}  # 记录从起点到每个节点的实际代价
    visited = set()  # 记录已访问的节点
    frames = []  # 存储动画帧

    frame_dir = "3-Astar/frames"  # 创建帧图像存储目录
    os.makedirs(frame_dir, exist_ok=True)

    frame_count = 0  # 帧计数器
    while open_set:  # 当开放列表不为空时
        f, g, current = heapq.heappop(open_set)  # 取出f值最小的节点
        if current in visited:  # 如果节点已访问,跳过
            continue
        visited.add(current)  # 标记节点为已访问

        # 生成当前状态的可视化帧
        frame_file = os.path.join(frame_dir, f"frame_{frame_count:03d}.png")
        visualize_grid_to_file(grid, visited=visited, filename=frame_file)
        frames.append(frame_file)
        frame_count += 1

        if current == goal:  # 如果到达目标
            path = []  # 重建路径
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            # 生成最终路径的可视化帧
            frame_file = os.path.join(frame_dir, f"frame_{frame_count:03d}.png")
            visualize_grid_to_file(grid, path[::-1], visited, filename=frame_file)
            frames.append(frame_file)
            break

        # 探索相邻节点
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:  # 上下左右四个方向
            neighbor = (current[0] + dx, current[1] + dy)
            # 检查邻居节点是否有效且可通行
            if (0 <= neighbor[0] < len(grid)) and (0 <= neighbor[1] < len(grid[0])) and grid[neighbor[0]][neighbor[1]] == 0:
                tentative_g = g + 1  # 计算新的g值
                # 如果找到更好的路径或是新节点
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g  # 更新g值
                    f_score = tentative_g + h(neighbor)  # 计算f值
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))  # 加入开放列表
                    came_from[neighbor] = current  # 记录路径

    # 生成GIF动画
    images = [imageio.v2.imread(frame) for frame in frames]
    imageio.mimsave(gif_name, images, duration=0.2)
    print(f"GIF 保存为 {gif_name}")

# 主函数
def main():
    # 随机生成地图大小(5-10之间)
    rows, cols = np.random.randint(5, 11, size=2)
    while True:
        # 随机生成地图,0表示可通行,1表示障碍,70%概率是可通行格子
        grid = np.random.choice([0, 1], size=(rows, cols), p=[0.7, 0.3])
        start = (0, 0)  # 起点为左上角
        goal = (rows - 1, cols - 1)  # 终点为右下角
        # 确保起点和终点可通行
        if grid[start[0]][start[1]] == 0 and grid[goal[0]][goal[1]] == 0:
            break

    print("随机地图：")
    print(grid)

    # 运行A*算法并生成可视化
    astar_with_gif(grid, start, goal, gif_name='astar_search.gif')

if __name__ == "__main__":
    main()
