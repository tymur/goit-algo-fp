import uuid
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# Вузол та побудова дерева/графа
class Node:
    def __init__(self, key, color="#9dd7ff"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Додає вузли/ребра в nx-граф та обчислює координати, викликаємо цю функцію рекурсивно лише один раз під час побудови позицій."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=str(node.val), ref=node)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def build_graph(root):
    """Повертає nx-граф та словник позицій вузлів для малювання."""
    g = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(g, root, pos)
    return g, pos

# Сервіс: колірні градієнти у HEX
def hex_color(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))

def gradient_hex(n, start="#08306B", end="#DEEBF7"):
    """Повертає список з n кольорів у HEX, що утворюють градієнт від start до end."""
    def to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    rs, gs, bs = to_rgb(start)
    re, ge, be = to_rgb(end)
    if n <= 1:
        return [start]
    out = []
    for i in range(n):
        t = i / (n - 1)
        r = rs + (re - rs) * t
        g = gs + (ge - gs) * t
        b = bs + (be - bs) * t
        out.append(hex_color(r, g, b))
    return out

# Ітеративні обходи (без рекурсії)

def nodes_iterative_bfs(root):
    """BFS: повертає список вузлів у порядку відвідування. Використовує чергу."""
    order = []
    q = deque([root])
    seen = set([root.id])
    while q:
        v = q.popleft()
        order.append(v)
        if v.left and v.left.id not in seen:
            seen.add(v.left.id)
            q.append(v.left)
        if v.right and v.right.id not in seen:
            seen.add(v.right.id)
            q.append(v.right)
    return order

def nodes_iterative_dfs(root):
    """DFS (preorder): повертає список вузлів у порядку відвідування. Використовує стек."""
    order = []
    stack = [root]
    seen = set()
    while stack:
        v = stack.pop()
        if v.id in seen:
            continue
        seen.add(v.id)
        order.append(v)
        # Спочатку покладемо праву, потім ліву — щоб ліва вийшла першою (preorder)
        if v.right:
            stack.append(v.right)
        if v.left:
            stack.append(v.left)
    return order

# Візуалізація кроків обходу
def animate_traversal(root, mode="bfs", pause=0.6, start_hex="#08306B", end_hex="#DEEBF7"):
    g, pos = build_graph(root)

    # Порядок відвідування
    order = nodes_iterative_bfs(root) if mode.lower() == "bfs" else nodes_iterative_dfs(root)

    # Палітра у HEX (темний -> світлий)
    palette = gradient_hex(len(order), start=start_hex, end=end_hex)

    # Початкові кольори — світло-сірі (не відвідані)
    base_color = "#D9D9D9"
    node_colors = {n: base_color for n in g.nodes()}
    labels = {n: data["label"] for n, data in g.nodes(data=True)}

    plt.ion()
    fig = plt.figure(figsize=(8, 5))
    for step, node in enumerate(order, 1):
        node_colors[node.id] = palette[step - 1]
        plt.clf()
        colors_now = [node_colors[n] for n in g.nodes()]
        nx.draw(g, pos=pos, labels=labels, arrows=False, node_size=2400, node_color=colors_now)
        plt.title(f"Обхід: {mode.upper()} — крок {step}/{len(order)} (вузол {node.val})")
        plt.tight_layout()
        plt.pause(pause)

    plt.ioff()
    plt.show()

# Приклад використання

if __name__ == "__main__":
    # Побудуємо прикладне дерево
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    # Анімація обходів:
    # 1) BFS
    animate_traversal(root, mode="bfs", pause=0.7)   # темний→світлий синій

    # 2) DFS
    animate_traversal(root, mode="dfs", pause=0.7)
