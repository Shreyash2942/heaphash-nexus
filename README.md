# HeapHash Nexus

Custom hash table and binary max-heap priority queue in Python, with 150 synthetic student records, an interactive CLI, automated tests, and a measured hash-versus-linear-search comparison.

**New to the project? Read the [complete project guide](guide.md)** for setup, every menu, step-by-step examples, commands, testing, troubleshooting, and submission instructions.

## Setup and run

Python **3.10 or newer** is required; final verification used **Python 3.14.4 on Windows 11**. The application uses the standard library. Pytest is the only testing dependency. Run commands from this directory:

```powershell
python -m pip install -r requirements.txt
python main.py
```

For an isolated Windows environment, run `python -m venv .venv`, then use `.venv/Scripts/python.exe` in place of `python`. On macOS/Linux, the environment interpreter is `.venv/bin/python`.

```powershell
python main.py --demo
python -m pytest -v
python -m src.performance.benchmark
python -m src.dataset.data_generator
```

The demonstration checks major operations and saves a fresh benchmark. The standalone benchmark also replaces `results/performance_results.txt`. Dataset generation preserves and validates an existing CSV; `--overwrite` intentionally regenerates it. Run correctness tests before interpreting performance measurements.

To retain the submitted measurements while experimenting:

```powershell
python main.py --demo --results results/my_demo.txt
python -m src.performance.benchmark --output results/my_benchmark.txt
```

Both CLI modes accept `--dataset PATH`; the application accepts `--results PATH`. Benchmark options include `--warmup N` and `--repetitions N`.

## Main menu

| Choice | Operations |
|---|---|
| 1. Hash Table | Insert/update, search, delete, display, statistics, collision demonstration |
| 2. Priority Queue | Insert, search, delete, peek, extract-max, heap display, validation |
| 3. Performance | Run benchmark; view saved results |
| 4. Dataset | Preview original records; validate source CSV |
| 5. Complete Demonstration | Check structures, collisions, heap, independence, and benchmark |
| 6. Reset | Reload CSV and rebuild both structures |
| 0. Exit | Exit gracefully; EOF and Ctrl+C also exit |

Invalid choices and fields trigger a new prompt. Interactive edits remain in memory and do not modify the CSV. Hash updates and queue edits are independent. Reset restores original records, preserving current state if reload fails. Demonstrations use isolated containers; benchmarks use original records in a fresh table.

## Data and configuration

Each frozen `DataItem` contains `student_id`, `name`, `program`, and `priority`. The CSV contains **150 unique IDs, 1001–1150**. Valid priorities are **1–100**; the current seeded dataset happens to range from **1 to 99**. Names and priorities may repeat. These are synthetic records.

Authoritative values are in [settings.py](src/config/settings.py):

| Setting | Default |
|---|---|
| Dataset count / first ID | 150 / 1001 |
| Generator seed | 42 |
| Priority bounds | 1–100 inclusive |
| Hash-table size | 211 buckets |
| Collision demonstration size | 10 buckets |
| Benchmark targets | 1001, 1025, 1075, 1125, 1150, 9999 (missing) |
| Warm-up / measured searches | 100 / 10,000 per target per algorithm |
| Saved results | `results/performance_results.txt` |

## Implemented algorithms

The hash table computes `key % table_size` and stores `(key, value)` pairs in separate Python lists. Duplicate keys update values without increasing the count. Missing search returns `None`; deletion returns a Boolean. The normal load factor is `150 / 211 ≈ 0.7109`. Capacity is configurable and does not resize automatically. Dictionaries are not entry storage; a statistics dictionary only formats output.

The normal dataset has distinct residues modulo 211. A separate size-10 demonstration inserts **1001, 1011, 1021** into bucket 1, deletes 1011, and verifies both survivors. Collision support is tested even though the normal dataset does not create collisions.

The priority queue stores a max-heap in a Python list, with parent `(i - 1) // 2` and children `2*i + 1`, `2*i + 2`. Insertion repairs upward. Root removal repairs downward. Arbitrary deletion selects direction based on the replacement's parent. Duplicate IDs are rejected, equal priorities have no FIFO guarantee, and empty peek/extract return `None`. The implementation does not use `heapq`.

| Operation | Hash table | Priority queue |
|---|---|---|
| Insert | Expected O(1 + α), worst O(n) | O(n), including duplicate-ID scan; repair O(log n) |
| Search | Expected O(1 + α), worst O(n) | O(n) |
| Delete | Expected O(1 + α), worst O(n) | O(n), including lookup; repair O(log n) |
| Peek / extract-max | — | O(1) / O(log n) |
| Heap validation | — | O(n) |
| Storage | O(m + n) | O(n) |

