"""Shared constants and paths, independent of the working directory."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATASET_PATH = DATA_DIR / "students.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
DOCS_DIR = PROJECT_ROOT / "docs"

DATASET_SIZE = 150
START_STUDENT_ID = 1001
MIN_PRIORITY = 1
MAX_PRIORITY = 100
HASH_TABLE_SIZE = 211
RANDOM_SEED = 42

CSV_FIELDS = ("student_id", "name", "program", "priority")
