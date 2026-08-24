from typing import Any, Literal

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.worker.celery_app import celery_app
from app.worker.tasks import process_task

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


class JobRequest(BaseModel):
    task: Literal["email", "export", "report", "sync"]
    payload: dict[str, Any] = Field(default_factory=dict)
    countdown: int = Field(default=0, ge=0, le=86_400)


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def create_job(request: JobRequest) -> dict[str, str]:
    result = process_task.apply_async(
        args=[request.task, request.payload], countdown=request.countdown
    )
    return {"id": result.id, "status": result.status.lower()}


@router.get("/{job_id}")
async def get_job(job_id: str) -> dict[str, Any]:
    result = AsyncResult(job_id, app=celery_app)
    if result.state == "PENDING":
        return {"id": job_id, "status": "pending", "result": None}
    payload: dict[str, Any] = {"id": job_id, "status": result.state.lower()}
    if result.successful():
        payload["result"] = result.result
    elif result.failed():
        payload["error"] = str(result.result)
    else:
        payload["progress"] = result.info
    return payload


@router.delete("/{job_id}", status_code=status.HTTP_202_ACCEPTED)
async def cancel_job(job_id: str) -> dict[str, str]:
    result = AsyncResult(job_id, app=celery_app)
    if result.successful():
        raise HTTPException(
            status_code=409, detail="Completed jobs cannot be cancelled."
        )
    result.revoke(terminate=False)
    return {"id": job_id, "status": "revoked"}
