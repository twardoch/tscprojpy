# this_file: tscprojpy/src/tscprojpy/cli.py
"""Command-line interface for tscprojpy."""

import fire
from rich.console import Console
from rich.panel import Panel

from . import __version__

console = Console()


def version():
    """Display version information."""
    console.print(
        Panel.fit(
            f"[bold cyan]tscprojpy[/bold cyan] version [bold green]{__version__}[/bold green]",
            title="Version Info",
        )
    )


def hello(name: str = "World"):
    """Say hello to someone.
    
    Args:
        name: Name to greet (default: World)
    """
    console.print(f"[bold green]Hello, {name}![/bold green]")


def main():
    """Main entry point for the CLI."""
    fire.Fire({
        "version": version,
        "hello": hello,
    })


if __name__ == "__main__":
    main()