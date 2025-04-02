import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    yield CliRunner()
