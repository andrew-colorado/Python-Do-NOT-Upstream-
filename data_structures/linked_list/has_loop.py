from __future__ import annotations

from collections.abc import Iterator
from typing import Any


class ContainsLoopError(Exception):
    pass


class Node:
    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next_node: Node | None = None

    def __iter__(self) -> Iterator[Any]:
        node = self
        visited = set()
        while node:
            if node in visited:
                raise ContainsLoopError
            visited.add(node)
            yield node.data
            node = node.next_node

    @property
    def has_loop(self) -> bool:
        """
        A loop is when the exact same Node appears more than once in a linked list.

        This uses Floyd's cycle-finding ("tortoise and hare") algorithm, which needs
        only O(1) auxiliary space instead of O(N). A slow pointer moves one node at a
        time and a fast pointer moves two nodes at a time. If the list has a loop, the
        fast pointer eventually catches up to the slow pointer. Otherwise, the fast
        pointer reaches the end of the list.
        https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare

        >>> root_node = Node(1)
        >>> root_node.next_node = Node(2)
        >>> root_node.next_node.next_node = Node(3)
        >>> root_node.next_node.next_node.next_node = Node(4)
        >>> root_node.has_loop
        False
        >>> root_node.next_node.next_node.next_node = root_node.next_node
        >>> root_node.has_loop
        True

        A single node, with or without a loop back to itself:

        >>> single_node = Node(1)
        >>> single_node.has_loop
        False
        >>> single_node.next_node = single_node
        >>> single_node.has_loop
        True

        Two nodes, with and without a loop back to the head:

        >>> head = Node(1)
        >>> head.next_node = Node(2)
        >>> head.has_loop
        False
        >>> head.next_node.next_node = head
        >>> head.has_loop
        True

        Different nodes holding equal data are not a loop:

        >>> head = Node(5)
        >>> head.next_node = Node(6)
        >>> head.next_node.next_node = Node(5)
        >>> head.next_node.next_node.next_node = Node(6)
        >>> head.has_loop
        False
        """
        slow_node: Node | None = self
        fast_node: Node | None = self
        while (
            slow_node is not None
            and fast_node is not None
            and fast_node.next_node is not None
        ):
            slow_node = slow_node.next_node
            fast_node = fast_node.next_node.next_node
            if slow_node is fast_node:
                return True
        return False
    root_node = Node(1)
    print(root_node.has_loop)  # False
