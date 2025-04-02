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
uv run beacon-db init
uv run beacon-db init --test
uv run beacon-db init --force
uv run beacon-db clean
```

## Adding New CLI Tools

When adding new CLI tools:

1. Create a new Python module in this directory
2. Use Typer to define your commands
3. Add an entry point in pyproject.toml if needed
4. Update this README with usage instructions
