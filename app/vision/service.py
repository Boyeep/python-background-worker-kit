from datetime import UTC, datetime
from uuid import uuid4

import cv2
import numpy as np

from app.config import Settings
from app.schemas import (
    AnalyzeResponse,
    BoundingBox,
    Detection,
    ImageMetadata,
    Metric,
    PipelineSummary,
)
from app.vision.pipelines import PipelineDefinition


class UnknownPipelineError(ValueError):
    pass


class InvalidImageError(ValueError):
    pass


def _starter_detection(image: np.ndarray) -> tuple[list[dict], list[dict], list[dict]]:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    edges = cv2.Canny(blurred, 60, 140)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_area = image.shape[0] * image.shape[1]
    detections = []
    largest_area_ratio = 0.0

    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        x, y, width, height = cv2.boundingRect(contour)
        area_ratio = (width * height) / image_area
        if area_ratio < 0.01:
            continue

        largest_area_ratio = max(largest_area_ratio, area_ratio)
        label = "primary-object" if area_ratio >= 0.12 else "object-candidate"
        detections.append(
            {
                "label": label,
                "confidence": min(0.98, round(0.42 + area_ratio * 2.8, 3)),
                "box": BoundingBox(x=x, y=y, width=width, height=height),
                "area_ratio": round(area_ratio, 4),
            }
        )

    metrics = [
        {
            "name": "edge_density",
            "value": round(float(np.count_nonzero(edges)) / image_area, 4),
        },
        {"name": "object_candidates", "value": len(detections)},
        {"name": "largest_detection_ratio", "value": round(largest_area_ratio, 4)},
    ]

    return detections, [], metrics


PIPELINE_REGISTRY: dict[str, PipelineDefinition] = {
    "starter-detection": PipelineDefinition(
        id="starter-detection",
        name="Starter Detection",
        summary=(
            "Detection-first sample pipeline that returns object-style boxes "
            "and confidence scores."
        ),
        tags=["detection", "default", "cpu"],
        runtime="opencv-cpu",
        sample_outputs=["object boxes", "confidence scores", "coverage metrics"],
        handler=_starter_detection,
    ),
}


def list_pipelines() -> list[PipelineSummary]:
    return [
        PipelineSummary(
            id=item.id,
            name=item.name,
            summary=item.summary,
            tags=item.tags,
            runtime=item.runtime,
            sample_outputs=item.sample_outputs,
        )
        for item in PIPELINE_REGISTRY.values()
    ]


def analyze_image(
    *,
    image_bytes: bytes,
    filename: str,
    content_type: str,
    pipeline_id: str,
    settings: Settings,
) -> AnalyzeResponse:
    pipeline = PIPELINE_REGISTRY.get(pipeline_id)
    if pipeline is None:
        raise UnknownPipelineError(f"Unknown pipeline '{pipeline_id}'.")

    if len(image_bytes) > settings.max_upload_size_mb * 1024 * 1024:
        raise InvalidImageError(
            f"Upload exceeds the {settings.max_upload_size_mb} MB limit."
        )

    buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise InvalidImageError("Unable to decode the uploaded image.")

    raw_detections, _, raw_metrics = pipeline.handler(image)
    limited_detections = raw_detections[: settings.sample_max_detections]

    return AnalyzeResponse(
        analysis_id=f"analysis_{uuid4().hex[:12]}",
        pipeline=PipelineSummary(
            id=pipeline.id,
            name=pipeline.name,
            summary=pipeline.summary,
            tags=pipeline.tags,
            runtime=pipeline.runtime,
            sample_outputs=pipeline.sample_outputs,
        ),
        image=ImageMetadata(
            filename=filename,
            content_type=content_type,
            width=int(image.shape[1]),
            height=int(image.shape[0]),
        ),
        detections=[
            Detection(
                label=item["label"],
                confidence=item["confidence"],
                box=item["box"],
                area_ratio=item.get("area_ratio"),
            )
            for item in limited_detections
        ],
        segmentations=[],
        metrics=[
            Metric(
                name=item["name"],
                value=item["value"],
                unit=item.get("unit"),
            )
            for item in raw_metrics
        ],
        generated_at=datetime.now(UTC),
    )
