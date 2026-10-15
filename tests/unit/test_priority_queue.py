"""Day 3 quality gates for the custom student binary max-heap."""

from dataclasses import FrozenInstanceError, replace
import random

import pytest

from src.config.settings import DATASET_PATH, DATASET_SIZE
from src.data_structures.priority_queue import PriorityQueue
from src.data_structures.priority_queue.helpers.heapify_down import heapify_down
from src.data_structures.priority_queue.helpers.heapify_up import heapify_up
from src.data_structures.priority_queue.helpers.validate_heap import validate_heap
from src.dataset.data_loader import load_dataset
from src.models.data_item import DataItem


def students(priorities):
    return [
        DataItem(1001 + index, f"Student {index}", "Computer Science", priority)
        for index, priority in enumerate(priorities)
    ]


def populated_queue(priorities):
    records = students(priorities)
    queue = PriorityQueue()
    for record in records:
        queue.insert(record)
    return queue, records


def assert_queue_state(queue, expected):
    """Check identity, count, maximum, and each parent/child relation."""
    snapshot = queue.heap
    assert len(queue) == queue.item_count == len(snapshot) == len(expected)
    assert len({record.student_id for record in snapshot}) == len(snapshot)
    assert {record.student_id: record for record in snapshot} == {
        record.student_id: record for record in expected
    }
    assert queue.validate_heap()
    assert all(
        snapshot[(child - 1) // 2].priority >= snapshot[child].priority
        for child in range(1, len(snapshot))
    )
    if expected:
        assert queue.peek().priority == max(record.priority for record in expected)
    else:
        assert queue.peek() is None


def test_empty_operations_are_safe_and_keep_an_empty_valid_heap():
    queue = PriorityQueue()
    assert queue.heap == ()
    assert queue.peek() is None
    assert queue.extract_max() is None
    assert queue.search(1001) is None
    assert queue.delete(1001) is False
    assert_queue_state(queue, [])


@pytest.mark.parametrize("priorities", [
    [10, 20, 30, 40, 50], [100, 80, 60, 40, 20],
    [50, 50, 50, 50], [1, 100, 25, 75, 99, 2],
])
def test_insertion_keeps_maximum_at_root_and_validates_after_every_change(priorities):
    queue = PriorityQueue()
    records = students(priorities)
    for position, record in enumerate(records, start=1):
        assert queue.insert(record) is None
        assert_queue_state(queue, records[:position])


def test_heapify_up_repairs_multiple_ancestor_levels():
    heap = students([90, 60, 80, 30, 40, 70, 100])
    original = set(heap)
    heapify_up(heap, len(heap) - 1)
    assert heap[0].priority == 100
    assert validate_heap(heap)
    assert set(heap) == original


@pytest.mark.parametrize("priorities", [
    [10, 90, 80, 70, 60, 50, 40],  # Larger left child and multiple levels
    [10, 80, 90, 50, 40, 60, 70],  # Larger right child
    [10, 90],                     # Only a left child
    [90, 80, 70],                 # Already valid
    [50, 50, 50], [50], [],
])
def test_heapify_down_repairs_children_without_losing_records(priorities):
    heap = students(priorities)
    original = set(heap)
    heapify_down(heap, 0)
    assert validate_heap(heap)
    assert set(heap) == original
    if priorities:
        assert heap[0].priority == max(priorities)


@pytest.mark.parametrize("priorities,expected", [
    ([], True), ([1], True), ([100, 100, 100], True),
    ([100, 80, 90, 50, 60, 70, 85], True),
    ([80, 90, 70], False), ([90, 70, 100], False),
    ([100, 70, 90, 80], False),  # A deeper violation despite a maximum root
])
def test_validator_checks_all_parent_child_relationships(priorities, expected):
    heap = students(priorities)
    before = list(heap)
    assert validate_heap(heap) is expected
    assert heap == before


def test_peek_preserves_root_and_entire_heap():
    queue, records = populated_queue([10, 80, 40, 100, 20])
    before = queue.heap
    assert queue.peek() is records[3]
    assert queue.peek() is records[3]
    assert queue.heap == before
    assert_queue_state(queue, records)


def test_single_student_peek_and_extract_return_original_record():
    queue, records = populated_queue([100])
    assert queue.peek() is records[0]
    assert queue.extract_max() is records[0]
    assert queue.extract_max() is None
    assert_queue_state(queue, [])


def test_search_by_id_is_independent_of_priority_order_and_does_not_mutate():
    queue, records = populated_queue([40, 10, 100, 70, 20])
    before = queue.heap
    for record in records:
        assert queue.search(record.student_id) is record
    assert queue.search(9999) is None
    assert queue.heap == before


@pytest.mark.parametrize("priorities,key,upward", [
    ([100, 70, 90, 20, 60, 80, 85], 1004, True),
    ([100, 90, 80, 60, 70, 50, 40], 1002, False),
])
def test_arbitrary_deletion_selects_the_needed_repair_direction(priorities, key, upward):
    queue, records = populated_queue(priorities)
    # These insertion orders already form valid heaps and force opposite repairs.
    assert queue.heap == tuple(records)
    index = next(i for i, record in enumerate(queue.heap) if record.student_id == key)
    parent = (index - 1) // 2
    assert (queue.heap[-1].priority > queue.heap[parent].priority) is upward
    assert queue.delete(key) is True
    assert queue.search(key) is None
    remaining = [record for record in records if record.student_id != key]
    assert_queue_state(queue, remaining)
    extracted = [queue.extract_max().priority for _ in range(len(queue))]
    assert extracted == sorted((record.priority for record in remaining), reverse=True)
    assert_queue_state(queue, [])


@pytest.mark.parametrize("key", [1001, 1002, 1007])
def test_delete_root_interior_or_last_record_preserves_other_students(key):
    queue, records = populated_queue([100, 90, 80, 70, 60, 50, 40])
    assert queue.delete(key) is True
    assert queue.delete(key) is False
    remaining = [record for record in records if record.student_id != key]
    assert_queue_state(queue, remaining)
    for record in remaining:
        assert queue.search(record.student_id) is record


def test_deleting_only_student_and_reinserting_same_id_is_safe():
    queue, records = populated_queue([50])
    assert queue.delete(1001) is True
    assert_queue_state(queue, [])
    assert queue.delete(1001) is False
    replacement = replace(records[0], priority=100)
    queue.insert(replacement)
    assert queue.peek() is replacement
    assert_queue_state(queue, [replacement])


def test_missing_delete_preserves_heap_and_count():
    queue, records = populated_queue([100, 20, 70, 10])
    before = queue.heap
    assert queue.delete(9999) is False
    assert queue.heap == before
    assert_queue_state(queue, records)


def test_equal_priorities_allow_search_deletion_and_extraction_without_losing_ids():
    queue, records = populated_queue([50] * 8)
    assert queue.delete(1003) is True
    remaining = [record for record in records if record.student_id != 1003]
    assert_queue_state(queue, remaining)
    extracted = []
    while queue:
        extracted.append(queue.extract_max())
        assert queue.validate_heap()
    assert set(extracted) == set(remaining)
    assert [record.priority for record in extracted] == [50] * len(remaining)
    assert_queue_state(queue, [])


@pytest.mark.parametrize("priority", [1, 50, 100])
def test_duplicate_student_ids_are_rejected_before_mutation(priority):
    queue, records = populated_queue([50, 90, 10])
    before = queue.heap
    with pytest.raises(ValueError, match="student_id 1001 already exists"):
        queue.insert(replace(records[0], name="Replacement", priority=priority))
    assert queue.heap == before
    assert_queue_state(queue, records)


@pytest.mark.parametrize("field,value", [
    ("student_id", 0), ("student_id", -1), ("student_id", True),
    ("student_id", "1001"), ("student_id", 1001.5),
    ("name", ""), ("name", "   "), ("name", None),
    ("program", ""), ("program", "\t"), ("program", 42),
    ("priority", 0), ("priority", 101), ("priority", True),
    ("priority", "50"), ("priority", 1.5),
])
def test_invalid_student_fields_are_rejected_without_changing_heap(field, value):
    queue, records = populated_queue([80, 20])
    before = queue.heap
    invalid = replace(students([50])[0], **{field: value})
    with pytest.raises(ValueError, match=field):
        queue.insert(invalid)
    assert queue.heap == before
    assert_queue_state(queue, records)


@pytest.mark.parametrize("record", [None, "student", {"student_id": 1001}])
def test_non_dataitem_insertions_are_rejected(record):
    queue = PriorityQueue()
    with pytest.raises(ValueError, match="record must be a DataItem"):
        queue.insert(record)
    assert_queue_state(queue, [])


@pytest.mark.parametrize("student_id,error", [
    (True, TypeError), (False, TypeError), (1001.0, TypeError),
    ("1001", TypeError), (None, TypeError), ([], TypeError),
    (0, ValueError), (-1, ValueError),
])
def test_search_and_delete_reject_invalid_ids_without_mutation(student_id, error):
    queue, records = populated_queue([50, 90])
    before = queue.heap
    for operation in (queue.search, queue.delete):
        with pytest.raises(error, match="student_id"):
            operation(student_id)
        assert queue.heap == before
    assert_queue_state(queue, records)


def test_snapshot_and_frozen_records_protect_heap_state():
    queue, records = populated_queue([50, 90])
    snapshot = queue.heap
    with pytest.raises(TypeError):
        snapshot[0] = records[0]
    with pytest.raises(FrozenInstanceError):
        snapshot[0].priority = 1
    queue.insert(DataItem(1003, "New Student", "Computer Science", 100))
    assert snapshot == (records[1], records[0])
    assert len(snapshot) == 2 and len(queue.heap) == 3
    assert queue.peek().priority == 100


@pytest.mark.parametrize("attribute", ["heap", "item_count"])
def test_public_state_properties_are_read_only(attribute):
    queue = PriorityQueue()
    with pytest.raises(AttributeError):
        setattr(queue, attribute, [])
    assert_queue_state(queue, [])


def test_two_queues_keep_independent_state_for_shared_records():
    first, records = populated_queue([50, 90])
    second = PriorityQueue()
    for record in records:
        second.insert(record)
    assert first.delete(1001)
    assert first.extract_max() is records[1]
    assert_queue_state(first, [])
    assert_queue_state(second, records)


@pytest.mark.parametrize("order", ["csv", "reverse", "shuffle", "ascending_priority"])
def test_all_150_csv_records_extract_in_descending_order_with_valid_heap(order):
    original_csv = DATASET_PATH.read_bytes()
    records = load_dataset()
    ordered = list(records)
    if order == "reverse":
        ordered.reverse()
    elif order == "shuffle":
        random.Random(42).shuffle(ordered)
    elif order == "ascending_priority":
        ordered.sort(key=lambda record: record.priority)
    queue = PriorityQueue()
    for index, record in enumerate(ordered, start=1):
        queue.insert(record)
        assert_queue_state(queue, ordered[:index])
    assert len(queue) == DATASET_SIZE == 150
    assert queue.peek().priority == max(record.priority for record in records)
    for record in records:
        assert queue.search(record.student_id) is record
    extracted = []
    while queue:
        before_count = len(queue)
        peeked = queue.peek()
        record = queue.extract_max()
        assert record is peeked
        extracted.append(record)
        assert len(queue) == before_count - 1
        assert queue.search(record.student_id) is None
        assert queue.validate_heap()
    assert [record.priority for record in extracted] == sorted(
        (record.priority for record in records), reverse=True
    )
    assert set(extracted) == set(records)
    assert_queue_state(queue, [])
    assert DATASET_PATH.read_bytes() == original_csv


def test_arbitrary_deletion_of_all_csv_students_keeps_heap_valid():
    records = load_dataset()
    queue = PriorityQueue()
    for record in records:
        queue.insert(record)
    remaining = {record.student_id: record for record in records}
    order = list(records)
    random.Random(19).shuffle(order)
    for record in order:
        assert queue.delete(record.student_id) is True
        del remaining[record.student_id]
        assert queue.search(record.student_id) is None
        assert_queue_state(queue, list(remaining.values()))


def test_mixed_operations_match_reference_records_without_assuming_tie_order():
    queue = PriorityQueue()
    reference = {}
    rng = random.Random(42)
    for step in range(600):
        key = rng.randint(1001, 1040)
        operation = rng.choice(("insert", "search", "delete", "peek", "extract"))
        if operation == "insert":
            record = DataItem(key, f"Student {step}", "Computer Science", rng.randint(1, 100))
            if key in reference:
                before = queue.heap
                with pytest.raises(ValueError, match="already exists"):
                    queue.insert(record)
                assert queue.heap == before
            else:
                queue.insert(record)
                reference[key] = record
        elif operation == "search":
            assert queue.search(key) is reference.get(key)
        elif operation == "delete":
            expected = key in reference
            reference.pop(key, None)
            assert queue.delete(key) is expected
        elif operation == "peek":
            before = queue.heap
            result = queue.peek()
            if reference:
                assert result is reference[result.student_id]
                assert result.priority == max(record.priority for record in reference.values())
            else:
                assert result is None
            assert queue.heap == before
        else:
            maximum = max((record.priority for record in reference.values()), default=None)
            result = queue.extract_max()
            if reference:
                assert result.priority == maximum
                assert result is reference.pop(result.student_id)
            else:
                assert result is None
        assert_queue_state(queue, list(reference.values()))
