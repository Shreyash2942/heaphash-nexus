# Integration Tests

This package will check interactions between dataset loading, both custom data structures, and benchmarking during Day 4. Only the package initializer exists after Day 1.

```text
integration/
|-- README.md     # Planned integration coverage
`-- __init__.py   # Makes integration a Python package
```

Planned files are `test_data_structures.py` and `test_performance.py`. They will load all 150 students into both structures, check representative IDs, verify that deleting from one structure leaves the other independent, and compare hash-search results with linear-search results.

No integration test cases exist yet. Once added, run them from the project root with `python -m pytest tests/integration -v`.

[Test organization](../README.md)
