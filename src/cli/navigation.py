"""Shared menu loop and recoverable action-error handling."""

from collections.abc import Callable, Mapping

from src.cli.input_handler import read_choice


def run_menu(
    title: str,
    actions: Mapping[str, tuple[str, Callable[[], object]]],
    *,
    exit_label: str = "Back",
) -> None:
    """Dispatch selected actions; invalid input retries without recursion."""
    while True:
        print(f"\n{title}")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print(f"0. {exit_label}")
        choice = read_choice("Choice: ", (*actions, "0"))
        if choice == "0":
            return
        try:
            actions[choice][1]()
        except (OSError, ValueError, TypeError) as error:
            print(f"Error: {error}")
