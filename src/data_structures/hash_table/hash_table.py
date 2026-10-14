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
    Search, insertion, and deletion take O(1 + chain length) time. With
    well-distributed keys and a bounded load factor this is O(1) on average;
    a chain containing all entries gives O(n) worst-case behavior. The table
    does not resize automatically.
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

    @property
    def load_factor(self) -> float:
        """Ratio of stored entries to buckets; may exceed 1 with chaining."""
        return self._item_count / self._table_size

    @property
    def buckets(self) -> tuple[tuple[tuple[int, ValueT], ...], ...]:
        """Return an immutable snapshot for inspection without exposing lists.

        Bucket containers are copied, but value objects are shared. Student
        DataItem values are immutable. Creating a snapshot takes O(m + n)
        for m buckets and n stored entries.
        """
        return tuple(tuple(bucket) for bucket in self._buckets)

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

    def statistics(self) -> dict[str, int | float]:
        """Report current occupancy in O(table_size) time.

        collision_count counts current entries beyond the first in each
        occupied bucket, not historical insertion events. A dict formats
        the returned report only; entries remain stored in bucket lists.
        """
        occupied = sum(1 for bucket in self._buckets if bucket)
        return {
            "table_size": self._table_size,
            "item_count": self._item_count,
            "load_factor": self.load_factor,
            "occupied_buckets": occupied,
            "empty_buckets": self._table_size - occupied,
            "collision_count": self._item_count - occupied,
            "max_chain_length": max(len(bucket) for bucket in self._buckets),
        }
