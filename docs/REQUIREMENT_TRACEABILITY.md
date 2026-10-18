# Assignment Requirement Traceability

This matrix maps the six-day requirements to the completed implementation and final evidence. The supplied six-day plan is the requirements baseline; no separate instructor rubric was supplied. Function names below identify meaningful tests within linked files.

| Requirement | Implementation / documentation | Verification evidence |
|---|---|---|
| Shared dataset with at least 100 records | [CSV](../data/students.csv): 150 records, four required fields, IDs 1001–1150 | [Dataset tests](../tests/unit/test_dataset.py); final CSV validation and demonstration |
| Reproducible generation, loading, validation | [Dataset package](../src/dataset/README.md), seed 42, frozen [DataItem](../src/models/data_item.py) | 74 dataset unit tests: schema, types, count, IDs, bounds, preservation |
| Custom hash-table state and modulo function | [HashTable](../src/data_structures/hash_table/hash_table.py), [helper](../src/data_structures/hash_table/helpers/hash_function.py); list-based buckets, size 211 | `test_new_table_uses_configured_size_and_starts_empty`, `test_modulo_hash_function` in [hash tests](../tests/unit/test_hash_table.py) |
| Hash insert, search, delete | [Operations](../src/data_structures/hash_table/operations/README.md) | Hash tests cover present/missing keys, invalid inputs, reinsertion, full dataset |
| Duplicate keys update, counts and statistics | `insert`, `item_count`, `load_factor`, `statistics` | `test_duplicate_key_updates_each_position_in_a_collision_chain`, `test_statistics_describe_current_occupancy_after_updates_and_deletions` |
| Separate chaining and deliberate collisions | Size-10 table; 1001, 1011, 1021 share bucket 1 | `test_required_collision_demonstration_preserves_remaining_records`; [recorded demo](validation/demo_output.txt) deletes 1011 and finds survivors |
| Explain hash choice and collision resolution | [Report](final_report.pdf), pp. 4–5; [editable report](final_report.docx) | [PDF layout](validation/report_layout.json), [independent Word layout](validation/word_layout.json): exactly two consecutive pages |
| Perfect and non-perfect hashing | Report p. 6; finite-set perfect versus general collision-prone mapping | Definition cited to NIST; examples include `k - 1001` on the fixed set and modulo collision 1001/1212 |
| Custom priority queue and list-based binary max-heap | [PriorityQueue](../src/data_structures/priority_queue/priority_queue.py), [repair helpers](../src/data_structures/priority_queue/helpers/README.md) | 71 [queue unit tests](../tests/unit/test_priority_queue.py); no use of `heapq` in core implementation |
| Parent/child indices, insertion, heapify up/down | Helpers and [operations](../src/data_structures/priority_queue/operations/README.md) | `test_heapify_up_repairs_multiple_ancestor_levels`, `test_heapify_down_repairs_children_without_losing_records` |
| Peek and extract maximum | Queue API returns `DataItem` or `None` | `test_peek_preserves_root_and_entire_heap`, single-record and full extraction tests |
| Search and arbitrary deletion with correct repair direction | ID lookup plus up/down decision after last-record replacement | `test_arbitrary_deletion_selects_the_needed_repair_direction` and root/interior/last deletion cases |
| Heap validity, equal priorities, empty and missing operations | `validate_heap`; ties valid without stable FIFO order | Validator, ties, empty operations, missing delete, and duplicate-ID rejection tests |
| Load all 150 records and extract descending priorities | Queue population and repeated `extract_max` | `test_all_150_csv_records_extract_in_descending_order_with_valid_heap` in three input orders |
| Shared-data integration and independent structures | [Integration fixtures and tests](../tests/integration/test_data_structures.py) | 15 tests cover all-record presence, representative deletion, duplicate hash update, extraction, and independence |
| Manual linear search and matching results | [linear_search.py](../src/performance/linear_search.py), benchmark validates full table and each target | `test_manual_linear_search_matches_hash_for_every_record_and_missing_keys`; disagreement rejected before any timing |
| Required timing protocol | [benchmark.py](../src/performance/benchmark.py): six specified targets, 100 warm-ups, 10,000 repetitions, `perf_counter`, alternate order | `test_required_default_protocol_counts_every_search_and_excludes_output`, timing-order and error tests |
| Results, averages, ratios and file output | [result.py](../src/performance/result.py), [saved actual measurements](../results/performance_results.txt) | 58 [performance integration tests](../tests/integration/test_performance.py); zero-time ratio and output protections included |
| Analyze actual performance after correctness passes | Report pp. 9–10; final aggregate ratio 10.241×; first-record exception and limitations stated | [Report metadata](report_metadata.json) contains source benchmark SHA-256; QA checks exact match |
| Main menu and all interactive structure operations | [CLI package](../src/cli/README.md), thin [main.py](../main.py) | 17 [input tests](../tests/unit/test_input_handler.py), 28 [CLI integration tests](../tests/integration/test_cli.py), recorded terminal walkthrough |
| Dataset/performance menus, demo, reset and graceful exit | Dedicated menus; reset publishes new state only after success; demo uses isolated containers | CLI integration tests include failed reset, EOF/Ctrl+C, invalid input, file errors, and preserved CSV |
| Architecture and data-flow diagrams | [Figures](diagrams/README.md): PNG, SVG, and report figures | Source/diagram review; PNG dimensions and file presence checked during QA |
| APA report, conclusion and references | PDF, DOCX and Markdown companion; cited primary sources; APA student-paper layout | 12 pages, embedded fonts, page numbering, two hashing pages, observed-results table, reference list |
| Root and per-folder documentation; valid commands | Published root README, complete guide, [implementation summary](SUMMARY.md), and each maintained folder's README | Documented commands executed; local links and directory-guide coverage checked |
| Final cleanup and complete regression | Two unused imports and obsolete `.gitkeep` markers removed | [Verbose final pytest](validation/pytest_output.txt): **312 passed**; no failures/errors/skips; AST and placeholder scan |
| Clean submission package | [Packaging guide](SUBMISSION.md), standard-library archive builder and manifest | Extracted-package pytest and complete demo, payload hash verification, ZIP integrity, exclusion checks |
| Focused Git progression and local-only artifacts | Focused development, documentation, cleanup and packaging commits | Root README and implementation summary are versioned; retired plan is removed; graphify artifacts and generated archive remain excluded from Git |

Read the [final QA record](QA_REPORT.md) for executed command details, outcomes, limitations, and artifact hashes.

[Documentation guide](README.md)
