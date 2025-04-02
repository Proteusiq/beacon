"""Tests for the database CLI functionality."""
import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from beacon.cli.db import app
from beacon.settings import BOOKS_DB_PATH, DEFAULT_COLLECTION_NAME

runner = CliRunner()


@pytest.fixture
def clean_db_path():
    """Ensure the database directory is clean before and after tests."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME
    
    # Clean up before test
    if db_path.exists():
        shutil.rmtree(db_path)
    
    # Make sure parent directory exists
    os.makedirs(BOOKS_DB_PATH, exist_ok=True)
    
    yield
    
    # Clean up after test
    if db_path.exists():
        shutil.rmtree(db_path)


@patch('beacon.cli.db.create_db')
def test_init_test_mode(mock_create_db, clean_db_path):
    """Test initializing the database in test mode."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME
    
    # Verify db doesn't exist yet
    assert not db_path.exists()
    
    # Run the init command with test mode
    result = runner.invoke(app, ["init", "--test"])
    
    # Check command succeeded
    assert result.exit_code == 0
    assert "Database initialized successfully" in result.stdout
    assert "test mode" in result.stdout
    
    # Verify mock was called with test_mode=True
    mock_create_db.assert_called_once_with(test_mode=True)
    
    # Create the directory to simulate successful DB creation after the test
    # This is just to ensure clean_db_path fixture can clean up properly
    os.makedirs(db_path, exist_ok=True)


def test_init_force_flag(clean_db_path):
    """Test that --force flag allows reinitializing an existing database."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME
    
    # Create a dummy file to simulate existing database
    os.makedirs(db_path, exist_ok=True)
    (db_path / "dummy.txt").write_text("test")
    
    # Run without force flag first - should not reinitialize
    result = runner.invoke(app, ["init", "--test"])
    assert "Database already exists" in result.stdout
    assert "Use --force to reinitialize" in result.stdout
    
    # Run with force flag - should reinitialize
    result = runner.invoke(app, ["init", "--test", "--force"])
    assert result.exit_code == 0
    assert "Database initialized successfully" in result.stdout


def test_clean_command(clean_db_path):
    """Test the clean command removes the database."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME
    
    # Create a dummy database
    os.makedirs(db_path, exist_ok=True)
    
    # Run clean command with auto-confirmation
    result = runner.invoke(app, ["clean"], input="y\n")
    
    # Check command succeeded
    assert result.exit_code == 0
    assert "has been removed" in result.stdout
    
    # Verify db was removed
    assert not db_path.exists()


def test_clean_nonexistent_db():
    """Test clean command handles case when database doesn't exist."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME
    
    # Ensure db doesn't exist
    if db_path.exists():
        shutil.rmtree(db_path)
    
    # Run clean command
    result = runner.invoke(app, ["clean"])
    
    # Check appropriate message
    assert "No database found to clean" in result.stdout
