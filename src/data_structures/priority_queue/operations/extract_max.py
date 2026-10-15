"""Remove the highest-priority student from a binary max-heap."""

from src.data_structures.priority_queue.helpers.heapify_down import heapify_down
from src.models.data_item import DataItem


def extract_max(heap: list[DataItem]) -> DataItem | None:
    """Return and remove the root in O(log n), or return None when empty."""
    if not heap:
        return None
    maximum = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        heapify_down(heap, 0)
    return maximum
