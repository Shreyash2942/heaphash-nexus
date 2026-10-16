# Tests

Tests remain outside the source package. Days 1-3 supply dataset, hash-table, and priority-queue unit tests. Day 4 adds full-dataset integration and performance correctness tests. Input-handling tests remain planned for Day 5.

```text
tests/
|-- README.md      # Test organization and execution
|-- __init__.py    # Makes tests a Python package
|-- unit/          # Dataset, hash-table, and priority-queue tests implemented
`-- integration/   # Shared-dataset behavior, independence, benchmarking, and reports
```

Run from the project root:

```powershell
python -m pytest -v
```

The root `pytest.ini` sets the test directory and source import path. Tests should verify returned values, state, and errors; benchmark timings themselves are not correctness assertions.

Integration fixtures load the real 150-record CSV once and build fresh containers for each test. Performance tests verify matching searches, exact warm-up and measured counts, pre-timing mismatch rejection, calculations, report output, and command errors. Synthetic clocks test arithmetic; they are not published benchmark measurements.

See [unit tests](unit/README.md) and [integration tests](integration/README.md).

[Project overview](../README.md)
