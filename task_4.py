import uuid
import networkx as nx
import matplotlib.pyplot as plt

# вузол
class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

# побудова графа з дерева 
def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
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

def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data['color'] for _, data in tree.nodes(data=True)]
    labels = {n: data['label'] for n, data in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()

#   -- візуалізація бінарної купи -- 

def heap_to_tree(heap, color_rule="root-min"):
    """
    Перетворює масив-купу (list) у бінарне дерево Node та повертає його корінь.
    - heap: масив (мін-/макс-купа), дозволено None-дирки, вони ігноруються
    - color_rule: просте підсвічування ('root-min', 'level', None)
    """
    if not heap:
        raise ValueError("Порожня купа")

    # створюємо всі вузли (пропускаємо None)
    nodes = [Node(v) if v is not None else None for v in heap]

    # з’єднуємо за індексами 2*i+1, 2*i+2
    for i, node in enumerate(nodes):
        if node is None:
            continue
        li, ri = 2*i + 1, 2*i + 2
        if li < len(nodes) and nodes[li] is not None:
            node.left = nodes[li]
        if ri < len(nodes) and nodes[ri] is not None:
            node.right = nodes[ri]

    # прості варіанти підсвічення
    if color_rule == "root-min":
        # корінь — темніший; діти — звичайні
        nodes[0].color = "#66b3ff"  # трохи темніший синій
    elif color_rule == "level":
        # фарбуємо рівні в різні відтінки
        level = 0
        next_break = 1
        for i, node in enumerate(nodes):
            if node is None:
                continue
            # палітра рівнів
            palette = ["#9dd7ff", "#7fc6ff", "#66b3ff", "#4da2ff", "#338fff"]
            node.color = palette[level % len(palette)]
            if i == next_break:
                level += 1
                next_break = 2**(level+1) - 2

    return nodes[0]  # корінь дерева

def draw_heap(heap, color_rule="root-min"):
    """
    фасад: з масиву-купи → дерево → малюнок.
    """
    root = heap_to_tree(heap, color_rule=color_rule)
    draw_tree(root)


#   Приклади

if __name__ == "__main__":
    # Мін-купа (root = найменший)
    min_heap = [0, 1, 4, 5, 10, 3]
    draw_heap(min_heap, color_rule="level")

    # Макс-купа (root = найбільший)
    max_heap = [42, 29, 18, 14, 7, 18, 12, 11, 13]
    draw_heap(max_heap, color_rule="root-min")
