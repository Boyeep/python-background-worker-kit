.PHONY: install dev check lint test run docker-up docker-down

install:
	python -m pip install -e ".[dev]"

dev:
	python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

run:
	python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

lint:
	python -m ruff check .

test:
	python -m pytest

check: lint test

docker-up:
	docker compose up --build

docker-down:
	docker compose down
