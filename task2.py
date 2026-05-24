"""
Завдання 2: знайти суму всіх значень у BST.

Рекурсивний обхід — кожен вузол відвідується рівно раз, O(n).
"""

from bst import BST, total_sum


if __name__ == "__main__":
    values = [50, 30, 70, 20, 40, 60, 80, 10, 35, 45]
    tree = BST.from_iterable(values)

    print(f"Вставлено значення: {values}")
    print(f"Сума через sum():   {sum(values)}  (перевірка)")
    print(f"Сума у дереві:      {total_sum(tree)}")
