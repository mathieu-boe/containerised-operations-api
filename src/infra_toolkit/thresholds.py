from collections.abc import Mapping


def find_threshold_violations(
    usage: Mapping[str, float],
    threshold: float = 85.0,
) -> list[str]:
    """Return resource names whose usage exceeds the threshold."""
    if not 0.0 <= threshold <= 100.0:
        raise ValueError("Threshold must be between 0 and 100.")

    return [resource for resource, percentage in usage.items() if percentage > threshold]
