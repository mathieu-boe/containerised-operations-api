from fastapi import FastAPI, Query

from infra_toolkit.health import check_status
from infra_toolkit.resource_usage import get_resource_usage
from infra_toolkit.system_info import get_system_info
from infra_toolkit.thresholds import find_threshold_violations

app = FastAPI(
    title="Infrastructure Operations API",
    description="An API for infrastructure health checks and operational reporting.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the health status of the API."""
    return {"status": check_status()}


@app.get("/system-info")
def system_info() -> dict[str, str]:
    """Return information about the system running the API."""
    return get_system_info()


@app.get("/resource-usage")
def resource_usage(
    threshold: float = Query(default=85.0, ge=0.0, le=100.0),
) -> dict[str, float | str | list[str]]:
    """Return resource usage and threshold evaluation."""
    usage = get_resource_usage()
    violations = find_threshold_violations(usage, threshold=threshold)

    return {
        **usage,
        "threshold": threshold,
        "status": "threshold_exceeded" if violations else "ok",
        "violations": violations,
    }
