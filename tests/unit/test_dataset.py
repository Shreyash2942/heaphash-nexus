"""Day 1 quality gates and invalid-input regressions for the shared dataset."""

import csv
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import random
import subprocess
import sys

import pytest

from src.config.settings import (
    CSV_FIELDS, DATASET_PATH, DATASET_SIZE, MAX_PRIORITY, MIN_PRIORITY,
    PROJECT_ROOT, RANDOM_SEED, START_STUDENT_ID,
)
from src.dataset.data_generator import (
    FIRST_NAMES, LAST_NAMES, PROGRAMS, generate_students, write_dataset,
)
from src.dataset.data_loader import load_dataset, load_or_generate_dataset
from src.dataset.validator import validate_dataset, validate_student
from src.models.data_item import DataItem


def write_csv(tmp_path: Path, text: str) -> Path:
    """Create a deliberately small or malformed input fixture."""
    path = tmp_path / "input.csv"
    path.write_text(text, encoding="utf-8")
    return path


def test_default_generation_meets_quality_gate():
    records = generate_students()
    validate_dataset(records, expected_size=DATASET_SIZE)
    assert len(records) == 150
    assert [record.student_id for record in records] == list(range(1001, 1151))
    assert len({record.student_id for record in records}) == DATASET_SIZE
    assert all(isinstance(record, DataItem) for record in records)
    assert all(MIN_PRIORITY <= record.priority <= MAX_PRIORITY for record in records)
    for record in records:
        first, last = record.name.split()
        assert first in FIRST_NAMES
        assert last in LAST_NAMES
        assert record.program in PROGRAMS


def test_generation_is_reproducible_and_seed_can_vary():
    assert generate_students() == generate_students(seed=RANDOM_SEED)
    assert generate_students(seed=RANDOM_SEED + 1) != generate_students()


def test_generation_does_not_change_global_random_state():
    state = random.getstate()
    generate_students()
    assert random.getstate() == state


def test_custom_dataset_size_and_start_id():
    records = generate_students(size=3, start_student_id=2001)
    assert [record.student_id for record in records] == [2001, 2002, 2003]


@pytest.mark.parametrize("arguments", [
    {"size": 0}, {"size": -1}, {"size": True}, {"size": 1.5},
    {"size": "150"}, {"seed": None}, {"seed": True}, {"seed": "42"},
    {"start_student_id": 0}, {"start_student_id": -1},
    {"start_student_id": True}, {"start_student_id": 1001.5},
])
def test_generator_rejects_invalid_arguments(arguments):
    with pytest.raises(ValueError):
        generate_students(**arguments)


def test_record_value_equality_and_immutability():
    record = DataItem(1001, "Alex Smith", "Computer Science", 50)
    assert record == DataItem(1001, "Alex Smith", "Computer Science", 50)
    with pytest.raises(FrozenInstanceError):
        record.priority = 100


@pytest.mark.parametrize("field,value,message", [
    ("student_id", 0, "student_id"), ("student_id", -1, "student_id"),
    ("student_id", True, "student_id"), ("student_id", "1001", "student_id"),
    ("student_id", 1001.5, "student_id"),
    ("name", "", "name"), ("name", "  ", "name"), ("name", None, "name"),
    ("program", "", "program"), ("program", "\t", "program"),
    ("program", 42, "program"),
    ("priority", 0, "priority"), ("priority", 101, "priority"),
    ("priority", True, "priority"), ("priority", "50", "priority"),
    ("priority", 1.5, "priority"),
])
def test_validator_rejects_invalid_fields(field, value, message):
    record = replace(generate_students(size=1)[0], **{field: value})
    with pytest.raises(ValueError, match=message):
        validate_student(record)
    with pytest.raises(ValueError, match=f"record 1:.*{message}"):
        validate_dataset([record])


def test_validator_rejects_non_record_values():
    with pytest.raises(ValueError, match="DataItem"):
        validate_dataset(["not a student"])


