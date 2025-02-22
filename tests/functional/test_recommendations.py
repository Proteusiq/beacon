from typing import TypedDict

import pytest


class Request(TypedDict):
    query: str
    expects: str


USER_STORIES: list[Request] = [
    {"query": "vampire love drama", "expects": "The Twillight Saga"},
    {"query": "a lawyer driving a fancy car", "expects": "The Lincoln Lawyer"},
    {"query": "a boy going to a magic school of wizards", "expects": "Harry Potter"},
]


def test_fail():
    with pytest.raises(AssertionError, match="beacon not ready"):
        assert True is False, "beacon not ready"
