"""Custom integer-key hash table backed by separate list-based chains."""

from typing import Generic, TypeVar

from src.config.settings import HASH_TABLE_SIZE
from src.data_structures.hash_table.helpers.hash_function import hash_function

ValueT = TypeVar("ValueT")


class HashTable(Generic[ValueT]):
    """Own the bucket storage and item count for a fixed-size hash table.

    Each bucket is a distinct list of ``(key, value)`` pairs. Values may be
    student records or other objects; no Python dict stores the entries.
    """

    def __init__(self, table_size: int = HASH_TABLE_SIZE) -> None:
        # Apply the same size validation used by every hash operation.
        hash_function(0, table_size)
        self._table_size = table_size
        self._buckets: list[list[tuple[int, ValueT]]] = [
            [] for _ in range(table_size)
        ]
        self._item_count = 0

    @property
    def table_size(self) -> int:
        """Number of buckets, fixed at construction time."""
        return self._table_size

    @property
    def item_count(self) -> int:
        """Number of distinct keys currently stored."""
        return self._item_count

    def __len__(self) -> int:
        return self._item_count
