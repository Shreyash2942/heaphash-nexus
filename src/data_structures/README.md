# Data Structures

These packages will implement the two algorithms manually. Day 1 creates their package structure; the hash table and priority queue algorithms are not implemented yet.

```text
data_structures/
|-- README.md        # Algorithm package guide
|-- __init__.py      # Makes data_structures a Python package
|-- hash_table/      # Separate-chaining hash table; planned for Day 2
`-- priority_queue/  # Binary max-heap priority queue; planned for Day 3
```

Both structures will accept the shared student records and manage independent internal state. Public structure methods will delegate to operation modules, while internal algorithm helpers will remain in helper packages.

See [the hash table](hash_table/README.md) and [the priority queue](priority_queue/README.md).

[Source packages](../README.md)
