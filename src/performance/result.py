"""Immutable measured search results and their derived comparisons."""

from dataclasses import dataclass, field
import math
import platform
from pathlib import Path

from src.config.settings import DATASET_PATH, PERFORMANCE_RESULTS_PATH


def _validate_count(value: int, name: str, minimum: int = 1) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


@dataclass(frozen=True, slots=True)
class SearchTiming:
    """Measured totals for one target; averages and ratio are calculated."""

    student_id: int
    scenario: str
    found: bool
    repetitions: int
    hash_total_seconds: float
    linear_total_seconds: float

    def __post_init__(self) -> None:
        if type(self.student_id) is not int:
            raise ValueError("student_id must be an integer")
        if not isinstance(self.scenario, str) or not self.scenario.strip():
            raise ValueError("scenario must be a non-empty string")
        if type(self.found) is not bool:
            raise ValueError("found must be a boolean")
        _validate_count(self.repetitions, "repetitions")
        for name in ("hash_total_seconds", "linear_total_seconds"):
            value = getattr(self, name)
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")

    @property
    def hash_average_seconds(self) -> float:
        return self.hash_total_seconds / self.repetitions

    @property
    def linear_average_seconds(self) -> float:
        return self.linear_total_seconds / self.repetitions

    @property
    def speed_ratio(self) -> float | None:
        """Linear time / hash time; None when the hash timer reads zero."""
        if self.hash_total_seconds == 0:
            return None
        return self.linear_total_seconds / self.hash_total_seconds


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """A run with equal repetitions for every target and search method."""

    dataset_size: int
    table_size: int
    warmup: int
    repetitions: int
    timings: tuple[SearchTiming, ...]
    python_version: str = field(default_factory=platform.python_version)
    platform_name: str = field(default_factory=platform.platform)

    def __post_init__(self) -> None:
        _validate_count(self.dataset_size, "dataset_size")
        _validate_count(self.table_size, "table_size")
        _validate_count(self.warmup, "warmup", minimum=0)
        _validate_count(self.repetitions, "repetitions")
        object.__setattr__(self, "timings", tuple(self.timings))
        if not self.timings or any(not isinstance(row, SearchTiming) for row in self.timings):
            raise ValueError("timings must contain SearchTiming records")
        if any(row.repetitions != self.repetitions for row in self.timings):
            raise ValueError("every target must use the run's repetition count")
        if len({row.student_id for row in self.timings}) != len(self.timings):
            raise ValueError("target student IDs must be unique")

    @property
    def measured_searches_per_algorithm(self) -> int:
        return self.repetitions * len(self.timings)

    @property
    def hash_total_seconds(self) -> float:
        return sum(row.hash_total_seconds for row in self.timings)

    @property
    def linear_total_seconds(self) -> float:
        return sum(row.linear_total_seconds for row in self.timings)

    @property
    def hash_average_seconds(self) -> float:
        return self.hash_total_seconds / self.measured_searches_per_algorithm

    @property
    def linear_average_seconds(self) -> float:
        return self.linear_total_seconds / self.measured_searches_per_algorithm

    @property
    def speed_ratio(self) -> float | None:
        """Ratio of overall totals, rather than an average of target ratios."""
        if self.hash_total_seconds == 0:
            return None
        return self.linear_total_seconds / self.hash_total_seconds


def _ratio_text(ratio: float | None) -> str:
    return "N/A" if ratio is None else f"{ratio:.3f}x"


def format_results(result: BenchmarkResult) -> str:
    """Format measured totals, per-search averages, and ratios outside timing."""
    lines = [
        "Hash Table vs. Linear Search Benchmark",
        "=" * 112,
        f"Dataset records: {result.dataset_size}",
        f"Hash table buckets: {result.table_size}",
        f"Targets: {len(result.timings)}",
        f"Warm-up searches per target per algorithm: {result.warmup}",
        f"Measured repetitions per target per algorithm: {result.repetitions}",
        f"Measured searches per algorithm: {result.measured_searches_per_algorithm}",
        "Timer: time.perf_counter()",
        "Measured order: hash first on alternating targets; linear first on the others.",
        "Setup, correctness checks, warm-up, printing, and file I/O are excluded from timing.",
        f"Python: {result.python_version}",
        f"Platform: {result.platform_name}",
        "",
        f"{'ID':>6} {'Scenario':<12} {'Found':<5} {'Hash total (s)':>15} "
        f"{'Linear total (s)':>17} {'Hash avg (us)':>15} {'Linear avg (us)':>17} {'Linear/hash':>12}",
        "-" * 112,
    ]
    for row in result.timings:
        lines.append(
            f"{row.student_id:>6} {row.scenario:<12} {'yes' if row.found else 'no':<5} "
            f"{row.hash_total_seconds:>15.9f} {row.linear_total_seconds:>17.9f} "
            f"{row.hash_average_seconds * 1_000_000:>15.6f} "
            f"{row.linear_average_seconds * 1_000_000:>17.6f} {_ratio_text(row.speed_ratio):>12}"
        )
    lines.extend([
        "",
        f"Overall hash total (s): {result.hash_total_seconds:.9f}",
        f"Overall linear total (s): {result.linear_total_seconds:.9f}",
        f"Overall average hash search (us): {result.hash_average_seconds * 1_000_000:.6f}",
        f"Overall average linear search (us): {result.linear_average_seconds * 1_000_000:.6f}",
        f"Overall linear/hash time ratio: {_ratio_text(result.speed_ratio)}",
        "",
        "Average = measured total / measured searches; us means microseconds.",
        "Ratio = linear time / hash time; above 1 means lower hash-search time,",
        "below 1 means lower linear-search time. N/A means the hash timer total was zero.",
        "These measurements describe this run, dataset, and machine; timings vary between runs.",
    ])
    return "\n".join(lines) + "\n"


def save_results(
    result: BenchmarkResult, path: str | Path = PERFORMANCE_RESULTS_PATH
) -> Path:
    """Save the latest report, creating its directory without altering the CSV."""
    destination = Path(path)
    if destination.resolve() == DATASET_PATH.resolve():
        raise ValueError("results path must not overwrite the source CSV dataset")
    report = format_results(result)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(report, encoding="utf-8")
    return destination
