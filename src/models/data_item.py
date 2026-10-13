"""Student record shared by the dataset and both data structures."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DataItem:
    """A student and their max-heap priority.

    Dataset validation is handled by ``src.dataset.validator``. Immutable
    records can be shared by independently managed data structures without
    accidentally changing a key or priority in another structure.
    """

    student_id: int
    name: str
    program: str
    priority: int
