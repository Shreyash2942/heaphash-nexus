# Data Structures

These packages separate the two manually implemented data structures. The hash table is implemented for Day 2 and the binary max-heap priority queue for Day 3.

```text
data_structures/
|-- README.md        # Algorithm package guide
|-- __init__.py      # Makes data_structures a Python package
|-- hash_table/      # Separate-chaining hash table; implemented in Day 2
`-- priority_queue/  # Binary max-heap priority queue; implemented in Day 3
```

The hash table owns its bucket lists and item count. The priority queue owns a separate heap list and derives its count from that list. Public methods delegate to operation modules, and internal helpers handle modulo hashing or heap maintenance. Both structures accept the shared immutable student records; changing one structure's contents does not change the other.

See [the hash table](hash_table/README.md) and [the priority queue](priority_queue/README.md).

[Source packages](../README.md)
