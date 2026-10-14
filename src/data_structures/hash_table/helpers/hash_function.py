"""Modulo hashing for integer keys."""

from src.config.settings import HASH_TABLE_SIZE


def hash_function(key: int, table_size: int = HASH_TABLE_SIZE) -> int:
    """Return ``key % table_size`` with a positive integer table size.

    Any integer key is supported, including zero and negative keys. Student
    dataset validation separately requires positive student IDs. Booleans
    are rejected rather than treated as integer keys or table sizes.
    """
    if type(key) is not int:
        raise TypeError("key must be an integer")
    if type(table_size) is not int:
        raise TypeError("table_size must be an integer")
    if table_size <= 0:
        raise ValueError("table_size must be positive")
    return key % table_size
