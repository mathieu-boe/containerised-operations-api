import pytest

from infra_toolkit.thresholds import find_threshold_violations


def test_returns_no_violations_when_usage_is_below_threshold() -> None:
    usage = {
        "cpu_percent": 40.0,
        "memory_percent": 60.0,
        "disk_percent": 70.0,
    }

    assert find_threshold_violations(usage) == []


def test_returns_resources_exceeding_threshold() -> None:
    usage = {
        "cpu_percent": 92.0,
        "memory_percent": 70.0,
        "disk_percent": 88.0,
    }

    assert find_threshold_violations(usage) == [
        "cpu_percent",
        "disk_percent",
    ]


def test_usage_equal_to_threshold_is_not_a_violation() -> None:
    usage = {"cpu_percent": 85.0}

    assert find_threshold_violations(usage) == []


@pytest.mark.parametrize("threshold", [-1.0, 100.1])
def test_rejects_invalid_threshold(threshold: float) -> None:
    with pytest.raises(ValueError, match="Threshold must be between 0 and 100"):
        find_threshold_violations({}, threshold)
