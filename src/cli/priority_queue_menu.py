"""Priority-queue prompts and presentation through the public queue API."""

from src.cli.application import Application
from src.cli.input_handler import read_student, read_student_id
from src.cli.navigation import run_menu
from src.utils.display import format_student


def insert_student(app: Application) -> None:
    student = read_student()
    app.priority_queue.insert(student)
    print(f"Inserted: {format_student(student)}")


def search_student(app: Application) -> None:
    print(format_student(app.priority_queue.search(read_student_id())))


def delete_student(app: Application) -> None:
    key = read_student_id()
    print(f"Deleted student {key}." if app.priority_queue.delete(key) else "No student found.")


def peek_student(app: Application) -> None:
    student = app.priority_queue.peek()
    print(f"Highest priority: {format_student(student)}" if student else "Priority queue is empty.")


def extract_student(app: Application) -> None:
    student = app.priority_queue.extract_max()
    print(f"Extracted: {format_student(student)}" if student else "Priority queue is empty.")


def display_heap(app: Application) -> None:
    print(f"Priority queue: {len(app.priority_queue)} students (heap array order)")
    if not app.priority_queue:
        print("Priority queue is empty.")
    for index, student in enumerate(app.priority_queue.heap):
        print(f"[{index}] {format_student(student)}")


def show_validation(app: Application) -> None:
    print("Heap is valid." if app.priority_queue.validate_heap() else "Heap is invalid.")


def priority_queue_menu(app: Application) -> None:
    run_menu("Priority Queue", {
        "1": ("Insert Student", lambda: insert_student(app)),
        "2": ("Search Student", lambda: search_student(app)),
        "3": ("Delete Student", lambda: delete_student(app)),
        "4": ("Peek Highest Priority", lambda: peek_student(app)),
        "5": ("Extract Maximum", lambda: extract_student(app)),
        "6": ("Display Heap", lambda: display_heap(app)),
        "7": ("Validate Heap", lambda: show_validation(app)),
    })
