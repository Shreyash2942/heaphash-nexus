# Unit Tests

These tests check one project feature at a time. The dataset suite is implemented for Day 1.

```text
unit/
|-- README.md        # Unit test coverage and execution
|-- __init__.py      # Makes unit a Python package
`-- test_dataset.py  # Generation, validation, CSV handling, and file preservation
```

Run only the dataset tests from the project root:

```powershell
python -m pytest tests/unit/test_dataset.py -v
```

Coverage includes the real 150-record dataset, sequential IDs, controlled names and programs, seed reproducibility, integer and text validation, duplicate IDs, malformed CSV, quoting and Unicode, missing files, and intentional overwrite behavior. Temporary files keep test scenarios separate from the source CSV.

Later days will add `test_hash_table.py`, `test_priority_queue.py`, and `test_input_handler.py`.

[Test organization](../README.md)
