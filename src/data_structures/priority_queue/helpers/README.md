# Heap Helpers

This package implements internal heap maintenance and validation for Day 3. Helpers work with a list of already validated student records and compare their priorities.

```text
helpers/
|-- README.md        # Index relationships and repair preconditions
|-- __init__.py      # Makes helpers a Python package
|-- heapify_up.py    # Moves an inserted or replaced record toward its parent
|-- heapify_down.py  # Moves a replacement toward its larger child
`-- validate_heap.py # Checks every parent/child priority relationship
```

For index `i`, the parent is `(i - 1) // 2`, the left child is `2 * i + 1`, and the right child is `2 * i + 2`.

`heapify_up(heap, index)` repairs an inserted or upward-replaced record in O(log n). The rest of the heap must already be valid. `heapify_down(heap, index)` repairs after root extraction or downward replacement in O(log n), choosing the greater-priority child. Its child subtrees must already be valid. These helpers expect a valid index supplied by the queue; heapify-down also handles an empty heap at index 0.

`validate_heap(heap)` scans all children in O(n) and returns a boolean for `parent.priority >= child.priority`. Empty heaps, single records, and ties are valid. It does not mutate the heap or replace student field and unique-ID validation at insertion.

[Priority queue](../README.md)