def test_validator_rejects_duplicate_ids():
    record = generate_students(size=1)[0]
    with pytest.raises(ValueError, match="duplicate student_id 1001"):
        validate_dataset([record, replace(record, name="Another Student")])


def test_equal_priorities_and_boundary_priorities_are_valid():
    records = [
        DataItem(1001, "Student One", "Computer Science", MIN_PRIORITY),
        DataItem(1002, "Student Two", "Computer Science", MAX_PRIORITY),
        DataItem(1003, "Student Three", "Computer Science", MAX_PRIORITY),
    ]
    validate_dataset(records)


def test_validator_rejects_empty_or_wrong_size_dataset():
    with pytest.raises(ValueError, match="at least one"):
        validate_dataset([])
    with pytest.raises(ValueError, match="expected 150 records, found 3"):
        validate_dataset(generate_students(size=3), expected_size=DATASET_SIZE)


@pytest.mark.parametrize("size", [0, -1, True, 1.5, "150"])
def test_validator_rejects_invalid_expected_size(size):
    with pytest.raises(ValueError, match="expected_size"):
        validate_dataset(generate_students(size=1), expected_size=size)


def test_csv_round_trip_and_reproducible_bytes(tmp_path):
    first = write_dataset(tmp_path / "first.csv")
    second = write_dataset(tmp_path / "second.csv")
    assert first.read_bytes() == second.read_bytes()
    assert load_dataset(first) == generate_students()
    with first.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream)
        assert next(reader) == list(CSV_FIELDS)
        assert len(list(reader)) == DATASET_SIZE


def test_writer_creates_parent_directories(tmp_path):
    path = write_dataset(tmp_path / "nested" / "data" / "students.csv")
    assert len(load_dataset(path)) == DATASET_SIZE


def test_csv_round_trip_preserves_quoted_and_unicode_text(tmp_path):
    records = [DataItem(1001, 'Renée "Rae", Smith', "Arts, Media\nand Design", 50)]
    path = write_dataset(tmp_path / "quoted.csv", records)
    assert load_dataset(path, expected_size=None) == records


def test_loader_accepts_bom_reordered_columns_and_trims_text(tmp_path):
    path = write_csv(tmp_path,
        '\ufeffpriority,program,name,student_id\n1, Computer Science , Alex Smith ,1001\n'
    )
    assert load_dataset(path, expected_size=None) == [
        DataItem(1001, "Alex Smith", "Computer Science", 1)
    ]


@pytest.mark.parametrize("header", [
    "", "student_id,name,program\n", "student_id,name,program,priority,extra\n",
    "student_id,name,name,priority\n", "id,name,program,priority\n",
])
def test_loader_rejects_missing_or_invalid_header(tmp_path, header):
    with pytest.raises(ValueError, match="CSV header"):
        load_dataset(write_csv(tmp_path, header), expected_size=None)


@pytest.mark.parametrize("row,message", [
    ("1001,Alex Smith,Computer Science\n", "wrong number of fields"),
    ("1001,Alex Smith,Computer Science,50,extra\n", "wrong number of fields"),
    ("invalid,Alex Smith,Computer Science,50\n", "student_id"),
    ("1001.5,Alex Smith,Computer Science,50\n", "student_id"),
    ("0,Alex Smith,Computer Science,50\n", "student_id"),
    ("1001,   ,Computer Science,50\n", "name"),
    ("1001,Alex Smith,  ,50\n", "program"),
    ("1001,Alex Smith,Computer Science,high\n", "priority"),
    ("1001,Alex Smith,Computer Science,1.5\n", "priority"),
    ("1001,Alex Smith,Computer Science,0\n", "priority"),
    ("1001,Alex Smith,Computer Science,101\n", "priority"),
    ('1001,"Unclosed name,Computer Science,50\n', "malformed CSV"),
])
def test_loader_rejects_bad_rows_with_line_context(tmp_path, row, message):
    path = write_csv(tmp_path, ",".join(CSV_FIELDS) + "\n" + row)
    with pytest.raises(ValueError, match=f"line 2:.*{message}"):
        load_dataset(path, expected_size=None)


