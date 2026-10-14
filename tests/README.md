# Tests

Tests remain outside the source package. Day 1 supplies dataset unit tests; later days will add data-structure, performance, input-handling, and integration tests.

```text
tests/
|-- README.md      # Test organization and execution
|-- __init__.py    # Makes tests a Python package
|-- unit/          # Tests for individual modules; dataset tests implemented
`-- integration/   # Tests combining project features; planned for Day 4
```

Run from the project root:

```powershell
python -m pytest -v
```

The root `pytest.ini` sets the test directory and source import path. Tests should verify returned values, state, and errors; benchmark timings themselves are not correctness assertions.

See [unit tests](unit/README.md) and [integration tests](integration/README.md).

[Project overview](../README.md)
