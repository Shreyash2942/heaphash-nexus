# Project Diagrams

These figures document the completed application. PNG versions are suitable for the APA report; SVG versions preserve editable vector geometry and text.

```text
diagrams/
|-- README.md                 # Figure contents and regeneration instructions
|-- .gitkeep                  # Original directory marker
|-- project_architecture.png  # Runtime layers, shared foundations, and module responsibilities
|-- project_architecture.svg  # Editable vector version of the architecture figure
|-- data_flow.png             # CSV validation, independent state, benchmark, and outputs
`-- data_flow.svg             # Editable vector version of the data-flow figure
```

`project_architecture.png` shows the entry point, CLI, application state, dataset package, custom structures, and performance package. Shared configuration and the immutable model support those workflows. The performance workflow calls the hash-table API and manual linear-search baseline.

`data_flow.png` shows validated records feeding independent editable structures and a separate benchmark. Interactive changes stay in memory; reset reloads the source CSV. Benchmark output is saved separately from student data.

Rebuild from the project root with `python tools/build_diagrams.py` after installing the optional `requirements-docs.txt` dependencies. Images are 1920 by 1480 pixels with 300-dpi metadata. See [build tools](../../tools/README.md).

[Project documentation](../README.md)
