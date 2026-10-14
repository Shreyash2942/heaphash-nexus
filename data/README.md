# Student Dataset

This folder stores the shared Day 1 CSV used by the Day 2 hash table and the planned priority queue and search comparison.

```text
data/
|-- README.md      # Dataset contents and regeneration guide
|-- .gitkeep       # Original marker for the data directory
`-- students.csv   # 150 generated student records with a header row
```

Columns are `student_id`, `name`, `program`, and `priority`. IDs run from 1001 through 1150. Names and programs come from controlled lists, priorities range from 1 through 100, and seed 42 makes generation reproducible. Names and priorities may repeat; IDs must be unique.

From the project root, `python -m src.dataset.data_generator` creates a missing CSV or validates an existing one without replacing it. Add `--overwrite` to intentionally regenerate it. Normal application interactions must not modify this source dataset.

See [dataset implementation](../src/dataset/README.md) and [unit tests](../tests/unit/README.md).

[Project overview](../README.md)
