# Beacon CLI Tools

This directory contains command-line interface tools for the Beacon project.

## Database Management

The `db.py` module provides tools for initializing and managing the vector database.

### Usage

Run the commands using `uv run`:

```bash
# Initialize the database with full data
uv run -m beacon.cli.db init

# Initialize with test data only (smaller dataset)
uv run -m beacon.cli.db init --test

# Force reinitialization even if database exists
uv run -m beacon.cli.db init --force

# Remove the existing database
uv run -m beacon.cli.db clean
```

If you've installed the package in development mode:

```bash
uv run beacon init
uv run beacon init --test
uv run beacon init --force
uv run beacon clean
```
