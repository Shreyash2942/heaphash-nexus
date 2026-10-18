# HeapHash Nexus: Complete Project Guide

This guide explains how to install, run, explore, test, and package HeapHash Nexus. You can use the application without reading or changing its Python source. For a shorter overview, see [README.md](README.md).

## Contents

1. [What the project does](#what-the-project-does)
2. [Requirements](#requirements)
3. [Open the project and set up Python](#open-the-project-and-set-up-python)
4. [First run and quick demonstration](#first-run-and-quick-demonstration)
5. [Main menu and navigation](#main-menu-and-navigation)
6. [Hash Table menu](#hash-table-menu)
7. [Priority Queue menu](#priority-queue-menu)
8. [Performance menu and benchmarking](#performance-menu-and-benchmarking)
9. [Dataset menu and CSV management](#dataset-menu-and-csv-management)
10. [Complete demonstration, reset, and exit](#complete-demonstration-reset-and-exit)
11. [Command reference](#command-reference)
12. [Run the tests](#run-the-tests)
13. [Use the structures from Python](#use-the-structures-from-python)
14. [Project organization and design](#project-organization-and-design)
15. [Read or rebuild the academic documentation](#read-or-rebuild-the-academic-documentation)
16. [Build and verify the submission](#build-and-verify-the-submission)
17. [Troubleshooting](#troubleshooting)
18. [Suggested first-time walkthrough](#suggested-first-time-walkthrough)

## What the project does

HeapHash Nexus implements two data structures from scratch and applies them to the same 150 student records:

| Component | Purpose | Behavior |
|---|---|---|
| Hash Table | Find a student by ID | Modulo hash function with separate chaining; an existing key is updated |
| Priority Queue | Retrieve the highest-priority student | Binary max-heap; a larger numeric priority is served first |
| Linear Search | Provide a comparison baseline | Scan the loaded records manually until a match is found |
| Benchmark | Measure both search methods | Check correctness, warm up, time searches, and save measurements |
| CLI | Explore the completed project | Menus for operations, dataset inspection, demonstration, and reset |

The CSV is a **synthetic, reproducibly generated dataset**, not an institutional student roster. The benchmark uses actual runtime measurements.

Interactive changes affect only the selected in-memory structure. They are **not saved to CSV**, are **not synchronized to the other structure**, and disappear when you exit or reset. The immutable source-record snapshot remains available for benchmarking.

## Requirements

| Use | Requirements |
|---|---|
| Run the application | Python 3.10 or newer; terminal; project files |
| Run automated tests | Python plus dependencies in [requirements.txt](requirements.txt) |
| Read the report | A PDF reader or a DOCX-compatible application |
| Rebuild figures and report | Optional dependencies in [requirements-docs.txt](requirements-docs.txt) |
| Rebuild the PDF | Optional documentation dependencies and Times New Roman font files |
| Check Word pagination | Windows with desktop Microsoft Word |
| Build a submission ZIP | Python standard library; completed project and QA artifacts |

The application needs no database, API key, account, server, or network connection. Installing dependencies may require internet access. Final project validation used Python 3.14.4 and Windows 11; other supported Python versions and operating systems were not separately certified.

## Open the project and set up Python

### Locate the correct folder

If you received a ZIP, extract it first. Open a terminal **inside the `heaphash-nexus` folder containing `main.py`, `src/`, and `requirements.txt`**. In Windows File Explorer, use the folder's Open in Terminal option. All commands below assume this folder is the current directory.

Check the Python version:

```powershell
python --version
```

It must be 3.10 or newer. If Windows recognizes `py` instead, check `py --version` and use `py` in place of `python` if that interpreter meets the requirement.

### Windows PowerShell: isolated environment

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

These commands use the environment interpreter directly and do not require activation. For later commands, replace `python` with `.\.venv\Scripts\python.exe` to keep using that environment. If you prefer activation and your PowerShell configuration permits it, run `.\.venv\Scripts\Activate.ps1`; afterward, `python` refers to the environment interpreter. Use `deactivate` to leave an activated environment.

### macOS/Linux: isolated environment

For bash or zsh:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Alternatively, invoke `.venv/bin/python` directly without activation. Use `deactivate` when finished with an activated environment.

### Existing Python environment

You may run `python main.py` directly because the application uses only the standard library. Installing `requirements.txt` adds pytest for testing; it is not required just to open the menus.

## First run and quick demonstration

Start interactive mode:

```powershell
python main.py
```

Expected startup text includes `Loaded 150 students.` followed by the main menu. Startup loads and validates `data/students.csv`, then populates both structures. If the selected CSV is missing, startup generates the default 150-record dataset at that path. An existing invalid CSV produces an error instead of being silently replaced.

For an automated demonstration without prompts:

```powershell
python main.py --demo --results results/my_demo.txt
```

Success ends with `Complete demonstration passed.` The result file contains actual measured times. The alternate results path preserves the final submitted benchmark and its match with the APA report.

For command-line help:

```powershell
python main.py --help
```

## Main menu and navigation

Type a choice number and press Enter. Every submenu uses **0** to return to the main menu.

| Main choice | Menu or action |
|---:|---|
| 1 | Hash Table |
| 2 | Priority Queue |
| 3 | Performance Comparison |
| 4 | Dataset Information |
| 5 | Run Complete Demonstration |
| 6 | Reset Data Structures |
| 0 | Exit |

Invalid menu choices cause another prompt. Student IDs must be positive integers; names and programs must contain text; priorities must be integers from **1 through 100**, inclusive. Incorrect fields are requested again. Equal names and priorities are permitted.

An insertion is published only after the required fields have been collected and validated. Ctrl+C or end-of-input exits gracefully, including from an unfinished prompt.

## Hash Table menu

Choose **1** from the main menu.

| Choice | Action | What to enter or expect |
|---:|---|---|
| 1 | Insert Student | ID, name, program, and priority; an existing ID updates its record |
| 2 | Search Student | ID; displays the stored record or `No student found.` |
| 3 | Delete Student | ID; reports whether removal occurred |
| 4 | Display Hash Table | Shows occupied bucket indices and their records |
| 5 | Show Collision Demonstration | Runs the separate size-10 collision example |
| 6 | Show Hash Table Statistics | Shows count, buckets, load, occupancy, collisions, and longest chain |
| 0 | Back | Returns to the main menu |

### Insert, update, search, and delete an example

With the original dataset loaded:

1. Select main **1**, then Hash Table **1**.
2. Enter ID `2001`, name `Alex Jordan`, program `Computer Science`, and priority `100`.
3. Select Hash Table **2** and enter `2001`. The inserted record is displayed.
4. Select Hash Table **1** again. Enter ID `2001`, name `Alex Jordan`, program `Data Science`, and priority `90`.
5. The application reports an update. Statistics show **151 students**, not 152: updating an existing key does not add another record.
6. Select Hash Table **3**, enter `2001`, and search again. The record is missing and the count returns to 150.

This sequence changes only the hash table. Searching the priority queue for 2001 still finds no record unless you insert it there separately.

### Understand the display and statistics

The default hash index is `student_id % 211`. The original dataset occupies 150 different buckets, so its load factor is approximately **0.7109**, current collisions are zero, and the longest chain is one. Records are shown in bucket order rather than sorted by student ID.

`Current collisions` counts entries beyond the first entry in each occupied bucket. It is not a historical counter. The table has a fixed capacity selected at construction and does not automatically resize. Separate chaining allows the item count to exceed the number of buckets.

### Collision demonstration

Select Hash Table **5**. A separate 10-bucket table inserts IDs **1001, 1011, and 1021** into bucket **1**. It finds all three, deletes 1011, and confirms that 1001 and 1021 remain searchable. It does not change your interactive hash table or queue.

## Priority Queue menu

Choose **2** from the main menu.

| Choice | Action | What to enter or expect |
|---:|---|---|
| 1 | Insert Student | ID, name, program, priority; duplicate IDs are rejected |
| 2 | Search Student | ID; finds a record independently of heap-array order |
| 3 | Delete Student | ID; removes that record and repairs the heap |
| 4 | Peek Highest Priority | Shows the root without removing it |
| 5 | Extract Maximum | Removes and displays a highest-priority record |
| 6 | Display Heap | Shows records by array index; index 0 is the root |
| 7 | Validate Heap | Checks all parent/child priority relationships |
| 0 | Back | Returns to the main menu |

### Try peek and extract-max

Starting with the original queue:

1. Select Priority Queue **1** and insert ID `2001`, name `Alex Jordan`, program `Computer Science`, priority `100`.
2. Select **4** to peek. The supplied CSV's maximum priority is 99, so this new record becomes the root.
3. Peek again. The same record remains because peek does not remove anything.
4. Select **5** to extract it, then **2** and search for `2001`. It is now missing from the queue.
5. Select **3** and delete original ID `1001` to try arbitrary deletion.
6. Select **7**. The output should say `Heap is valid.`
7. Return with **0**, then select main **6** to restore both structures from the CSV.

The root has a maximum priority, but the entire heap array is **not sorted**. Repeated extraction produces nonincreasing priorities. Equal-priority records have no guaranteed FIFO order. Empty peek/extraction are safe and display an empty-queue message.

To replace a queue record, delete its existing ID and insert the replacement. Queue insertion rejects duplicates rather than updating them. Deleting or extracting a queue record leaves the hash table unchanged.

## Performance menu and benchmarking

Choose **3** from the main menu:

| Choice | Action |
|---:|---|
| 1 | Run Hash vs. Linear Search Benchmark |
| 2 | View Latest Results |
| 0 | Return to the main menu |

The benchmark uses the original loaded source records in a fresh hash table, so interactive insertions, updates, and deletions do not change the workload. If you intentionally change the CSV during a session, reset first to reload it before benchmarking.

The default protocol uses:

- 150 records and a 211-bucket table.
- Targets `1001`, `1025`, `1075`, `1125`, `1150`, and missing ID `9999`.
- 100 warm-up searches per target per algorithm.
- 10,000 measured searches per target per algorithm: **60,000 per algorithm** overall.
- `time.perf_counter()` with alternating measurement order.
- Agreement checks before timing; setup, validation, warm-up, printing, and saving outside timed regions.

Use the standalone runner to save a separate experiment:

```powershell
python -m pytest -v
python -m src.performance.benchmark --output results/my_benchmark.txt
```

`python -m src.performance.benchmark` without `--output` replaces `results/performance_results.txt`. The CLI Performance menu and complete demonstration also replace their configured results file. To direct all menu-based reports elsewhere, start with:

```powershell
python main.py --results results/my_session.txt
```

### Read the results

| Output | Meaning |
|---|---|
| Found | Whether the target record exists |
| Hash/Linear total (s) | Total measured seconds for that target and method |
| Hash/Linear avg (us) | Total divided by repetitions, expressed in microseconds |
| Linear/hash | Linear time divided by hash time; above 1 favors hash search, below 1 favors linear search |
| Overall ratio | Sum of linear totals divided by sum of hash totals |
| N/A | Hash total was zero, so a ratio could not be calculated |

The saved academic run has a **10.241× aggregate linear/hash ratio**, with a faster linear lookup for the first record. Your timings will vary. This small ordered dataset has no normal-table collisions under modulus 211; the experiment does not prove that hashing always wins or measure collision-heavy timing. Tests check correctness rather than requiring a particular speed winner.

You may adjust experimental counts, for example:

```powershell
python -m src.performance.benchmark --warmup 10 --repetitions 1000 --output results/trial_benchmark.txt
```

This is a different protocol from the assignment's required 100/10,000 configuration. Keep the submitted dataset and results unchanged unless you also intend to regenerate and revalidate the report.

## Dataset menu and CSV management

Choose main **4**:

| Choice | Action |
|---:|---|
| 1 | Show source path, loaded count, ID range, and actual priority range |
| 2 | Preview the first 10 loaded students |
| 3 | Re-read and validate the current CSV on disk |
| 0 | Return to the main menu |

Validation reports if a valid CSV now differs from the loaded snapshot. It does not reload the structures; use main **6** for that.

### File format

The loader expects exactly these four column names; their order may differ. This illustration contains only two example rows, while the application requires **150 valid rows**:

```csv
student_id,name,program,priority
1001,Example Student,Computer Science,75
1002,Another Student,Data Science,90
```

IDs must be positive unique integers. Priorities must be integers from 1 to 100. Names/programs cannot be blank. Use UTF-8 CSV; fields containing commas must be quoted according to CSV rules. Names and priorities may repeat. The supplied IDs run from 1001 to 1150; seed 42 reproduces the default generated records. Its actual priorities range from 1 to 99.

### Create or validate data

```powershell
python -m src.dataset.data_generator
```

This validates and preserves an existing default CSV, or generates one if missing. Intentional regeneration uses `--overwrite` and replaces that file:

```powershell
python -m src.dataset.data_generator --overwrite
```

For experimentation without replacing the submitted CSV:

```powershell
python -m src.dataset.data_generator --output data/practice_students.csv
python main.py --dataset data/practice_students.csv --results results/practice_session.txt
```

The custom file still needs 150 valid records. The original benchmark target labels describe the supplied dataset's order; preserve that dataset for the academic comparison. The benchmark command itself does not generate a missing CSV.

## Complete demonstration, reset, and exit

**Main 5: Complete Demonstration.** Loads the current CSV into isolated containers; exercises hash operations, deliberate collisions, queue operations, peek/extract, heap validity, independent state, benchmark agreement, and report saving. It preserves your interactive containers and source CSV. It does replace its configured results file.

**Main 6: Reset Data Structures.** Re-reads the CSV and rebuilds both structures, discarding interactive edits. It uses the file's current valid contents, so it restores the supplied original records only when the CSV itself is unchanged. If reload or reconstruction fails, the previous interactive state remains. Reset does not recreate a missing CSV.

**Main 0: Exit.** Prints `Goodbye.` and exits. Ctrl+C or end-of-input also exits gracefully. There is no save-edits operation; restart reloads the CSV. Normal completion exits with status 0; startup or noninteractive demonstration errors exit with status 1. Argument-parser errors such as unknown flags use status 2. Recoverable interactive action errors return to their menu.

## Command reference

Unless explicitly redirected, paths point to the project defaults. Custom relative paths are interpreted from your terminal's working directory; quote paths containing spaces.

| Command | Purpose |
|---|---|
| `python main.py` | Start interactive menus |
| `python main.py --help` | Show application flags |
| `python main.py --demo --results results/my_demo.txt` | Run all major features without prompts, preserving final measurements |
| `python main.py --dataset data/practice_students.csv --results results/my_session.txt` | Use a separate source and report path |
| `python -m src.dataset.data_generator` | Create missing default data or validate existing data |
| `python -m src.dataset.data_generator --output data/practice_students.csv` | Create or validate another dataset file |
| `python -m src.performance.benchmark --output results/my_benchmark.txt` | Run the standard protocol to a separate report |
| `python -m src.performance.benchmark --help` | Show benchmark flags |
| `python -m pytest -v` | Run the complete automated suite |
| `python tools/build_submission.py --verify` | Package and test an extracted copy |

The application supports `--dataset`, `--results`, and `--demo`. The benchmark supports `--dataset`, `--output`, `--warmup`, and `--repetitions`. The generator supports `--output` and `--overwrite`. Results and source CSV paths must differ.

## Run the tests

Install the testing dependency into the interpreter you use, then run the suite:

```powershell
python -m pip install -r requirements.txt
python -m pytest -v
```

The validated baseline is **312 passing tests**: 211 unit and 101 integration tests.

| Area | Tests | Examples |
|---|---:|---|
| Dataset | 74 | Generator, schema, fields, uniqueness, count, bounds, preservation |
| Hash Table | 49 | Operations, updates, collisions, safe deletion, statistics |
| Priority Queue | 71 | Heap repair, ties, duplicates, empty cases, descending extraction |
| CLI input | 17 | Menu choices, integers, text, priority limits |
| Shared structures | 15 | Full dataset, deletion, independent state |
| Performance | 58 | Search agreement, timing protocol, calculations, saving |
| CLI integration | 28 | Menus, reset, demonstrations, errors, exit |

To narrow a diagnostic run:

```powershell
python -m pytest tests/unit/test_hash_table.py -v
python -m pytest tests/unit/test_priority_queue.py -v
python -m pytest tests/integration/test_cli.py -v
```

Do not accept performance conclusions while correctness tests fail. Existing final evidence is in [docs/validation/](docs/validation/README.md). To intentionally replace recorded regression evidence, capture the full suite rather than a selected test file:

```powershell
python -m pytest -v --junitxml=docs/validation/test_results.xml > docs/validation/pytest_output.txt
```

Check the terminal command's exit status and resulting transcript before using that evidence. These files document the run; ordinary test runs do not require replacing them.

## Use the structures from Python

Run these examples from the project root, for example in `python`'s interactive prompt or a separate script there. They modify only local Python objects.

### Load the dataset and use both APIs

```python
from src.dataset.data_loader import load_dataset
from src.data_structures.hash_table import HashTable
from src.data_structures.priority_queue import PriorityQueue

records = load_dataset()
table = HashTable()  # Default: 211 buckets.
queue = PriorityQueue()
for student in records:
    table.insert(student.student_id, student)
    queue.insert(student)

print(table.search(1001))
print(table.statistics())
print(queue.peek())           # Does not remove the root.
print(queue.extract_max())    # Removes a highest-priority record.
assert queue.validate_heap()
assert table.delete(1001)
assert table.search(1001) is None
assert queue.search(9999) is None
```

### Construct deliberate collisions

```python
from src.data_structures.hash_table import HashTable
from src.models.data_item import DataItem

collisions = HashTable(10)
for student_id in (1001, 1011, 1021):
    record = DataItem(student_id, f"Student {student_id}", "Demonstration", 50)
    collisions.insert(student_id, record)
assert len(collisions.buckets[1]) == 3
assert collisions.delete(1011)
assert collisions.search(1001) is not None
assert collisions.search(1021) is not None
```

`HashTable.insert(key, value)` updates duplicates and returns `None`; `search` returns a value or `None`; `delete` returns a Boolean. Queue insertion accepts a validated `DataItem` and rejects duplicate IDs. Queue search returns a record or `None`, deletion returns a Boolean, and peek/extract return a record or `None`. Bucket and heap inspection properties return immutable snapshots, and `DataItem` fields are frozen.

## Project organization and design

```text
heaphash-nexus/
|-- README.md                 # Concise overview and starting commands
|-- guide.md                  # Complete user, developer, and submission guide
|-- .gitattributes            # Exact-byte preservation for dataset/result checksums
|-- main.py                   # Thin CLI entry point
|-- requirements.txt          # Test dependencies; application uses standard library
|-- requirements-docs.txt     # Optional documentation tools
|-- pytest.ini                # Test configuration
|-- data/                     # Synthetic, validated 150-student CSV
|-- src/                      # Reusable implementation
|   |-- config/               # Default paths and numeric settings
|   |-- models/               # Immutable DataItem record
|   |-- dataset/              # CSV generation, loading, and validation
|   |-- data_structures/      # Algorithms implemented from scratch
|   |   |-- hash_table/       # State, chained operations, modulo helper
|   |   `-- priority_queue/   # State, heap operations, repair/validation helpers
|   |-- performance/          # Linear search, benchmark runner, result representation
|   |-- cli/                  # Application state, prompts, menus, demo, reset
|   `-- utils/                # Shared display formatting
|-- tests/                    # Unit and integration tests
|-- results/                  # Saved benchmark and optional personal experiments
|-- docs/                     # Implementation summary, report, diagrams, and QA evidence
|-- tools/                    # Reproducible report, verification, and packaging scripts
`-- submission/               # Local ZIP, checksum, and extracted-package evidence
```

Every maintained source/documentation folder has its own README with a more detailed annotated tree. Start with [source packages](src/README.md), [structures](src/data_structures/README.md), [performance](src/performance/README.md), [CLI](src/cli/README.md), or [tests](tests/README.md).

Algorithms live outside the CLI. The hash table uses explicit list chains rather than a dictionary for entry storage; its statistics dictionary only formats results. The heap is maintained manually without `heapq`. Shared frozen records can be referenced safely by independent containers.

For a heap element at index `i`, parent/left/right indices are `(i - 1) // 2`, `2*i + 1`, and `2*i + 2`. Heap repair is O(log n), but public insertion is O(n) because duplicate-ID detection scans the queue. Queue search/arbitrary deletion are O(n), peek O(1), extraction O(log n), and validation O(n). Hash operations have expected O(1 + load factor) work under suitable distribution and O(n) worst-case work. A prime table size does not guarantee good distribution.

Defaults are centralized in [settings.py](src/config/settings.py): 150 records, first ID 1001, allowed priorities 1–100, hash size 211, seed 42, six benchmark targets, 100 warm-ups, and 10,000 repetitions. Changing assignment defaults also requires reviewing tests, documentation, report assumptions, and QA tooling; the final audit intentionally enforces the submitted configuration.

## Read or rebuild the academic documentation

The existing report is ready to read; you do not need documentation dependencies to use the application:

- [APA PDF](docs/final_report.pdf): fixed-layout, 12-page report.
- [Editable Word report](docs/final_report.docx) and [Markdown companion](docs/final_report.md).
- [Architecture and data-flow diagrams](docs/diagrams/README.md): PNG and editable SVG.
- [Requirement traceability](docs/REQUIREMENT_TRACEABILITY.md), [QA report](docs/QA_REPORT.md), and [validation evidence](docs/validation/README.md).
- [Implementation summary](docs/SUMMARY.md): completed work, decisions, results, and verification from the six-day development plan.

The hashing explanation occupies pages 4–5, perfect/non-perfect hashing is on page 6, the heap design is on page 7, and benchmark method/results are on pages 9–10. Author and instructor names are deliberately left blank as requested by the project owner.

### Rebuild on the validated Windows setup

```powershell
python -m pip install -r requirements-docs.txt
python tools/build_diagrams.py
python tools/build_report.py
python tools/export_report.py
powershell -NoProfile -ExecutionPolicy Bypass -File tools/check_word_layout.ps1
python tools/verify_project.py
```

The report builder reads the **saved final benchmark**; it does not measure searches. PDF generation uses ReportLab and Times New Roman font files in `C:/Windows/Fonts`; `python tools/export_report.py --font-dir "D:/Fonts"` selects a different directory containing `times.ttf`, `timesbd.ttf`, `timesi.ttf`, and `timesbi.ttf`. The independent Word check requires desktop Word on Windows and runs an invisible instance. Its PowerShell policy override applies only to that process.

Changing report content can change page layout. The current QA audit checks the submitted 12-page layout and report measurements. If you intentionally change those assumptions, update the audit checks and revalidate them. Optional `--author`, `--instructor`, and `--date` flags in the report builder support personalization; leave them omitted to retain the current blank names.

The audit reads recorded regression evidence, checks documentation and artifacts, and exercises CLI commands with temporary reports. It does not rerun pytest. Run the complete suite separately after code changes. Git-exclusion checks run only in a Git working copy. See [tools/README.md](tools/README.md) for the individual scripts.

## Build and verify the submission

After the final tests and documentation checks pass:

```powershell
python tools/build_submission.py --verify
```

The tool creates:

| Local output | Purpose |
|---|---|
| `submission/heaphash-nexus-submission.zip` | Project, main README, this guide, source, dataset, tests, report, and evidence |
| `submission/heaphash-nexus-submission.zip.sha256` | SHA-256 digest of the archive |
| `submission/VALIDATION.json` | Archive integrity, payload hashes, extracted tests, and demo outcomes |
| `submission/packaged_pytest.txt` | Full test output from the extracted copy |
| `submission/packaged_demo.txt` | Complete demonstration output from the extracted copy |

The ZIP has one `heaphash-nexus/` top-level folder and a `SUBMISSION_MANIFEST.json` containing payload file hashes. `--verify` extracts into a temporary directory, checks every payload, and runs all tests and the complete demonstration using the current interpreter with test dependencies installed. It preserves submitted measurements. Omitting `--verify` builds the archive without executing the extracted tests.

The package excludes Git internals, environments, caches, Office lock files, local graphify output, the original implementation plan, and temporary experiment files. Only the default CSV and final benchmark are included from `data/` and `results/`.

The root README, this guide, and `docs/SUMMARY.md` are versioned project documentation and are included in the package. The obsolete implementation plan has been removed after its useful history was summarized. Graphify artifacts and `submission/` remain excluded from Git. No packaging command pushes to GitHub.

For a reviewer, extract the ZIP, enter its project folder, install `requirements.txt`, run `python -m pytest -v`, then use `python main.py` or the alternate-output demonstration command. See [docs/SUBMISSION.md](docs/SUBMISSION.md).

## Troubleshooting

| Symptom | Action |
|---|---|
| `python` is not recognized | Check the installed interpreter and PATH; on Windows try the `py` launcher, or invoke the environment interpreter directly |
| `main.py` or `requirements.txt` cannot be found | Open the terminal in the extracted project folder containing those files |
| `No module named pytest` | Run `python -m pip install -r requirements.txt` with the same interpreter used for tests |
| PowerShell blocks environment activation | Use `.\.venv\Scripts\python.exe` directly; activation is optional |
| Startup says the CSV is invalid | Read the reported row/field/count error; fix a separate working copy or intentionally regenerate with the dataset generator |
| Standalone benchmark says the CSV is missing | Run the dataset generator first, or supply an existing valid file through `--dataset` |
| Reset fails after CSV removal or editing | Restore a valid CSV and reset again; existing interactive structures are preserved after a failed reset |
| Duplicate queue ID error | Delete that queue record first, or choose a new positive ID; hash insertions instead update duplicates |
| Deleted hash record still appears in the queue | Expected: the two structures have independent state |
| Heap display looks unsorted | Expected: only parent/child order and a highest-priority root are guaranteed |
| Dataset preview ignores interactive edits | Expected: it displays the original loaded snapshot |
| Benchmark ignores interactive edits | Expected: the comparison uses original records and a fresh table |
| View Latest Results says no saved report exists | Run the benchmark in that session or select the correct `--results` path |
| Fresh timings differ from the report | Expected: timings depend on the run and machine; use alternate output paths to preserve the submitted evidence |
| Permission or output-file error | Use a writable output path and close conflicting files; interactive errors return to the menu |
| Report/font dependency missing | Install optional documentation dependencies; select a font directory containing all four required Times New Roman files |
| Word layout check cannot run | Use the validated Windows desktop Word setup for that optional check; ordinary application use and tests do not require Word |
| Packaging says report or QA evidence is stale | Regenerate report/PDF after intentional measurement changes, check layout, rerun documentation QA, then rebuild |

## Suggested first-time walkthrough

1. Open the project folder in a terminal and verify Python 3.10 or newer.
2. Create an environment and install `requirements.txt` if you want to run tests.
3. Run `python -m pytest -v`; confirm all tests pass.
4. Run `python main.py --results results/my_session.txt`.
5. Visit Dataset Information; inspect the source and preview, then validate the CSV.
6. Visit Hash Table; search ID 1001, try the ID-2001 insert/update/delete example, and run the collision demonstration.
7. Visit Priority Queue; try the priority-100 example, peek, extract, delete a record, and validate the heap.
8. Reset from the main menu to restore both structures from CSV.
9. Run the complete demonstration, then view its report through Performance Comparison.
10. Exit with 0, read the APA report, and use the submission builder if you need a verified ZIP.

[Return to the main README](README.md)
