# Priority Queue Operations

This package implements the priority queue's operation logic. The owning `PriorityQueue` validates public inputs and passes its private heap list to these internal functions.

```text
operations/
|-- README.md       # Internal operation responsibilities
|-- __init__.py     # Makes operations a Python package
|-- insert.py       # Rejects duplicate IDs, appends a student, and repairs upward
|-- search.py       # Scans the heap by student ID
|-- delete.py       # Removes by ID and chooses upward or downward repair
|-- peek.py         # Reads the root without mutation
`-- extract_max.py  # Removes the root and repairs downward when needed
```

Peek and extract-max return a `DataItem` or `None` on an empty heap. Search returns the matching record or `None`. Delete returns whether it removed a record. Insertion returns `None` and rejects a duplicate ID with `ValueError` before mutation. Counts come from the owner's list length rather than separate mutable bookkeeping.

Search and duplicate checking scan IDs because the heap is ordered by priority, not by ID. Arbitrary deletion moves the last record into the removed position. A replacement that exceeds its parent moves upward; otherwise it moves downward. Removing the last record or the only record avoids unnecessary repair.

Insertion and removal call [heap helpers](../helpers/README.md) to restore max-heap order. Application code should use the public queue methods rather than calling these internal functions or mutating heap storage directly.

[Priority queue](../README.md)
