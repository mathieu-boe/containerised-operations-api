from unittest.mock import patch

from infra_toolkit.resource_usage import get_resource_usage


def test_get_resource_usage_returns_expected_metrics() -> None:
    with (
        patch(
            "infra_toolkit.resource_usage.psutil.cpu_percent",
            return_value=25.0,
        ),
        patch("infra_toolkit.resource_usage.psutil.virtual_memory") as mock_memory,
        patch("infra_toolkit.resource_usage.psutil.disk_usage") as mock_disk,
    ):
        mock_memory.return_value.percent = 60.0
        mock_disk.return_value.percent = 75.0

        usage = get_resource_usage()

    assert usage == {
        "cpu_percent": 25.0,
        "memory_percent": 60.0,
        "disk_percent": 75.0,
    }


""" The following function calls on actual system value, we want the tests to be deterministic for now.

def test_get_resource_usage_returns_percentages_in_valid_range() -> None:
    usage = get_resource_usage()

    assert set(usage) == {
        "cpu_percent",
        "memory_percent",
        "disk_percent",
    }
    assert all(0.0 <= value <= 100.0 for value in usage.values())"""


def test_get_resource_usage_returns_percentages_in_valid_range() -> None:
    with (
        patch(
            "infra_toolkit.resource_usage.psutil.cpu_percent",
            return_value=12.5,
        ),
        patch("infra_toolkit.resource_usage.psutil.virtual_memory") as mock_memory,
        patch("infra_toolkit.resource_usage.psutil.disk_usage") as mock_disk,
    ):
        mock_memory.return_value.percent = 45.0
        mock_disk.return_value.percent = 80.0

        usage = get_resource_usage()

    assert set(usage) == {
        "cpu_percent",
        "memory_percent",
        "disk_percent",
    }
    assert all(0.0 <= value <= 100.0 for value in usage.values())
