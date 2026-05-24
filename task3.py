"""
Завдання 3: оптимальне з'єднання кабелів.

Класична задача: маємо n кабелів різної довжини, треба з'єднати їх
у один. Кожне з'єднання двох кабелів коштує суму їхніх довжин,
загальна вартість — сума всіх з'єднань. Знайти порядок з мінімальною
вартістю.

Жадібна стратегія: на кожному кроці беремо два найкоротші кабелі,
з'єднуємо, кладемо результат назад. Min-heap дає це за O(n log n).

Чому жадібний підхід оптимальний: довжини коротких кабелів увійдуть
у вартість стільки разів, скільки рівнів вони пройдуть в "дереві
злиття". Якщо ми зливаємо короткі першими, вони беруть участь у
багатьох наступних сумах — це і є ціна. Тому "відкладати" короткі
тільки збільшує штраф. Ця сама ідея лежить в основі алгоритму Хаффмана.
"""

from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass, field


@dataclass
class MergeNode:
    """Вузол у дереві злиття: лист = початковий кабель, внутрішній = з'єднання."""
    value: int
    left: MergeNode | None = field(default=None, repr=False)
    right: MergeNode | None = field(default=None, repr=False)


def min_merge_cost(cables: list[int], verbose: bool = False) -> tuple[int, MergeNode]:
    """
    Повертає (мінімальна_загальна_вартість, корінь_дерева_злиття).

    Дерево злиття — це послідовність операцій, представлена у вигляді
    бінарного дерева. Внутрішні вузли позначені сумою своїх дітей.
    Загальна вартість = сума значень усіх внутрішніх вузлів.
    """
    if not cables:
        return 0, MergeNode(0)
    if len(cables) == 1:
        return 0, MergeNode(cables[0])

    # лічильник потрібен для тай-брейку: коли значення рівні, heapq
    # буде намагатися порівнювати MergeNode об'єкти, і це впаде
    counter = itertools.count()
    heap: list[tuple[int, int, MergeNode]] = [
        (c, next(counter), MergeNode(c)) for c in cables
    ]
    heapq.heapify(heap)

    total_cost = 0
    step = 1
    while len(heap) > 1:
        v1, _, n1 = heapq.heappop(heap)
        v2, _, n2 = heapq.heappop(heap)
        merged_value = v1 + v2
        total_cost += merged_value
        merged_node = MergeNode(merged_value, n1, n2)
        heapq.heappush(heap, (merged_value, next(counter), merged_node))

        if verbose:
            print(f"  step {step:>2}: merge {v1} + {v2} = {merged_value}  (total cost: {total_cost})")
        step += 1

    return total_cost, heap[0][2]


def naive_merge_cost(cables: list[int]) -> int:
    """
    Наївний підхід: зливаємо у тому порядку як прийшли (left-fold).
    Корисно для порівняння — показує наскільки жадібний кращий.
    """
    if not cables:
        return 0
    current = cables[0]
    total = 0
    for c in cables[1:]:
        merged = current + c
        total += merged
        current = merged
    return total


# ---------- візуалізація дерева злиття ----------

def _compute_positions(root: MergeNode) -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}
    counter = [0]

    def visit(node: MergeNode | None, depth: int) -> None:
        if node is None:
            return
        visit(node.left, depth + 1)
        positions[id(node)] = (counter[0], -depth)
        counter[0] += 1
        visit(node.right, depth + 1)

    visit(root, 0)
    return positions


def draw_merge_tree(root: MergeNode, filename: str, title: str) -> None:
    """Малює дерево злиття: листи (оригінальні кабелі) зеленим, внутрішні вузли червоним."""
    import matplotlib.pyplot as plt
    import networkx as nx

    g = nx.DiGraph()
    labels: dict[int, str] = {}
    colors: list[str] = []
    positions = _compute_positions(root)

    def add(node: MergeNode | None) -> None:
        if node is None:
            return
        g.add_node(id(node))
        labels[id(node)] = str(node.value)
        for child in (node.left, node.right):
            if child is not None:
                g.add_edge(id(node), id(child))
                add(child)

    add(root)

    # вузли у порядку, в якому networkx їх віддасть
    for node_id in g.nodes:
        # лист, якщо не має вихідних ребер до дітей у нашому графі
        out = list(g.successors(node_id))
        colors.append("#a5d6a7" if not out else "#ef9a9a")

    fig, ax = plt.subplots(figsize=(max(7, len(positions) * 0.5), 5))
    nx.draw(
        g, pos=positions, ax=ax, with_labels=True, labels=labels,
        node_size=900, node_color=colors, edgecolors="#424242",
        font_size=10, font_weight="bold", arrows=False,
    )
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"  графік збережено: {filename}")


if __name__ == "__main__":
    cables = [8, 4, 6, 12, 3, 1, 5]

    print(f"Кабелі: {cables}")
    print()
    print("Жадібне об'єднання (min-heap):")
    optimal_cost, merge_root = min_merge_cost(cables, verbose=True)
    print(f"\n  оптимальна вартість: {optimal_cost}")

    naive = naive_merge_cost(cables)
    print(f"  наївне об'єднання (у порядку списку): {naive}")
    print(f"  економія від жадібного: {naive - optimal_cost} ({(naive - optimal_cost) / naive * 100:.1f}%)")

    draw_merge_tree(merge_root, "merge_tree.png", title=f"Дерево злиття (cost={optimal_cost})")
