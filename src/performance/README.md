# Performance Comparison

This package implements the Day 4 comparison of custom hash-table search with manual linear search. Both methods use the same validated student records and target IDs; the runner verifies matching results before any measurement begins.

```text
performance/
|-- README.md        # Benchmark protocol, API, commands, and interpretation
|-- __init__.py      # Makes performance a Python package
|-- linear_search.py # Manual sequential student-ID search
|-- benchmark.py     # Input checks, warm-up, timing, and standalone benchmark command
`-- result.py        # Immutable timing records, calculations, text formatting, and saving
```

Run from the project root, accepting results only after the correctness suite passes:

```powershell
python -m pytest -v
python -m src.performance.benchmark
```

The benchmark command loads `data/students.csv` once, validates its 150 records, builds a fresh hash table, runs the comparison, and saves [performance_results.txt](../../results/performance_results.txt). The interactive menu remains planned for Day 5.

| Target ID | Scenario |
|---:|---|
| 1001 | Beginning |
| 1025 | Early |
| 1075 | Middle |
| 1125 | Late |
| 1150 | End |
| 9999 | Missing |

Each method performs 100 warm-up searches per target, then 10,000 measured searches per target: 60,000 measured searches per algorithm. Timing uses `time.perf_counter()`. The first measured algorithm alternates between targets. Dataset loading, table construction, correctness checks, warm-up, printing, formatting, and file writes stay outside measured regions. Both methods include their normal public-function validation and loop/call overhead.

The runner is read-only with respect to its dataset and any supplied hash table. It checks the complete table against the dataset and compares both methods for every target before timing the first target. A missing ID must return `None` from both searches. A mismatch raises `ValueError`; existing output is preserved when the command fails before saving.

| API | Purpose |
|---|---|
| `linear_search(records, student_id)` | Manually scans records; returns a `DataItem` or `None` |
| `run_benchmark(records, hash_table=None, ...)` | Returns a `BenchmarkResult`; does not print or save |
| `SearchTiming` | Immutable target ID, scenario, found flag, repetition count, and measured totals |
| `BenchmarkResult` | Immutable run configuration, timing rows, environment, and calculated totals |
| `format_results(result)` | Produces the text report without writing a file |
| `save_results(result, path=...)` | Saves or replaces the latest report and creates parent directories |

`run_benchmark` accepts optional `targets`, `warmup`, and `repetitions`. Its programmatic API supports smaller valid datasets for tests and demonstrations. The command validates a complete 150-record CSV and supports `--dataset PATH`, `--output PATH`, `--warmup N`, and `--repetitions N`. Report output cannot overwrite the source CSV. Standard assignment measurements use the defaults above.

Per-target averages divide each measured total by its repetitions. Overall averages divide summed measured totals by all measured searches per algorithm. The speed ratio is total linear time divided by total hash time, rather than an average of per-target ratios. A ratio above 1 means lower hash-search time; below 1 means lower linear-search time. A zero hash timer total produces `N/A` for the ratio. Report averages use microseconds (`us`); totals use seconds.

Measurements describe one run on the recorded Python version and platform. Search position, dataset size, collisions, and machine activity affect results; correctness tests do not require any method to win.

See [integration and performance tests](../../tests/integration/README.md) and [saved results](../../results/README.md).

[Source packages](../README.md)
