"""
cli.py
Command-Line Interface for Local Container Manager
Student: Kushagra Kaushik | Roll: S24BCAU0112
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import argparse
import sys
import json
from src.container_manager import ContainerManager


def print_table(headers: list, rows: list):
    """Pretty-print a table to stdout."""
    if not rows:
        print("  (no results)")
        return
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in widths)
    sep = "  " + "  ".join("-" * w for w in widths)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        print(fmt.format(*[str(v) for v in row]))


def cmd_list(manager: ContainerManager, args):
    """Handler: lcm list"""
    containers = manager.list_containers(all_containers=args.all)
    if not containers:
        print("No containers found." + (" (try --all to see stopped ones)" if not args.all else ""))
        return
    headers = ["ID", "Image", "Status", "Names", "Ports"]
    rows = [
        [
            c.get("ID", "")[:12],
            c.get("Image", ""),
            c.get("Status", ""),
            c.get("Names", ""),
            c.get("Ports", ""),
        ]
        for c in containers
    ]
    print_table(headers, rows)


def cmd_run(manager: ContainerManager, args):
    """Handler: lcm run"""
    env = {}
    if args.env:
        for e in args.env:
            if "=" in e:
                k, v = e.split("=", 1)
                env[k] = v

    print(f"  Starting container from image: {args.image} ...")
    result = manager.run_container(
        image=args.image,
        name=args.name,
        port=args.port,
        detach=not args.interactive,
        env=env or None,
    )
    if result["success"]:
        cid = result.get("container_id", result["stdout"][:12])
        print(f"  [OK] Container started! ID: {cid}")
    else:
        print(f"  [ERR] Error: {result['stderr']}")
        sys.exit(1)


def cmd_start(manager: ContainerManager, args):
    """Handler: lcm start"""
    result = manager.start_container(args.container)
    if result["success"]:
        print(f"  [OK] Container '{args.container}' started.")
    else:
        print(f"  [ERR] Error: {result['stderr']}")
        sys.exit(1)


def cmd_stop(manager: ContainerManager, args):
    """Handler: lcm stop"""
    result = manager.stop_container(args.container)
    if result["success"]:
        print(f"  [OK] Container '{args.container}' stopped.")
    else:
        print(f"  [ERR] Error: {result['stderr']}")
        sys.exit(1)


def cmd_inspect(manager: ContainerManager, args):
    """Handler: lcm inspect"""
    result = manager.inspect_container(args.container)
    if result["success"]:
        data = result.get("data", {})
        print(f"\n  Container: {data.get('Name', args.container)}")
        print(f"  Image:     {data.get('Config', {}).get('Image', 'N/A')}")
        print(f"  Status:    {data.get('State', {}).get('Status', 'N/A')}")
        print(f"  IP:        {data.get('NetworkSettings', {}).get('IPAddress', 'N/A')}")
        if args.json:
            print("\n  Full JSON:")
            print(json.dumps(data, indent=2))
    else:
        print(f"  ✘ Error: {result['stderr']}")
        sys.exit(1)


def cmd_remove(manager: ContainerManager, args):
    """Handler: lcm remove"""
    if not args.force:
        confirm = input(f"  Remove container '{args.container}'? [y/N] ")
        if confirm.lower() != "y":
            print("  Aborted.")
            return
    result = manager.remove_container(args.container, force=args.force)
    if result["success"]:
        print(f"  [OK] Container '{args.container}' removed.")
    else:
        print(f"  [ERR] Error: {result['stderr']}")
        sys.exit(1)


def cmd_logs(manager: ContainerManager, args):
    """Handler: lcm logs"""
    result = manager.get_logs(args.container, tail=args.tail)
    if result["success"]:
        print(result["stdout"])
        if result["stderr"]:
            print(result["stderr"])
    else:
        print(f"  [ERR] Error: {result['stderr']}")
        sys.exit(1)


def cmd_images(manager: ContainerManager, args):
    """Handler: lcm images"""
    images = manager.list_images()
    if not images:
        print("  No images found locally.")
        return
    headers = ["Repository", "Tag", "ID", "Size"]
    rows = [
        [
            img.get("Repository", ""),
            img.get("Tag", ""),
            img.get("ID", "")[:12],
            img.get("Size", ""),
        ]
        for img in images
    ]
    print_table(headers, rows)


def cmd_pull(manager: ContainerManager, args):
    """Handler: lcm pull"""
    print(f"  Pulling image: {args.image} ...")
    result = manager.pull_image(args.image)
    if result["success"]:
        print(f"  [OK] Image '{args.image}' pulled successfully.")
    else:
        print(f"  [ERR] Error: {result['stderr']}")
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lcm",
        description="LCM - Local Container Manager | CBCA321 | Kushagra Kaushik (S24BCAU0112)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lcm list                     # Show running containers
  lcm list --all               # Show all containers
  lcm run nginx --name web -p 8080:80
  lcm stop web
  lcm remove web
  lcm inspect web --json
  lcm logs web --tail 100
  lcm images
  lcm pull python:3.10
        """,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # list
    p_list = sub.add_parser("list", help="List containers")
    p_list.add_argument("-a", "--all", action="store_true", help="Show stopped containers too")
    p_list.set_defaults(func=cmd_list)

    # run
    p_run = sub.add_parser("run", help="Run a new container")
    p_run.add_argument("image", help="Docker image to run")
    p_run.add_argument("--name", help="Container name")
    p_run.add_argument("-p", "--port", help="Port mapping e.g. 8080:80")
    p_run.add_argument("-e", "--env", action="append", metavar="KEY=VALUE", help="Environment variable")
    p_run.add_argument("-i", "--interactive", action="store_true", help="Run interactively (foreground)")
    p_run.set_defaults(func=cmd_run)

    # start
    p_start = sub.add_parser("start", help="Start a stopped container")
    p_start.add_argument("container", help="Container ID or name")
    p_start.set_defaults(func=cmd_start)

    # stop
    p_stop = sub.add_parser("stop", help="Stop a running container")
    p_stop.add_argument("container", help="Container ID or name")
    p_stop.set_defaults(func=cmd_stop)

    # inspect
    p_inspect = sub.add_parser("inspect", help="Inspect a container")
    p_inspect.add_argument("container", help="Container ID or name")
    p_inspect.add_argument("--json", action="store_true", help="Show full JSON output")
    p_inspect.set_defaults(func=cmd_inspect)

    # remove
    p_remove = sub.add_parser("remove", aliases=["rm"], help="Remove a container")
    p_remove.add_argument("container", help="Container ID or name")
    p_remove.add_argument("-f", "--force", action="store_true", help="Force remove running container")
    p_remove.set_defaults(func=cmd_remove)

    # logs
    p_logs = sub.add_parser("logs", help="View container logs")
    p_logs.add_argument("container", help="Container ID or name")
    p_logs.add_argument("--tail", type=int, default=50, help="Number of lines (default: 50)")
    p_logs.set_defaults(func=cmd_logs)

    # images
    p_images = sub.add_parser("images", help="List local images")
    p_images.set_defaults(func=cmd_images)

    # pull
    p_pull = sub.add_parser("pull", help="Pull an image from Docker Hub")
    p_pull.add_argument("image", help="Image name e.g. nginx, python:3.10")
    p_pull.set_defaults(func=cmd_pull)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        manager = ContainerManager()
    except EnvironmentError as e:
        print(f"\n  [ERR] {e}\n")
        sys.exit(1)

    args.func(manager, args)


if __name__ == "__main__":
    main()
