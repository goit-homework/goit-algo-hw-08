"""
Просте двійкове дерево пошуку (Binary Search Tree).

Підтримує вставку, пошук мінімуму, суму всіх значень та візуалізацію
через matplotlib (зберігається у PNG).

Інваріант: для кожного вузла — все що зліва < node.value < все що справа.
Дублікати ігноруються.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    value: int | float
    left: Node | None = field(default=None, repr=False)
    right: Node | None = field(default=None, repr=False)


class BST:
    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int | float) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Node | None, value: int | float) -> Node:
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        # value == node.value -> ignore duplicate
        return node

    @classmethod
    def from_iterable(cls, values) -> BST:
        tree = cls()
        for v in values:
            tree.insert(v)
        return tree


def find_min(tree: BST) -> int | float:
    """
    Найменше значення в BST = найлівіший вузол.

    Йдемо по лівих посиланнях до тих пір, доки є куди йти. Це O(h),
    де h — висота дерева, замість O(n) як був би повний обхід.
    """
    if tree.root is None:
        raise ValueError("дерево порожнє")
    node = tree.root
    while node.left is not None:
        node = node.left
    return node.value


def total_sum(tree: BST) -> int | float:
    """
    Сума всіх значень у дереві.

    Тут BST-властивість не допомагає (доводиться відвідати кожен вузол),
    тому це звичайний рекурсивний обхід — O(n).
    """
    return _sum(tree.root)


def _sum(node: Node | None) -> int | float:
    if node is None:
        return 0
    return node.value + _sum(node.left) + _sum(node.right)


# ---------- візуалізація ----------

def _compute_positions(root: Node | None) -> dict[int, tuple[float, float]]:
    """
    Для кожного вузла повертає координати (x, y) для малювання.

    x присвоюється in-order обходом — це гарантує що ліві піддерева
    будуть зліва, а праві справа, без перетину гілок.
    y = від'ємна глибина (корінь зверху).
    """
    positions: dict[int, tuple[float, float]] = {}
    counter = [0]

    def visit(node: Node | None, depth: int) -> None:
        if node is None:
            return
        visit(node.left, depth + 1)
        positions[id(node)] = (counter[0], -depth)
        counter[0] += 1
        visit(node.right, depth + 1)

    visit(root, 0)
    return positions


def draw_tree(tree: BST, filename: str, title: str = "BST") -> None:
    """Малює BST через networkx + matplotlib і зберігає у PNG."""
    import matplotlib.pyplot as plt
    import networkx as nx

    if tree.root is None:
        raise ValueError("неможливо намалювати порожнє дерево")

    g = nx.DiGraph()
    labels: dict[int, str] = {}
    positions = _compute_positions(tree.root)

    def add_edges(node: Node | None) -> None:
        if node is None:
            return
        g.add_node(id(node))
        labels[id(node)] = str(node.value)
        for child in (node.left, node.right):
            if child is not None:
                g.add_edge(id(node), id(child))
                add_edges(child)

    add_edges(tree.root)

    fig, ax = plt.subplots(figsize=(max(6, len(positions) * 0.6), 5))
    nx.draw(
        g, pos=positions, ax=ax, with_labels=True, labels=labels,
        node_size=900, node_color="#90caf9", edgecolors="#1565c0",
        font_size=11, font_weight="bold", arrows=False,
    )
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"  графік збережено: {filename}")
