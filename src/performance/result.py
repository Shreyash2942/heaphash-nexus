"""Immutable measured search results and their derived comparisons."""

from dataclasses import dataclass, field
import math
import platform


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
