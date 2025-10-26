# Завдання 1. Однозв'язний список


from collections.abc import Iterable

class Node:
    """Вузол однозв'язного списку."""
    __slots__ = ("data", "next")

    def __init__(self, data: object, next: "Node | None" = None):
        self.data = data
        self.next = next


class LinkedList:
    """Клас однозв'язного списку з базовими операціями."""
    def __init__(self, items: Iterable | None = None):
        self.head: Node | None = None
        if items:
            for x in items:
                self.append(x)


    # Додаткові методи

    def append(self, data: object) -> None:
        """Додає вузол у кінець списку."""
        new = Node(data)
        if not self.head:
            self.head = new
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new

    def to_list(self) -> list[object]:
        """Повертає список значень для зручного виводу."""
        out: list[object] = []
        cur = self.head
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out


    # 1) Реверсування списку

    def reverse(self) -> None:
        """Реверсує список, змінюючи посилання між вузлами."""
        prev, cur = None, self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    # 2) Сортування методом вставок


    def insertion_sort(self) -> None:
        """Сортує однозв’язний список методом вставок (in-place)."""
        sorted_head: Node | None = None
        cur = self.head
        while cur:
            nxt = cur.next
            sorted_head = self._sorted_insert_node(sorted_head, cur)
            cur = nxt
        self.head = sorted_head

    @staticmethod
    def _sorted_insert_node(head: Node | None, node: Node) -> Node | None:
        """Вставка вузла у відсортований список."""
        node.next = None
        if head is None or node.data < head.data:
            node.next = head
            return node
        cur = head
        while cur.next and cur.next.data <= node.data:
            cur = cur.next
        node.next = cur.next
        cur.next = node
        return head

    # 3) Злиття двох відсортованих списків

    @staticmethod
    def merge_sorted_lists(a: "LinkedList", b: "LinkedList") -> "LinkedList":
        """Зливає два відсортовані списки в один відсортований."""
        dummy = Node(None)
        tail = dummy
        pa, pb = a.head, b.head

        while pa and pb:
            if pa.data <= pb.data:
                tail.next = pa
                pa = pa.next
            else:
                tail.next = pb
                pb = pb.next
            tail = tail.next

        tail.next = pa if pa else pb

        merged = LinkedList()
        merged.head = dummy.next
        return merged



# ТЕСТУВАННЯ


# Реверсування
lst = LinkedList([5, 3, 8, 4, 2])
lst.reverse()
assert lst.to_list() == [2, 4, 8, 3, 5], "Помилка у реверсі"

# Сортування вставками
lst.insertion_sort()
assert lst.to_list() == [2, 3, 4, 5, 8], "Помилка у сортуванні вставками"

# Злиття двох відсортованих списків
a = LinkedList([1, 3, 5])
b = LinkedList([2, 4, 6, 7])
merged = LinkedList.merge_sorted_lists(a, b)
assert merged.to_list() == [1, 2, 3, 4, 5, 6, 7], "Помилка у злитті списків"

print("Усі три критерії виконано: реверсування, сортування, злиття — працюють коректно.")
