# Shared Utilities

This package implements shared student presentation helpers used by the Day 5 CLI.

```text
utils/
|-- README.md     # Shared presentation utilities
|-- __init__.py   # Makes utils a Python package
`-- display.py    # Student field formatting and collection display
```

`format_student()` renders all four student fields or a missing-record message. `display_students()` renders a collection or an empty-collection message. Structure-specific bucket/heap display remains in its menu module and reads public snapshots. Dataset validation and data-structure algorithms remain in their own packages.

[Source packages](../README.md)
