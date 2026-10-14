# Hash Table

This package is the Day 2 location for the custom hash table. Only the package structure exists after Day 1.

```text
hash_table/
|-- README.md     # Planned hash-table design
|-- __init__.py   # Makes hash_table a Python package
|-- operations/   # Planned insert, search, and delete functions
`-- helpers/      # Planned modulo hash function
```

The planned `hash_table.py` will own a list of bucket lists, use `key % table_size`, and resolve collisions through separate chaining. Duplicate keys will update existing values. The normal table size will come from shared configuration and default to 211.

See [operations](operations/README.md) and [helpers](helpers/README.md).

[Data structures](../README.md)
