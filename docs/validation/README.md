# Final Validation Evidence

These files record executed checks for the final submission. They are review evidence, not application inputs.

```text
validation/
|-- README.md           # Evidence descriptions and reproduction
|-- demo_output.txt     # Successful complete demonstration and final real benchmark
|-- menu_output.txt     # Terminal walkthrough across menus, invalid input, and reset
|-- pytest_output.txt   # Final verbose source-tree regression output
|-- test_results.xml    # Machine-readable final test counts and outcomes
|-- report_layout.json  # PDF pagination, embedded fonts, and document hashes
|-- word_layout.json    # Independent Microsoft Word pagination check
`-- validation.json     # Command checks, consistency checks, and artifact digests
```

Repeat checks from the project root with `python main.py --demo` and `python -m pytest -v`. Rerunning the demonstration without `--results` replaces the benchmark; regenerate the academic report afterward. Pass a different results path to preserve the submitted measurements.

Final PDF inspection and the independent Word check verify that the hashing explanation occupies exactly two consecutive pages in each format. Extracted-package execution and integrity evidence are recorded separately in the generated local `submission/` directory.

[Documentation guide](../README.md)
