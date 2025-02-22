from typing import TypedDict

import pytest

from beacon import recommeder


class Request(TypedDict):
    query: str
    expects: str


USER_STORIES: list[Request] = [
    {"query": "vampire love drama", "expects": "Twilight Saga"},
    {"query": "a lawyer driving a fancy car", "expects": "The Lincoln Lawyer"},
    {"query": "a boy going to a magic school of wizards", "expects": "Harry Potter"},
]


@pytest.mark.parametrize("story", USER_STORIES, ids=["twillight", "lincoln", "potter"])
def test_becons(story):
    # Arrange
    query = story.get("query")
    expected = story.get("expects")

    # Act
    recommendations = recommeder.recommend(query)

    # Assert
    assert any(expected in rec["title"] for rec in recommendations)


def test_fail():
    with pytest.raises(AssertionError, match="beacon not ready"):
        assert True is False, "beacon not ready"
