# Priority Queue

This package is the Day 3 location for a custom priority queue backed by a Python-list binary max-heap. Only the package structure exists after Day 1.

```text
priority_queue/
|-- README.md     # Planned priority-queue design
|-- __init__.py   # Makes priority_queue a Python package
|-- operations/   # Planned insertion, search, deletion, peek, and extraction
`-- helpers/      # Planned heap maintenance and validity checks
```

The planned `priority_queue.py` will own the heap and expose its public interface. The highest-priority record will stay at index 0; every parent priority must be at least its child priorities. Equal priorities will be allowed. The core implementation will not use `heapq`.

See [operations](operations/README.md) and [helpers](helpers/README.md).

[Data structures](../README.md)
