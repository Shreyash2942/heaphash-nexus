"""Day 5 menu workflows, reset guarantees, demonstration, and entry point."""

from dataclasses import replace
import subprocess
import sys

import pytest

from src.cli.application import Application
from src.cli import application as application_module
from src.cli import dataset_menu as dataset_ui
from src.cli import demonstration
from src.cli import hash_table_menu as hash_ui
from src.cli import menu as main_ui
from src.cli import performance_menu as performance_ui
from src.cli import priority_queue_menu as queue_ui
from src.config.settings import DATASET_SIZE, PROJECT_ROOT
from src.data_structures.priority_queue import PriorityQueue
from src.dataset.data_generator import write_dataset
from src.dataset.data_loader import load_dataset
from src.performance.result import format_results


@pytest.fixture
def app(tmp_path, records):
    source = write_dataset(tmp_path / "students.csv", records)
    return Application(source, tmp_path / "results" / "report.txt")


def feed(monkeypatch, values):
    responses = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))


def state(app):
    return app.records, app.hash_table.buckets, app.priority_queue.heap


def test_application_populates_independent_structures_from_same_records(app):
    assert len(app.records) == len(app.hash_table) == len(app.priority_queue) == DATASET_SIZE
    assert app.priority_queue.validate_heap()
    for student in app.records:
        assert app.hash_table.search(student.student_id) is student
        assert app.priority_queue.search(student.student_id) is student


def test_application_creates_a_missing_dataset_once(tmp_path):
    source = tmp_path / "new" / "students.csv"
    app = Application(source, tmp_path / "report.txt")
    assert source.exists()
    assert tuple(load_dataset(source)) == app.records
    assert len(app.hash_table) == len(app.priority_queue) == 150


def test_results_path_cannot_be_the_source_csv(app):
    original = app.dataset_path.read_bytes()
    with pytest.raises(ValueError, match="must not overwrite"):
        Application(app.dataset_path, app.dataset_path)
    assert app.dataset_path.read_bytes() == original


def test_reset_discards_interactive_edits_and_rebuilds_both_structures(app):
    original_csv = app.dataset_path.read_bytes()
    original_records = app.records
    app.hash_table.delete(1001)
    app.priority_queue.delete(1075)
    added = replace(app.records[0], student_id=2000, priority=100)
    app.hash_table.insert(2000, added)
    app.priority_queue.insert(added)
    app.reset()
    assert app.records == original_records
    assert app.hash_table.search(2000) is app.priority_queue.search(2000) is None
    assert len(app.hash_table) == len(app.priority_queue) == 150
    assert app.priority_queue.validate_heap()
    for student in app.records:
        assert app.hash_table.search(student.student_id) is student
        assert app.priority_queue.search(student.student_id) is student
    assert app.dataset_path.read_bytes() == original_csv


@pytest.mark.parametrize("problem", ["malformed", "missing"])
def test_failed_source_reload_preserves_all_interactive_state(app, problem):
    app.hash_table.delete(1001)
    app.priority_queue.delete(1075)
    before = state(app)
    if problem == "malformed":
        app.dataset_path.write_text("invalid CSV", encoding="utf-8")
    else:
        app.dataset_path.unlink()
    with pytest.raises((OSError, ValueError)):
        app.reset()
    assert state(app) == before


def test_rebuild_failure_does_not_publish_a_partially_reset_structure(app, monkeypatch):
    app.hash_table.delete(1001)
    before = state(app)

    class FailingQueue(PriorityQueue):
        def insert(self, student):
            if len(self) == 5:
                raise ValueError("simulated rebuild failure")
            super().insert(student)

    monkeypatch.setattr(application_module, "PriorityQueue", FailingQueue)
    with pytest.raises(ValueError, match="rebuild failure"):
        app.reset()
    assert state(app) == before


def test_hash_update_and_new_insert_do_not_change_queue_or_csv(app, monkeypatch):
    original_csv = app.dataset_path.read_bytes()
    original_queue = app.priority_queue.heap
    feed(monkeypatch, ["1001", "Updated Name", "New Program", "100"])
    hash_ui.insert_student(app)
    assert app.hash_table.search(1001).name == "Updated Name"
    assert app.priority_queue.search(1001) is app.records[0]
    assert len(app.hash_table) == 150
    feed(monkeypatch, ["2000", "New Student", "Computer Science", "50"])
    hash_ui.insert_student(app)
    assert app.hash_table.search(2000).student_id == 2000
    assert app.priority_queue.search(2000) is None
    assert app.priority_queue.heap == original_queue
    assert app.dataset_path.read_bytes() == original_csv


