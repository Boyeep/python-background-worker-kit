import time
from datetime import UTC, datetime
from typing import Any

from app.worker.celery_app import celery_app


@celery_app.task(
    bind=True,
    name="worker.process",
    autoretry_for=(RuntimeError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_task(self: Any, task_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    self.update_state(state="PROGRESS", meta={"progress": 25, "stage": "validating"})
    if payload.get("fail_until_retry", 0) > self.request.retries:
        raise RuntimeError("Simulated transient dependency failure")
    time.sleep(min(float(payload.get("delay", 0)), 1.0))
    self.update_state(state="PROGRESS", meta={"progress": 75, "stage": "processing"})
    return {
        "task_type": task_type,
        "processed": payload,
        "completed_at": datetime.now(UTC).isoformat(),
    }


@celery_app.task(name="worker.heartbeat")
def heartbeat() -> dict[str, str]:
    return {"status": "ok", "at": datetime.now(UTC).isoformat()}
