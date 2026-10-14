"""Insert or replace a key/value pair within one collision chain."""

from typing import TypeVar

ValueT = TypeVar("ValueT")


def insert(bucket: list[tuple[int, ValueT]], key: int, value: ValueT) -> bool:
    """Return True for a new key or False when replacing an existing value."""
    for index, (existing_key, _) in enumerate(bucket):
        if existing_key == key:
            bucket[index] = (key, value)
            return False
    bucket.append((key, value))
    return True
