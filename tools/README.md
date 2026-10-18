# Documentation and Submission Tools

These optional tools create submission artifacts; the application itself uses only the Python standard library.

```text
tools/
|-- README.md          # Tool usage and optional dependencies
`-- build_diagrams.py  # Rebuild editable SVG and 300-dpi PNG project diagrams
```

From the project root, install `python -m pip install -r requirements-docs.txt` and run `python tools/build_diagrams.py` to rebuild the architecture and data-flow figures.

[Project overview](../README.md)
