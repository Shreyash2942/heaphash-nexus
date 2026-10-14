# Command-Line Interface

This package will implement interactive project navigation during Day 5. Only the package initializer exists after Day 1; the application menus are not available yet.

```text
cli/
|-- README.md     # Planned menus and interaction rules
`-- __init__.py   # Makes cli a Python package
```

Planned modules are `menu.py`, `hash_table_menu.py`, `priority_queue_menu.py`, `performance_menu.py`, `dataset_menu.py`, and `input_handler.py`. They will provide data-structure operations, dataset inspection, benchmarking, a complete demonstration, reset, and exit.

Menus will call public interfaces rather than implement hashing or heap algorithms. Input handling will reject invalid choices and record fields. Interactive changes will leave the original CSV unchanged; reset will rebuild both structures from that dataset.

The root `main.py` entry point will be added when the CLI is implemented.

[Source packages](../README.md)
