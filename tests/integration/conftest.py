"""Shared real dataset and independent structures for integration tests."""

import pytest

from src.config.settings import DATASET_PATH
from src.data_structures.hash_table import HashTable
from src.data_structures.priority_queue import PriorityQueue
from src.dataset.data_loader import load_dataset


@pytest.fixture(scope="session")
def records():
    """Load the real CSV once, keeping immutable records shared across tests."""
    original_csv = DATASET_PATH.read_bytes()
    students = tuple(load_dataset())
    yield students
    assert DATASET_PATH.read_bytes() == original_csv


@pytest.fixture
def structures(records):
    """Build fresh mutable containers referencing the same loaded students."""
    table = HashTable()
    queue = PriorityQueue()
    for student in records:
        table.insert(student.student_id, student)
        queue.insert(student)
    return table, queue
