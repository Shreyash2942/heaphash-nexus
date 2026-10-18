# Project Implementation Summary

HeapHash Nexus is a completed Python project implementing a custom chained hash table and a binary max-heap priority queue over the same 150 student records. This document preserves the completed work and decisions from the former `IMPLEMENTATION_PLAN.md`, replacing its development checklist with a concise record of what was delivered.

For instructions, start with the root [README](../README.md) or the [complete project guide](../guide.md). For requirement-by-requirement evidence, see [traceability](REQUIREMENT_TRACEABILITY.md) and [final QA](QA_REPORT.md).

## Goals and final outcome

The project provides custom insert, search, and delete operations for both structures; priority-queue peek and extract-max; explicit collision handling; one validated shared dataset; a manual linear-search baseline; actual runtime measurements; an interactive CLI; automated tests; and an APA report with diagrams and references.

The supplied CSV contains **150 synthetic student records**, with unique IDs **1001–1150**. Allowed priorities are **1–100**; the seeded file's actual range is **1–99**. The benchmark uses actual measured execution times. No external institutional student roster is claimed.

## Work completed across the six development days

| Day | Implementation completed | Verification and deliverables |
|---|---|---|
| 1: Foundation and dataset | Modular packages, shared settings, frozen `DataItem`, seeded CSV generation, loading and validation | 150-record CSV, schema/type/uniqueness/bounds checks, reproducible seed 42, dataset tests |
| 2: Hash Table | List-based buckets, modulo helper, insert/update, search, delete, item count, load factor and statistics | Size-10 collisions for 1001/1011/1021, safe deletion of 1011, duplicate updates, all-record storage and hash tests |
| 3: Priority Queue | List-based binary max-heap, index relationships, upward/downward repair, insert, search, arbitrary delete, peek, extract-max and validation | Empty cases, ties, duplicate-ID rejection, both deletion repair directions, 150-record loading and descending extraction |
| 4: Integration and performance | Shared-dataset integration, manual linear scan, verified benchmark runner, immutable result representation, averages/ratios and saved output | Matching search results, independent structures, six required targets, timing-protocol and result tests, actual measurements |
| 5: CLI and complete integration | Main and submenu navigation, reusable validation, all operations, dataset/performance menus, collision demo, complete demo, reset and entry point | Interactive terminal walkthroughs, graceful exit, failed-reset preservation, input and CLI integration tests |
| 6: Report and final submission | APA PDF/DOCX/Markdown, architecture/data-flow figures, hashing analysis, actual-results analysis, references, README guides, traceability, cleanup and packaging | Final regression, successful complete demo, matching report/result digests, verified report pagination, manifest/checksum and extracted-package execution |

Subsequent documentation work added the complete [guide.md](../guide.md), reviewed all 52 final-checklist items, and replaced the retired implementation plan with this summary. The root README is now included in Git for publication on GitHub.

## Architecture and implementation decisions

| Area | Final design |
|---|---|
| Entry point | `main.py` delegates to the CLI; it contains no data-structure algorithms |
| Data model | Frozen `DataItem(student_id, name, program, priority)` records |
| Dataset | Generator, loader and validator in `src/dataset/`; valid source CSV is preserved during interactions |
| Hash Table | `src/data_structures/hash_table/`; each bucket is a separate Python list of explicit key-value pairs |
| Priority Queue | `src/data_structures/priority_queue/`; manually maintained max-heap in a Python list |
| Performance | `src/performance/`; manual linear search, validated timing runner and result formatting/saving |
| CLI | `src/cli/`; prompts, presentation, independent containers, demonstrations and atomic reset |
| Tests | `tests/unit/` and `tests/integration/`, separate from implementation |
| Documentation | Per-folder READMEs, complete guide, academic report, diagrams, traceability and QA evidence |

### Hash Table

The normal table uses **211 buckets** and computes `key % table_size`. Collisions use separate chaining. Duplicate keys update their stored value without increasing `item_count`; missing search returns `None` and missing deletion returns `False`. Statistics expose occupancy, load factor and current chain lengths.

The default load factor is `150 / 211`, approximately **0.7109**. The consecutive supplied IDs have distinct residues modulo 211. A separate 10-bucket demonstration deliberately places 1001, 1011 and 1021 into bucket 1, removes 1011, and verifies the remaining records. A statistics dictionary formats output only; dictionaries do not store the custom table's entries.

Expected operation work is O(1 + load factor) under suitable distribution; worst-case work is O(n). Capacity is fixed rather than automatically resized. Perfect/non-perfect hashing and the limits of the normal dataset's collision-free mapping are explained in the report.

### Priority Queue

