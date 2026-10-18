"""CLI prompt validation and propagation of graceful-exit signals."""

import pytest

from src.cli.input_handler import read_choice, read_int, read_student, read_student_id, read_text
from src.models.data_item import DataItem


def feed(monkeypatch, values):
    responses = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))


def test_choice_retries_unknown_blank_and_non_integer_choices(monkeypatch):
    feed(monkeypatch, ["", "bad", "-1", "1.0", "9", " 2 "])
    assert read_choice("Choice: ", ("0", "1", "2")) == "2"


@pytest.mark.parametrize("values,expected", [
    (["text", "", "2.5", " 42 "], 42),
    (["True", "False", "+7"], 7),
    (["-20"], -20),
])
def test_integer_prompt_retries_malformed_values(monkeypatch, values, expected):
    feed(monkeypatch, values)
    assert read_int("Number: ") == expected


@pytest.mark.parametrize("values,expected", [
    (["0", "-1", "101", "1"], 1),
    (["101", "100"], 100),
])
def test_integer_bounds_are_inclusive(monkeypatch, values, expected):
    feed(monkeypatch, values)
    assert read_int("Priority: ", minimum=1, maximum=100) == expected


def test_student_id_rejects_non_positive_values(monkeypatch):
    feed(monkeypatch, ["invalid", "0", "-3", "1001"])
    assert read_student_id() == 1001


def test_text_prompt_requires_non_empty_trimmed_value(monkeypatch):
    feed(monkeypatch, ["", "  ", "\t", "  Student Name  "])
    assert read_text("Name: ") == "Student Name"


def test_student_prompt_retries_each_invalid_field(monkeypatch):
    feed(monkeypatch, [
        "not an id", "0", "2000", "", "  Student Name  ", " ",
        " Computer Science ", "high", "0", "101", "100",
    ])
    assert read_student() == DataItem(2000, "Student Name", "Computer Science", 100)


@pytest.mark.parametrize("signal", [EOFError, KeyboardInterrupt])
@pytest.mark.parametrize("reader", [
    lambda: read_choice("Choice: ", ("0", "1")),
    lambda: read_int("Integer: "),
    lambda: read_text("Text: "),
    read_student,
])
def test_exit_signals_propagate_to_application_boundary(monkeypatch, signal, reader):
    def interrupted(prompt):
        raise signal

    monkeypatch.setattr("builtins.input", interrupted)
    with pytest.raises(signal):
        reader()
