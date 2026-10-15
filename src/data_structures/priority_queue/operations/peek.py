"""Read a max-heap's root without changing the queue."""

from src.models.data_item import DataItem


def peek(heap: list[DataItem]) -> DataItem | None:
    """Return a highest-priority student in O(1), or None when empty."""
    return heap[0] if heap else None
