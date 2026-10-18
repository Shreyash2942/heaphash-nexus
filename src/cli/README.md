# Command-Line Interface

This package implements the Day 5 interactive application. Menus collect input, call the completed data-structure and benchmark interfaces, and display results. Hashing and heap maintenance stay in their existing algorithm packages.

```text
cli/
|-- README.md               # Commands, menu choices, and state rules
|-- __init__.py             # Makes cli a Python package
|-- application.py          # Original loaded records and independent editable structures
|-- input_handler.py        # Choice, integer, text, and student-record prompts
|-- navigation.py           # Shared menu loop and recoverable action-error handling
|-- menu.py                 # Main navigation, arguments, reset action, and graceful exit
|-- hash_table_menu.py      # Hash operations, bucket display, statistics, and collision demo
|-- priority_queue_menu.py  # Queue operations, heap display, and heap validation
|-- performance_menu.py     # Verified benchmarks and viewing the latest saved report
|-- dataset_menu.py         # Source information, first-10 preview, and CSV validation
`-- demonstration.py        # Complete demonstration using separate temporary containers
```

Run from the project root:

```powershell
python main.py
```

The root entry point delegates to `menu.main()`. Startup loads the 150-record CSV, or generates the reproducible default dataset if the selected CSV is missing. Invalid existing data produces a clear error and exit status 1. The main menu provides:

| Choice | Action |
|---:|---|
| 1 | Hash Table |
| 2 | Priority Queue |
| 3 | Performance Comparison |
| 4 | Dataset Information |
| 5 | Run Complete Demonstration |
| 6 | Reset Data Structures |
| 0 | Exit |

Every submenu uses `0` to return. Hash Table offers insert, search, delete, occupied-bucket display, the size-10 collision demonstration, and current statistics. Priority Queue offers insert, search, delete, peek, extract-max, heap-array display, and heap validation. Performance offers a benchmark run or viewing the latest report. Dataset offers source information, a preview of the first 10 loaded students, and validation of the current CSV on disk.

Record prompts require a positive student ID, non-empty name/program, and a priority from 1 through 100. Invalid choices and field values retry. An existing hash key updates its value; a duplicate queue ID reports an error without changing the queue. Missing searches and empty queue operations produce readable messages. File and validation errors return to the current menu. EOF or Ctrl+C exits gracefully, including during an unfinished record prompt.

Interactive operations change only the selected structure. The loaded source-record tuple stays unchanged, and neither structure writes student edits to the CSV. Benchmarks use that original loaded dataset in a fresh hash table, preserving interactive changes. Dataset validation re-reads the source file and reports when it differs from the loaded snapshot.

Reset re-reads and validates the CSV, builds both containers, then replaces the loaded records and containers together. If loading or rebuilding fails, the existing interactive state remains intact. Reset does not regenerate a missing CSV or save edits.

The complete demonstration validates the current CSV, demonstrates hash insertion/search/deletion, deliberate collisions, queue insertion/search/deletion, peek, extract-max, heap validity, independent state, benchmarking, and report saving. It uses separate containers and preserves interactive edits. It saves the latest real report to the configured results path.

Run the demonstration without prompts:

```powershell
python main.py --demo
```

`--dataset PATH` selects a source CSV and `--results PATH` selects the saved report. These paths must differ. Both options work with interactive mode or `--demo`. Defaults are `data/students.csv` and `results/performance_results.txt`, resolved relative to the project rather than the current working directory.

Run `python -m pytest -v` before accepting benchmark conclusions. See [CLI integration tests](../../tests/integration/README.md), [input tests](../../tests/unit/README.md), and [benchmark details](../performance/README.md).

[Source packages](../README.md)
