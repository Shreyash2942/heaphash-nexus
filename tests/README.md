# Tests

Tests remain outside the source package. Days 1-3 supply dataset, hash-table, and priority-queue unit tests. Day 4 adds full-dataset integration and performance correctness tests. Day 5 adds input validation and CLI integration tests.

```text
tests/
|-- README.md      # Test organization and execution
|-- __init__.py    # Makes tests a Python package
|-- unit/          # Dataset, hash-table, priority-queue, and input-validation tests
`-- integration/   # Shared state, benchmarking, reports, menus, reset, and demonstration
```

Run from the project root:

```powershell
python -m pytest -v
```

The root `pytest.ini` sets the test directory and source import path. Tests should verify returned values, state, and errors; benchmark timings themselves are not correctness assertions.

Integration fixtures load the real 150-record CSV once and build fresh containers for each test. Performance tests verify matching searches, exact warm-up and measured counts, pre-timing mismatch rejection, calculations, report output, and command errors. Synthetic clocks test arithmetic; they are not published benchmark measurements.

CLI tests clone the real records into temporary CSV files and reports. They exercise menus, duplicate handling, source preservation, reset failures, isolated demonstrations, non-interactive `--demo`, startup errors, and graceful EOF/Ctrl+C exit. Test runs do not replace the project's saved benchmark report.

See [unit tests](unit/README.md) and [integration tests](integration/README.md).

[Project overview](../README.md)
