import pygame
import networkx as nx
import time
from collections import defaultdict

# 初始化pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimal DFS Path Visualization with Animation")
clock = pygame.time.Clock()

# 莫兰迪色系
BACKGROUND = (229, 231, 233)  # 浅灰
EDGE_COLOR = (169, 169, 169)  # 深灰
NODE_COLOR = (163, 191, 250)  # 莫兰迪蓝
CURRENT_NODE_COLOR = (216, 167, 177)  # 莫兰迪红
PATH_COLOR = (247, 220, 180)  # 莫兰迪黄

# 定义城市图（有向图）
city_graph_example = {
    'Arad': ['Zerind', 'Sibiu', 'Timisoara'],
    'Zerind': ['Arad', 'Oradea'],
    'Oradea': ['Zerind', 'Sibiu'],
    'Sibiu': ['Arad', 'Oradea', 'Fagaras', 'Rimnicu Vilcea'],
    'Timisoara': ['Arad', 'Lugoj'],
    'Lugoj': ['Timisoara', 'Mehadia'],
    'Mehadia': ['Lugoj', 'Drobeta'],
    'Drobeta': ['Mehadia', 'Craiova'],
    'Craiova': ['Drobeta', 'Rimnicu Vilcea', 'Pitesti'],
    'Rimnicu Vilcea': ['Sibiu', 'Craiova', 'Pitesti'],
    'Fagaras': ['Sibiu', 'Bucharest'],
    'Pitesti': ['Rimnicu Vilcea', 'Craiova', 'Bucharest'],
    'Bucharest': ['Fagaras', 'Pitesti', 'Giurgiu', 'Urziceni'],
    'Giurgiu': ['Bucharest'],
    'Urziceni': ['Bucharest', 'Hirsova', 'Vaslui'],
    'Hirsova': ['Urziceni', 'Eforie'],
    'Eforie': ['Hirsova'],
    'Vaslui': ['Urziceni', 'Iasi'],
    'Iasi': ['Vaslui', 'Neamt'],
    'Neamt': ['Iasi']
}
# 使用networkx创建有向图并计算节点位置
G = nx.DiGraph(city_graph_example)
raw_pos = nx.spring_layout(G, k=0.6, scale=1.0, center=(0, 0))

# 调整位置确保节点在窗口内
pos = {}
MARGIN = 50
NODE_SIZE = 6
LABEL_OFFSET = 15
for node, (x, y) in raw_pos.items():
    scaled_x = (x + 1) * (WIDTH - 2 * MARGIN) / 2 + MARGIN
    scaled_y = (y + 1) * (HEIGHT - 2 * MARGIN) / 2 + MARGIN
    scaled_x = max(MARGIN + NODE_SIZE, min(WIDTH - MARGIN - NODE_SIZE - LABEL_OFFSET, scaled_x))
    scaled_y = max(MARGIN + NODE_SIZE, min(HEIGHT - MARGIN - NODE_SIZE - LABEL_OFFSET, scaled_y))
    pos[node] = (scaled_x, scaled_y)

# DFS算法
def dfs_search_path(start, end, G, screen, pos):
    stack = [(start, [start])]
    all_paths = []
    
    while stack:
        current, path = stack.pop()
        if current == end:
            all_paths.append(path)
            continue
        
        for neighbor in G[current]:
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))
        
        # 动画绘制当前状态
        animate_step(screen, G, pos, path, current)
    
    # 找到最短路径
    if all_paths:
        shortest_path = min(all_paths, key=len)
        return shortest_path
    return None

# 动画绘制函数
def animate_step(screen, G, pos, current_path, current_node):
    screen.fill(BACKGROUND)
    
    # 绘制边
    for edge in G.edges():
        start_pos = pos[edge[0]]
        end_pos = pos[edge[1]]
        pygame.draw.line(screen, EDGE_COLOR, start_pos, end_pos, 1)
    
    # 绘制路径（逐步动画）
    for i in range(len(current_path) - 1):
        start_pos = pos[current_path[i]]
        end_pos = pos[current_path[i + 1]]
        for t in range(10):  # 分10步绘制路径
            interp_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t / 10
            interp_y = start_pos[1] + (end_pos[1] - start_pos[1]) * t / 10
            pygame.draw.line(screen, PATH_COLOR, start_pos, (interp_x, interp_y), 2)
            draw_nodes(screen, G, pos, current_path, current_node, t / 10)
            pygame.display.flip()
            clock.tick(60)

    # 绘制完整路径
    for i in range(len(current_path) - 1):
        start_pos = pos[current_path[i]]
        end_pos = pos[current_path[i + 1]]
        pygame.draw.line(screen, PATH_COLOR, start_pos, end_pos, 2)

    # 绘制节点
    draw_nodes(screen, G, pos, current_path, current_node, 1.0)
    pygame.display.flip()
    time.sleep(0.1)  # 控制整体节奏

# 绘制节点函数（带淡入效果）
def draw_nodes(screen, G, pos, current_path, current_node, alpha):
    font = pygame.font.SysFont('SimHei', 14)
    for node in G.nodes():
        color = NODE_COLOR if node in current_path else NODE_COLOR
        size = NODE_SIZE
        if node == current_node:
            color = CURRENT_NODE_COLOR
            # 淡入效果：大小随alpha变化
            size = int(NODE_SIZE + 4 * (1 - abs(1 - 2 * alpha)))  # 最大放大到10
        
        pygame.draw.circle(screen, color, (int(pos[node][0]), int(pos[node][1])), size)
        
        # 固定显示城市名称
        text = font.render(node, True, EDGE_COLOR)
        text_rect = text.get_rect(center=(pos[node][0], pos[node][1] + LABEL_OFFSET))
        screen.blit(text, text_rect)

# 主循环
def main():
    start = 'Arad'
    end = 'Bucharest'
    running = True
    shortest_path = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not shortest_path:
            shortest_path = dfs_search_path(start, end, G, screen, pos)
        
        if shortest_path:
            screen.fill(BACKGROUND)
            # 绘制最终状态
            for edge in G.edges():
                pygame.draw.line(screen, EDGE_COLOR, pos[edge[0]], pos[edge[1]], 1)
            for i in range(len(shortest_path) - 1):
                pygame.draw.line(screen, PATH_COLOR, pos[shortest_path[i]], pos[shortest_path[i + 1]], 2)
            draw_nodes(screen, G, pos, shortest_path, shortest_path[-1], 1.0)
            font = pygame.font.SysFont('SimHei', 20)
            text = font.render(f"最短路径: {' -> '.join(shortest_path)}", True, EDGE_COLOR)
            screen.blit(text, (20, 20))
            pygame.display.flip()
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()