Expected hash bounds assume suitable distribution; a prime modulus does not guarantee it. Here `n` is item count, `m` is bucket count, and `α = n/m`.

## Benchmark and verification

The baseline manually scans records. Before timing, the runner verifies full table contents and target agreement. It uses `time.perf_counter()`, alternates measured order across targets, and excludes setup, checks, warm-up, printing, and file I/O. Timed blocks include loop and public-search overhead. Each algorithm performs **60,000 measured searches**.

The saved final run averaged **0.146247 μs for hash search** and **1.497640 μs for linear search**, with a **10.241× linear/hash time ratio**. Linear search was faster for the first record. Reruns vary; these measurements describe this dataset and machine. The report discusses the small ordered dataset, normal-table absence of collisions, and lack of independent repeated timing blocks.

The final suite passed **312 tests**: 211 unit and 101 integration tests. It covers dataset validation, structure operations, collisions, duplicate behavior, heap invariants, descending extraction, independent state, benchmark correctness, result arithmetic, input validation, and CLI workflows. Tests do not require a timing winner.

## Project structure

Every maintained folder has a README with a local annotated tree and links.

```text
heaphash-nexus/
|-- README.md                 # Published project overview, setup, usage, and final results
|-- guide.md                  # Complete instructions for users, developers, and reviewers
|-- .gitattributes            # Preserve dataset and benchmark bytes for recorded checksums
|-- main.py                   # Thin CLI entry point
|-- requirements.txt          # Test dependency; runtime uses standard library
|-- requirements-docs.txt     # Optional report and diagram dependencies
|-- pytest.ini                # Test discovery and import configuration
|-- data/                     # Validated, seeded 150-record CSV
|-- src/                      # Implementation packages
|   |-- config/               # Shared paths and configuration
|   |-- models/               # Frozen student record
|   |-- dataset/              # Generator, CSV loader, and validator
|   |-- data_structures/      # Custom algorithms and storage
|   |   |-- hash_table/       # Chained table, operations, modulo helper
|   |   `-- priority_queue/   # Binary max-heap, operations, repair helpers
|   |-- performance/          # Linear baseline, benchmark, result representation
|   |-- cli/                  # Menus, prompts, state, reset, demonstration
|   `-- utils/                # Shared display helpers
|-- tests/                    # Unit and integration regression suite
|-- results/                  # Actual saved benchmark
|-- docs/                     # Implementation summary, APA report, figures, and QA evidence
|-- tools/                    # Documentation and submission builders
`-- submission/               # Generated local ZIP, checksums, package verification
```

The root README, guide, and [implementation summary](docs/SUMMARY.md) are included in Git and the submission ZIP. The obsolete implementation plan has been replaced by the summary. Local graphify artifacts remain excluded from Git and submission; the generated submission ZIP stays outside Git. Dataset and benchmark bytes are preserved so their recorded checksums remain valid after checkout or download.

## Academic documentation and submission

- [Implementation summary](docs/SUMMARY.md): completed work across the six development days, design decisions, results, and verification.
- [APA PDF](docs/final_report.pdf), [editable Word report](docs/final_report.docx), [readable companion](docs/final_report.md).
- [Architecture and data-flow figures](docs/diagrams/README.md), including editable SVG.
- [Requirement traceability](docs/REQUIREMENT_TRACEABILITY.md) and [final QA](docs/QA_REPORT.md).
- [Submission instructions](docs/SUBMISSION.md) and [build tools](tools/README.md).

The report uses actual measurements and includes a two-page hashing explanation, perfect/non-perfect hashing, heap design, testing, CLI discussion, limitations, and references. Unspecified author/instructor names are omitted; optional builder flags personalize the title page.

```powershell
python -m pip install -r requirements-docs.txt
python tools/build_diagrams.py
python tools/build_report.py
python tools/export_report.py
powershell -NoProfile -ExecutionPolicy Bypass -File tools/check_word_layout.ps1
python tools/verify_project.py
python tools/build_submission.py --verify
```

PDF generation uses ReportLab and embeds Times New Roman from the Windows fonts directory (`--font-dir PATH` supports another font directory). The independent Word pagination check requires desktop Word on Windows; the execution-policy option affects only that PowerShell process. If saved measurements change, rebuild the report and repeat layout checks before packaging. Documentation dependencies are not needed to run the application or tests.
