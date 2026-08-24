from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str


class PipelineSummary(BaseModel):
    id: str
    name: str
    summary: str
    tags: list[str]
    runtime: str
    sample_outputs: list[str]


class PipelineCatalogResponse(BaseModel):
    pipelines: list[PipelineSummary]


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Detection(BaseModel):
    label: str
    confidence: float = Field(ge=0, le=1)
    box: BoundingBox
    area_ratio: float | None = Field(default=None, ge=0, le=1)


class PolygonPoint(BaseModel):
    x: int
    y: int


class SegmentationRegion(BaseModel):
    label: str
    confidence: float = Field(ge=0, le=1)
    polygon: list[PolygonPoint]
    box: BoundingBox
    area_ratio: float | None = Field(default=None, ge=0, le=1)


class Metric(BaseModel):
    name: str
    value: float | int | str
    unit: str | None = None


class ImageMetadata(BaseModel):
    filename: str
    content_type: str
    width: int
    height: int


class AnalyzeResponse(BaseModel):
    analysis_id: str
    pipeline: PipelineSummary
    image: ImageMetadata
    detections: list[Detection]
    segmentations: list[SegmentationRegion]
    metrics: list[Metric]
    generated_at: datetime


class ErrorResponse(BaseModel):
    detail: str
