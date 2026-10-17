"""Hash-table interaction and an isolated collision demonstration."""

from src.cli.application import Application
from src.cli.input_handler import read_student, read_student_id
from src.cli.navigation import run_menu
from src.data_structures.hash_table import HashTable
from src.data_structures.hash_table.helpers.hash_function import hash_function
from src.models.data_item import DataItem
from src.utils.display import format_student


def insert_student(app: Application) -> None:
    student = read_student()
    existed = app.hash_table.search(student.student_id) is not None
    app.hash_table.insert(student.student_id, student)
    print(f"{'Updated' if existed else 'Inserted'}: {format_student(student)}")


def search_student(app: Application) -> None:
    print(format_student(app.hash_table.search(read_student_id())))


def delete_student(app: Application) -> None:
    key = read_student_id()
    print(f"Deleted student {key}." if app.hash_table.delete(key) else "No student found.")


def display_table(table: HashTable[DataItem]) -> None:
    print(f"Hash table: {len(table)} students in {table.table_size} buckets")
    if not table:
        print("Hash table is empty.")
    for index, bucket in enumerate(table.buckets):
        if bucket:
            print(f"Bucket {index}:")
            for _, student in bucket:
                print(f"  {format_student(student)}")


def show_statistics(app: Application) -> None:
    statistics = app.hash_table.statistics()
    for label, key in (
        ("Students", "item_count"), ("Buckets", "table_size"),
        ("Load factor", "load_factor"), ("Occupied buckets", "occupied_buckets"),
        ("Empty buckets", "empty_buckets"), ("Current collisions", "collision_count"),
        ("Longest chain", "max_chain_length"),
    ):
        value = statistics[key]
        print(f"{label}: {value:.4f}" if key == "load_factor" else f"{label}: {value}")


def collision_demonstration() -> HashTable[DataItem]:
    """Prove size-10 collisions and safe middle deletion using a separate table."""
    table = HashTable[DataItem](10)
    print("Collision demonstration (separate size-10 table)")
    for key in (1001, 1011, 1021):
        table.insert(key, DataItem(key, f"Student {key}", "Demonstration", 50))
        print(f"Student {key} maps to bucket {hash_function(key, table.table_size)}.")
    if not all(table.search(key) is not None for key in (1001, 1011, 1021)):
        raise ValueError("collision demonstration could not retrieve every record")
    display_table(table)
    if not table.delete(1011) or table.search(1011) is not None:
        raise ValueError("collision demonstration deletion failed")
    if not all(table.search(key) is not None for key in (1001, 1021)):
        raise ValueError("collision demonstration lost another record")
    print("Deleted 1011; 1001 and 1021 remain searchable. Collision demonstration passed.")
    display_table(table)
    return table


def hash_table_menu(app: Application) -> None:
    run_menu("Hash Table", {
        "1": ("Insert Student", lambda: insert_student(app)),
        "2": ("Search Student", lambda: search_student(app)),
        "3": ("Delete Student", lambda: delete_student(app)),
        "4": ("Display Hash Table", lambda: display_table(app.hash_table)),
        "5": ("Show Collision Demonstration", collision_demonstration),
        "6": ("Show Hash Table Statistics", lambda: show_statistics(app)),
    })
