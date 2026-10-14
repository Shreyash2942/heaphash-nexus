# Data Structures

These packages separate the two manually implemented data structures. The hash table is implemented for Day 2; the priority queue remains scheduled for Day 3.

```text
data_structures/
|-- README.md        # Algorithm package guide
|-- __init__.py      # Makes data_structures a Python package
|-- hash_table/      # Separate-chaining hash table; implemented in Day 2
`-- priority_queue/  # Binary max-heap priority queue; planned for Day 3
```

The hash table owns its bucket lists and item count. Public methods delegate chain operations to operation modules and use the modulo helper to select a bucket. The priority queue will own independent state when implemented. Both structures are designed to accept the shared student records.

See [the hash table](hash_table/README.md) and [the priority queue](priority_queue/README.md).

[Source packages](../README.md)
