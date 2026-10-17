"""Main navigation and graceful application startup/exit."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from src.cli.application import Application
from src.cli.dataset_menu import dataset_menu
from src.cli.hash_table_menu import hash_table_menu
from src.cli.navigation import run_menu
from src.cli.performance_menu import performance_menu
from src.cli.priority_queue_menu import priority_queue_menu
from src.config.settings import DATASET_PATH, PERFORMANCE_RESULTS_PATH


def run(app: Application) -> None:
    print(f"Loaded {len(app.records)} students. Changes stay in the selected structure.")
    run_menu("Main Menu", {
        "1": ("Hash Table", lambda: hash_table_menu(app)),
        "2": ("Priority Queue", lambda: priority_queue_menu(app)),
        "3": ("Performance Comparison", lambda: performance_menu(app)),
        "4": ("Dataset Information", lambda: dataset_menu(app)),
    }, exit_label="Exit")
    print("Goodbye.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Hash Table and Priority Queue Project")
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    parser.add_argument("--results", type=Path, default=PERFORMANCE_RESULTS_PATH)
    arguments = parser.parse_args(argv)
    try:
        app = Application(arguments.dataset, arguments.results)
        run(app)
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
    except (OSError, ValueError, TypeError) as error:
        print(f"Unable to start application: {error}")
        return 1
    return 0
