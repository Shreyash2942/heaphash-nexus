# Documentation and Submission Tools

These optional tools create submission artifacts; the application itself uses only the Python standard library.

```text
tools/
|-- README.md             # Tool usage and optional dependencies
|-- build_diagrams.py     # Rebuild editable SVG and 300-dpi PNG project diagrams
|-- build_report.py       # Build APA Word paper and Markdown from saved measurements
|-- export_report.py      # Render PDF directly with embedded Times New Roman fonts
|-- check_word_layout.ps1 # Verify Word pagination independently on Windows
|-- verify_project.py     # Audit documentation, saved regression, and CLI commands
`-- build_submission.py   # Create a clean local ZIP and SHA-256 manifest
```

From the project root, install `python -m pip install -r requirements-docs.txt` and run `python tools/build_diagrams.py` to rebuild the architecture and data-flow figures.

Run `python tools/build_report.py` to create the Word paper, Markdown companion, and benchmark metadata. Optional `--author "Full Name"`, `--instructor "Instructor Name"`, and `--date "October 18, 2026"` personalize the title page. Omitted names are not replaced with invented text. Generation reads the saved real benchmark without rerunning it.

Run `python tools/export_report.py` to render the generated Word content into PDF using ReportLab. It embeds the Times New Roman fonts from `C:/Windows/Fonts`; `--font-dir PATH` accepts another directory containing `times.ttf`, `timesbd.ttf`, `timesi.ttf`, and `timesbi.ttf`. This avoids dependence on Word's PDF export service. The report uses US Letter, one-inch margins, 12-point Times New Roman with 24-point body leading, page numbers, and hanging references.

On Windows with desktop Word, `powershell -NoProfile -ExecutionPolicy Bypass -File tools/check_word_layout.ps1` independently verifies that the Word hashing explanation occupies exactly two consecutive pages. The execution-policy override affects only that process. The script creates and closes its own invisible Word instance and does not modify the document.

Run `python tools/build_submission.py` to create the ignored local submission ZIP with a payload manifest and checksum. Add `--verify` to check every payload hash and run all tests and the complete demonstration from a temporary extracted copy. Packaging uses the standard library; extracted tests use the installed pytest dependency. See [submission instructions](../docs/SUBMISSION.md).

After capturing the final test output and Word layout, `python tools/verify_project.py` validates recorded test results, PDF layout and embedded fonts, benchmark agreement, folder guides, local links, imports, diagrams, documented application commands, and Git exclusions. It writes evidence under `docs/validation/` and keeps the submitted benchmark unchanged. PyMuPDF is an optional documentation dependency used for this audit.

[Project overview](../README.md)