The maximum-priority record is at index 0. Parent and child indices are `(i - 1) // 2`, `2*i + 1` and `2*i + 2`. Insertion repairs upward; root extraction repairs downward. Arbitrary deletion moves the final record into the gap and selects the appropriate repair direction. The implementation does not use `heapq`.

Duplicate student IDs are rejected. Equal priorities are valid without a FIFO guarantee. Empty peek/extract return `None`. Heap repair is O(log n), but public insertion is O(n) because it includes a duplicate-ID scan. Search and arbitrary deletion are O(n); peek is O(1), extraction O(log n), and validation O(n).

### CLI and independent state

The main menu exposes Hash Table, Priority Queue, Performance Comparison, Dataset Information, Complete Demonstration, Reset and Exit. Invalid input is retried; missing records and empty structures have readable output. EOF and Ctrl+C exit gracefully.

Interactive edits affect only the selected structure and are not written to CSV. Benchmarks use the original loaded records in a fresh table. Demonstrations use isolated containers. Reset reloads the current valid CSV and publishes both rebuilt structures together; failure preserves the previous interactive state.

## Actual performance experiment

The required experiment uses targets **1001, 1025, 1075, 1125, 1150 and 9999**, with **100 warm-up searches** and **10,000 measured searches per target per algorithm**. Each method performs **60,000 measured searches**. The runner checks agreement before measuring, uses `time.perf_counter()`, alternates measured order, and excludes setup, validation, warm-up, printing and saving from timed blocks.

| Final saved measurement | Hash Table | Linear Search |
|---|---:|---:|
| Total measured time | 0.008774800 s | 0.089858400 s |
| Overall average per search | 0.146247 microseconds | 1.497640 microseconds |

The aggregate linear/hash time ratio is **10.241×**. Linear search was faster for the first record. These results describe one run on Python 3.14.4 and Windows 11 with a small, ordered synthetic dataset and no normal-table collisions; they do not establish a universal speedup. Reruns vary.

See [saved measurements](../results/performance_results.txt), [report metadata](report_metadata.json), and report pages 9–10. The summary quotes the saved run rather than introducing new timing data. Git preserves the CSV and benchmark bytes so their recorded SHA-256 digests remain valid after checkout or download.

## Testing and quality evidence

The completed baseline has **312 passing tests**, with no failures, errors or skips:

| Test area | Count |
|---|---:|
| Dataset unit tests | 74 |
| Hash Table unit tests | 49 |
| Priority Queue unit tests | 71 |
| CLI input unit tests | 17 |
| Shared-structure integration tests | 15 |
| Performance integration tests | 58 |
| CLI integration tests | 28 |
| **Total** | **312** |

Coverage includes collisions, duplicate behavior, missing/empty operations, heap invariants, both deletion repair directions, descending extraction, independent containers, failed reset, CSV preservation, timing protocol, result arithmetic, menus and graceful exit. Tests do not require a particular algorithm to win a timing comparison.

The complete demonstration passed from the source project and the extracted submission. Package verification checks ZIP integrity, payload hashes, the complete test suite and the extracted application's demonstration. The [validation folder](validation/README.md) contains source evidence; generated `submission/VALIDATION.json` records local archive checks.

## Documentation delivered

- [Root README](../README.md): setup, usage, configuration, design and results.
- [Complete guide](../guide.md): all menus, examples, command reference, API use, troubleshooting and packaging.
- [APA PDF](final_report.pdf), [Word report](final_report.docx) and [Markdown companion](final_report.md): 12-page report with design, testing, actual performance, conclusion and primary references.
- Hash-function and collision-resolution explanation on report pages **4–5**, perfect/non-perfect hashing on page **6**, and heap design on page **7**.
- [Architecture and data-flow diagrams](diagrams/README.md): PNG and editable SVG versions, plus rebuild tooling.
- [Requirement traceability](REQUIREMENT_TRACEABILITY.md), [QA report](QA_REPORT.md), and [submission instructions](SUBMISSION.md).

The report uses US Letter pages, one-inch margins, Times New Roman 12 with 24-point body leading, page numbers and hanging references. PDF and Word pagination were independently checked. Author and instructor names remain blank at the owner's request.

## Cleanup and publication

The obsolete implementation plan was removed after its useful content was consolidated here. Python/test caches are disposable development artifacts and remain excluded from Git and submission. Source, tests, the dataset, actual benchmark, academic deliverables, folder guides, QA evidence and reproducible build tools are retained because they support running or reviewing the project.

The root README, guide and this summary are versioned with the completed project. Local graphify artifacts, environments, caches and generated submission archives remain excluded from Git; graphify output is also excluded from the submission. Focused commits preserve the actual development progression. Publication uses a normal Git push to the configured project remote.

[Documentation guide](README.md)
