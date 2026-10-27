"""
cli.py – Command-Line Interface for Local Container Manager

Usage:
    python cli.py list [--running]
    python cli.py run <image> [--name NAME] [--port HOST:CONTAINER]
    python cli.py start <id_or_name>
    python cli.py stop <id_or_name>
    python cli.py remove <id_or_name> [--force]
    python cli.py inspect <id_or_name>
"""

import argparse
import sys
import logging
import json
import os
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text

from container_service import ContainerService

# ─── Logging Setup ────────────────────────────────────────────────────────────

LOG_FILE = Path(__file__).parent / "app.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ─── Config ───────────────────────────────────────────────────────────────────

CONFIG_FILE = Path(__file__).parent / "config.json"
if CONFIG_FILE.exists():
    with open(CONFIG_FILE) as f:
        config = json.load(f)
else:
    config = {}

console = Console()


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_service() -> ContainerService:
    try:
        return ContainerService()
    except ConnectionError as e:
        console.print(f"[bold red]{e}[/bold red]")
        sys.exit(1)


def print_banner():
    banner = Text("🐳  Local Container Manager  🐳", style="bold cyan")
    console.print(Panel(banner, box=box.DOUBLE_EDGE, style="cyan"))


# ─── Command Handlers ─────────────────────────────────────────────────────────

def cmd_list(args):
    """List all (or only running) containers."""
    service = get_service()
    show_all = not args.running
    try:
        containers = service.list_containers(all=show_all)
    except RuntimeError as e:
        console.print(str(e))
        return

    if not containers:
        console.print("[yellow]No containers found.[/yellow]")
        return

    table = Table(
        title=f"{'All' if show_all else 'Running'} Containers",
        box=box.ROUNDED,
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Image", style="yellow")
    table.add_column("Status", style="white")
    table.add_column("Created", style="dim")

    for c in containers:
        status_color = "green" if c["status"] == "running" else "red"
        table.add_row(
            c["id"],
            c["name"],
            c["image"],
            f"[{status_color}]{c['status']}[/{status_color}]",
            c["created"],
        )
    console.print(table)


def cmd_run(args):
    """Run a new container from an image."""
    service = get_service()
    ports = None
    if args.port:
        host_port, container_port = args.port.split(":")
        ports = {f"{container_port}/tcp": int(host_port)}

    console.print(f"[cyan]⏳  Starting container from image '[bold]{args.image}[/bold]'...[/cyan]")
    try:
        info = service.run_container(
            image=args.image,
            name=args.name or None,
            ports=ports,
        )
        console.print(f"[bold green]✅  Container started![/bold green]")
        console.print(f"   ID   : [cyan]{info['id']}[/cyan]")
        console.print(f"   Name : [green]{info['name']}[/green]")
        console.print(f"   Image: [yellow]{info['image']}[/yellow]")
    except RuntimeError as e:
        console.print(str(e))


def cmd_start(args):
    """Start a stopped container."""
    service = get_service()
    console.print(f"[cyan]⏳  Starting container '[bold]{args.id}[/bold]'...[/cyan]")
    try:
        service.start_container(args.id)
        console.print(f"[bold green]✅  Container '[cyan]{args.id}[/cyan]' started successfully.[/bold green]")
    except RuntimeError as e:
        console.print(str(e))


def cmd_stop(args):
    """Stop a running container."""
    service = get_service()
    console.print(f"[cyan]⏳  Stopping container '[bold]{args.id}[/bold]'...[/cyan]")
    try:
        service.stop_container(args.id)
        console.print(f"[bold green]✅  Container '[cyan]{args.id}[/cyan]' stopped successfully.[/bold green]")
    except RuntimeError as e:
        console.print(str(e))


def cmd_remove(args):
    """Remove a container."""
    service = get_service()
    console.print(f"[cyan]⏳  Removing container '[bold]{args.id}[/bold]'...[/cyan]")
    try:
        service.remove_container(args.id, force=args.force)
        console.print(f"[bold green]✅  Container '[cyan]{args.id}[/cyan]' removed.[/bold green]")
    except RuntimeError as e:
        console.print(str(e))


def cmd_inspect(args):
    """Inspect and display container details."""
    service = get_service()
    try:
        info = service.inspect_container(args.id)
    except RuntimeError as e:
        console.print(str(e))
        return

    status_color = "green" if info["status"] == "running" else "red"

    table = Table(
        title=f"Container Details – {info['name']}",
        box=box.ROUNDED,
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("Property", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Full ID", info["id"])
    table.add_row("Short ID", info["short_id"])
    table.add_row("Name", info["name"])
    table.add_row("Status", f"[{status_color}]{info['status']}[/{status_color}]")
    table.add_row("Image", info["image"])
    table.add_row("Created", info["created"])
    table.add_row("IP Address", info["ip_address"])
    table.add_row("Restart Count", str(info["restart_count"]))
    table.add_row("Platform", info["platform"])
    table.add_row("Command", " ".join(info["cmd"]) if info["cmd"] else "N/A")

    ports_str = ""
    for internal, bindings in info["ports"].items():
        if bindings:
            for b in bindings:
                ports_str += f"{b['HostPort']} → {internal}\n"
        else:
            ports_str += f"{internal} (not published)\n"
    table.add_row("Ports", ports_str.strip() or "None")

    console.print(table)


# ─── Argument Parser ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lcm",
        description="🐳  Local Container Manager – Manage Docker containers easily.",
    )
    subparsers = parser.add_subparsers(title="commands", dest="command", metavar="<command>")
    subparsers.required = True

    # list
    p_list = subparsers.add_parser("list", help="List containers")
    p_list.add_argument("--running", action="store_true", help="Show only running containers")
    p_list.set_defaults(func=cmd_list)

    # run
    p_run = subparsers.add_parser("run", help="Run a container from an image")
    p_run.add_argument("image", help="Docker image (e.g. nginx, ubuntu:22.04)")
    p_run.add_argument("--name", help="Optional container name")
    p_run.add_argument("--port", metavar="HOST:CONTAINER", help="Port mapping, e.g. 8080:80")
    p_run.set_defaults(func=cmd_run)

    # start
    p_start = subparsers.add_parser("start", help="Start a stopped container")
    p_start.add_argument("id", metavar="id_or_name", help="Container name or ID")
    p_start.set_defaults(func=cmd_start)

    # stop
    p_stop = subparsers.add_parser("stop", help="Stop a running container")
    p_stop.add_argument("id", metavar="id_or_name", help="Container name or ID")
    p_stop.set_defaults(func=cmd_stop)

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove a container")
    p_remove.add_argument("id", metavar="id_or_name", help="Container name or ID")
    p_remove.add_argument("--force", action="store_true", help="Force remove even if running")
    p_remove.set_defaults(func=cmd_remove)

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Show detailed info about a container")
    p_inspect.add_argument("id", metavar="id_or_name", help="Container name or ID")
    p_inspect.set_defaults(func=cmd_inspect)

    return parser


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    print_banner()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
