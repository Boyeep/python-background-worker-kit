# Python Background Worker Kit

FastAPI + Celery + Redis starter for reliable asynchronous workloads.

## Included

- typed job submission, status, progress, result, and cancellation APIs
- separate API, worker, Redis, and scheduler services
- automatic exponential-backoff retry example
- Celery Beat scheduled heartbeat
- eager local/test mode that works without Redis
- task metadata suitable for a custom dashboard or Flower
- Docker Compose, Ruff, Pytest, and CI

Run the production-shaped stack with `docker compose up --build`. For a
dependency-free local test loop, install `.[dev]`, leave `WORKER_EAGER=true`,
and run `python -m uvicorn app.main:app --reload`.

Submit work through `POST /api/v1/jobs`, then poll `GET /api/v1/jobs/{id}`.
