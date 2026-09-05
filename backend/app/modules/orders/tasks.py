"""
Order-related Celery tasks.
"""

from app.core.logging import get_logger
from app.tasks import celery_app

logger = get_logger(__name__)


@celery_app.task(bind=True, max_retries=3, name="app.tasks.order.estimate_delivery")
def estimate_delivery_time(self, order_id: int, from_address: str, to_address: str) -> dict:
    """Estimate delivery time based on addresses."""
    try:
        logger.info(f"Estimating delivery time for order {order_id}")
        return {
            "order_id": order_id,
            "estimated_minutes": 30,
            "distance_km": 5.2,
        }
    except Exception as exc:
        logger.error(f"Error estimating delivery time: {exc}")
        raise self.retry(exc=exc, countdown=30)


@celery_app.task(bind=True, max_retries=3, name="app.tasks.order.assign_courier")
def assign_courier_to_order(self, order_id: int) -> str:
    """Assign nearest available courier to order."""
    try:
        logger.info(f"Assigning courier to order {order_id}")
        return f"Courier assigned to order {order_id}"
    except Exception as exc:
        logger.error(f"Error assigning courier: {exc}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, max_retries=3, name="app.tasks.order.update_delivery_tracking")
def update_delivery_tracking(
    self,
    order_id: int,
    lat: float,
    lon: float,
    progress: int,
) -> str:
    """Update delivery tracking with new location."""
    try:
        logger.info(f"Updating tracking for order {order_id}: lat={lat}, lon={lon}")
        return f"Tracking updated for order {order_id}"
    except Exception as exc:
        logger.error(f"Error updating delivery tracking: {exc}")
        raise self.retry(exc=exc, countdown=30)
