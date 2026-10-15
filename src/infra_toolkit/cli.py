import argparse
import json

from infra_toolkit.health import check_status
from infra_toolkit.resource_usage import get_resource_usage
from infra_toolkit.system_info import get_system_info
from infra_toolkit.thresholds import find_threshold_violations


def parse_threshold(value: str) -> float:
    """Parse and validate a resource usage threshold."""
    try:
        threshold = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Threshold must be a number between 0 and 100.") from exc

    if not 0.0 <= threshold <= 100.0:
        raise argparse.ArgumentTypeError("Threshold must be between 0 and 100.")

    return threshold


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="infra-toolkit",
        description="A toolkit for infrastructure operations.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("health", help="Check toolkit health")
    subparsers.add_parser("system-info", help="Display system information")
    resource_parser = subparsers.add_parser(
        "resource-usage",
        help="Display resource usage",
    )

    resource_parser.add_argument(
        "--threshold",
        type=parse_threshold,
        default=85.0,
        help="Resource usage warning threshold (default: 85%%).",
    )

    resource_parser.add_argument(
        "--json",
        action="store_true",
        help="Output resource usage as JSON.",
    )

    args = parser.parse_args()

    if args.command == "health":
        print(f"Status: {check_status()}")

    elif args.command == "system-info":
        info = get_system_info()
        print("System Information")
        print("------------------")
        print(f"Operating system: {info['operating_system']}")
        print(f"Python version: {info['python_version']}")
        print(f"Architecture: {info['architecture']}")

    elif args.command == "resource-usage":
        usage = get_resource_usage()
        violations = find_threshold_violations(
            usage,
            threshold=args.threshold,
        )

        if args.json:
            result = {
                **usage,
                "threshold": args.threshold,
                "status": "threshold_exceeded" if violations else "ok",
                "violations": violations,
            }
            print(json.dumps(result, indent=2))
            return 1 if violations else 0

        print("Resource Usage")
        print("--------------")
        # Display each percentage to one decimal place.
        print(f"CPU usage: {usage['cpu_percent']:.1f}%")
        print(f"Memory usage: {usage['memory_percent']:.1f}%")
        print(f"Disk usage: {usage['disk_percent']:.1f}%")

        if violations:
            print()
            print(f"WARNING: Resource usage threshold exceeded ({args.threshold:g}%).")

            resource_labels = {
                "cpu_percent": "CPU",
                "memory_percent": "Memory",
                "disk_percent": "Disk",
            }

            for resource in violations:
                print(f"- {resource_labels[resource]}")
        else:
            print()
            print("Status: All resource usage is within thresholds.")

        return 1 if violations else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
