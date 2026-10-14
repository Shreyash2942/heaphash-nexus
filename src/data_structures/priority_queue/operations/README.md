# Priority Queue Operations

This package will contain the priority queue's public operation logic during Day 3. It currently contains only the package initializer.

```text
operations/
|-- README.md     # Planned priority-queue operations
`-- __init__.py   # Makes operations a Python package
```

Planned modules are `insert.py`, `search.py`, `delete.py`, `peek.py`, and `extract_max.py`. Peek will return the highest-priority record without removing it; extract-max will return and remove it. Search and arbitrary deletion will identify students by ID.

Insertion and removal will use [heap helpers](../helpers/README.md) to restore heap order. Removing a record must not affect the independent hash table.

[Priority queue](../README.md)
