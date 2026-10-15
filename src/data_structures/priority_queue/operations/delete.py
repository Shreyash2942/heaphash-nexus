"""Delete an arbitrary student and restore heap order in the correct direction."""

from src.data_structures.priority_queue.helpers.heapify_down import heapify_down
from src.data_structures.priority_queue.helpers.heapify_up import heapify_up
from src.models.data_item import DataItem


def delete(heap: list[DataItem], student_id: int) -> bool:
    """Remove a student by ID and report success; return False when missing.

    Finding the record takes O(n). If the last record replaces it, repair
    upward when it exceeds its new parent; otherwise repair downward.
    Removing the last element needs no repair. Heap repair takes O(log n).
    """
    for index, student in enumerate(heap):
        if student.student_id != student_id:
            continue
        last = heap.pop()
        if index < len(heap):
            heap[index] = last
            parent = (index - 1) // 2
            if index > 0 and heap[index].priority > heap[parent].priority:
                heapify_up(heap, index)
            else:
                heapify_down(heap, index)
        return True
    return False
