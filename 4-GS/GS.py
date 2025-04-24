import heapq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio
import os

# 可视化并保存为图片帧
def visualize_grid_to_file(grid, path=None, visited=None, filename='frame.png'):
    rows, cols = len(grid), len(grid[0])
    fig, ax = plt.subplots()
    cmap = mcolors.ListedColormap(['white', 'black'])  # 白色表示可通行，黑色表示障碍物
    bounds = [-0.5, 0.5, 1.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    ax.imshow(grid, cmap=cmap, norm=norm)
    ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])

    # 可视化已访问节点
    if visited:
        for (x, y) in visited:
            ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='blue', alpha=0.3))

    # 可视化路径
    if path:
        for (x, y) in path:
            ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='red', alpha=0.5))

    plt.savefig(filename)  # 保存当前帧为图片
    plt.close()

# 贪婪搜索核心算法
def greedy_search(grid, start, goal, gif_name='greedy_search.gif'):
    def h(pos):
        # 启发函数（曼哈顿距离）
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    open_set = []  # 优先队列
    heapq.heappush(open_set, (h(start), start))  # 将起点加入优先队列
    came_from = {}  # 路径追踪
    visited = set()  # 已访问节点
    frames = []  # 存储帧文件路径

    frame_dir = "4-GS/frames_greedy"  # 存储帧的目录
    os.makedirs(frame_dir, exist_ok=True)

    frame_count = 0
    while open_set:
        _, current = heapq.heappop(open_set)  # 取出优先级最高的节点
        if current in visited:
            continue
        visited.add(current)

        # 保存当前帧
        frame_file = os.path.join(frame_dir, f"frame_{frame_count:03d}.png")
        visualize_grid_to_file(grid, visited=visited, filename=frame_file)
        frames.append(frame_file)
        frame_count += 1

        if current == goal:
            # 找到目标节点，回溯路径
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            # 保存最终路径帧
            frame_file = os.path.join(frame_dir, f"frame_{frame_count:03d}.png")
            visualize_grid_to_file(grid, path[::-1], visited, filename=frame_file)
            frames.append(frame_file)
            break

        # 遍历邻居节点
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < len(grid)) and (0 <= neighbor[1] < len(grid[0])) and grid[neighbor[0]][neighbor[1]] == 0:
                if neighbor not in visited:
                    heapq.heappush(open_set, (h(neighbor), neighbor))
                    came_from[neighbor] = current

    # 将所有帧合成为 GIF
    images = [imageio.v2.imread(frame) for frame in frames]
    imageio.mimsave(gif_name, images, duration=0.2)
    print(f"GIF 保存为 {gif_name}")

# 主程序
def main():
    # 随机生成地图
    rows, cols = np.random.randint(5, 11, size=2)
    while True:
        grid = np.random.choice([0, 1], size=(rows, cols), p=[0.7, 0.3])  # 70% 为可通行，30% 为障碍物
        start = (0, 0)
        goal = (rows - 1, cols - 1)
        # 确保起点和终点不被障碍物阻挡
        if grid[start[0]][start[1]] == 0 and grid[goal[0]][goal[1]] == 0:
            break

    print("随机地图：")
    print(grid)

    # 执行贪婪搜索并生成 GIF
    greedy_search(grid, start, goal, gif_name='greedy_search.gif')

if __name__ == "__main__":
    main()
