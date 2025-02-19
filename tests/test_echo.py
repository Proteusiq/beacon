from beacon.echo import echo


def test_echo():
    assert echo("ping") == "pong"
