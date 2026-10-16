"""Day 4 checks of shared records and independent data-structure state."""

from dataclasses import replace

import pytest

from src.config.settings import DATASET_SIZE, HASH_TABLE_SIZE


def test_both_structures_contain_all_150_shared_records(records, structures):
    table, queue = structures
    assert len(records) == len(table) == len(queue) == DATASET_SIZE == 150
    assert table.table_size == HASH_TABLE_SIZE
    assert queue.validate_heap()
    assert queue.peek().priority == max(student.priority for student in records)
    for student in records:
        assert table.search(student.student_id) is student
        assert queue.search(student.student_id) is student


@pytest.mark.parametrize("student_id", [1001, 1075, 1150, 9999])
def test_representative_and_missing_searches_match_without_mutating(student_id, records, structures):
    table, queue = structures
    before = table.buckets, queue.heap
    expected = next((student for student in records if student.student_id == student_id), None)
    assert table.search(student_id) is expected
    assert queue.search(student_id) is expected
    assert (table.buckets, queue.heap) == before


@pytest.mark.parametrize("student_id", [1001, 1075, 1150])
@pytest.mark.parametrize("changed_structure", ["table", "queue"])
def test_deletion_from_one_structure_preserves_the_other(student_id, changed_structure, records, structures):
    table, queue = structures
    expected = next(student for student in records if student.student_id == student_id)
    changed, unchanged = (table, queue) if changed_structure == "table" else (queue, table)
    original_other_state = queue.heap if changed_structure == "table" else table.buckets
    assert changed.delete(student_id) is True
    assert changed.search(student_id) is None
    assert changed.delete(student_id) is False
    assert unchanged.search(student_id) is expected
    assert len(changed) == DATASET_SIZE - 1
    assert len(unchanged) == DATASET_SIZE
    assert (queue.heap if changed_structure == "table" else table.buckets) == original_other_state
    for student in records:
        if student.student_id != student_id:
            assert table.search(student.student_id) is student
            assert queue.search(student.student_id) is student
    assert queue.validate_heap()


def test_sequential_deletions_from_both_structures_keep_remaining_records(records, structures):
    table, queue = structures
    removed = (1001, 1075, 1150)
    for position, student_id in enumerate(removed, start=1):
        assert table.delete(student_id)
        assert queue.delete(student_id)
        assert len(table) == len(queue) == DATASET_SIZE - position
        assert queue.validate_heap()
    for student in records:
        if student.student_id in removed:
            assert table.search(student.student_id) is queue.search(student.student_id) is None
        else:
            assert table.search(student.student_id) is queue.search(student.student_id) is student


def test_hash_duplicate_update_does_not_replace_the_queued_record(records, structures):
    table, queue = structures
    original = next(student for student in records if student.student_id == 1075)
    replacement = replace(original, name="Updated Student", priority=100)
    before_heap = queue.heap
    table.insert(original.student_id, replacement)
    assert table.search(original.student_id) is replacement
    assert queue.search(original.student_id) is original
    assert queue.heap == before_heap
    assert len(table) == len(queue) == DATASET_SIZE


def test_queue_extraction_leaves_hash_table_and_loaded_records_intact(records, structures):
    table, queue = structures
    before_buckets = table.buckets
    removed = queue.peek()
    assert queue.extract_max() is removed
    assert queue.search(removed.student_id) is None
    assert table.search(removed.student_id) is removed
    assert table.buckets == before_buckets
    assert removed in records
    assert len(table) == DATASET_SIZE and len(queue) == DATASET_SIZE - 1
    assert queue.validate_heap()


def test_missing_deletion_changes_neither_structure(structures):
    table, queue = structures
    before = table.buckets, queue.heap
    assert table.delete(9999) is False
    assert queue.delete(9999) is False
    assert (table.buckets, queue.heap) == before
    assert len(table) == len(queue) == DATASET_SIZE
