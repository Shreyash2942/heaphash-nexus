"""Generate reproducible student records without changing global random state.

Run ``python -m src.dataset.data_generator`` to create the default CSV.
An existing file is preserved unless ``--overwrite`` is explicitly supplied.
"""

import argparse
import random
from pathlib import Path

from src.config.settings import (
    DATASET_PATH,
    DATASET_SIZE,
    MAX_PRIORITY,
    MIN_PRIORITY,
    RANDOM_SEED,
    START_STUDENT_ID,
)
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
