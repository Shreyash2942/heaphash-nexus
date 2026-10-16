# Configuration

This package provides one place for shared settings. Paths are resolved from the project location, so loading the default dataset works even when the working directory changes.

```text
config/
|-- README.md       # Configuration guide
|-- __init__.py     # Makes config a Python package
`-- settings.py     # Dataset and benchmark constants, CSV fields, and absolute paths
```

The dataset uses 150 records, IDs starting at 1001, priorities from 1 through 100, and random seed 42. The hash table defaults to 211 buckets; its constructor also accepts another positive integer size for collision demonstrations. `DATASET_PATH` points to `data/students.csv`; results and documentation have their own directory constants.

Benchmark defaults are `BENCHMARK_WARMUP = 100` and `BENCHMARK_REPETITIONS = 10_000`. `BENCHMARK_TARGETS` pairs IDs 1001, 1025, 1075, 1125, 1150, and 9999 with their scenario names. `PERFORMANCE_RESULTS_PATH` points to `results/performance_results.txt`.

[Source packages](../README.md)
