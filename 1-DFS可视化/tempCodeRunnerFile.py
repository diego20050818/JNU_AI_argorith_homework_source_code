# %%
import matplotlib.pyplot as plt
import networkx as nx

# %%
#定义有向图
city_graph = {
    '广州': ['珠海', '香港', '上海', '杭州','蒙德'],  
    '珠海': ['广州', '香港', '深圳', '澳门'],
    '北京': ['上海', '杭州', '广州', '香港'],
    '上海': ['北京', '杭州', '广州', '深圳'],
    '杭州': ['北京', '上海', '广州', '苏州'],
    '香港': ['广州', '珠海', '深圳', '澳门'],
    '深圳': ['珠海', '香港', '广州', '上海'],
    '澳门': ['珠海', '香港'],
    '奥么恩': ['蒙德', '贝洛伯格', '稻妻'],
    '蒙德': ['奥么恩', '贝洛伯格', '圣芙蕾雅','广州'], 
    '贝洛伯格': ['奥么恩', '蒙德', '稻妻'],
    '稻妻': ['奥么恩', '贝洛伯格', '圣芙蕾雅'],
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


# %%
#定义起始点和目的地
start = '广州'
end = '翁法罗斯'
#stack = [(start,[start])]
#visited = set()
#all_path = []
path = []
stack = []

def dfs_search_path(point=start, end=end, G=city_graph):
    stack.append(point)
    if point == end:
        print(f"寻找到从{start}到{end}的路径: {stack}")
        path.append(list(stack))
        stack.pop()
        return
    for neighbor in G[point]:
        if neighbor not in stack:
            dfs_search_path(neighbor, end, G)
    stack.pop()

try: 
    dfs_search_path()
    count = []
    for i in path:
        count.append(len(i))
    min_index = count.index(min(count))
    print(f"{start}到{end}最短路径为{path[min_index]},长度为{len(path[min_index])-1}")
except:
    print("输入图像不是全连通图")
print(path)


  

# %%
#画出有向图
G = nx.DiGraph()
for city in city_graph:
    G.add_node(city)
    for neighbor in city_graph[city]:
        G.add_edge(city, neighbor)

# %%
pos = nx.spring_layout(G)


plt.figure(figsize=(12,8))
plt.title("DFS path finding",fontsize=14)

default_color = '#ffffd2'
current_color = '#a8d8ea'
visited_color = '#fcbad3'
path_color = '#aa96da'

nx.draw_networkx_nodes(G,pos,node_color=default_color)
nx.draw_networkx_edges(G,pos,alpha=0.3,edge_color=visited_color)
nx.draw_networkx_labels(G, pos, font_family='SimHei')

plt.ion()
plt.show()



# %%
def dfs_search_path_visual(point=start, end=end, G=city_graph):
    stack.append(point)
    if point == end:
        print(f"寻找到从{start}到{end}的路径: {stack}")
        path.append(list(stack))
        stack.pop()
        return
    for neighbor in G[point]:
        if neighbor not in stack:
            # 可视化当前节点和边
            nx.draw_networkx_nodes(G, pos, nodelist=[neighbor], node_color=current_color)
            nx.draw_networkx_edges(G, pos, edgelist=[(point, neighbor)], edge_color=current_color)
            plt.pause(0.5)
            dfs_search_path_visual(neighbor, end, G)
            # 恢复颜色
            nx.draw_networkx_nodes(G, pos, nodelist=[neighbor], node_color=default_color)
            nx.draw_networkx_edges(G, pos, edgelist=[(point, neighbor)], edge_color=visited_color)
            plt.pause(0.5)
    stack.pop()

            
        


