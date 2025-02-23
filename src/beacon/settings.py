from pathlib import Path
from typing import Final

# data settings
DATA_PATH: Path = Path("data")
BOOKS_DB_PATH: Path = DATA_PATH / "books"
BOOKS_CSV_URI: str = (
    "https://raw.githubusercontent.com/Proteusiq/igia/refs/heads/main/data/goodreads_top100_from1980to2023_final.csv"
)

# filter settings
LANGUAGE: Final = "English"
MIN_REVIEWS: Final = 300

# query settings
DEFAULT_LIMIT: Final = 5
DEFAULT_COLLECTION_NAME: Final = "books"
