"""Student priority queue backed by a manually maintained binary max-heap."""

from src.data_structures.priority_queue.helpers.validate_heap import validate_heap as is_valid_heap
from src.data_structures.priority_queue.operations.delete import delete as delete_student
from src.data_structures.priority_queue.operations.extract_max import extract_max as remove_maximum
from src.data_structures.priority_queue.operations.insert import insert as insert_student
from src.data_structures.priority_queue.operations.peek import peek as peek_maximum
from src.data_structures.priority_queue.operations.search import search as find_student
from src.dataset.validator import validate_student
from src.models.data_item import DataItem


def _validate_student_id(student_id: int) -> None:
    if type(student_id) is not int:
        raise TypeError("student_id must be an integer")
    if student_id <= 0:
        raise ValueError("student_id must be positive")


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

    def insert(self, student: DataItem) -> None:
        """Queue a valid student; raise ValueError for invalid or duplicate data.

        IDs remain unique so search and deletion identify one record. Checking
        uniqueness by scanning the list makes insertion O(n), including the
        O(log n) upward heap repair. The source student is never modified.
        """
        validate_student(student)
        insert_student(self._heap, student)

    def extract_max(self) -> DataItem | None:
        """Remove and return a highest-priority student, or None when empty."""
        return remove_maximum(self._heap)

    def peek(self) -> DataItem | None:
        """Return a highest-priority student without removing it, or None."""
        return peek_maximum(self._heap)

    def search(self, student_id: int) -> DataItem | None:
        """Return a student by positive integer ID, or None when missing."""
        _validate_student_id(student_id)
        return find_student(self._heap, student_id)

    def delete(self, student_id: int) -> bool:
        """Remove a student by ID; return whether removal occurred."""
        _validate_student_id(student_id)
        return delete_student(self._heap, student_id)

    def validate_heap(self) -> bool:
        """Check every parent/child priority, treating an empty heap as valid."""
        return is_valid_heap(self._heap)
