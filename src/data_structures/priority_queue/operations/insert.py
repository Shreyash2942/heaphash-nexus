"""Insert a student while preserving unique IDs and max-heap order."""

from src.data_structures.priority_queue.helpers.heapify_up import heapify_up
from src.models.data_item import DataItem


def insert(heap: list[DataItem], student: DataItem) -> None:
    """Append a validated student and repair upward; reject duplicate IDs.

    The O(n) ID scan completes before mutation, then heap maintenance takes
    O(log n). The public queue validates student fields before calling here.
    """
    for existing in heap:
        if existing.student_id == student.student_id:
            raise ValueError(
                f"student_id {student.student_id} already exists in priority queue"
            )
    heap.append(student)
    heapify_up(heap, len(heap) - 1)
