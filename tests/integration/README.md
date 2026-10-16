# Integration Tests

This package implements Day 4 checks combining the real dataset, both custom data structures, and performance benchmarking.

```text
integration/
|-- README.md                # Integration coverage and execution
|-- __init__.py              # Makes integration a Python package
|-- conftest.py              # Loads the CSV once and creates fresh table/queue fixtures
|-- test_data_structures.py  # Shared records, representative operations, and independent state
`-- test_performance.py      # Search agreement, timing protocol, calculations, reports, and errors
```

The session-scoped `records` fixture loads all 150 students once as a tuple of immutable `DataItem` objects. Function-scoped `structures` fixtures populate a fresh hash table and queue from those same objects. A final fixture check confirms the source CSV stayed unchanged.

Structure tests search 1001, 1075, 1150, and missing ID 9999; remove representative students; verify counts and heap validity; and confirm changes in one structure preserve the other. Hash duplicate updates and queue extraction are also checked for independence.

Performance tests compare hash and manual linear searches, verify the default six targets and 60,000 measured searches per method, reject mismatches before timing starts, and check immutable result calculations. Synthetic clocks make arithmetic and protocol checks deterministic. File and command tests cover report saving, errors, and preservation of existing output and source data. No speed threshold is asserted.

Run from the project root:

```powershell
python -m pytest tests/integration -v
```

After the complete suite passes, run the real [benchmark](../../src/performance/README.md) to produce [saved measurements](../../results/README.md).

[Test organization](../README.md)
