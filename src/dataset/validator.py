"""Validation shared by generated records and CSV loading."""

from collections.abc import Sequence

from src.config.settings import MAX_PRIORITY, MIN_PRIORITY
from src.models.data_item import DataItem


def validate_student(student: DataItem) -> None:
    """Raise ``ValueError`` if any required student field is invalid."""
    if not isinstance(student, DataItem):
        raise ValueError("record must be a DataItem")
    if type(student.student_id) is not int or student.student_id <= 0:
        raise ValueError("student_id must be a positive integer")
    if not isinstance(student.name, str) or not student.name.strip():
        raise ValueError("name must be a non-empty string")
    if not isinstance(student.program, str) or not student.program.strip():
        raise ValueError("program must be a non-empty string")
    if type(student.priority) is not int:
        raise ValueError("priority must be an integer")
    if not MIN_PRIORITY <= student.priority <= MAX_PRIORITY:
        raise ValueError(
            f"priority must be between {MIN_PRIORITY} and {MAX_PRIORITY}"
        )


def validate_dataset(
    records: Sequence[DataItem], expected_size: int | None = None
) -> None:
    """Validate all fields, unique IDs, and optionally the exact record count.

    A dataset must contain at least one student. Equal names and priorities
    are valid. Booleans are rejected for integer fields.
    """
    if expected_size is not None:
        if type(expected_size) is not int or expected_size <= 0:
            raise ValueError("expected_size must be a positive integer or None")
        if len(records) != expected_size:
            raise ValueError(
                f"expected {expected_size} records, found {len(records)}"
            )
    if not records:
        raise ValueError("dataset must contain at least one record")

    seen_ids: set[int] = set()
    for position, student in enumerate(records, start=1):
        try:
            validate_student(student)
        except ValueError as error:
            raise ValueError(f"record {position}: {error}") from error
        if student.student_id in seen_ids:
            raise ValueError(
                f"record {position}: duplicate student_id {student.student_id}"
            )
        seen_ids.add(student.student_id)
