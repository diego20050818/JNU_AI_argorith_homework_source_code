import matplotlib.pyplot as plt
import networkx as nx
import imageio
import os
from collections import deque
from copy import deepcopy

# 初始变量域
domains = {
    'A': ['R', 'G', 'B'],
    'B': ['R', 'G', 'B'],
    'C': ['R', 'G', 'B'],
    'D': ['R', 'G', 'B'],
}

# 变量之间的约束关系（无向图）
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]

# 双向加入所有弧
def get_all_arcs(edges):
    return deque([(xi, xj) for xi, xj in edges] + [(xj, xi) for xi, xj in edges])

# 判断是否一致（不允许相邻同色）
def revise(xi, xj, domains):
    revised = False
    new_domain = []
    for x in domains[xi]:
        if any(x != y for y in domains[xj]):
            new_domain.append(x)
        else:
            revised = True
    if revised:
        domains[xi] = new_domain
    return revised

# 可视化函数
def draw_graph(domains, step, removed_arc=None):
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)

    color_map = {'R': 'red', 'G': 'green', 'B': 'blue'}

    fig, ax = plt.subplots()
    plt.title(f'Step {step}', fontsize=14)

    # 节点显示 domain
    labels = {node: ','.join(domains[node]) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)

    # 节点颜色为灰（固定）
    nx.draw(G, pos, with_labels=False, node_size=1200, node_color="lightgray", ax=ax)

    # 高亮当前处理的弧
    if removed_arc:
        nx.draw_networkx_edges(G, pos, edgelist=[removed_arc], width=2.5, edge_color="red")

    filename = f"ac3_step_{step}.png"
    plt.savefig(filename)
    plt.close()
    return filename

# AC-3 主过程
def ac3(domains, edges):
    queue = get_all_arcs(edges)
    step = 0
    frames = []
    domains = deepcopy(domains)

    frames.append(draw_graph(domains, step))
    step += 1

    while queue:
        xi, xj = queue.popleft()
        if revise(xi, xj, domains):
            if not domains[xi]:
                print(f"Domain wiped out at {xi}, inconsistency found.")
                return None
            for xk, _ in filter(lambda arc: arc[1] == xi and arc[0] != xj, get_all_arcs(edges)):
                queue.append((xk, xi))
        frames.append(draw_graph(domains, step, removed_arc=(xi, xj)))
        step += 1

    return domains, frames

# 生成GIF
def make_gif(frames, output='ac3_visual.gif'):
    images = [imageio.imread(frame) for frame in frames]
    imageio.mimsave(output, images, fps=1)
    for frame in frames:
        os.remove(frame)

# 主函数
def main():
    result, frames = ac3(domains, edges)
    make_gif(frames)
    print("AC-3 可视化生成完毕：ac3_visual.gif")
    if result:
        print("最终域：")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("存在冲突，无法满足约束。")

if __name__ == "__main__":
    main()
