"""Search one collision chain by key."""

from typing import TypeVar

ValueT = TypeVar("ValueT")


def search(bucket: list[tuple[int, ValueT]], key: int) -> ValueT | None:
    """Return the stored value, or None if the chain contains no matching key."""
    for existing_key, value in bucket:
        if existing_key == key:
            return value
    return None
