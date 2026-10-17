"""Complete demonstration using core APIs and separate temporary containers."""

from src.cli.application import Application
from src.cli.hash_table_menu import collision_demonstration
from src.config.settings import MAX_PRIORITY
from src.data_structures.hash_table import HashTable
from src.data_structures.priority_queue import PriorityQueue
from src.dataset.data_loader import load_dataset
from src.models.data_item import DataItem
from src.performance.benchmark import run_benchmark
from src.performance.result import BenchmarkResult, format_results, save_results


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"demonstration failed: {message}")


def run_demonstration(app: Application) -> BenchmarkResult:
    """Exercise requirements without changing the user's interactive containers."""
    original_csv = app.dataset_path.read_bytes()
    records = tuple(load_dataset(app.dataset_path))
    print(f"1. Loaded and validated {len(records)} students.")
    table = HashTable[DataItem]()
    queue = PriorityQueue()
    for student in records:
        table.insert(student.student_id, student)
        queue.insert(student)
    temporary = DataItem(
        max(student.student_id for student in records) + 1,
        "Demonstration Student", "Computer Science", MAX_PRIORITY,
    )

    table.insert(temporary.student_id, temporary)
    _require(table.search(temporary.student_id) is temporary, "hash insert/search")
    _require(table.delete(temporary.student_id), "hash deletion")
    _require(table.search(temporary.student_id) is None, "hash missing search")
    print("2. Hash table insert, search, and delete passed.")
    collision_demonstration()
    print("3. Separate chaining and collision deletion passed.")

    queue.insert(temporary)
    _require(queue.search(temporary.student_id) is temporary, "queue insert/search")
    _require(queue.validate_heap(), "heap after insertion")
    _require(queue.delete(temporary.student_id), "queue deletion")
    _require(queue.search(temporary.student_id) is None, "queue missing search")
    _require(queue.validate_heap(), "heap after deletion")
    print("4. Priority queue insert, search, and delete passed.")
    before = len(queue)
    maximum = queue.peek()
    _require(maximum is not None and len(queue) == before, "peek must preserve root")
    extracted = queue.extract_max()
    _require(extracted is maximum and len(queue) == before - 1, "extract-max")
    _require(table.search(extracted.student_id) is extracted, "independent hash state")
    print("5. Peek and extract-max passed; hash-table contents stayed independent.")
    _require(queue.validate_heap(), "heap after extraction")
    print("6. Max-heap validation passed.")

    result = run_benchmark(records, table)
    print("7. Hash and linear search agreement and benchmarking completed.")
    destination = save_results(result, app.results_path)
    print(format_results(result), end="")
    _require(app.dataset_path.read_bytes() == original_csv, "source CSV was changed")
    print(f"8. Results saved to: {destination}")
    print("Complete demonstration passed. Interactive structures were preserved.")
    return result
