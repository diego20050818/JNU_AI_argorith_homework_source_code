# %%
import plotly.graph_objects as go
import networkx as nx

# %%
# 定义有向图
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
# 定义起始点和目的地
start = '广州'
end = '翁法罗斯'
path = []
stack = []

# %%
# 画出有向图
# %% 
# 修改导入部分
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.io import curdoc
from bokeh.palettes import Category20
import networkx as nx
import numpy as np

# %% 修改可视化部分
G = nx.DiGraph()
for city in city_graph:
    G.add_node(city)
    for neighbor in city_graph[city]:
        G.add_edge(city, neighbor)

pos = nx.spring_layout(G, k=2)

# 创建 Bokeh 画布
p = figure(title="DFS Path Finding", tools="pan,wheel_zoom,reset", 
          x_range=(-2, 2), y_range=(-2, 2))

# 绘制初始边
edge_source = ColumnDataSource(data={
    'xs': [],
    'ys': [],
    'colors': []
})

# 绘制节点
node_x = [pos[k][0] for k in G.nodes]
node_y = [pos[k][1] for k in G.nodes]
labels = list(G.nodes)

# 添加节点和标签
p.circle(node_x, node_y, size=15, fill_color='#ffffd2', line_color='black')
labels = LabelSet(x=node_x, y=node_y, text=labels, text_font_size='10pt',
                  x_offset=5, y_offset=5, text_color='black')
p.add_layout(labels)

# 高亮起点终点
start_idx = labels.text.index(start)
end_idx = labels.text.index(end)
p.circle([node_x[start_idx], node_x[end_idx]], 
        [node_y[start_idx], node_y[end_idx]], 
        size=15, color='#66c18c')

# 动态更新函数
def update_edges(steps):
    new_data = {
        'xs': [],
        'ys': [],
        'colors': []
    }
    for step in steps:
        point, neighbor, status = step
        x0, y0 = pos[point]
        x1, y1 = pos[neighbor]
        new_data['xs'].append([x0, x1])
        new_data['ys'].append([y0, y1])
        new_data['colors'].append('#a8d8ea' if status == 'current' else '#fcbad3')
    
    edge_source.stream(new_data, rollover=1000)  # 保留最多1000条边

# 初始化渲染
edge_renderer = p.multi_line('xs', 'ys', source=edge_source, 
                            line_color='colors', line_width=2)

# 显示画布
output_notebook()
handle = show(p, notebook_handle=True)
# 修改搜索函数
def dfs_search_path(point=start, end=end, G=G):
    global steps  # 添加全局声明
    stack.append(point)
    if point == end:
        path.append(list(stack))
        stack.pop()
        return
    for neighbor in G[point]:
        if neighbor not in stack:
            steps.append((point, neighbor, 'current'))
            update_edges(steps)  # 实时更新
            dfs_search_path(neighbor, end, G)
            steps.append((point, neighbor, 'visited'))
            update_edges(steps)  # 实时更新
    stack.pop()
# 调用搜索并保持展示
steps = []  # 初始化steps数组
dfs_search_path()
def dfs_search_path(point=start, end=end, G=G):
    stack.append(point)
    if point == end:
        path.append(list(stack))
        stack.pop()
        return
    for neighbor in G[point]:
        if neighbor not in stack:
            steps.append((point, neighbor, 'current'))
            dfs_search_path(neighbor, end, G)
            steps.append((point, neighbor, 'visited'))
    stack.pop()
# 修改可视化更新逻辑
with fig.batch_update():
    fig.data = [trace for trace in fig.data if not trace.line.color]  # 保留基础布局
    for point, neighbor, status in steps:
        color = '#a8d8ea' if status == 'current' else '#ffffd2'
        x0, y0 = pos[point]
        x1, y1 = pos[neighbor]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines', line=dict(width=2, color=color)))
        fig.show()

dfs_search_path()
visualize_steps(steps, G, pos)

# 计算并打印最短路径
count = []
for i in path:
    count.append(len(i))
min_index = count.index(min(count))
print(f"{start}到{end}最短路径为{path[min_index]}, 长度为{len(path[min_index])-1}")
print(path)





