from infra_toolkit.health import check_status


def test_check_status_returns_operational() -> None:
    assert check_status() == "operational"
