from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.config import get_settings
from app.schemas import AnalyzeResponse
from app.vision.service import InvalidImageError, UnknownPipelineError, analyze_image

router = APIRouter(prefix="/api/v1")


@router.post("/analyze", response_model=AnalyzeResponse, tags=["inference"])
async def analyze_image_route(
    file: UploadFile = File(...),
    pipeline_id: str = Form(...),
) -> AnalyzeResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image uploads are supported.",
        )

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file was empty.",
        )

    try:
        return analyze_image(
            image_bytes=image_bytes,
            filename=file.filename or "upload",
            content_type=file.content_type,
            pipeline_id=pipeline_id,
            settings=get_settings(),
        )
    except UnknownPipelineError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except InvalidImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
