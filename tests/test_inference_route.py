from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import fixture_bytes, normalize_analysis_payload, snapshot_json

client = TestClient(app)


def test_analyze_route_matches_starter_detection_snapshot() -> None:
    response = client.post(
        "/api/v1/analyze",
        data={"pipeline_id": "starter-detection"},
        files={
            "file": (
                "detection-scene.png",
                fixture_bytes("detection-scene.png"),
                "image/png",
            )
        },
    )

    assert response.status_code == 200
    assert normalize_analysis_payload(response.json()) == snapshot_json(
        "starter-detection-response.json"
    )


def test_analyze_route_rejects_non_image_upload() -> None:
    response = client.post(
        "/api/v1/analyze",
        data={"pipeline_id": "starter-detection"},
        files={"file": ("notes.txt", b"not-an-image", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only image uploads are supported."
