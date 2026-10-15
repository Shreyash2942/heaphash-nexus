"""Restore max-heap order below an element after removal or replacement."""

from src.models.data_item import DataItem


def heapify_down(heap: list[DataItem], index: int) -> None:
    """Repair downward from a valid index in O(log n) time.

    Child subtrees must already satisfy max-heap order. Children occupy
    ``2 * index + 1`` and ``2 * index + 2``; swap with the larger child.
    An empty heap at index 0 is also safe.
    """
    while True:
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index
        if left < len(heap) and heap[left].priority > heap[largest].priority:
            largest = left
        if right < len(heap) and heap[right].priority > heap[largest].priority:
            largest = right
        if largest == index:
            break
        heap[index], heap[largest] = heap[largest], heap[index]
        index = largest
