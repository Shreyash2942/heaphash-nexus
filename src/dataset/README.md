# Dataset Handling

This package implements the Day 1 data workflow: generate reproducible student records, write CSV, load it into `DataItem` objects, and validate the contents.

```text
dataset/
|-- README.md          # Dataset workflow and usage
|-- __init__.py        # Makes dataset a Python package
|-- data_generator.py  # Seeded generation, CSV writing, and generation command
|-- data_loader.py     # CSV parsing and loading or generating the default dataset
`-- validator.py       # Field, unique-ID, and optional record-count validation
```

Run from the project root:

```powershell
python -m src.dataset.data_generator
```

The command creates `data/students.csv` when missing and validates an existing file without replacing it. Add `--overwrite` only when intentionally regenerating the dataset; `--output PATH` selects a different CSV destination.

`generate_students()` returns the seeded records. `write_dataset()` validates before writing and protects existing files by default. `load_dataset()` requires 150 records by default; `expected_size=None` allows smaller demonstrations. `load_or_generate_dataset()` creates a missing default-sized dataset and reports invalid existing data without replacing it.

Validation rejects non-positive or duplicate IDs, empty names or programs, and priorities outside 1-100. CSV errors include file and line context where available.

See [stored data](../../data/README.md) and [dataset tests](../../tests/unit/README.md).

[Source packages](../README.md)
