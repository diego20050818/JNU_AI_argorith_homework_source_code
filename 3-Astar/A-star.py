import heapq  # 导入堆队列模块,用于优先队列实现
import numpy as np  # 导入numpy用于数组操作
import matplotlib.pyplot as plt  # 导入matplotlib用于可视化
import networkx as nx  # 导入networkx用于图结构操作
import imageio  # 导入imageio用于生成GIF动画
import os  # 导入os模块用于文件操作

# 新的颜色方案
COLORS = {
    'background': '#F5F5F5',  # 浅灰色背景
    'node': '#FFFFFF',        # 白色节点
    'obstacle': '#2C3E50',    # 深蓝色障碍物
    'start': '#E74C3C',       # 红色起点
    'end': '#2ECC71',         # 绿色终点
    'visited': '#3498DB',     # 蓝色已访问
    'path': '#F1C40F',        # 黄色路径
    'edge': '#BDC3C7'         # 灰色边
}

def create_graph_from_grid(grid):
    """将网格转换为图结构"""
    G = nx.Graph()
    rows, cols = grid.shape
    
    # 添加节点
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:  # 可通行区域
                G.add_node((i, j))
    
    # 添加边
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                # 检查四个方向
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 0:
                        G.add_edge((i, j), (ni, nj))
    
    return G

def visualize_graph_to_file(G, grid, path=None, visited=None, filename='frame.png'):
    """可视化图结构并保存为图片"""
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    
    # 设置背景色
    plt.gca().set_facecolor(COLORS['background'])
    
    # 计算节点位置
    pos = {node: (node[1], -node[0]) for node in G.nodes()}
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, edge_color=COLORS['edge'], width=1.5)
    
    # 绘制节点
    node_colors = []
    for node in G.nodes():
        if node in visited:
            node_colors.append(COLORS['visited'])
        elif node in path:
            node_colors.append(COLORS['path'])
        elif node == start:
            node_colors.append(COLORS['start'])
        elif node == goal:
            node_colors.append(COLORS['end'])
        else:
            node_colors.append(COLORS['node'])
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
    
    # 添加节点标签
    labels = {node: f'({node[0]},{node[1]})' for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()

# A* 搜索算法实现 + 生成GIF动画
def astar_with_gif(grid, start, goal, gif_name='astar_search.gif'):
    def h(pos):  # 启发式函数:计算曼哈顿距离
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    G = create_graph_from_grid(grid)
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
        visualize_graph_to_file(G, grid, visited=visited, filename=frame_file)
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
            visualize_graph_to_file(G, grid, path[::-1], visited, filename=frame_file)
            frames.append(frame_file)
            break

        # 探索相邻节点
        for neighbor in G.neighbors(current):
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
