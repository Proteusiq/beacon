from pathlib import Path
from typing import Final

# Data settings
DATA_PATH: Path = Path("data")
BOOKS_DB_PATH: Path = DATA_PATH / "books"
BOOKS_CSV_PATH: Path = DATA_PATH / "goodreads_top100_from1980to2023_final.csv"

# Filter settings
LANGUAGE: Final = "English"
MIN_REVIEWS: Final = 300

# Query settings
DEFAULT_LIMIT: Final = 5
