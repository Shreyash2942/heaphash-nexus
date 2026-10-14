# Unit Tests

These tests check one project feature at a time. Dataset tests are implemented for Day 1 and hash-table tests for Day 2.

```text
unit/
|-- README.md           # Unit test coverage and execution
|-- __init__.py         # Makes unit a Python package
|-- test_dataset.py     # Generation, validation, CSV handling, and file preservation
`-- test_hash_table.py  # Operations, collisions, statistics, and all 150 records
```

Run only the dataset tests from the project root:

```powershell
python -m pytest tests/unit/test_dataset.py -v
```

Coverage includes the real 150-record dataset, sequential IDs, controlled names and programs, seed reproducibility, integer and text validation, duplicate IDs, malformed CSV, quoting and Unicode, missing files, and intentional overwrite behavior. Temporary files keep test scenarios separate from the source CSV.

Run the Day 2 checks with `python -m pytest tests/unit/test_hash_table.py -v`. They cover empty tables, insertion, duplicate-key replacement, missing keys, invalid inputs, chain deletion, counts, occupancy, immutable bucket snapshots, and all 150 students. They also exercise deliberate collisions at size 10, a size-1 table, and a reproducible mixed-operation workload against a reference mapping.

Later days will add `test_priority_queue.py` and `test_input_handler.py`.

[Test organization](../README.md)
