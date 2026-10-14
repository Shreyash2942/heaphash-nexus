"""Day 2 operation, collision, statistics, and full-dataset quality gates."""

from dataclasses import replace
import random

import pytest

from src.config.settings import DATASET_PATH, DATASET_SIZE, HASH_TABLE_SIZE
from src.data_structures.hash_table import HashTable
from src.data_structures.hash_table.helpers.hash_function import hash_function
from src.dataset.data_loader import load_dataset
from src.models.data_item import DataItem


def student(student_id: int) -> DataItem:
    return DataItem(student_id, f"Student {student_id}", "Computer Science", 50)


def test_new_table_uses_configured_size_and_starts_empty():
    table = HashTable()
    assert table.table_size == HASH_TABLE_SIZE == 211
    assert len(table.buckets) == HASH_TABLE_SIZE
    assert all(bucket == () for bucket in table.buckets)
    assert table.item_count == len(table) == 0
    assert table.load_factor == 0.0
    assert table.search(1001) is None
    assert table.delete(1001) is False
    assert table.item_count == 0


@pytest.mark.parametrize("key,size,expected", [
    (1001, 10, 1), (1011, 10, 1), (1021, 10, 1),
    (0, 10, 0), (-1, 10, 9), (-21, 10, 9),
    (1001, 1, 0), (10**100, 10, 0), (1001, 211, 157),
])
def test_modulo_hash_function(key, size, expected):
    assert hash_function(key, size) == expected


def test_hash_helper_uses_configured_default_size():
    assert hash_function(1001) == 1001 % HASH_TABLE_SIZE


@pytest.mark.parametrize("size", [0, -1, -211])
def test_non_positive_size_is_rejected(size):
    with pytest.raises(ValueError, match="table_size must be positive"):
        HashTable(size)
    with pytest.raises(ValueError, match="table_size must be positive"):
        hash_function(1001, size)


@pytest.mark.parametrize("size", [True, False, 10.0, "10", None])
def test_non_integer_size_is_rejected(size):
    with pytest.raises(TypeError, match="table_size must be an integer"):
        HashTable(size)
    with pytest.raises(TypeError, match="table_size must be an integer"):
        hash_function(1001, size)


@pytest.mark.parametrize("key", [True, False, 1001.0, "1001", None, [], {}])
def test_invalid_keys_are_rejected_without_changing_state(key):
    table = HashTable(10)
    table.insert(1001, student(1001))
    before = table.buckets
    with pytest.raises(TypeError, match="key must be an integer"):
        hash_function(key, 10)
    for operation in (
        lambda: table.insert(key, student(1002)),
        lambda: table.search(key),
        lambda: table.delete(key),
    ):
        with pytest.raises(TypeError, match="key must be an integer"):
            operation()
        assert table.buckets == before
        assert table.item_count == 1


def test_insert_and_search_return_the_stored_student():
    table = HashTable[DataItem]()
    record = student(1001)
    assert table.insert(record.student_id, record) is None
    assert table.search(1001) is record
    assert table.item_count == len(table) == 1
    assert table.load_factor == pytest.approx(1 / HASH_TABLE_SIZE)
    assert table.search(9999) is None


def test_distinct_buckets_do_not_share_chain_storage():
    table = HashTable(10)
    table.insert(1001, "first")
    table.insert(1002, "second")
    assert table.buckets[1] == ((1001, "first"),)
    assert table.buckets[2] == ((1002, "second"),)
    assert table.statistics()["occupied_buckets"] == 2


def test_required_collision_demonstration_preserves_remaining_records():
    table = HashTable[DataItem](10)
    records = [student(key) for key in (1001, 1011, 1021)]
    for record in records:
        table.insert(record.student_id, record)
    assert table.buckets[1] == tuple((record.student_id, record) for record in records)
    assert all(table.search(record.student_id) is record for record in records)
    assert table.statistics()["collision_count"] == 2
    assert table.delete(1011) is True
    assert table.search(1011) is None
    assert table.search(1001) is records[0]
    assert table.search(1021) is records[2]
    assert table.item_count == len(table) == 2
    assert table.statistics()["collision_count"] == 1


@pytest.mark.parametrize("key", [1001, 1011, 1021])
def test_duplicate_key_updates_each_position_in_a_collision_chain(key):
    table = HashTable[DataItem](10)
    for original_key in (1001, 1011, 1021):
        table.insert(original_key, student(original_key))
    replacement = replace(student(key), name="Updated Student", priority=100)
    original_statistics = table.statistics()
    table.insert(key, replacement)
    table.insert(key, replacement)
    assert table.search(key) is replacement
    assert table.item_count == 3
    assert len(table.buckets[1]) == 3
    assert table.statistics() == original_statistics
    for other_key in (1001, 1011, 1021):
        if other_key != key:
            assert table.search(other_key) == student(other_key)


@pytest.mark.parametrize("key", [1001, 1011, 1021])
def test_delete_first_middle_or_last_collision_preserves_other_entries(key):
    table = HashTable(10)
    keys = (1001, 1011, 1021)
    for original_key in keys:
        table.insert(original_key, str(original_key))
    assert table.delete(key) is True
    assert table.delete(key) is False
    assert table.search(key) is None
    assert len(table) == 2
    for remaining_key in keys:
        if remaining_key != key:
            assert table.search(remaining_key) == str(remaining_key)


