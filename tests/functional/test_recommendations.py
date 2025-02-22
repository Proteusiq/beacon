from typing import TypedDict

import pytest

from beacon import recommeder


class Request(TypedDict):
    query: str
    expects: str


USER_STORIES: list[Request] = [
    {"query": "vampire love drama", "expects": "The Twillight Saga"},
    {"query": "a lawyer driving a fancy car", "expects": "The Lincoln Lawyer"},
    {"query": "a boy going to a magic school of wizards", "expects": "Harry Potter"},
]


@pytest.mark.xfail(reason="show cases tdd done right")
@pytest.mark.parametrize("story", USER_STORIES, ids=["twilight", "lincoln", "potter"])
def test_becons(story):
    # Arrange
    query = story.get("query")
    expected = story.get("expects")

    # Act
    recommendations = recommeder.recommend(query)

    # Assert
    assert any(expected in recommendation for recommendation in recommendations)


def test_fail():
    with pytest.raises(AssertionError, match="beacon not ready"):
        assert True is False, "beacon not ready"
