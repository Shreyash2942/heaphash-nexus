# Hash Table Operations

This package will contain insertion, search, and deletion logic during Day 2. It currently contains only the package initializer.

```text
operations/
|-- README.md     # Planned hash-table operations
`-- __init__.py   # Makes operations a Python package
```

Planned modules are `insert.py`, `search.py`, and `delete.py`. Insertion will update an existing key instead of adding a duplicate. Search will return `None` for a missing key. Deletion must preserve other records in the same collision chain.

Callers will use the future `HashTable` interface rather than changing buckets directly.

[Hash table](../README.md)
