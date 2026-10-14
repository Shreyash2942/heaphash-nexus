# Hash Table

This package implements the Day 2 hash table using a list of bucket lists. Each bucket stores `(key, value)` pairs, and separate chaining preserves entries when keys collide.

```text
hash_table/
|-- README.md      # Hash-table API, design, and examples
|-- __init__.py    # Exports HashTable from the package
|-- hash_table.py  # Owns buckets, counts, public operations, and statistics
|-- operations/    # Insert, search, and delete within a collision chain
`-- helpers/       # Validated modulo hash function
```

`HashTable(table_size=211)` uses the default from shared configuration. The table stays at its configured size and can hold more entries than buckets. Keys must be integers; zero and negative keys are supported, while booleans and other types raise `TypeError`. Student dataset validation separately requires positive student IDs. Invalid non-positive table sizes raise `ValueError`.

| Public member | Behavior |
|---|---|
| `insert(key, value)` | Stores or replaces a value; returns `None` |
| `search(key)` | Returns the stored value or `None` when missing |
| `delete(key)` | Returns `True` if removed, otherwise `False` |
| `item_count`, `len(table)` | Number of distinct keys currently stored |
| `table_size` | Fixed number of buckets |
| `load_factor` | `item_count / table_size` |
| `buckets` | Immutable snapshot of the bucket containers for inspection |
| `statistics()` | Current size, count, load factor, occupancy, collisions, and longest chain |

`collision_count` counts current entries beyond the first in each occupied bucket, rather than historical collision events. Updating a key does not change the item count or collision count. Deletion updates both counts as appropriate. The statistics dictionary is a reporting value; key/value storage uses list-based chains.

The bucket snapshot copies containers, but its value objects are shared. Student `DataItem` objects are immutable. If `None` is stored as a value, `search()` alone cannot distinguish that value from a missing key; `delete()` still reports removal correctly.

From the project root, load all 150 students:

```python
from src.data_structures.hash_table import HashTable
from src.dataset.data_loader import load_dataset

table = HashTable()
for student in load_dataset():
    table.insert(student.student_id, student)
print(table.search(1075))
print(table.statistics())
```

Demonstrate deliberate collisions and safe deletion:

```python
collisions = HashTable(table_size=10)
for key in (1001, 1011, 1021):
    collisions.insert(key, f"Student {key}")
print(collisions.buckets[1])       # All three pairs share bucket 1
assert collisions.delete(1011)
assert collisions.search(1001) == "Student 1001"
assert collisions.search(1021) == "Student 1021"
assert collisions.search(1011) is None
```

Search, insertion, and deletion scan one chain: average O(1) with well-distributed keys and a bounded load factor, and worst-case O(n). Statistics scan the buckets in O(table_size); the snapshot takes O(table_size + item_count). The 150 consecutive dataset IDs occupy distinct buckets at size 211; the size-10 example deliberately creates collisions.

Run `python -m pytest tests/unit/test_hash_table.py -v` from the project root for operation, collision, and full-dataset checks.

See [operations](operations/README.md) and [helpers](helpers/README.md).

[Data structures](../README.md)
