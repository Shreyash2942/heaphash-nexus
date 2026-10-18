# Performance Results

This folder stores actual measurements from the Day 4 hash-table versus linear-search benchmark. The report was generated after the correctness suite passed.

```text
results/
|-- README.md                # Benchmark output, reproduction, and interpretation
|-- .gitkeep                 # Original marker for the results directory
`-- performance_results.txt  # Measured per-target and overall search results
```

`performance_results.txt` records dataset and bucket counts, targets, warm-up and repetition counts, timer, measurement order, Python version, and platform. Each target has hash and linear totals in seconds, per-search averages in microseconds, and a linear/hash time ratio. Overall averages use all 60,000 measured searches per algorithm.

Reproduce from the project root:

```powershell
python -m pytest -v
python -m src.performance.benchmark
```

The command replaces the latest report with fresh measurements. It uses 150 records, a 211-bucket hash table, six targets, 100 warm-up searches per target per method, and 10,000 measured repetitions per target per method. Loading, construction, validation, warm-up, printing, and saving are excluded from timing.

Reports can also be generated through the CLI Performance menu or Run Complete Demonstration. `python main.py --demo` runs the full demonstration without prompts and saves the latest report. `--results PATH` selects another report file for the application. The checked-in report was refreshed during the Day 5 terminal demonstration after the correctness suite passed.

The ratio is total linear time divided by total hash time. Above 1 means lower hash time; below 1 means lower linear time. A beginning-of-list target can favor linear search, while later or missing targets scan more records. Interpret these measurements for their recorded run and environment; the tests do not assume a speed winner.

See [benchmark implementation](../src/performance/README.md) and [performance correctness tests](../tests/integration/README.md).

[Project overview](../README.md)
