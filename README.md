# Python Computer Vision API Kit

A backend-only template for building typed computer-vision APIs with FastAPI,
OpenCV, NumPy, and Pydantic. It contains no frontend application or JavaScript
toolchain.

## Included

- health, pipeline catalog, and image-analysis endpoints
- detection-first response contracts with optional segmentation support
- an OpenCV CPU sample pipeline that is easy to replace
- upload validation and normalized API errors
- committed image fixtures and snapshot-backed tests
- Docker development and production targets
- an OpenAPI contract in `docs/openapi.yaml`

## Requirements

- Python 3.12+
- Docker and Docker Compose (optional)

## Local development

```bash
python -m venv .venv
```

Activate the virtual environment, then run:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive documentation is
available at `http://127.0.0.1:8000/docs`.

Copy `.env.example` to `.env` before changing local configuration.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Runtime health |
| `GET` | `/api/v1/pipelines` | Available vision pipelines |
| `POST` | `/api/v1/analyze` | Analyze an uploaded image |

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyze \
  -F "pipeline_id=starter-detection" \
  -F "file=@tests/fixtures/detection-scene.png"
```

## Quality checks

```bash
python -m ruff check .
python -m pytest
```

Or, where Make is available:

```bash
make check
```

## Docker

```bash
docker compose up --build
```

The `app/vision` package is the replacement boundary for a real YOLO, ONNX
Runtime, TensorRT, or hosted inference implementation. Keep HTTP concerns in
`app/api/routes` and model-specific processing inside `app/vision`.
