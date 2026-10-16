# Source Code

This package separates configuration, student records, dataset handling, algorithms, benchmarking, and user interaction. Day 1 implements `config`, `models`, and `dataset`; Day 2 adds the custom hash table; Day 3 adds the priority queue and binary max-heap; Day 4 adds the verified hash-versus-linear benchmark. CLI packages provide the foundation for Day 5.

```text
src/
|-- README.md          # Guide to the source packages
|-- __init__.py        # Makes src a Python package
|-- config/            # Shared constants and project paths; implemented
|-- models/            # Immutable student record; implemented
|-- dataset/           # CSV generation, loading, and validation; implemented
|-- data_structures/   # Hash table and binary max-heap priority queue; implemented
|-- performance/       # Manual linear search, verified benchmarking, and reports; implemented
|-- cli/               # Interactive menus and input handling; planned for Day 5
`-- utils/             # Shared display utilities; planned for Day 5
```

Start with [configuration](config/README.md), [the data model](models/README.md), [dataset handling](dataset/README.md), [data structures](data_structures/README.md), and [performance](performance/README.md). [CLI](cli/README.md) and [utilities](utils/README.md) describe later work.

[Project overview](../README.md)
