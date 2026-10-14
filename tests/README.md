# Tests

Tests remain outside the source package. Day 1 supplies dataset unit tests and Day 2 adds hash-table unit tests. Later days will add priority-queue, performance, input-handling, and integration tests.

```text
tests/
|-- README.md      # Test organization and execution
|-- __init__.py    # Makes tests a Python package
|-- unit/          # Dataset and hash-table tests implemented
`-- integration/   # Tests combining project features; planned for Day 4
```

Run from the project root:

```powershell
python -m pytest -v
```

The root `pytest.ini` sets the test directory and source import path. Tests should verify returned values, state, and errors; benchmark timings themselves are not correctness assertions.

See [unit tests](unit/README.md) and [integration tests](integration/README.md).

[Project overview](../README.md)
