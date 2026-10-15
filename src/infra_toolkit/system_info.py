import platform


def get_system_info() -> dict[str, str]:
    """Return basic information about the current system.
    dict[str, str] is a type hint indicating that the function returns a dictionary with string keys and string values."""
    return {
        "operating_system": platform.system(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
    }