def test_hash_menu_handles_navigation_operations_display_and_collisions(app, monkeypatch, capsys):
    original_queue = app.priority_queue.heap
    feed(monkeypatch, [
        "invalid", "1", "2000", "Menu Student", "Computer Science", "60",
        "2", "2000", "3", "2000", "3", "9999", "4", "5", "6", "0",
    ])
    hash_ui.hash_table_menu(app)
    assert app.hash_table.search(2000) is None
    assert len(app.hash_table) == 150
    assert app.priority_queue.heap == original_queue
    output = capsys.readouterr().out
    assert "Menu Student" in output and "Collision demonstration passed" in output
    assert "Current collisions" in output


def test_collision_demo_uses_a_separate_table_and_preserves_surviving_records(app):
    before = state(app)
    table = hash_ui.collision_demonstration()
    assert len(table) == 2 and table.table_size == 10
    assert table.search(1011) is None
    assert table.search(1001) is not None and table.search(1021) is not None
    assert table.statistics()["collision_count"] == 1
    assert state(app) == before


def test_queue_menu_handles_insert_peek_extract_search_delete_and_validation(app, monkeypatch):
    original_table = app.hash_table.buckets
    feed(monkeypatch, [
        "1", "2000", "Queue Student", "Computer Science", "100",
        "4", "5", "2", "2000", "3", "1001", "6", "7", "0",
    ])
    queue_ui.priority_queue_menu(app)
    assert app.priority_queue.search(2000) is None
    assert app.priority_queue.search(1001) is None
    assert len(app.priority_queue) == 149
    assert app.priority_queue.validate_heap()
    assert app.hash_table.buckets == original_table


def test_duplicate_queue_insert_is_reported_and_menu_continues(app, monkeypatch, capsys):
    before = state(app)
    feed(monkeypatch, ["1", "1001", "Duplicate", "Computer Science", "100", "7", "0"])
    queue_ui.priority_queue_menu(app)
    assert state(app) == before
    output = capsys.readouterr().out
    assert "already exists" in output and "Heap is valid" in output


def test_queue_menu_safely_handles_empty_structure(app, monkeypatch, capsys):
    app.priority_queue = PriorityQueue()
    feed(monkeypatch, ["4", "5", "2", "1001", "3", "1001", "6", "7", "0"])
    queue_ui.priority_queue_menu(app)
    assert len(app.priority_queue) == 0 and app.priority_queue.validate_heap()
    output = capsys.readouterr().out
    assert "Priority queue is empty" in output and "Heap is valid" in output


def test_dataset_menu_information_preview_and_validation_use_source_records(app, monkeypatch, capsys):
    app.hash_table.delete(1001)
    before = state(app)
    feed(monkeypatch, ["1", "2", "3", "0"])
    dataset_ui.dataset_menu(app)
    assert state(app) == before
    output = capsys.readouterr().out
    assert "Showing 10 of 150" in output and "Dataset valid: 150" in output


def test_changed_valid_csv_is_detected_and_reset_reloads_it(app, capsys):
    updated = [replace(app.records[0], name="External Change"), *app.records[1:]]
    write_dataset(app.dataset_path, updated, overwrite=True)
    dataset_ui.validate_source(app)
    assert "differs from the loaded records" in capsys.readouterr().out
    assert app.records[0].name != "External Change"
    app.reset()
    assert app.records[0].name == "External Change"
    assert app.hash_table.search(1001).name == "External Change"
    assert app.priority_queue.search(1001).name == "External Change"


def test_dataset_validation_errors_return_to_menu_without_modifying_state(app, monkeypatch, capsys):
    before = state(app)
    app.dataset_path.write_text("invalid CSV", encoding="utf-8")
    feed(monkeypatch, ["3", "0"])
    dataset_ui.dataset_menu(app)
    assert state(app) == before
    assert "Error:" in capsys.readouterr().out


