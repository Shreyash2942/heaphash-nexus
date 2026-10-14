# Data Model

`DataItem` represents a student shared by dataset handling, the hash table, and the planned priority queue. Its fields are `student_id`, `name`, `program`, and `priority`.

```text
models/
|-- README.md       # Student model guide
|-- __init__.py     # Makes models a Python package
`-- data_item.py    # Immutable DataItem dataclass
```

Records are immutable so a stored key or heap priority cannot change accidentally. Field validity and duplicate IDs are checked by [dataset validation](../dataset/README.md), rather than by the model constructor.

[Source packages](../README.md)
