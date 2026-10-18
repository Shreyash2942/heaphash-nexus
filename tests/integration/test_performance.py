"""Search agreement, benchmark protocol, and result calculations for Day 4.

Synthetic clocks verify calculations without asserting machine-dependent speed.
Actual benchmark measurements are generated separately after correctness passes.
"""

from collections import Counter
from dataclasses import FrozenInstanceError, replace
from types import SimpleNamespace
import subprocess
import sys

import pytest

from src.config.settings import (
    BENCHMARK_REPETITIONS, BENCHMARK_TARGETS, BENCHMARK_WARMUP,
    DATASET_PATH, PROJECT_ROOT,
)
from src.performance import benchmark
from src.performance.benchmark import run_benchmark
from src.performance.linear_search import linear_search
from src.performance.result import BenchmarkResult, SearchTiming, format_results, save_results


def synthetic_result():
    """Known totals for arithmetic checks, not real performance measurements."""
    return BenchmarkResult(
        150, 211, 100, 10,
        (SearchTiming(1001, "Present", True, 10, 2.0, 6.0),
         SearchTiming(9999, "Missing", False, 10, 8.0, 8.0)),
        python_version="test-python", platform_name="test-platform",
    )


def test_manual_linear_search_matches_hash_for_every_record_and_missing_keys(records, structures):
    table, _ = structures
    for student in records:
        assert linear_search(records, student.student_id) is student
        assert table.search(student.student_id) is student
    for key in (9999, 0, -1):
        assert linear_search(records, key) is table.search(key) is None
    assert linear_search([], 1001) is None


@pytest.mark.parametrize("key", [True, False, "1001", 1001.0, None])
def test_linear_search_rejects_non_integer_keys(records, key):
    with pytest.raises(TypeError, match="student_id must be an integer"):
        linear_search(records, key)


def test_linear_search_handles_a_different_dataset_order(records):
    reversed_records = tuple(reversed(records))
    for key in (1001, 1075, 1150, 9999):
        assert linear_search(reversed_records, key) == linear_search(records, key)


def test_required_default_protocol_counts_every_search_and_excludes_output(records, structures, monkeypatch, capsys):
    table, queue = structures
    before = table.buckets, queue.heap, tuple(records)
    hash_counts, linear_counts = Counter(), Counter()
    original_hash = table.search
    original_linear = benchmark.linear_search
    phase = {"timed": False, "clock_calls": 0}

    def clock():
        phase["clock_calls"] += 1
        phase["timed"] = not phase["timed"]
        return float(phase["clock_calls"])

    def hash_spy(key):
        hash_counts[(key, phase["timed"])] += 1
        return original_hash(key)

    def linear_spy(students, key):
        assert students == records
        linear_counts[(key, phase["timed"])] += 1
        return original_linear(students, key)

    monkeypatch.setattr(table, "search", hash_spy)
    monkeypatch.setattr(benchmark, "linear_search", linear_spy)
    monkeypatch.setattr(benchmark, "time", SimpleNamespace(perf_counter=clock))
    result = run_benchmark(records, table)
    assert result.warmup == BENCHMARK_WARMUP == 100
    assert result.repetitions == BENCHMARK_REPETITIONS == 10_000
    assert [(row.student_id, row.scenario) for row in result.timings] == list(BENCHMARK_TARGETS)
    assert [row.found for row in result.timings] == [True] * 5 + [False]
    assert result.measured_searches_per_algorithm == 60_000
    for key, _ in BENCHMARK_TARGETS:
        assert hash_counts[(key, True)] == linear_counts[(key, True)] == 10_000
        # Every target has one agreement check and 100 untimed warm-ups.
        # Present IDs also have one full-table content check.
        assert linear_counts[(key, False)] == 101
        assert hash_counts[(key, False)] == (102 if key != 9999 else 101)
    assert phase["clock_calls"] == 24
    assert not phase["timed"]
    assert (table.buckets, queue.heap, tuple(records)) == before
    assert capsys.readouterr().out == ""


def test_alternating_measurement_order_and_known_timer_totals(records, monkeypatch):
    # Row 1: hash=2, linear=6. Row 2: linear=8, hash=4 seconds.
    ticks = iter((0, 2, 10, 16, 20, 28, 30, 34))
    monkeypatch.setattr(benchmark, "time", SimpleNamespace(perf_counter=lambda: next(ticks)))
    result = run_benchmark(
        records, targets=((1001, "Beginning"), (9999, "Missing")),
        warmup=0, repetitions=2,
    )
    assert [(row.hash_total_seconds, row.linear_total_seconds) for row in result.timings] == [(2, 6), (4, 8)]
    assert result.hash_total_seconds == 6
    assert result.linear_total_seconds == 14
    assert result.hash_average_seconds == 1.5
    assert result.linear_average_seconds == 3.5
    assert result.speed_ratio == pytest.approx(14 / 6)


