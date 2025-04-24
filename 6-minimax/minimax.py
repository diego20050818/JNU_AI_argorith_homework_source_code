import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os, imageio

class Node:
    def __init__(self, value, children=None, name=""):
        self.value = value
        self.children = children or []
        self.name = name

# Minimax without pruning
def minimax(node, depth, maximizingPlayer, path=[], frames=[]):
    path.append(node)
    fig, ax = plt.subplots()
    draw_tree(node, highlight=path, ax=ax)
    os.makedirs("6-minimax/frames_minimax", exist_ok=True)
    filename = f"6-minimax/frames_minimax/frame_{len(frames):03d}.png"
    fig.savefig(filename)
    plt.close()
    frames.append(filename)

    if depth == 0 or not node.children:
        return node.value

    if maximizingPlayer:
        value = float('-inf')
        for child in node.children:
            value = max(value, minimax(child, depth - 1, False, path[:], frames))
        return value
    else:
        value = float('inf')
        for child in node.children:
            value = min(value, minimax(child, depth - 1, True, path[:], frames))
        return value

# Draw the tree
def draw_tree(node, x=0, y=0, dx=3, dy=-2, ax=None, highlight=[]):
    if ax is None:
        fig, ax = plt.subplots()
    ax.add_patch(patches.Circle((x, y), 0.3, fill=True, color='skyblue' if node in highlight else 'lightgray'))
    ax.text(x, y, f"{node.name}\n{node.value}", ha='center', va='center')
    if node.children:
        step = dx / len(node.children)
        for i, child in enumerate(node.children):
            cx = x + (i - (len(node.children) - 1)/2)*dx
            cy = y + dy
            ax.plot([x, cx], [y, cy], color='black')
            draw_tree(child, cx, cy, dx/2, dy, ax, highlight)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 2)
    ax.axis('off')

# Create a sample tree
def create_tree():
    A = Node(0, name="A")
    B = Node(0, name="B")
    C = Node(0, name="C")
    A1 = Node(3, name="A1")
    A2 = Node(5, name="A2")
    B1 = Node(6, name="B1")
    B2 = Node(9, name="B2")
    C1 = Node(1, name="C1")
    C2 = Node(2, name="C2")

    A.children = [A1, A2]
    B.children = [B1, B2]
    C.children = [C1, C2]
    root = Node(0, [A, B, C], name="Root")
    return root

# Run minimax and save GIF
def run_minimax():
    os.makedirs("frames_minimax", exist_ok=True)
    root = create_tree()
    frames = []
    minimax(root, 3, True, [], frames)

    images = [imageio.v2.imread(f) for f in frames]
    imageio.mimsave("minimax.gif", images, duration=0.8)
    print("Minimax GIF saved as minimax.gif")

if __name__ == "__main__":
    run_minimax()