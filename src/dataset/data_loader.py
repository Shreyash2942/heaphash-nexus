"""Load a validated CSV dataset as shared DataItem records."""

import csv
from pathlib import Path

from src.config.settings import CSV_FIELDS, DATASET_PATH, DATASET_SIZE
from src.dataset.validator import validate_dataset, validate_student
from src.models.data_item import DataItem


def load_dataset(
    path: str | Path = DATASET_PATH,
    expected_size: int | None = DATASET_SIZE,
) -> list[DataItem]:
    """Load CSV records, rejecting malformed rows and duplicate student IDs.

    The project dataset must contain 150 records by default. Use
    ``expected_size=None`` for smaller demonstrations. Errors include the
    path and CSV line number where possible. This function never writes.
    """
    source = Path(path)
    records: list[DataItem] = []
    seen_ids: set[int] = set()
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        try:
            fields = reader.fieldnames
            if (
                fields is None
                or len(fields) != len(CSV_FIELDS)
                or set(fields) != set(CSV_FIELDS)
            ):
                raise ValueError(
                    f"{source}: CSV header must contain exactly "
                    + ", ".join(CSV_FIELDS)
                )

            for row in reader:
                line = reader.line_num
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f"{source}: line {line}: wrong number of fields")
                try:
                    student_id = int(row["student_id"])
                except ValueError as error:
                    raise ValueError(
                        f"{source}: line {line}: student_id must be an integer"
                    ) from error
                try:
                    priority = int(row["priority"])
                except ValueError as error:
                    raise ValueError(
                        f"{source}: line {line}: priority must be an integer"
                    ) from error
                student = DataItem(
                    student_id=student_id,
                    name=row["name"].strip(),
                    program=row["program"].strip(),
                    priority=priority,
                )
                try:
                    validate_student(student)
                except ValueError as error:
                    raise ValueError(f"{source}: line {line}: {error}") from error
                if student.student_id in seen_ids:
                    raise ValueError(
                        f"{source}: line {line}: duplicate student_id "
                        f"{student.student_id}"
                    )
                seen_ids.add(student.student_id)
                records.append(student)
        except (csv.Error, UnicodeError) as error:
            raise ValueError(
                f"{source}: line {reader.line_num}: malformed CSV: {error}"
            ) from error

    try:
        validate_dataset(records, expected_size=expected_size)
    except ValueError as error:
        raise ValueError(f"{source}: {error}") from error
    return records


def load_or_generate_dataset(path: str | Path = DATASET_PATH) -> list[DataItem]:
    """Load an existing project dataset or generate it when absent.

    Invalid existing data is reported rather than silently replaced.
    Interactive features should modify the returned collection only.
    """
    from src.dataset.data_generator import write_dataset

    source = Path(path)
    if not source.exists():
        write_dataset(source)
    return load_dataset(source)
