# Hash Table Helpers

This package implements the modulo helper used by every public hash-table operation.

```text
helpers/
|-- README.md         # Hashing rules and examples
|-- __init__.py       # Makes helpers a Python package
`-- hash_function.py  # Validates inputs and calculates key % table_size
```

`hash_function(key, table_size=211)` uses the configured default size. Both arguments must be integers, excluding booleans, and the size must be positive. Zero and negative keys remain valid; modulo still produces an index from 0 through `table_size - 1`.

With size 10, keys 1001, 1011, and 1021 all map to bucket 1. Hashing chooses that bucket; the table's separate chain preserves all three values. The dataset validator separately enforces positive IDs for student records.

[Hash table](../README.md)
