import warnings

from beacon import settings
from beacon.recommender import recommend

__all__ = [
    "recommend",
]

COLLECTION = settings.BOOKS_DB_PATH / "collection"

if not COLLECTION.exists() or not any(COLLECTION.iterdir()):
    warnings.warn(
        "Database is Empty. Run `uv run python -m beacon.setup`",
        category=ResourceWarning,
        stacklevel=2,
    )
