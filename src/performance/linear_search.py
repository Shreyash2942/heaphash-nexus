"""Manual student-ID search over the same records used by the hash table."""

from collections.abc import Sequence

from src.models.data_item import DataItem


def linear_search(records: Sequence[DataItem], student_id: int) -> DataItem | None:
    """Scan in dataset order and return the matching record or None in O(n).

    Like the integer-key hash table, this accepts any integer search key,
    excluding booleans. Student field validation happens before benchmarking.
    """
    if type(student_id) is not int:
        raise TypeError("student_id must be an integer")
    for student in records:
        if student.student_id == student_id:
            return student
    return None
