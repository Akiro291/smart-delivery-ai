"""
Celery task configuration for async background tasks.
"""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "smart_delivery",
    broker=(
        f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}"
        f"@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//"
    ),
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_soft_time_limit=300,
    task_time_limit=600,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    broker_transport_options={
        "visibility_timeout": 3600,
    },
)

# Import tasks modules
celery_app.autodiscover_tasks(
    ["app.modules.users", "app.modules.orders", "app.modules.notifications", "app.modules.ai"]
)
