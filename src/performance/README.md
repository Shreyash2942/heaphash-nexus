# Performance Comparison

This package will implement the Day 4 comparison of custom hash-table search with manual linear search. Only the package initializer exists after Day 1.

```text
performance/
|-- README.md     # Planned benchmarking workflow
`-- __init__.py   # Makes performance a Python package
```

Planned modules are `linear_search.py`, `benchmark.py`, and `result.py`. Both search methods will use the same 150 student records and the targets 1001, 1025, 1075, 1125, 1150, and missing ID 9999.

Measurements will use `time.perf_counter()`, 100 warm-up searches, and 10,000 measured repetitions per target. Correctness must be verified before timing results are accepted, and printing must stay outside timed regions. Actual measurements will be saved in [results](../../results/README.md).

[Source packages](../README.md)
