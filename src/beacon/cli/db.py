"""Database management CLI for Beacon.

This module provides command-line tools for initializing and managing the vector database.

Usage:
    # Run with uv
    uv run -m beacon.cli.db init
    uv run -m beacon.cli.db init --test
    uv run -m beacon.cli.db clean
    
    # Or if installed in development mode
    uv run beacon-db init
    uv run beacon-db init --test
    uv run beacon-db clean
"""
import os
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from beacon.crud.create import create_db
from beacon.settings import BOOKS_DB_PATH, DEFAULT_COLLECTION_NAME

app = typer.Typer(help="Beacon database management tools")
console = Console()


@app.command()
def init(
    test_mode: bool = typer.Option(
        False, "--test", "-t", help="Initialize with test data only (smaller dataset)"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force reinitialization even if database exists"
    ),
) -> None:
    """Initialize the vector database with book data.

    This command loads book data from the configured source and creates a vector database
    for similarity search. By default, it will not overwrite an existing database.
    """
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME
    
    # Check if database already exists
    if db_path.exists() and not force:
        console.print(
            Panel(
                "[yellow]Database already exists![/]\n\n"
                f"Path: [bold]{db_path}[/]\n\n"
                "Use [bold]--force[/] to reinitialize.",
                title="⚠️ Warning",
                expand=False,
            )
        )
        return

    # Create parent directories if they don't exist
    os.makedirs(BOOKS_DB_PATH, exist_ok=True)
    
    # Initialize with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Initializing {'test ' if test_mode else ''}database...", total=None
        )
        
        try:
            create_db(test_mode=test_mode)
            progress.update(task, completed=True)
            
            mode_text = "[bold yellow]test mode[/]" if test_mode else "[bold green]full mode[/]"
            console.print(
                Panel(
                    f"Database initialized successfully in {mode_text}!\n\n"
                    f"Path: [bold]{db_path}[/]",
                    title="✅ Success",
                    expand=False,
                )
            )
        except Exception as e:
            progress.update(task, completed=True)
            console.print(
                Panel(
                    f"[bold red]Error:[/] {str(e)}",
                    title="❌ Failed",
                    expand=False,
                )
            )
            raise typer.Exit(code=1)


@app.command()
def clean() -> None:
    """Remove the existing vector database.
    
    This command deletes the database files completely.
    """
    db_path = BOOKS_DB_PATH / DEFAULT_COLLECTION_NAME
    
    if not db_path.exists():
        console.print(
            Panel(
                "No database found to clean.",
                title="ℹ️ Info",
                expand=False,
            )
        )
        return
    
    if typer.confirm(f"Are you sure you want to delete the database at {db_path}?"):
        try:
            import shutil
            shutil.rmtree(db_path)
            console.print(
                Panel(
                    f"Database at [bold]{db_path}[/] has been removed.",
                    title="✅ Success",
                    expand=False,
                )
            )
        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]Error:[/] {str(e)}",
                    title="❌ Failed",
                    expand=False,
                )
            )
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
