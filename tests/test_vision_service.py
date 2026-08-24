from app.config import Settings
from app.vision.service import analyze_image
from tests.helpers import fixture_bytes


def test_starter_detection_pipeline_uses_detection_fixture() -> None:
    result = analyze_image(
        image_bytes=fixture_bytes("detection-scene.png"),
        filename="detection-scene.png",
        content_type="image/png",
        pipeline_id="starter-detection",
        settings=Settings(),
    )

    assert result.pipeline.id == "starter-detection"
    assert result.image.width == 320
    assert result.image.height == 240
    assert len(result.detections) >= 2
    assert result.detections[0].label == "primary-object"
    assert result.segmentations == []
    assert any(metric.name == "edge_density" for metric in result.metrics)