@pytest.mark.parametrize("changed", ["missing", "updated", "extra"])
def test_mismatched_table_is_rejected_before_any_timing(records, structures, monkeypatch, changed):
    table, _ = structures
    if changed == "missing":
        table.delete(1001)
    elif changed == "updated":
        table.insert(1001, replace(records[0], name="Different value"))
    else:
        table.insert(9999, replace(records[0], student_id=9999))
    before = table.buckets

    def forbidden_timer():
        pytest.fail("A mismatched dataset must not be timed")

    monkeypatch.setattr(benchmark, "time", SimpleNamespace(perf_counter=forbidden_timer))
    with pytest.raises(ValueError, match="same records"):
        run_benchmark(records, table)
    assert table.buckets == before


def test_even_a_late_target_disagreement_prevents_all_timing(records, monkeypatch):
    original = benchmark.linear_search

    def incorrect_linear(students, key):
        return None if key == 1150 else original(students, key)

    monkeypatch.setattr(benchmark, "linear_search", incorrect_linear)
    monkeypatch.setattr(benchmark, "time", SimpleNamespace(
        perf_counter=lambda: pytest.fail("All targets must agree before timing starts")
    ))
    with pytest.raises(ValueError, match="disagree for student_id 1150"):
        run_benchmark(records)


@pytest.mark.parametrize("options", [
    {"warmup": -1}, {"warmup": True}, {"warmup": 1.5},
    {"repetitions": 0}, {"repetitions": -1}, {"repetitions": True},
    {"repetitions": 1.5}, {"targets": ()}, {"targets": ((1001, ""),)},
    {"targets": ((True, "Present"),)}, {"targets": (("1001", "Present"),)},
    {"targets": ((1001, "Present"), (1001, "Again"))},
    {"targets": ((1001,),)}, {"targets": ("1001",)},
])
def test_invalid_benchmark_options_are_rejected_before_timing(records, monkeypatch, options):
    monkeypatch.setattr(benchmark, "time", SimpleNamespace(
        perf_counter=lambda: pytest.fail("Invalid options must not be timed")
    ))
    with pytest.raises(ValueError):
        run_benchmark(records, **options)


@pytest.mark.parametrize("problem", ["empty", "duplicate", "invalid"])
def test_invalid_records_are_rejected_before_timing(records, monkeypatch, problem):
    invalid = [] if problem == "empty" else list(records)
    if problem == "duplicate":
        invalid.append(records[0])
    elif problem == "invalid":
        invalid[0] = replace(records[0], priority=101)
    monkeypatch.setattr(benchmark, "time", SimpleNamespace(
        perf_counter=lambda: pytest.fail("Invalid records must not be timed")
    ))
    with pytest.raises(ValueError):
        run_benchmark(invalid)


def test_run_builds_a_fresh_table_and_accepts_a_smaller_valid_dataset(records):
    result = run_benchmark(records[:3], targets=((1001, "Present"), (9999, "Missing")), warmup=0, repetitions=2)
    assert result.dataset_size == 3
    assert result.measured_searches_per_algorithm == 4
    assert [row.found for row in result.timings] == [True, False]
    assert all(row.hash_total_seconds >= 0 and row.linear_total_seconds >= 0 for row in result.timings)


def test_result_calculations_use_totals_and_search_counts():
    result = synthetic_result()
    first = result.timings[0]
    assert first.hash_average_seconds == pytest.approx(0.2)
    assert first.linear_average_seconds == pytest.approx(0.6)
    assert first.speed_ratio == 3.0
    assert result.measured_searches_per_algorithm == 20
    assert result.hash_total_seconds == 10
    assert result.linear_total_seconds == 14
    assert result.hash_average_seconds == 0.5
    assert result.linear_average_seconds == 0.7
    assert result.speed_ratio == 1.4  # Ratio of totals, not mean of 3x and 1x.
    with pytest.raises(FrozenInstanceError):
        result.repetitions = 1
    with pytest.raises(FrozenInstanceError):
        first.hash_total_seconds = 0


def test_zero_hash_time_is_reported_as_unavailable_ratio():
    timing = SearchTiming(9999, "Missing", False, 10, 0, 1)
    result = BenchmarkResult(150, 211, 0, 10, (timing,))
    assert timing.speed_ratio is result.speed_ratio is None
    assert timing.hash_average_seconds == 0
    assert "Overall linear/hash time ratio: N/A" in format_results(result)


