# Configuration

This package provides one place for shared settings. Paths are resolved from the project location, so loading the default dataset works even when the working directory changes.

```text
config/
|-- README.md       # Configuration guide
|-- __init__.py     # Makes config a Python package
`-- settings.py     # Dataset constants, CSV fields, and absolute project paths
```

The dataset uses 150 records, IDs starting at 1001, priorities from 1 through 100, and random seed 42. The planned hash table uses 211 buckets. `DATASET_PATH` points to `data/students.csv`; results and documentation have their own directory constants.

[Source packages](../README.md)
