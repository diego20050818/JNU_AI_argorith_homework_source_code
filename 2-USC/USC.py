import networkx as nx
from queue import PriorityQueue

import matplotlib.pyplot as plt
# 设置字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def usc_visualization(graph, start_node, end_node):
    G = nx.Graph()
    # 将字典转换为边的列表
    edges = [(node, neighbor) for node in graph for neighbor in graph[node]]
    G.add_edges_from(edges)
    
    pos = nx.spring_layout(G)
    # 使用莫兰迪色系
    nx.draw(G, pos, with_labels=True, node_color='#B0A8B9', edge_color='#A3A3A3')
    
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start_node, [start_node]))
    
    while not pq.empty():
        cost, node, path = pq.get()
        if node not in visited:
            visited.add(node)
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#E6B8B7')
            plt.pause(0.5)
            
            if node == end_node:
                nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='red', width=2)
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')
                plt.show()
                return
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    pq.put((cost + 1, neighbor, path + [neighbor]))
                    nx.draw_networkx_edges(G, pos, edgelist=[(node, neighbor)], edge_color='#8C8C8C')
                    plt.pause(0.05)
    
    plt.show()

if __name__ == "__main__":
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
    usc_visualization(city_graph_example, 'Arad', 'Bucharest')
