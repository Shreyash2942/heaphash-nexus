"""Check the parent/child ordering of a binary max-heap."""

from collections.abc import Sequence

from src.models.data_item import DataItem


def validate_heap(heap: Sequence[DataItem]) -> bool:
    """Return whether every parent priority is at least its child's in O(n).

    Empty and single-element heaps are valid, and equal priorities are
    allowed. Student field validation is performed separately at insertion.
    """
    for child in range(1, len(heap)):
        parent = (child - 1) // 2
        if heap[parent].priority < heap[child].priority:
            return False
    return True
