# Project Documentation

The academic report describes completed code and actual saved measurements. Word is editable, PDF preserves the verified layout, and Markdown provides a readable companion.

```text
docs/
|-- README.md                    # Academic and submission documentation guide
|-- SUMMARY.md                   # Completed six-day implementation, decisions, and results
|-- final_report.docx            # APA student paper with figures and real results
|-- final_report.pdf             # Font-embedded PDF submission copy with page numbers
|-- final_report.md              # Readable report content and linked figures
|-- report_metadata.json         # Report details and benchmark SHA-256 digest
|-- REQUIREMENT_TRACEABILITY.md  # Requirements mapped to code and evidence
|-- QA_REPORT.md                 # Final regression, commands, and documentation checks
|-- SUBMISSION.md                # Archive contents and reproduction instructions
|-- diagrams/                    # Architecture and data-flow PNG and SVG figures
`-- validation/                  # Regression, demonstration, and layout evidence
```

The report includes two consecutive pages on hash-function selection and separate chaining, perfect/non-perfect hashing, heap design, CLI behavior, testing, and performance limitations. Optional author/instructor flags in the builder accept personal details without inserting fabricated names.

Start with the [implementation summary](SUMMARY.md), then read the [PDF](final_report.pdf), [Word document](final_report.docx), or [Markdown companion](final_report.md). Review [traceability](REQUIREMENT_TRACEABILITY.md), [QA](QA_REPORT.md), [validation evidence](validation/README.md), [diagrams](diagrams/README.md), and [submission instructions](SUBMISSION.md).

See [build tools](../tools/README.md) to regenerate documentation. The builder reads `results/performance_results.txt`; if that file changes, regenerate the report and PDF before packaging.

[Project overview](../README.md)
