"""Loaded dataset and independently owned interactive data structures."""

from collections.abc import Sequence
from pathlib import Path

from src.config.settings import DATASET_PATH, PERFORMANCE_RESULTS_PATH
from src.data_structures.hash_table import HashTable
from src.data_structures.priority_queue import PriorityQueue
from src.dataset.data_loader import load_or_generate_dataset
from src.models.data_item import DataItem


class Application:
    """Keep source records separate from editable hash-table and queue state."""

    def __init__(
        self,
        dataset_path: str | Path = DATASET_PATH,
        results_path: str | Path = PERFORMANCE_RESULTS_PATH,
    ) -> None:
        self.dataset_path = Path(dataset_path).resolve()
        self.results_path = Path(results_path).resolve()
        if self.dataset_path == self.results_path:
            raise ValueError("results path must not overwrite the source CSV dataset")
        self._replace_records(load_or_generate_dataset(self.dataset_path))

    def _replace_records(self, records: Sequence[DataItem]) -> None:
        """Build both containers fully before publishing replacement state."""
        students = tuple(records)
        table = HashTable[DataItem]()
        queue = PriorityQueue()
        for student in students:
            table.insert(student.student_id, student)
            queue.insert(student)
        self.records, self.hash_table, self.priority_queue = students, table, queue
