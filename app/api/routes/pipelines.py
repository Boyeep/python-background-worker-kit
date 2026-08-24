from fastapi import APIRouter

from app.schemas import PipelineCatalogResponse
from app.vision.service import list_pipelines

router = APIRouter(prefix="/api/v1")


@router.get("/pipelines", response_model=PipelineCatalogResponse, tags=["pipelines"])
def get_pipelines() -> PipelineCatalogResponse:
    return PipelineCatalogResponse(pipelines=list_pipelines())
