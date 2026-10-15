"""Find a student by ID without assuming IDs follow heap order."""

from src.models.data_item import DataItem


def search(heap: list[DataItem], student_id: int) -> DataItem | None:
    """Scan by student ID in O(n), returning None when missing."""
    for student in heap:
        if student.student_id == student_id:
            return student
    return None
