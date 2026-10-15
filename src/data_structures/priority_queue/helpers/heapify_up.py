"""Repair a binary max-heap from a newly inserted or replaced element."""

from src.models.data_item import DataItem


def heapify_up(heap: list[DataItem], index: int) -> None:
    """Move a valid indexed element upward until its parent is at least as large.

    The rest of the heap must already satisfy max-heap order. Each step
    moves to parent ``(index - 1) // 2``, taking O(log n) time overall.
    """
    while index > 0:
        parent = (index - 1) // 2
        if heap[parent].priority >= heap[index].priority:
            break
        heap[parent], heap[index] = heap[index], heap[parent]
        index = parent
