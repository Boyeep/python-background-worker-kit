from celery import Celery

from app.config import get_settings

settings = get_settings()
broker_url = "memory://" if settings.worker_eager else settings.redis_url
result_backend = "cache+memory://" if settings.worker_eager else settings.redis_url
celery_app = Celery("worker-kit", broker=broker_url, backend=result_backend)
celery_app.conf.update(
    task_always_eager=settings.worker_eager,
    task_store_eager_result=True,
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    beat_schedule={
        "heartbeat-every-minute": {
            "task": "worker.heartbeat",
            "schedule": 60.0,
        }
    },
)
