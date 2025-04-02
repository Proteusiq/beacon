import shutil
from unittest.mock import patch

from beacon.cli.db import app
from beacon.settings import BOOKS_DB_PATH, DEFAULT_COLLECTION_NAME


@patch("beacon.cli.db.create_db")
def test_init_test_mode(mock_create_db, clean_db_path, runner):
    """test initializing the database in test mode."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME

    assert not db_path.exists()

    result = runner.invoke(app, ["init", "--test"])

    assert result.exit_code == 0
    assert "Database initialized successfully" in result.stdout
    assert "test mode" in result.stdout

    mock_create_db.assert_called_once_with(test_mode=True)

    db_path.mkdir(parents=True, exist_ok=True)


def test_init_force_flag(clean_db_path, runner):
    """test that --force flag allows reinitializing an existing database."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME

    db_path.mkdir(parents=True, exist_ok=True)
    (db_path / "dummy.txt").write_text("test")

    result = runner.invoke(app, ["init", "--test"])
    assert "Database already exists" in result.stdout
    assert "Use --force to reinitialize" in result.stdout

    result = runner.invoke(app, ["init", "--test", "--force"])
    assert result.exit_code == 0
    assert "Database initialized successfully" in result.stdout


def test_clean_command(clean_db_path, runner):
    """test the clean command removes the database."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME

    db_path.mkdir(parents=True, exist_ok=True)

    result = runner.invoke(app, ["clean"], input="y\n")

    assert result.exit_code == 0
    assert "has been removed" in result.stdout

    assert not db_path.exists()


def test_clean_nonexistent_db(runner):
    """test clean command handles case when database doesn't exist."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME

    if db_path.exists():
        shutil.rmtree(db_path)

    result = runner.invoke(app, ["clean"])

    assert "No database found to clean" in result.stdout