def test_loader_rejects_duplicate_ids_with_line_context(tmp_path):
    path = write_csv(tmp_path,
        "student_id,name,program,priority\n"
        "1001,Alex Smith,Computer Science,50\n"
        "1001,Jamie Lee,Accounting,90\n"
    )
    with pytest.raises(ValueError, match="line 3: duplicate student_id 1001"):
        load_dataset(path, expected_size=None)


def test_loader_rejects_header_only_and_incomplete_project_dataset(tmp_path):
    with pytest.raises(ValueError, match="at least one"):
        load_dataset(write_csv(tmp_path, ",".join(CSV_FIELDS) + "\n"), expected_size=None)
    path = write_dataset(tmp_path / "small.csv", generate_students(size=3))
    with pytest.raises(ValueError, match="expected 150 records, found 3"):
        load_dataset(path)


def test_loader_reports_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_dataset(tmp_path / "missing.csv")


def test_loader_reports_invalid_encoding(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_bytes(b"student_id,name,program,priority\n1001,\xff,CS,50\n")
    with pytest.raises(ValueError, match="malformed CSV"):
        load_dataset(path, expected_size=None)


def test_writer_requires_explicit_overwrite(tmp_path):
    path = write_dataset(tmp_path / "students.csv")
    original = path.read_bytes()
    with pytest.raises(FileExistsError):
        write_dataset(path, generate_students(seed=1))
    assert path.read_bytes() == original
    replacement = generate_students(seed=1)
    write_dataset(path, replacement, overwrite=True)
    assert load_dataset(path) == replacement


def test_writer_validates_before_touching_existing_file(tmp_path):
    path = write_dataset(tmp_path / "students.csv")
    original = path.read_bytes()
    with pytest.raises(ValueError, match="duplicate"):
        write_dataset(path, [generate_students()[0]] * 2, overwrite=True)
    assert path.read_bytes() == original


def test_load_or_generate_creates_missing_and_preserves_existing_dataset(tmp_path):
    path = tmp_path / "students.csv"
    assert load_or_generate_dataset(path) == generate_students()
    custom = generate_students(seed=7)
    write_dataset(path, custom, overwrite=True)
    original = path.read_bytes()
    assert load_or_generate_dataset(path) == custom
    assert path.read_bytes() == original


def test_load_or_generate_does_not_replace_invalid_existing_file(tmp_path):
    path = write_csv(tmp_path, "invalid dataset\n")
    original = path.read_bytes()
    with pytest.raises(ValueError):
        load_or_generate_dataset(path)
    assert path.read_bytes() == original


def test_project_dataset_matches_default_generation_from_any_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    records = load_dataset()
    assert DATASET_PATH.is_absolute()
    assert len(records) == DATASET_SIZE
    assert records == generate_students()
    assert records[0].student_id == START_STUDENT_ID
    assert records[-1].student_id == START_STUDENT_ID + DATASET_SIZE - 1


def test_generator_command_preserves_existing_and_overwrites_only_when_requested(tmp_path):
    path = tmp_path / "students.csv"
    command = [sys.executable, "-m", "src.dataset.data_generator", "--output", str(path)]
    created = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True)
    assert created.returncode == 0, created.stderr
    assert len(load_dataset(path)) == DATASET_SIZE

    custom = generate_students(seed=9)
    write_dataset(path, custom, overwrite=True)
    preserved = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True)
    assert preserved.returncode == 0, preserved.stderr
    assert "Preserved" in preserved.stdout
    assert load_dataset(path) == custom

    overwritten = subprocess.run(
        command + ["--overwrite"], cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    assert overwritten.returncode == 0, overwritten.stderr
    assert load_dataset(path) == generate_students()


def test_generator_command_reports_invalid_existing_dataset(tmp_path):
    path = write_csv(tmp_path, "invalid dataset\n")
    result = subprocess.run(
        [sys.executable, "-m", "src.dataset.data_generator", "--output", str(path)],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert "Dataset error:" in result.stderr
    assert "Traceback" not in result.stderr
    assert path.read_text() == "invalid dataset\n"