def test_benchmark_uses_original_records_and_preserves_edited_interactive_state(app, capsys):
    performance_ui.view_results(app)
    assert "No saved benchmark results" in capsys.readouterr().out
    app.hash_table.delete(1001)
    app.priority_queue.extract_max()
    before = state(app)
    result = performance_ui.run_performance(app)
    assert result.dataset_size == 150 and result.measured_searches_per_algorithm == 60_000
    assert app.results_path.read_text(encoding="utf-8") == format_results(result)
    assert state(app) == before
    performance_ui.view_results(app)
    assert "Measured searches per algorithm: 60000" in capsys.readouterr().out


def test_performance_file_errors_are_recoverable(app, tmp_path, monkeypatch, capsys):
    app.results_path = tmp_path  # An existing directory cannot be a report file.
    before = state(app)
    feed(monkeypatch, ["1", "2", "0"])
    performance_ui.performance_menu(app)
    assert state(app) == before
    assert "Error:" in capsys.readouterr().out


def test_complete_demonstration_preserves_interactive_edits_and_source(app, capsys):
    app.hash_table.delete(1001)
    app.priority_queue.delete(1075)
    before = state(app)
    original_csv = app.dataset_path.read_bytes()
    result = demonstration.run_demonstration(app)
    assert result.dataset_size == 150 and result.measured_searches_per_algorithm == 60_000
    assert app.results_path.exists()
    assert state(app) == before
    assert app.dataset_path.read_bytes() == original_csv
    assert "Complete demonstration passed" in capsys.readouterr().out


def test_failed_demonstration_does_not_claim_success_or_change_state(app, monkeypatch, capsys):
    def fail_collision():
        raise ValueError("simulated collision failure")

    before = state(app)
    monkeypatch.setattr(demonstration, "collision_demonstration", fail_collision)
    with pytest.raises(ValueError, match="collision failure"):
        demonstration.run_demonstration(app)
    assert state(app) == before
    assert not app.results_path.exists()
    assert "Complete demonstration passed" not in capsys.readouterr().out


def test_main_navigation_visits_all_submenus_and_reset(app, monkeypatch, capsys):
    app.hash_table.delete(1001)
    feed(monkeypatch, ["bad", "1", "0", "2", "0", "3", "0", "4", "0", "6", "0"])
    main_ui.run(app)
    assert len(app.hash_table) == len(app.priority_queue) == 150
    output = capsys.readouterr().out
    assert "Goodbye" in output and "Reset complete" in output


@pytest.mark.parametrize("signal", [EOFError, KeyboardInterrupt])
@pytest.mark.parametrize("prefix", [[], ["1", "1", "2000", "Student", "Computer Science"]])
def test_eof_or_ctrl_c_at_main_or_mid_insert_exits_without_partial_mutation(app, monkeypatch, capsys, signal, prefix):
    before = state(app)
    responses = iter(prefix)

    def interrupted(prompt):
        try:
            return next(responses)
        except StopIteration:
            raise signal

    monkeypatch.setattr("builtins.input", interrupted)
    monkeypatch.setattr(main_ui, "Application", lambda *args: app)
    assert main_ui.main([]) == 0
    assert state(app) == before
    assert "Goodbye" in capsys.readouterr().out


def test_bad_startup_dataset_exits_with_clear_error_without_prompting(tmp_path, monkeypatch, capsys):
    path = tmp_path / "invalid.csv"
    path.write_text("invalid CSV", encoding="utf-8")
    monkeypatch.setattr("builtins.input", lambda prompt: pytest.fail("Cannot prompt with invalid data"))
    assert main_ui.main(["--dataset", str(path), "--results", str(tmp_path / "report.txt")]) == 1
    assert "Application error:" in capsys.readouterr().out
    assert path.read_text(encoding="utf-8") == "invalid CSV"


def test_demo_flag_runs_without_any_interactive_prompts(app, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: pytest.fail("Demo must be non-interactive"))
    assert main_ui.main([
        "--demo", "--dataset", str(app.dataset_path), "--results", str(app.results_path),
    ]) == 0
    assert "Complete demonstration passed" in capsys.readouterr().out


def test_main_entrypoint_runs_from_another_working_directory(tmp_path):
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "main.py"), "--results", str(tmp_path / "report.txt")],
        input="0\n", cwd=tmp_path, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Loaded 150 students" in result.stdout and "Goodbye" in result.stdout
    assert "Traceback" not in result.stderr
