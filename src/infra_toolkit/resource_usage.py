from pathlib import Path

import psutil


def get_resource_usage() -> dict[str, float]:
    """Return current CPU, memory, and disk usage percentages."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage(Path.cwd()).percent

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "disk_percent": disk_percent,
    }
