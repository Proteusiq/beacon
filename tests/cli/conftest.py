import shutil

import pytest

from beacon.settings import BOOKS_DB_PATH, DEFAULT_COLLECTION_NAME


@pytest.fixture
def clean_db_path():
    """ensure the database directory is clean before and after tests."""
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME

    if db_path.exists():
        shutil.rmtree(db_path)

    BOOKS_DB_PATH.mkdir(parents=True, exist_ok=True)

    yield

    if db_path.exists():
        shutil.rmtree(db_path)
