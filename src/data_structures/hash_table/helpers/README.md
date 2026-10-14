# Hash Table Helpers

This package will hold the internal hash-function logic during Day 2. It currently contains only the package initializer.

```text
helpers/
|-- README.md     # Planned hashing helper
`-- __init__.py   # Makes helpers a Python package
```

The planned `hash_function.py` will calculate `key % table_size`. Hashing chooses a bucket; separate chaining in the table handles keys that map to the same bucket.

[Hash table](../README.md)
