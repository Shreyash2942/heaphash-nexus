"""Student presentation helpers; algorithms remain in data-structure packages."""

from collections.abc import Sequence

from src.models.data_item import DataItem


def format_student(student: DataItem | None) -> str:
    if student is None:
        return "No student found."
    return (
        f"ID: {student.student_id} | Name: {student.name} | "
        f"Program: {student.program} | Priority: {student.priority}"
    )


def display_students(records: Sequence[DataItem]) -> None:
    if not records:
        print("No students to display.")
        return
    for student in records:
        print(format_student(student))
