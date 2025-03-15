import networkx as nx
from collections import deque

import matplotlib.pyplot as plt
# 设置字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def bfs_visualization(graph, start_node, end_node):
    G = nx.Graph()
    # 将字典转换为边的列表
    edges = [(node, neighbor) for node in graph for neighbor in graph[node]]
    G.add_edges_from(edges)
    
    pos = nx.spring_layout(G)
    # 使用莫兰迪色系
    nx.draw(G, pos, with_labels=True, node_color='#B0A8B9', edge_color='#A3A3A3')
    
    visited = set()
    queue = deque([(start_node, [start_node])])
    
    while queue:
        node, path = queue.popleft()
        if node not in visited:
            visited.add(node)
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#E6B8B7')
            plt.pause(0.5)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if neighbor == end_node:
                        final_path = path + [neighbor]
                        nx.draw_networkx_edges(G, pos, edgelist=[(final_path[i], final_path[i+1]) for i in range(len(final_path)-1)], edge_color='red', width=2)
                        nx.draw_networkx_nodes(G, pos, nodelist=final_path, node_color='red')
                        plt.show()
                        return
                    queue.append((neighbor, path + [neighbor]))
                    nx.draw_networkx_edges(G, pos, edgelist=[(node, neighbor)], edge_color='#8C8C8C')
                    plt.pause(0.05)
    
    plt.show()

if __name__ == "__main__":
    city_graph = {
        '广州': ['珠海', '香港', '上海', '杭州','蒙德'],  
        '珠海': ['广州', '香港', '深圳', '澳门'],
        '北京': ['上海', '杭州', '广州', '香港'],
        '上海': ['北京', '杭州', '广州', '深圳'],
        '杭州': ['北京', '上海', '广州', '苏州'],
        '香港': ['广州', '珠海', '深圳', '澳门'],
        '深圳': ['珠海', '香港', '广州', '上海'],
        '澳门': ['珠海', '香港','翁法罗斯'],
        '尼伯龙根': ['蒙德', '贝洛伯格', '稻妻'],
        '蒙德': ['尼伯龙根', '贝洛伯格', '圣芙蕾雅','广州'], 
        '贝洛伯格': ['尼伯龙根', '蒙德', '稻妻'],
        '稻妻': ['尼伯龙根', '贝洛伯格', '圣芙蕾雅'],
        '圣芙蕾雅': ['蒙德', '稻妻', '罗浮'],
        '罗浮': ['圣芙蕾雅', '匹诺康尼', '翁法罗斯'],
        '匹诺康尼': ['罗浮', '翁法罗斯'],
        '翁法罗斯': ['罗浮', '匹诺康尼'],
        '苏州': ['杭州', '上海'],
        '成都': ['广州', '北京', '上海'],
        '重庆': ['成都', '上海', '深圳'],
        '武汉': ['北京', '广州', '上海'],
        '南京': ['上海', '杭州', '苏州']
    }
    bfs_visualization(city_graph, '广州', '圣芙蕾雅')