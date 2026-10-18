# Final Submission Package

Build the local archive from the project root:

```powershell
python tools/build_submission.py
```

The output is `submission/heaphash-nexus-submission.zip`, with `heaphash-nexus/` as its single top-level directory. The companion `.sha256` file verifies the archive. The archive's `SUBMISSION_MANIFEST.json` records the size and SHA-256 digest of every payload file. The builder refuses missing deliverables, mismatched benchmark/report sources, or stale report layout evidence.

Use `python tools/build_submission.py --verify` to also check archive integrity and every manifest hash, extract into a temporary directory, run its full regression suite and complete demonstration, and write local package-validation evidence. This was the final packaging command used for submission. It uses the current Python environment, where test dependencies must already be installed.

Included content:

- Published root README, complete [project guide](../guide.md), [implementation summary](SUMMARY.md), entry point, dependencies and pytest configuration.
- All implementation packages, 150-record CSV, tests and per-folder READMEs.
- Saved final benchmark and methodology.
- APA PDF and editable Word report, Markdown companion, metadata, diagrams, traceability, and QA evidence.
- Reproducible documentation and packaging tools.

Excluded content includes `.git`, virtual environments, Python caches, pytest caches, editor files, Office lock files, graphify artifacts, the original implementation plan, generated submission directories, and temporary experiment results. The archive includes only the required dataset and final performance report from those two folders.

Extract the ZIP into a new directory, open its `heaphash-nexus/` folder, and run:

```powershell
python -m pip install -r requirements.txt
python -m pytest -v
python main.py
python main.py --demo --results results/reviewer_demo.txt
```

Using a separate demonstration-results path preserves the submitted benchmark and its match with the academic report. To rerun the standalone benchmark while preserving it, use `python -m src.performance.benchmark --output results/reviewer_benchmark.txt`.

The final extracted-package checks are recorded locally in `submission/VALIDATION.json`, with pytest and demonstration transcripts. The generated archive and graphify artifacts remain Git-ignored. The root README, guide, and implementation summary are versioned project documentation. The obsolete development plan has been removed. Packaging itself does not push to GitHub; publication is a separate Git operation.

The title page omits author/instructor names that were not provided. To personalize it, regenerate using `python tools/build_report.py --author "Full Name" --instructor "Instructor Name"`, regenerate the PDF, check Word pagination, refresh QA evidence, and rebuild the archive. The submission date is October 18, 2026.

[Documentation guide](README.md)
