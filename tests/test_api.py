from unittest.mock import patch

from fastapi.testclient import TestClient

from infra_toolkit.api import app

client = TestClient(app)


def test_health_endpoint_returns_operational_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "operational"}


def test_system_info_endpoint_returns_system_details() -> None:
    response = client.get("/system-info")

    assert response.status_code == 200
    assert set(response.json()) == {
        "operating_system",
        "python_version",
        "architecture",
    }


@patch("infra_toolkit.api.get_resource_usage")
def test_resource_usage_endpoint_returns_usage(mock_usage) -> None:
    mock_usage.return_value = {
        "cpu_percent": 20.0,
        "memory_percent": 40.0,
        "disk_percent": 60.0,
    }

    response = client.get("/resource-usage")

    assert response.status_code == 200
    assert response.json() == {
        "cpu_percent": 20.0,
        "memory_percent": 40.0,
        "disk_percent": 60.0,
        "threshold": 85.0,
        "status": "ok",
        "violations": [],
    }


def test_resource_usage_endpoint_rejects_invalid_threshold() -> None:
    response = client.get("/resource-usage?threshold=101")

    assert response.status_code == 422
