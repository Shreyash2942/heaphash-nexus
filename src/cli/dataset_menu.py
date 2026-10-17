"""Dataset information, preview, and source-file validation."""

from src.cli.application import Application
from src.cli.navigation import run_menu
from src.dataset.data_loader import load_dataset
from src.utils.display import display_students


def show_information(app: Application) -> None:
    print(f"Source CSV: {app.dataset_path}")
    print(f"Loaded students: {len(app.records)}")
    print(f"Student IDs: {min(s.student_id for s in app.records)}-{max(s.student_id for s in app.records)}")
    print(f"Priorities: {min(s.priority for s in app.records)}-{max(s.priority for s in app.records)}")
    print("Interactive edits do not change these source records.")


def preview_dataset(app: Application) -> None:
    preview = app.records[:10]
    print(f"Showing {len(preview)} of {len(app.records)} loaded students:")
    display_students(preview)


def validate_source(app: Application) -> None:
    fresh = tuple(load_dataset(app.dataset_path))
    print(f"Dataset valid: {len(fresh)} students with unique IDs and valid fields.")
    if fresh != app.records:
        print("The CSV differs from the loaded records. Use Reset Data Structures to reload it.")


def dataset_menu(app: Application) -> None:
    run_menu("Dataset Information", {
        "1": ("Show Dataset Information", lambda: show_information(app)),
        "2": ("Preview First 10 Students", lambda: preview_dataset(app)),
        "3": ("Validate Source CSV", lambda: validate_source(app)),
    })
