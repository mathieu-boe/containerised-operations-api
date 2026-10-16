# Containerised Operations API

A Python-based infrastructure operations API and CLI, built as part of my hands-on AWS and DevOps portfolio. This project builds on reusable [infrastructure monitoring logic](https://github.com/mathieu-boe/python-infrastructure-toolkit) and extends it with a REST API, automated testing, and containerisation.

## Objectives

- Reuse practical Python infrastructure operations logic in a standalone application.
- Expose health checks, system information, and resource monitoring through a REST API.
- Apply automated testing, linting, and formatting checks.
- Package the application for consistent execution using Docker.
- Practise Linux, Git, GitHub Actions, and professional software development workflows.
- Build towards cloud operations, containerisation, and AWS deployment use cases.

## Current status

**Milestone 1 — Project setup and infrastructure toolkit integration** (completed)

- [x] Independent repository created for Project 2.
- [x] Python package structure copied into the new repository.
- [x] Existing infrastructure health-check logic integrated.
- [x] Existing system information and resource monitoring modules integrated.
- [x] Existing threshold evaluation logic integrated.
- [x] CLI and its automated tests included.
- [x] Project metadata updated for the Containerised Operations API.
- [x] Initial quality checks verified in the new repository.
- [x] Initial Git commit created.

**Milestone 2 — REST API implementation** (implemented locally)

- [x] FastAPI application created in `src/infra_toolkit/api.py`.
- [x] `GET /health` endpoint implemented.
- [x] `GET /system-info` endpoint implemented.
- [x] `GET /resource-usage` endpoint implemented.
- [x] Configurable resource threshold supported through a query parameter.
- [x] Threshold validation configured to accept values from 0 to 100, inclusive.
- [x] API responses include resource measurements, evaluation status, and threshold violations.
- [x] Automated API tests added.
- [x] API manually tested using HTTP requests.
- [x] All tests and quality checks verified in the new repository.

**Milestone 3 — Containerisation with Docker** (implemented locally)

- [x] Dockerfile created for the API application.
- [x] `.dockerignore` configured to exclude unnecessary files.
- [x] Docker image builds successfully.
- [x] API runs inside a container.
- [x] API endpoints tested against the running container.
- [x] Container port mapping and runtime configuration documented.
- [x] Container execution verified without requiring AWS resources.

**Milestone 4 — Continuous integration with GitHub Actions** (completed)

- [x] GitHub Actions workflow included in the repository.
- [x] Workflow configured to install the project and development dependencies.
- [x] Ruff linting and formatting checks configured.
- [x] pytest execution configured.
- [x] Workflow verified against the new repository.
- [x] Docker build validation added to CI.
- [x] All required CI checks passing on GitHub.

**Milestone 5 — Documentation and project verification** (completed)

- [x] README structure established to match the Infrastructure Automation Toolkit project.
- [x] Local setup and API usage documented.
- [x] Docker build and run instructions verified.
- [x] All local tests and quality checks passing.
- [x] GitHub Actions pipeline passing.
- [x] Repository committed and pushed to GitHub.

## Development

The project uses Python 3.14+, FastAPI for the REST API, Uvicorn for the development server, and `psutil` for resource monitoring. pytest provides automated testing, while Ruff handles linting and formatting.

A local virtual environment is stored in `.venv/` and excluded from version control through `.gitignore`.

### Clone the repository

Clone using SSH or HTTPS:

```bash
# SSH (requires an SSH key configured with GitHub)
git clone git@github.com:mathieu-boe/containerised-operations-api.git

# Alternatively, use HTTPS
git clone https://github.com/mathieu-boe/containerised-operations-api.git
```

Enter the project directory and create a virtual environment:

```bash
cd containerised-operations-api
python3 -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode with its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

### Run the API

Start the development server from the repository root:

```bash
python -m uvicorn infra_toolkit.api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Stop the server with `Ctrl+C`.

### Health check endpoint

Request the API health status:

```bash
curl http://127.0.0.1:8000/health
```

Expected output:

```json
{
  "status": "operational"
}
```

The endpoint provides a simple operational status response.

### System information endpoint

Request information about the environment running the API:

```bash
curl http://127.0.0.1:8000/system-info
```

Example output:

```json
{
  "operating_system": "Linux",
  "python_version": "3.14.4",
  "architecture": "x86_64"
}
```

*Note: The output reflects the environment where the API is executed, so values may differ across operating systems and machines.*

### Resource usage endpoint

Request current CPU, memory, and disk usage:

```bash
curl http://127.0.0.1:8000/resource-usage
```

Example output:

```json
{
  "cpu_percent": 1.0,
  "memory_percent": 7.5,
  "disk_percent": 0.5,
  "threshold": 85.0,
  "status": "ok",
  "violations": []
}
```

*Note: These percentages are illustrative. Actual values depend on system activity and the environment where the application runs.*

The endpoint returns the resource measurements, configured threshold, evaluation status, and a list of resources exceeding the threshold.

### Configurable resource thresholds

Override the default threshold of 85% using the `threshold` query parameter:

```bash
curl "http://127.0.0.1:8000/resource-usage?threshold=90"
```

Decimal thresholds are supported:

```bash
curl "http://127.0.0.1:8000/resource-usage?threshold=87.5"
```

When resource usage exceeds the configured threshold, the response reports `threshold_exceeded` and identifies the affected resources.

Example response:

```json
{
  "cpu_percent": 92.0,
  "memory_percent": 60.0,
  "disk_percent": 88.0,
  "threshold": 90.0,
  "status": "threshold_exceeded",
  "violations": [
    "cpu_percent"
  ]
}
```

A warning is triggered only when resource usage **exceeds** the configured threshold; usage equal to the threshold does not trigger a violation.

Thresholds outside the inclusive range of 0–100 are rejected by API validation. For example:

```bash
curl "http://127.0.0.1:8000/resource-usage?threshold=101"
```

This request returns HTTP status `422 Unprocessable Entity`.

### Interactive API documentation

FastAPI generates interactive API documentation automatically.

Open the following URL while the development server is running:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema is available at:

```text
http://127.0.0.1:8000/openapi.json
```

The interactive documentation can be used to inspect endpoint parameters, view response schemas, and send test requests.

### Command-line interface

The project retains the `infra-toolkit` CLI for local infrastructure operations.

Run a health check:

```bash
infra-toolkit health
```

Expected output:

```text
Status: operational
```

Display system information:

```bash
infra-toolkit system-info
```

Monitor resource usage:

```bash
infra-toolkit resource-usage
```

Use a custom threshold and JSON output:

```bash
infra-toolkit resource-usage --threshold 90 --json
```

The CLI provides an alternative to making HTTP requests when running infrastructure checks locally.

### Exit codes

The `resource-usage` CLI command uses exit codes so that scripts and CI pipelines can react to monitoring results.

| Exit code | Meaning |
|---|---|
| `0` | Monitoring completed; no threshold exceeded. |
| `1` | Monitoring completed; at least one threshold exceeded. |
| `2` | Invalid command-line arguments. |

The same monitoring exit codes apply to human-readable and JSON output. The `health` and `system-info` commands return `0` when successful.

### Docker containerisation

Docker packages the application and its runtime dependencies into an image, allowing the API to run consistently across compatible environments.

The container uses Python 3.14 slim, installs the application from `pyproject.toml`, and runs Uvicorn as a non-root user. The image excludes development files, tests, local virtual environments, and Git metadata from its build context.

## Build the image

Run from the repository root:

```bash
docker build -t containerised-operations-api:0.1.0 .
```

## Start the container

```bash
docker run -d \
  --name operations-api \
  -p 8000:8000 \
  containerised-operations-api:0.1.0
```

The API is available on the host at `http://localhost:8000`.

## Test the endpoints

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/system-info
curl -i "http://localhost:8000/resource-usage?threshold=85"
```

The health endpoint should return HTTP `200 OK` with an operational status. The system information and resource usage endpoints should also return HTTP `200 OK`.

Test input validation with an invalid threshold:

```bash
curl -i "http://localhost:8000/resource-usage?threshold=101"
```

This should return HTTP `422`, because thresholds must be between 0 and 100 inclusive.

## Inspect and stop the container

```bash
docker ps
docker logs operations-api
docker stop operations-api
docker rm operations-api
```

The final two commands stop and remove the container. The built image remains available locally.

## Containerisation notes

- The container listens on port `8000`; the `-p 8000:8000` option publishes that port on the host.
- The API runs as a non-root user inside the container.
- Resource measurements describe the environment visible to the application inside the container and may differ from host-level measurements.
- Local Docker testing does not require AWS credentials or AWS infrastructure.

### Run quality checks and automated tests

Run these commands from the repository root with the virtual environment activated:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -v
```

To apply automatic formatting:

```bash
python -m ruff format .
```

The automated test suite covers the infrastructure toolkit, CLI behaviour, threshold evaluation, and API endpoints. Resource measurements are mocked where appropriate to keep tests deterministic.

### Continuous integration

The GitHub Actions workflow, named **CI - Python Quality and Docker Build**, runs when code is pushed to `main` or a pull request targets `main`.

The `quality` job installs the project and development dependencies, runs Ruff linting and formatting checks, and executes the automated test suite. The `docker-build` job builds the Docker image to validate the Dockerfile and image build process without publishing the image to a registry.

## Security and cost

The application runs locally during development and does not require AWS credentials or provision AWS resources. Local API and Docker testing should not incur AWS infrastructure costs.

The API exposes system information and resource usage for the environment where it runs. These endpoints should be reviewed before exposing the application to an untrusted network.

Secrets, local virtual environments, generated build metadata, and unnecessary development files must not be committed to version control.

This project is a learning exercise. A production deployment would require additional controls such as authentication, network restrictions, container resource limits, secure configuration, and operational monitoring.
