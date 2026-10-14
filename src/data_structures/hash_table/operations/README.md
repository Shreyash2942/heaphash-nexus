# Hash Table Operations

This package implements insertion, search, and deletion within one bucket's collision chain. `HashTable` selects the bucket and maintains the overall item count.

```text
operations/
|-- README.md     # Internal chain operation contracts
|-- __init__.py   # Makes operations a Python package
|-- insert.py     # Appends a new key or replaces the value for an existing key
|-- search.py     # Returns the matching value or None
`-- delete.py     # Removes one matching pair while preserving other entries
```

The internal `insert()` helper returns `True` for a new key and `False` for an update. The internal `delete()` helper returns whether it removed an entry. The owning table uses these flags to adjust its count exactly once. Search and deletion check each key rather than assuming the first chain entry matches.

Application callers should use `table.insert()`, `table.search()`, and `table.delete()` rather than calling these internal helpers or changing buckets directly. The public insert method returns `None`.

[Hash table](../README.md)
