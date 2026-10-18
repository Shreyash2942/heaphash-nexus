"""Build a clean local project ZIP with a SHA-256 payload manifest.

Optional --verify extracts the new archive into an isolated temporary directory,
checks every payload hash, runs its full test suite and complete demonstration,
and records evidence outside the archive. No Git operations or network access.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "submission"
ARCHIVE = OUTPUT / "heaphash-nexus-submission.zip"
PREFIX = "heaphash-nexus/"
IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".git", ".venv", "venv", "submission"}


def digest_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def payload_files():
    files = [ROOT / name for name in (
        "README.md", "main.py", "requirements.txt", "requirements-docs.txt", "pytest.ini", ".gitignore",
        "data/README.md", "data/students.csv", "results/README.md", "results/performance_results.txt",
    )]
    for name in ("src", "tests", "docs", "tools"):
        files.extend((ROOT / name).rglob("*"))
    selected = []
    for path in files:
        relative = path.relative_to(ROOT)
        if not path.is_file() or any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if path.name.startswith("~$") or path.name == ".gitkeep" or path.suffix in (".pyc", ".pyo", ".tmp"):
            continue
        require(not path.is_symlink(), f"refusing a symlink in submission: {relative}")
        selected.append(path)
    return sorted(set(selected), key=lambda path: path.relative_to(ROOT).as_posix())


def build():
    required = ["README.md", "data/students.csv", "results/performance_results.txt", "docs/final_report.docx",
                "docs/final_report.pdf", "docs/final_report.md", "docs/REQUIREMENT_TRACEABILITY.md",
                "docs/QA_REPORT.md", "docs/SUBMISSION.md", "docs/validation/validation.json",
                "docs/validation/test_results.xml", "docs/validation/demo_output.txt"]
    require(all((ROOT / name).is_file() for name in required), "a required deliverable is missing")
    metadata = json.loads((ROOT / "docs/report_metadata.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "docs/validation/validation.json").read_text(encoding="utf-8"))
    layout = json.loads((ROOT / "docs/validation/report_layout.json").read_text(encoding="utf-8"))
    benchmark_hash = digest_bytes((ROOT / "results/performance_results.txt").read_bytes())
    require(metadata["benchmark"]["sha256"] == validation["benchmark_sha256"] == benchmark_hash,
            "benchmark, report, and final QA evidence differ")
    require(validation["passed"] and validation["test_total"] == 312, "final QA did not pass")
    for suffix in ("pdf", "docx"):
        actual = digest_bytes((ROOT / f"docs/final_report.{suffix}").read_bytes())
        require(actual == layout[f"{suffix}_sha256"] == validation[f"{suffix}_sha256"],
                f"{suffix} layout or QA evidence is stale")
    OUTPUT.mkdir(exist_ok=True)
    files = payload_files()
    require(all((ROOT / name) in files for name in required), "required content was excluded")
    manifest = {
        "project": "HeapHash Nexus", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "algorithm": "SHA-256", "files": {},
    }
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            content = path.read_bytes()
            archive.writestr(PREFIX + relative, content)
            manifest["files"][relative] = {"bytes": len(content), "sha256": digest_bytes(content)}
        archive.writestr(PREFIX + "SUBMISSION_MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
    checksum = digest_bytes(ARCHIVE.read_bytes())
    ARCHIVE.with_suffix(".zip.sha256").write_text(f"{checksum}  {ARCHIVE.name}\n", encoding="ascii")
    print(f"Created {ARCHIVE} ({len(files)} payload files; {ARCHIVE.stat().st_size:,} bytes)")
    print(f"SHA-256: {checksum}")
    return checksum


def verify(checksum):
    with ZipFile(ARCHIVE) as archive:
        require(archive.testzip() is None, "archive CRC integrity failed")
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate archive members")
        for name in names:
            require(name.startswith(PREFIX) and ".." not in Path(name).parts and "\\" not in name,
                    f"unsafe archive member: {name}")
            relative = Path(name.removeprefix(PREFIX))
            require(not any(part in IGNORED_PARTS for part in relative.parts), f"unwanted directory: {name}")
            require(relative.name != "IMPLEMENTATION_PLAN.md"
                    and not any(part.startswith(("graphify", ".graphify")) for part in relative.parts),
                    f"local-only artifact was included: {name}")
        manifest = json.loads(archive.read(PREFIX + "SUBMISSION_MANIFEST.json"))
        require(set(names) == {PREFIX + name for name in manifest["files"]} | {PREFIX + "SUBMISSION_MANIFEST.json"},
                "archive and manifest member lists differ")
        for name, properties in manifest["files"].items():
            content = archive.read(PREFIX + name)
            require(len(content) == properties["bytes"] and digest_bytes(content) == properties["sha256"],
                    f"manifest verification failed: {name}")
        with TemporaryDirectory(prefix="heaphash-submission-check-") as temporary:
            archive.extractall(temporary)
            project = Path(temporary) / PREFIX.rstrip("/")
            before = digest_bytes((project / "results/performance_results.txt").read_bytes())
            regression = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=project,
                                        capture_output=True, text=True, timeout=60)
            (OUTPUT / "packaged_pytest.txt").write_text(regression.stdout + regression.stderr, encoding="utf-8")
            require(regression.returncode == 0 and "312 passed" in regression.stdout, "extracted-package regression failed")
            demonstration = subprocess.run([sys.executable, "main.py", "--demo", "--results", str(Path(temporary) / "demo.txt")],
                                           cwd=project, capture_output=True, text=True, timeout=60)
            (OUTPUT / "packaged_demo.txt").write_text(demonstration.stdout + demonstration.stderr, encoding="utf-8")
            require(demonstration.returncode == 0 and "Complete demonstration passed." in demonstration.stdout,
                    "extracted-package demonstration failed")
            require(digest_bytes((project / "results/performance_results.txt").read_bytes()) == before,
                    "package checks overwrote submitted measurements")
    result = {
        "passed": True, "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "archive": ARCHIVE.name, "archive_sha256": checksum,
        "payload_files": len(manifest["files"]), "manifest_verified": True, "crc_integrity_passed": True,
        "regression_tests_passed": 312, "complete_demonstration_passed": True,
        "submitted_measurements_preserved": True, "local_only_artifacts_excluded": True,
        "environment": "Current Python environment with project test dependencies already installed",
    }
    (OUTPUT / "VALIDATION.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Extracted-package verification passed: all payload hashes, 312 tests, and complete demonstration.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="verify payload and execute the extracted application and tests")
    arguments = parser.parse_args()
    archive_hash = build()
    if arguments.verify:
        verify(archive_hash)
