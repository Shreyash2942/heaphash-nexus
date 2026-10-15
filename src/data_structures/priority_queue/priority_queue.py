"""Student priority queue backed by a manually maintained binary max-heap."""

from src.models.data_item import DataItem


class PriorityQueue:
    """Own an independent list of student records ordered by priority.

    The greatest priority is at index 0. Public snapshots cannot change the
    heap's containers, and immutable DataItem values protect stored keys and
    priorities. Equal priorities do not promise insertion-order stability.
    """

    def __init__(self) -> None:
        self._heap: list[DataItem] = []

    @property
    def item_count(self) -> int:
        """Number of students currently queued."""
        return len(self._heap)

    @property
    def heap(self) -> tuple[DataItem, ...]:
        """Return an immutable O(n) snapshot of the heap in array order."""
        return tuple(self._heap)

    def __len__(self) -> int:
        return len(self._heap)
