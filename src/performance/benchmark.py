"""Compare verified hash and manual linear searches on a shared dataset."""

from collections.abc import Callable, Sequence
import time

from src.config.settings import BENCHMARK_REPETITIONS, BENCHMARK_TARGETS, BENCHMARK_WARMUP
from src.data_structures.hash_table import HashTable
from src.dataset.validator import validate_dataset
from src.models.data_item import DataItem
from src.performance.linear_search import linear_search
from src.performance.result import BenchmarkResult, SearchTiming


def _measure_hash(search: Callable[[int], DataItem | None], key: int, repetitions: int) -> float:
    started = time.perf_counter()
    for _ in range(repetitions):
        search(key)
    return time.perf_counter() - started


def _measure_linear(records: tuple[DataItem, ...], key: int, repetitions: int) -> float:
    started = time.perf_counter()
    for _ in range(repetitions):
        linear_search(records, key)
    return time.perf_counter() - started


def run_benchmark(
    records: Sequence[DataItem],
    hash_table: HashTable[DataItem] | None = None,
    *,
    targets: Sequence[tuple[int, str]] = BENCHMARK_TARGETS,
    warmup: int = BENCHMARK_WARMUP,
    repetitions: int = BENCHMARK_REPETITIONS,
) -> BenchmarkResult:
    """Verify records and target results before measuring either algorithm.

    Build a fresh table unless one is supplied. A supplied table must match
    the complete dataset; it is never changed. Setup, checks, warm-up, output,
    and file I/O are excluded from measured time. Alternate the first timed
    algorithm across targets. This function neither prints nor saves files.
    """
    for value, name, minimum in ((warmup, "warmup", 0), (repetitions, "repetitions", 1)):
        if type(value) is not int or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}")
    students = tuple(records)
    validate_dataset(students)
    selected = tuple(targets)
    if not selected:
        raise ValueError("at least one benchmark target is required")
    seen: set[int] = set()
    for target in selected:
        if not isinstance(target, (tuple, list)) or len(target) != 2:
            raise ValueError("targets must be (student_id, scenario) pairs")
        key, scenario = target
        if type(key) is not int:
            raise ValueError("target student_id must be an integer")
        if not isinstance(scenario, str) or not scenario.strip():
            raise ValueError("target scenario must be a non-empty string")
        if key in seen:
            raise ValueError("target student IDs must be unique")
        seen.add(key)

    table = HashTable[DataItem]() if hash_table is None else hash_table
    if hash_table is None:
        for student in students:
            table.insert(student.student_id, student)
    search = table.search
    if table.item_count != len(students) or any(
        search(student.student_id) != student for student in students
    ):
        raise ValueError("hash table and dataset must contain the same records")

    # Validate every target before starting even the first measured search.
    verified = []
    for key, scenario in selected:
        expected = linear_search(students, key)
        if search(key) != expected:
            raise ValueError(f"hash and linear search disagree for student_id {key}")
        verified.append((key, scenario.strip(), expected is not None))

    timings = []
    for index, (key, scenario, found) in enumerate(verified):
        for _ in range(warmup):
            search(key)
            linear_search(students, key)
        if index % 2 == 0:
            hash_seconds = _measure_hash(search, key, repetitions)
            linear_seconds = _measure_linear(students, key, repetitions)
        else:
            linear_seconds = _measure_linear(students, key, repetitions)
            hash_seconds = _measure_hash(search, key, repetitions)
        timings.append(SearchTiming(
            key, scenario, found, repetitions, hash_seconds, linear_seconds,
        ))
    return BenchmarkResult(
        dataset_size=len(students), table_size=table.table_size, warmup=warmup,
        repetitions=repetitions, timings=tuple(timings),
    )
