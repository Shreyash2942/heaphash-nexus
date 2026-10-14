"""Custom integer-key hash table backed by separate list-based chains."""

from typing import Generic, TypeVar

from src.config.settings import HASH_TABLE_SIZE
from src.data_structures.hash_table.helpers.hash_function import hash_function
from src.data_structures.hash_table.operations.delete import delete as delete_from_bucket
from src.data_structures.hash_table.operations.insert import insert as insert_into_bucket
from src.data_structures.hash_table.operations.search import search as search_bucket

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

    def insert(self, key: int, value: ValueT) -> None:
        """Store a pair, replacing an existing key without increasing the count."""
        index = hash_function(key, self._table_size)
        if insert_into_bucket(self._buckets[index], key, value):
            self._item_count += 1

    def search(self, key: int) -> ValueT | None:
        """Return the value for a key, or None if it is absent.

        If a caller stores None as a value, this return value alone cannot
        distinguish that stored value from a missing key.
        """
        index = hash_function(key, self._table_size)
        return search_bucket(self._buckets[index], key)

    def delete(self, key: int) -> bool:
        """Remove a key and return True; return False when it is absent."""
        index = hash_function(key, self._table_size)
        if delete_from_bucket(self._buckets[index], key):
            self._item_count -= 1
            return True
        return False
