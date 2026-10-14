# Source Code

This package separates configuration, student records, dataset handling, algorithms, benchmarking, and user interaction. Day 1 implements `config`, `models`, and `dataset`; Day 2 adds the custom hash table. Other packages provide the foundation for later days.

```text
src/
|-- README.md          # Guide to the source packages
|-- __init__.py        # Makes src a Python package
|-- config/            # Shared constants and project paths; implemented
|-- models/            # Immutable student record; implemented
|-- dataset/           # CSV generation, loading, and validation; implemented
|-- data_structures/   # Hash table implemented; max-heap planned for Day 3
|-- performance/       # Linear search and benchmarking; planned for Day 4
|-- cli/               # Interactive menus and input handling; planned for Day 5
`-- utils/             # Shared display utilities; planned for Day 5
```

Start with [configuration](config/README.md), [the data model](models/README.md), [dataset handling](dataset/README.md), and [data structures](data_structures/README.md). [Performance](performance/README.md), [CLI](cli/README.md), and [utilities](utils/README.md) describe later work.

[Project overview](../README.md)