@pytest.mark.parametrize("field,value", [
    ("repetitions", 0), ("repetitions", True),
    ("hash_total_seconds", -1), ("hash_total_seconds", float("nan")),
    ("linear_total_seconds", float("inf")), ("linear_total_seconds", True),
    ("scenario", ""), ("student_id", True), ("found", 1),
])
def test_invalid_target_result_values_are_rejected(field, value):
    with pytest.raises(ValueError):
        replace(synthetic_result().timings[0], **{field: value})


@pytest.mark.parametrize("change", [
    {"dataset_size": 0}, {"table_size": 0}, {"warmup": -1},
    {"repetitions": 0}, {"repetitions": 20}, {"timings": ()},
    {"timings": ("invalid",)},
])
def test_inconsistent_run_result_values_are_rejected(change):
    with pytest.raises(ValueError):
        replace(synthetic_result(), **change)


def test_duplicate_result_targets_are_rejected():
    result = synthetic_result()
    with pytest.raises(ValueError, match="unique"):
        replace(result, timings=(result.timings[0], result.timings[0]))


def test_format_and_file_output_include_protocol_units_and_calculated_values(tmp_path):
    result = synthetic_result()
    text = format_results(result)
    assert "Dataset records: 150" in text
    assert "Measured searches per algorithm: 20" in text
    assert "Overall hash total (s): 10.000000000" in text
    assert "Overall average hash search (us): 500000.000000" in text
    assert "Overall linear/hash time ratio: 1.400x" in text
    assert "test-python" in text and "test-platform" in text
    assert "Missing" in text and "no" in text
    assert "time.perf_counter()" in text and "excluded from timing" in text
    path = save_results(result, tmp_path / "nested" / "report.txt")
    assert path.read_text(encoding="utf-8") == text
    updated = replace(result, warmup=0)
    save_results(updated, path)
    assert path.read_text(encoding="utf-8") == format_results(updated)


def test_result_writer_cannot_overwrite_the_source_dataset():
    original = DATASET_PATH.read_bytes()
    with pytest.raises(ValueError, match="must not overwrite"):
        save_results(synthetic_result(), DATASET_PATH)
    assert DATASET_PATH.read_bytes() == original


def test_command_loads_csv_exactly_once_and_saves_after_success(records, monkeypatch, tmp_path, capsys):
    calls = []

    def load_once(path):
        calls.append(path)
        return records

    output = tmp_path / "results.txt"
    monkeypatch.setattr(benchmark, "load_dataset", load_once)
    monkeypatch.setattr(sys, "argv", ["benchmark", "--output", str(output), "--warmup", "0", "--repetitions", "2"])
    benchmark.main()
    assert len(calls) == 1
    assert output.exists()
    assert "Results saved to:" in capsys.readouterr().out


def test_benchmark_module_command_runs_on_real_dataset(tmp_path):
    output = tmp_path / "report.txt"
    result = subprocess.run(
        [sys.executable, "-m", "src.performance.benchmark", "--output", str(output),
         "--warmup", "0", "--repetitions", "2"],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    text = output.read_text(encoding="utf-8")
    assert "Dataset records: 150" in text
    assert "Measured searches per algorithm: 12" in text
    assert all(str(key) in text for key, _ in BENCHMARK_TARGETS)
    assert "Results saved to:" in result.stdout


@pytest.mark.parametrize("problem", ["missing", "malformed", "count", "same_output"])
def test_command_errors_leave_existing_output_untouched(tmp_path, monkeypatch, capsys, problem):
    dataset = tmp_path / "students.csv"
    output = tmp_path / "report.txt"
    output.write_text("existing report", encoding="utf-8")
    if problem in ("malformed", "same_output"):
        dataset.write_text("not a CSV dataset", encoding="utf-8")
    arguments = ["benchmark", "--dataset", str(dataset), "--output", str(output)]
    if problem == "count":
        arguments = ["benchmark", "--dataset", str(DATASET_PATH), "--output", str(output), "--repetitions", "0"]
    elif problem == "same_output":
        arguments = ["benchmark", "--dataset", str(dataset), "--output", str(dataset)]
    monkeypatch.setattr(sys, "argv", arguments)
    with pytest.raises(SystemExit) as error:
        benchmark.main()
    assert error.value.code == 1
    assert "Benchmark error:" in capsys.readouterr().err
    assert output.read_text(encoding="utf-8") == "existing report"
    if problem == "same_output":
        assert dataset.read_text(encoding="utf-8") == "not a CSV dataset"
