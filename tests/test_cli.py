import json

import pytest

from infra_toolkit.cli import main


def test_health_command_prints_status(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr("sys.argv", ["infra-toolkit", "health"])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Status: operational\n"
    assert captured.err == ""


def test_help_command_exits_successfully(
    monkeypatch,
) -> None:
    monkeypatch.setattr("sys.argv", ["infra-toolkit", "--help"])

    try:
        main()
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("Help should exit successfully")


def test_system_info_command_prints_system_details(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr("sys.argv", ["infra-toolkit", "system-info"])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "System Information" in captured.out
    assert "Operating system:" in captured.out
    assert "Python version:" in captured.out
    assert "Architecture:" in captured.out
    assert captured.err == ""


def test_resource_usage_command_prints_metrics(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr("sys.argv", ["infra-toolkit", "resource-usage"])
    monkeypatch.setattr(
        "infra_toolkit.cli.get_resource_usage",
        lambda: {
            "cpu_percent": 25.0,
            "memory_percent": 60.0,
            "disk_percent": 75.0,
        },
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == (
        "Resource Usage\n"
        "--------------\n"
        "CPU usage: 25.0%\n"
        "Memory usage: 60.0%\n"
        "Disk usage: 75.0%\n"
        "\n"
        "Status: All resource usage is within thresholds.\n"
    )
    assert captured.err == ""


def test_resource_usage_command_warns_when_threshold_exceeded(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr("sys.argv", ["infra-toolkit", "resource-usage"])
    monkeypatch.setattr(
        "infra_toolkit.cli.get_resource_usage",
        lambda: {
            "cpu_percent": 92.0,
            "memory_percent": 60.0,
            "disk_percent": 88.0,
        },
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "CPU usage: 92.0%" in captured.out
    assert "Disk usage: 88.0%" in captured.out
    assert "WARNING: Resource usage threshold exceeded (85%)." in captured.out
    assert "- CPU" in captured.out
    assert "- Disk" in captured.out
    assert "- Memory" not in captured.out
    assert captured.err == ""


def test_resource_usage_command_uses_custom_threshold(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["infra-toolkit", "resource-usage", "--threshold", "90"],
    )
    monkeypatch.setattr(
        "infra_toolkit.cli.get_resource_usage",
        lambda: {
            "cpu_percent": 92.0,
            "memory_percent": 85.0,
            "disk_percent": 88.0,
        },
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "WARNING: Resource usage threshold exceeded (90%)." in captured.out
    assert "- CPU" in captured.out
    assert "- Memory" not in captured.out
    assert "- Disk" not in captured.out
    assert captured.err == ""


@pytest.mark.parametrize(
    ("threshold", "error_message"),
    [
        ("-1", "Threshold must be between 0 and 100."),
        ("101", "Threshold must be between 0 and 100."),
        ("abc", "Threshold must be a number between 0 and 100."),
    ],
)
def test_resource_usage_command_rejects_invalid_threshold(
    monkeypatch,
    capsys,
    threshold,
    error_message,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["infra-toolkit", "resource-usage", "--threshold", threshold],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 2
    assert error_message in captured.err
    assert "Traceback" not in captured.err


def test_resource_usage_command_outputs_valid_json(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["infra-toolkit", "resource-usage", "--json"],
    )
    monkeypatch.setattr(
        "infra_toolkit.cli.get_resource_usage",
        lambda: {
            "cpu_percent": 25.0,
            "memory_percent": 60.0,
            "disk_percent": 75.0,
        },
    )

    exit_code = main()
    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 0
    assert result == {
        "cpu_percent": 25.0,
        "memory_percent": 60.0,
        "disk_percent": 75.0,
        "threshold": 85.0,
        "status": "ok",
        "violations": [],
    }
    assert captured.err == ""


def test_resource_usage_json_returns_one_when_threshold_exceeded(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "infra-toolkit",
            "resource-usage",
            "--threshold",
            "90",
            "--json",
        ],
    )
    monkeypatch.setattr(
        "infra_toolkit.cli.get_resource_usage",
        lambda: {
            "cpu_percent": 92.0,
            "memory_percent": 60.0,
            "disk_percent": 88.0,
        },
    )

    exit_code = main()
    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 1
    assert result["threshold"] == 90.0
    assert result["status"] == "threshold_exceeded"
    assert result["violations"] == ["cpu_percent"]
    assert captured.err == ""
