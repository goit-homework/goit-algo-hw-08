"""
Завдання 1: знайти найменше значення в BST.

Використовуємо властивість BST: мінімум завжди в найлівішому вузлі.
"""

from bst import BST, find_min, draw_tree


if __name__ == "__main__":
    values = [50, 30, 70, 20, 40, 60, 80, 10, 35, 45]
    tree = BST.from_iterable(values)

    print(f"Вставлено значення: {values}")
    print(f"Мінімум у дереві:   {find_min(tree)}")

    draw_tree(tree, "tree.png", title="BST для task1 та task2")
