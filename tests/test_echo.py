import pytest

from beacon.echo import echo


def test_echo():
    assert echo("ping") == "pong"


def test_fail():
    with pytest.raises(AssertionError, match="beacon"):
        assert True is False, "beacon is not becon"
