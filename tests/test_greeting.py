import pytest

from greeting import greet_person


def test_greet_person_by_name():
    assert greet_person("Ada Lovelace") == "Hello, Ada Lovelace!"


def test_greet_person_trims_surrounding_whitespace():
    assert greet_person("  Ada Lovelace  ") == "Hello, Ada Lovelace!"


@pytest.mark.parametrize("name", ["", "   \t"])
def test_greet_person_rejects_blank_name(name):
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet_person(name)
