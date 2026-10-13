"""Generate reproducible student records without changing global random state.

Run ``python -m src.dataset.data_generator`` to create the default CSV.
An existing file is preserved unless ``--overwrite`` is explicitly supplied.
"""

import argparse
from collections.abc import Sequence
import csv
from dataclasses import asdict
import random
from pathlib import Path

from src.config.settings import (
    CSV_FIELDS,
    DATASET_PATH,
    DATASET_SIZE,
    MAX_PRIORITY,
    MIN_PRIORITY,
    RANDOM_SEED,
    START_STUDENT_ID,
)
from src.dataset.validator import validate_dataset
from src.models.data_item import DataItem

FIRST_NAMES = (
    "Alex", "Avery", "Cameron", "Casey", "Drew", "Emerson", "Harper",
    "Jamie", "Jordan", "Morgan", "Parker", "Quinn", "Riley", "Rowan", "Taylor",
)
LAST_NAMES = (
    "Adams", "Baker", "Brown", "Chen", "Davis", "Garcia", "Johnson",
    "Kim", "Lee", "Martinez", "Patel", "Robinson", "Smith", "Wilson", "Young",
)
PROGRAMS = (
    "Computer Science", "Information Technology", "Cybersecurity",
    "Business Management", "Accounting", "Healthcare Administration",
)


def generate_students(
    size: int = DATASET_SIZE,
    seed: int = RANDOM_SEED,
    start_student_id: int = START_STUDENT_ID,
) -> list[DataItem]:
    """Return sequentially identified students generated with a local seed.

    Names and priorities may repeat; student IDs never repeat. Smaller sizes
    are supported for tests and demonstrations.
    """
    if type(size) is not int or size <= 0:
        raise ValueError("size must be a positive integer")
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    if type(start_student_id) is not int or start_student_id <= 0:
        raise ValueError("start_student_id must be a positive integer")

    rng = random.Random(seed)
    return [
        DataItem(
            student_id=start_student_id + offset,
            name=f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}",
            program=rng.choice(PROGRAMS),
            priority=rng.randint(MIN_PRIORITY, MAX_PRIORITY),
        )
        for offset in range(size)
    ]


def write_dataset(
    path: str | Path = DATASET_PATH,
    records: Sequence[DataItem] | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    """Write validated students to CSV, protecting existing files by default.

    Validation completes before opening the destination, including when
    overwriting, so invalid records cannot erase an existing valid dataset.
    """
    students = generate_students() if records is None else list(records)
    validate_dataset(students)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if overwrite else "x"
    with destination.open(mode, encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(student) for student in students)
    return destination


def main() -> None:
    """Create or validate the project CSV from the command line."""
    from src.dataset.data_loader import load_dataset

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DATASET_PATH)
    parser.add_argument("--overwrite", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.output.exists() and not arguments.overwrite:
            students = load_dataset(arguments.output)
            print(f"Preserved existing dataset: {arguments.output} ({len(students)} records)")
        else:
            destination = write_dataset(
                arguments.output, overwrite=arguments.overwrite
            )
            students = load_dataset(destination)
            print(f"Generated dataset: {destination} ({len(students)} records)")
    except (OSError, ValueError) as error:
        parser.exit(status=1, message=f"Dataset error: {error}\n")


if __name__ == "__main__":
    main()