def test_missing_key_in_an_occupied_bucket_does_not_change_state():
    table = HashTable(10)
    for key in (1001, 1011, 1021):
        table.insert(key, key)
    before = table.buckets
    assert table.search(1031) is None
    assert table.delete(1031) is False
    assert table.buckets == before
    assert table.item_count == 3


def test_delete_then_reinsert_reuses_key_without_stale_entries():
    table = HashTable(10)
    table.insert(1001, "original")
    assert table.delete(1001) is True
    assert table.item_count == 0
    assert table.buckets[1] == ()
    table.insert(1001, "replacement")
    assert table.search(1001) == "replacement"
    assert table.item_count == 1
    assert table.buckets[1] == ((1001, "replacement"),)


def test_general_integer_keys_and_none_values_are_supported():
    table = HashTable(10)
    for key in (0, -10, 10**100):
        table.insert(key, None)
    assert table.item_count == 3
    for key in (0, -10, 10**100):
        assert table.search(key) is None
        assert table.delete(key) is True
        assert table.delete(key) is False
    assert table.item_count == 0


def test_statistics_describe_current_occupancy_after_updates_and_deletions():
    table = HashTable(10)
    assert table.statistics() == {
        "table_size": 10, "item_count": 0, "load_factor": 0.0,
        "occupied_buckets": 0, "empty_buckets": 10,
        "collision_count": 0, "max_chain_length": 0,
    }
    for key in (1001, 1011, 1021, 1002):
        table.insert(key, key)
    assert table.statistics() == {
        "table_size": 10, "item_count": 4, "load_factor": 0.4,
        "occupied_buckets": 2, "empty_buckets": 8,
        "collision_count": 2, "max_chain_length": 3,
    }
    table.insert(1011, "updated")
    assert table.statistics()["collision_count"] == 2
    table.delete(1002)
    assert table.statistics()["occupied_buckets"] == 1
    for key in (1001, 1011, 1021):
        table.delete(key)
    assert table.statistics()["max_chain_length"] == 0
    assert table.statistics()["empty_buckets"] == 10
    assert table.statistics()["collision_count"] == 0
    assert table.load_factor == 0.0


def test_bucket_and_statistics_snapshots_cannot_change_table_structure():
    table = HashTable(10)
    table.insert(1001, "original")
    buckets = table.buckets
    statistics = table.statistics()
    with pytest.raises(TypeError):
        buckets[1][0] = (1001, "tampered")
    statistics["item_count"] = 999
    assert table.item_count == table.statistics()["item_count"] == 1
    table.insert(1001, "replacement")
    table.insert(1011, "other")
    assert buckets[1] == ((1001, "original"),)
    assert table.search(1001) == "replacement"
    assert len(table.buckets[1]) == 2


@pytest.mark.parametrize("attribute", ["table_size", "item_count", "load_factor", "buckets"])
def test_public_state_properties_are_read_only(attribute):
    table = HashTable(10)
    with pytest.raises(AttributeError):
        setattr(table, attribute, 0)
    table.insert(1001, "student")
    assert table.item_count == 1
    assert table.table_size == 10


@pytest.mark.parametrize("size", [1, 10, HASH_TABLE_SIZE])
def test_full_csv_dataset_can_be_inserted_searched_and_deleted(size):
    original_csv = DATASET_PATH.read_bytes()
    records = load_dataset()
    table = HashTable[DataItem](size)
    for record in records:
        table.insert(record.student_id, record)
    assert table.item_count == len(table) == DATASET_SIZE == 150
    assert all(table.search(record.student_id) is record for record in records)
    assert table.search(9999) is None
    assert table.load_factor == pytest.approx(DATASET_SIZE / size)
    assert table.table_size == size
    if size == 1:
        assert table.statistics()["max_chain_length"] == DATASET_SIZE
        assert table.statistics()["collision_count"] == DATASET_SIZE - 1
    if size == HASH_TABLE_SIZE:
        assert table.statistics()["collision_count"] == 0

    for remaining, record in zip(range(DATASET_SIZE - 1, -1, -1), reversed(records)):
        assert table.delete(record.student_id) is True
        assert table.search(record.student_id) is None
        assert table.item_count == remaining
    assert table.statistics()["occupied_buckets"] == 0
    assert table.statistics()["max_chain_length"] == 0
    assert DATASET_PATH.read_bytes() == original_csv


def test_two_tables_manage_independent_state_for_shared_student_records():
    record = student(1001)
    first, second = HashTable(), HashTable()
    first.insert(record.student_id, record)
    second.insert(record.student_id, record)
    assert first.delete(1001) is True
    assert first.search(1001) is None
    assert second.search(1001) is record
    assert len(first) == 0 and len(second) == 1


def test_reproducible_mixed_operations_match_reference_mapping():
    rng = random.Random(42)
    table = HashTable[str](3)
    reference: dict[int, str] = {}
    for step in range(600):
        key = rng.randint(-20, 20)
        operation = rng.choice(("insert", "search", "delete"))
        if operation == "insert":
            value = f"value {step}"
            table.insert(key, value)
            reference[key] = value
        elif operation == "delete":
            expected = key in reference
            reference.pop(key, None)
            assert table.delete(key) is expected
        else:
            assert table.search(key) == reference.get(key)
        assert table.item_count == len(table) == len(reference)
        assert table.load_factor == pytest.approx(len(reference) / 3)
        assert all(table.search(candidate) == reference.get(candidate) for candidate in range(-20, 21))
        report = table.statistics()
        assert report["collision_count"] == len(reference) - report["occupied_buckets"]
