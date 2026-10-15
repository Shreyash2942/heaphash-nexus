# Tests

Tests remain outside the source package. Days 1-3 supply dataset, hash-table, and priority-queue unit tests. Later days will add performance, input-handling, and integration tests.

```text
tests/
|-- README.md      # Test organization and execution
|-- __init__.py    # Makes tests a Python package
|-- unit/          # Dataset, hash-table, and priority-queue tests implemented
`-- integration/   # Tests combining project features; planned for Day 4
```

Run from the project root:

```powershell
python -m pytest -v
```

The root `pytest.ini` sets the test directory and source import path. Tests should verify returned values, state, and errors; benchmark timings themselves are not correctness assertions.

See [unit tests](unit/README.md) and [integration tests](integration/README.md).

[Project overview](../README.md)
