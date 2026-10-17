"""Reusable prompts that retry invalid input and propagate exit signals."""

from collections.abc import Collection

from src.config.settings import MAX_PRIORITY, MIN_PRIORITY
from src.models.data_item import DataItem


def read_choice(prompt: str, choices: Collection[str]) -> str:
    """Read one listed choice; EOF and Ctrl+C are handled by the entry point."""
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print(f"Choose one of: {', '.join(choices)}.")


def read_int(
    prompt: str, *, minimum: int | None = None, maximum: int | None = None
) -> int:
    """Read a whole number within optional inclusive bounds."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Enter a value of at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a value no greater than {maximum}.")
            continue
        return value


def read_text(prompt: str) -> str:
    """Read a non-empty name or program, trimming surrounding whitespace."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("A value is required.")


def read_student_id() -> int:
    return read_int("Student ID: ", minimum=1)


def read_student() -> DataItem:
    return DataItem(
        student_id=read_student_id(),
        name=read_text("Name: "),
        program=read_text("Program: "),
        priority=read_int(
            f"Priority ({MIN_PRIORITY}-{MAX_PRIORITY}): ",
            minimum=MIN_PRIORITY, maximum=MAX_PRIORITY,
        ),
    )
