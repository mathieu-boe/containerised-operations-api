from infra_toolkit.system_info import get_system_info


def test_get_system_info_returns_expected_keys() -> None:
    info = get_system_info()

    assert set(info.keys()) == {
        "operating_system",
        "python_version",
        "architecture",
    }


def test_get_system_info_returns_non_empty_strings() -> None:
    info = get_system_info()

    assert all(isinstance(value, str) and value for value in info.values())
