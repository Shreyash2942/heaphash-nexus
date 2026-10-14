"""Delete one key/value pair from a collision chain."""

from typing import TypeVar

ValueT = TypeVar("ValueT")


def delete(bucket: list[tuple[int, ValueT]], key: int) -> bool:
    """Remove only the matching pair and return whether it was present."""
    for index, (existing_key, _) in enumerate(bucket):
        if existing_key == key:
            del bucket[index]
            return True
    return False
