from rich.console import Console
from rich.panel import Panel

def print_beginning(version):
    Console().print(
        Panel.fit(
            f"[bold cyan]Google Dorking Automation[/]\n[dim]Author:  Luke Lauterbach (Sentinel Technologies)\nVersion: {version}[/dim]",
            border_style="cyan",
            padding=(0, 2),
        )
    )