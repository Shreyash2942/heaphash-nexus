# Source Code

This package separates configuration, student records, dataset handling, algorithms, benchmarking, and user interaction. Days 1-4 implement the dataset, both custom structures, and the verified hash-versus-linear benchmark. Day 5 adds the interactive application, complete demonstration, and reset workflow. Academic documentation and final submission checks remain scheduled for Day 6.

```text
src/
|-- README.md          # Guide to the source packages
|-- __init__.py        # Makes src a Python package
|-- config/            # Shared constants and project paths; implemented
|-- models/            # Immutable student record; implemented
|-- dataset/           # CSV generation, loading, and validation; implemented
|-- data_structures/   # Hash table and binary max-heap priority queue; implemented
|-- performance/       # Manual linear search, verified benchmarking, and reports; implemented
|-- cli/               # Menus, input validation, independent state, demo, and reset
`-- utils/             # Shared student display helpers
```

Start with [configuration](config/README.md), [the data model](models/README.md), [dataset handling](dataset/README.md), [data structures](data_structures/README.md), [performance](performance/README.md), [CLI](cli/README.md), and [utilities](utils/README.md).

From the project root, run `python main.py` for interactive menus or `python main.py --demo` for a complete demonstration without prompts. The root entry point delegates to the CLI and contains no data-structure algorithms.

[Project overview](../README.md)
