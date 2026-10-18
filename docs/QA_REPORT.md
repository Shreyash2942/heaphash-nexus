# Final Quality Assurance Record

Final checks were completed on October 18, 2026, with Python 3.14.4 on Windows 11. The six-day plan supplied by the owner is the requirements baseline; no separate instructor rubric was available.

| Check | Result and evidence |
|---|---|
| Initial full regression | 312 passed before the final real benchmark |
| Final full regression | `python -m pytest -v --junitxml=docs/validation/test_results.xml`: **312 passed**, no failures, errors, or skips; [verbose transcript](validation/pytest_output.txt), [JUnit XML](validation/test_results.xml) |
| Test breakdown | 211 unit: dataset 74, hash 49, queue 71, inputs 17; 101 integration: structures 15, performance 58, CLI 28 |
| Complete demonstration | `python main.py --demo` passed, saved final measurements; [transcript](validation/demo_output.txt) |
| Interactive terminal walkthrough | Main navigation, invalid choice, collision demo, hash statistics/search, queue peek/extract/validation, performance run/view, dataset info/preview/validation, reset, exit; [transcript](validation/menu_output.txt) |
| README application commands | Entry-point help, dataset generator preserving existing CSV, standalone benchmark with alternate output, complete demo with alternate results, interactive startup/navigation; return codes in [validation JSON](validation/validation.json) |
| Benchmark correctness | All six target results agree; five present records and one missing ID; dataset and table match before timing |
| Required benchmark protocol | 150 records, 211 buckets, 100 warm-ups and 10,000 measurements per target per algorithm; six required targets; `time.perf_counter()` |
| Actual final results | Hash total 0.008774800 s; linear total 0.089858400 s; average 0.146247 μs / 1.497640 μs; aggregate linear/hash ratio **10.241×** |
| Report/result agreement | Every table row and aggregate ratio checked; benchmark SHA-256 matches [report metadata](report_metadata.json) |
| APA document layout | PDF and Word each 12 pages; hashing explanation exactly pp. 4–5; US Letter, one-inch margins, Times New Roman 12, 24-point body leading, page numbers, hanging references |
| PDF/Word verification | PDF fonts embedded; figures, hashing pages, performance table, title page and references inspected; [PDF evidence](validation/report_layout.json), [independent Word evidence](validation/word_layout.json) |
| Figures | Architecture and data flow match code; PNG dimensions 1920 × 1480 with editable SVG companions |
| Configuration | Dataset 150, start ID 1001, allowed priorities 1–100, seed 42, hash size 211, collision size 10, all six targets, 100/10,000 searches agree with documentation |
| Cleanup | Two unused test imports and four obsolete directory markers removed; Python AST import audit; no TODO/FIXME/debugging or dead experimental code found in implementation review |
| Documentation | Every maintained folder has an annotated README; all local documentation links resolve |
| Complete project guide | Root [guide.md](../guide.md) explains setup, all menus, examples, API use, testing, results, documentation tools, packaging, and troubleshooting; linked from the main README and included in the submission |
| Source preservation | Terminal command checks preserve both source CSV and submitted benchmark; digests recorded |
| Requirements | [Traceability matrix](REQUIREMENT_TRACEABILITY.md) maps implemented requirements to source, tests, report pages, and evidence |
| Submission | Clean local ZIP with payload manifest/checksum; extracted-package regression and complete demonstration recorded in local `submission/VALIDATION.json` |
| Git constraints | Root overview/plan, graphify artifacts and local archive remain excluded from Git; no push performed |

The application depends only on the standard library. Tests use pytest. Optional documentation tools use python-docx, Pillow, ReportLab, and PyMuPDF; Word is used only for an independent pagination check. Word's PDF export stalled on this machine, so the final PDF is rendered directly from the generated Word content using ReportLab with embedded fonts. Both formats have independently verified pagination.

The first-record linear search was faster than hash search. Results describe one machine and an ordered synthetic dataset whose IDs do not collide at size 211. No timing threshold is asserted by tests, and the project makes no universal speedup claim. Duplicate checking makes the implemented queue's public insertion O(n), despite O(log n) heap repair. These limitations are discussed in the report.

Author/instructor names were not supplied and are omitted from the title page. Institution, course, and date are included. Package verification is performed after archive creation and is kept outside the archive to avoid a self-referential checksum cycle.

[Documentation guide](README.md)
