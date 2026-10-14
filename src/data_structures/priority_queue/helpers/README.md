# Heap Helpers

This package will contain internal heap maintenance and validation during Day 3. It currently contains only the package initializer.

```text
helpers/
|-- README.md     # Planned heap algorithms
`-- __init__.py   # Makes helpers a Python package
```

Planned modules are `heapify_up.py`, `heapify_down.py`, and `validate_heap.py`. For index `i`, the parent is `(i - 1) // 2`, the left child is `2 * i + 1`, and the right child is `2 * i + 2`.

Heapify-up will repair order after insertion or upward replacement. Heapify-down will repair order after root extraction or downward replacement. Validation will check `parent.priority >= child.priority`, including equal priorities.

[Priority queue](../README.md)
