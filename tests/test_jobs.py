from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_job_completes_and_exposes_result() -> None:
    created = client.post(
        "/api/v1/jobs", json={"task": "report", "payload": {"account": 42}}
    )
    assert created.status_code == 202
    response = client.get(f"/api/v1/jobs/{created.json()['id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["result"]["processed"] == {"account": 42}


def test_job_payload_is_validated() -> None:
    response = client.post("/api/v1/jobs", json={"task": "unknown"})
    assert response.status_code == 422
