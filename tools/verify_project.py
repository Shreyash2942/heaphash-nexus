"""Check final documentation, recorded regression, and documented CLI commands.

Requires the optional documentation dependencies. Does not rerun pytest or
overwrite the final benchmark; reads the recorded JUnit regression evidence.
"""

import ast
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET

from PIL import Image
import pymupdf


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/validation"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    metadata = json.loads((ROOT / "docs/report_metadata.json").read_text(encoding="utf-8"))
    benchmark_path = ROOT / metadata["benchmark"]["source"]
    benchmark_hash = digest(benchmark_path)
    require(benchmark_hash == metadata["benchmark"]["sha256"], "report benchmark is stale")
    settings = runpy.run_path(str(ROOT / "src/config/settings.py"))
    documented_configuration = {
        "DATASET_SIZE": 150, "START_STUDENT_ID": 1001, "MIN_PRIORITY": 1,
        "MAX_PRIORITY": 100, "HASH_TABLE_SIZE": 211, "RANDOM_SEED": 42,
        "BENCHMARK_WARMUP": 100, "BENCHMARK_REPETITIONS": 10000,
    }
    require(all(settings[key] == value for key, value in documented_configuration.items()),
            "configuration differs from final documentation")
    require([key for key, _ in settings["BENCHMARK_TARGETS"]] == [1001, 1025, 1075, 1125, 1150, 9999],
            "benchmark targets differ from documentation")
    with (ROOT / "data/students.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 150 and [int(row["student_id"]) for row in rows] == list(range(1001, 1151)),
            "supplied CSV count or IDs differ from documentation")
    require((min(int(row["priority"]) for row in rows), max(int(row["priority"]) for row in rows)) == (1, 99),
            "actual CSV priority range differs from documentation")
    xml = ET.parse(EVIDENCE / "test_results.xml")
    cases = xml.findall(".//testcase")
    require(len(cases) == metadata["test_count"] == 312, "unexpected regression count")
    require(not xml.findall(".//failure") and not xml.findall(".//error")
            and not xml.findall(".//skipped"), "regression did not completely pass")
    counts = Counter(case.get("classname").split(".")[1] for case in cases)
    require(counts == {"unit": 211, "integration": 101}, "test category counts differ")
    by_file = Counter(case.get("classname") for case in cases)
    require("Complete demonstration passed." in (EVIDENCE / "demo_output.txt").read_text(),
            "complete demonstration evidence is missing")

    pdf_path = ROOT / "docs/final_report.pdf"
    with pymupdf.open(pdf_path) as pdf:
        page_text = [page.get_text() for page in pdf]
        require(len(pdf) == 12, "unexpected PDF page count")
        require("Hash Function Selection" in page_text[3]
                and "Collision Resolution" in page_text[4]
                and "Perfect and Non-Perfect Hashing" in page_text[5], "hash explanation page layout differs")
        require("Correctness is independent" in page_text[4], "collision explanation overflowed")
        for row in metadata["benchmark"]["rows"]:
            require(all(value in page_text[9] for value in (row[0], row[5], row[6], row[7])),
                    f"PDF results differ for {row[0]}")
        require(metadata["benchmark"]["ratio"] in page_text[9], "PDF aggregate ratio differs")
        embedded_fonts = set()
        for page in pdf:
            used_fonts = {span["font"] for block in page.get_text("dict")["blocks"]
                          for line in block.get("lines", []) for span in line["spans"]}
            for font in page.get_fonts():
                # ReportLab also declares an unused standard Helvetica resource.
                # Require embedding for every font actually used to draw text.
                if font[3].split("+")[-1] in used_fonts:
                    require(bool(pdf.extract_font(font[0])[3]), "PDF uses an unembedded font")
                    embedded_fonts.add(font[3])
    word_layout = json.loads((EVIDENCE / "word_layout.json").read_text(encoding="utf-8-sig"))
    require(word_layout["docx_sha256"] == digest(ROOT / "docs/final_report.docx"), "Word check is stale")
    require((word_layout["hash_function_page"], word_layout["collision_resolution_page"],
             word_layout["hash_explanation_last_page"]) == (4, 5, 5), "Word hashing pages differ")
    report_layout = {
        "renderer": "ReportLab", "total_pages": 12,
        "hash_function_page": 4, "collision_resolution_page": 5,
        "hash_explanation_last_page": 5, "embedded_fonts": sorted(embedded_fonts),
        "pdf_sha256": digest(pdf_path), "docx_sha256": digest(ROOT / "docs/final_report.docx"),
        "paper": "US Letter; 1-inch margins; Times New Roman 12; 24-point body leading",
        "independent_word_check": "word_layout.json",
    }
    (EVIDENCE / "report_layout.json").write_text(json.dumps(report_layout, indent=2) + "\n", encoding="utf-8")

    roots = [ROOT / name for name in ("src", "tests", "docs", "data", "results", "tools")]
    maintained = [ROOT] + [folder for root in roots for folder in [root, *root.rglob("*")]
                           if folder.is_dir() and "__pycache__" not in folder.parts]
    for folder in maintained:
        require((folder / "README.md").is_file(), f"missing folder README: {folder}")
    readmes = [folder / "README.md" for folder in maintained]
    markdown_files = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md")),
                      *[path for path in readmes if not path.is_relative_to(ROOT / "docs") and path != ROOT / "README.md"]]
    links = 0
    link_targets = []
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            link_targets.append((path.parent / target.split("#")[0], path, target))
            links += 1

    code_files = [ROOT / "main.py"] + [p for name in ("src", "tests", "tools")
                                      for p in (ROOT / name).rglob("*.py")]
    for path in code_files:
        text = path.read_text(encoding="utf-8")
        if not path.is_relative_to(ROOT / "tools"):
            require(not re.search(r"\b(TODO|FIXME|HACK|NotImplementedError)\b", text), f"unfinished code: {path}")
        tree = ast.parse(text, filename=str(path))
        if path.name == "__init__.py":
            continue  # Public package re-exports are intentional.
        names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    local = alias.asname or (alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name)
                    if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                        continue
                    require(local in names, f"unused import: {path}: {local}")
    for name in ("project_architecture", "data_flow"):
        with Image.open(ROOT / f"docs/diagrams/{name}.png") as picture:
            require(picture.size == (1920, 1480), f"wrong diagram dimensions: {name}")
        require((ROOT / f"docs/diagrams/{name}.svg").is_file(), f"missing vector figure: {name}")

    dataset_hash = digest(ROOT / "data/students.csv")
    commands = []
    with TemporaryDirectory(prefix="heaphash-command-check-") as temporary:
        def run(arguments, input_text=None):
            completed = subprocess.run([sys.executable, *arguments], cwd=ROOT, input=input_text,
                                       capture_output=True, text=True, timeout=60)
            require(completed.returncode == 0, f"command failed: {arguments}: {completed.stderr}")
            commands.append({"arguments": arguments, "returncode": completed.returncode,
                             "output_tail": completed.stdout[-250:]})
            return completed.stdout
        output = str(Path(temporary) / "benchmark.txt")
        run(["-m", "src.dataset.data_generator"])
        run(["-m", "src.performance.benchmark", "--output", output])
        require(Path(output).is_file(), "benchmark command did not save output")
        run(["main.py", "--help"])
        demo = run(["main.py", "--demo", "--results", output])
        require("Complete demonstration passed." in demo, "README demonstration command failed")
        script = "invalid\n1\n5\n6\n2\n1001\n0\n2\n4\n5\n7\n0\n3\n1\n2\n0\n4\n1\n2\n3\n0\n6\n0\n"
        menu = run(["main.py", "--results", output], script)
        for expected in ("Choose one of:", "Collision demonstration passed.", "Heap is valid.",
                         "Dataset valid:", "Reset complete:", "Goodbye."):
            require(expected in menu, f"terminal walkthrough missed {expected}")
        (EVIDENCE / "menu_output.txt").write_text(menu, encoding="utf-8")
    require(digest(ROOT / "data/students.csv") == dataset_hash, "commands modified the source dataset")
    require(digest(benchmark_path) == benchmark_hash, "command checks replaced final measurements")
    for resolved, source, target in link_targets:
        require(resolved.exists() or resolved.resolve() == (EVIDENCE / "validation.json").resolve(),
                f"broken local link: {source}: {target}")
    git_checkout = (ROOT / ".git").exists()
    if git_checkout:
        for excluded in ("README.md", "IMPLEMENTATION_PLAN.md", "graphify-out", "submission"):
            outcome = subprocess.run(["git", "check-ignore", "--quiet", excluded], cwd=ROOT)
            require(outcome.returncode == 0, f"local artifact is not excluded: {excluded}")
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
        require(not any(name in ("README.md", "IMPLEMENTATION_PLAN.md") or name.startswith(("graphify-out/", ".graphify", "submission/")) for name in tracked),
                "a local-only artifact is tracked")
    result = {
        "passed": True, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(),
        "test_total": len(cases), "test_categories": dict(counts), "tests_by_module": dict(by_file),
        "folder_readmes": len(readmes), "local_links_checked": links,
        "python_files_audited": len(code_files), "commands": commands,
        "documented_configuration": documented_configuration,
        "dataset_sha256": dataset_hash, "benchmark_sha256": benchmark_hash,
        "pdf_sha256": digest(pdf_path), "docx_sha256": digest(ROOT / "docs/final_report.docx"),
        "final_measurements_preserved": True, "git_checkout_checked": git_checkout,
        "local_artifacts_excluded_from_git": True if git_checkout else None,
        "no_push_performed": True,
    }
    (EVIDENCE / "validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    require(all(resolved.exists() for resolved, _, _ in link_targets), "a generated evidence link is missing")
    print(f"Validation passed: {len(cases)} recorded passing tests; {len(readmes)} folder guides; {links} local links; {len(commands)} command checks.")


if __name__ == "__main__":
    main()
