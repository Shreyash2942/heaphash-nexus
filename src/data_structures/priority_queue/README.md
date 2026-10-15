# Priority Queue

This package implements the Day 3 student priority queue using a Python list as a binary max-heap. The greatest priority stays at index 0, and every parent priority is at least its child priorities. Heap algorithms are implemented manually without `heapq`.

```text
priority_queue/
|-- README.md          # Queue API, behavior, complexity, and examples
|-- __init__.py        # Exports PriorityQueue from the package
|-- priority_queue.py  # Owns the heap, public interface, and input validation
|-- operations/        # Insertion, search, deletion, peek, and extract-max
`-- helpers/           # Upward/downward heap repair and validity checks
```

`PriorityQueue()` starts empty and accepts immutable `DataItem` student records. Equal priorities are valid; their extraction order is not guaranteed. IDs remain unique: insertion rejects a duplicate with `ValueError` before changing the heap. Existing records are not silently replaced.

| Public member | Behavior |
|---|---|
| `insert(student)` | Validates and queues a student; returns `None` |
| `search(student_id)` | Returns the original record, or `None` if missing |
| `delete(student_id)` | Removes that student; returns `True`, or `False` if missing |
| `peek()` | Returns a highest-priority record without removing it, or `None` when empty |
| `extract_max()` | Removes and returns a highest-priority record, or `None` when empty |
| `validate_heap()` | Returns whether all parent/child priorities satisfy max-heap order |
| `item_count`, `len(queue)` | Number of queued records, derived from the heap list |
| `heap` | Immutable tuple snapshot in heap array order, rather than sorted order |

Insertion reuses [student validation](../../dataset/README.md): positive integer IDs, non-empty names and programs, and integer priorities from 1 to 100. Invalid records and duplicate IDs raise `ValueError`. Search and deletion require a positive integer student ID; booleans and other non-integer types raise `TypeError`, while non-positive integers raise `ValueError`. Rejected operations preserve queue state.

For array index `i`, the parent is `(i - 1) // 2`, the left child is `2 * i + 1`, and the right child is `2 * i + 2`. Insertion repairs upward. Extract-max replaces the root with the last record and repairs downward. Arbitrary deletion replaces the removed record with the last one, then repairs upward if that replacement exceeds its new parent, or downward otherwise. Deleting the last record needs no repair.

| Operation | Time |
|---|---|
| Peek and count | O(1) |
| Extract-max | O(log n) |
| Heapify-up or heapify-down | O(log n) |
| Insert | O(n): unique-ID scan plus O(log n) heap repair |
| Search or delete by student ID | O(n): ID scan; deletion then repairs in O(log n) |
| Validate heap or create a snapshot | O(n) |

From the project root, insert and inspect all 150 students:

```python
from src.data_structures.priority_queue import PriorityQueue
from src.dataset.data_loader import load_dataset

queue = PriorityQueue()
for student in load_dataset():
    queue.insert(student)
assert len(queue) == 150
assert queue.validate_heap()
highest = queue.peek()
assert queue.extract_max() is highest
assert len(queue) == 149
assert queue.validate_heap()
```

Repeated extraction yields priorities in non-increasing order, including ties. Queue operations change only the queue's own list; they do not write the CSV or modify the independent hash table. The tuple snapshot shares immutable student values, so it cannot change queued IDs or priorities.

Run `python -m pytest tests/unit/test_priority_queue.py -v` from the project root for operation tests, both arbitrary-deletion repair directions, ties, invalid inputs, full-dataset checks, and descending extraction.

See [operations](operations/README.md) and [helpers](helpers/README.md).

[Data structures](../README.md)
