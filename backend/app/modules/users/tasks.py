"""
User-related Celery tasks.
"""

from app.tasks import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(bind=True, max_retries=3, name="app.tasks.user.send_welcome_email")
def send_welcome_email(self, user_id: int, email: str, full_name: str) -> str:
    """Send welcome email to new user."""
    try:
        logger.info(f"Sending welcome email to {email}")
        return f"Welcome email sent to {email}"
    except Exception as exc:
        logger.error(f"Error sending welcome email: {exc}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, max_retries=3, name="app.tasks.user.send_password_reset")
def send_password_reset_email(self, user_id: int, email: str, reset_token: str) -> str:
    """Send password reset email."""
    try:
        logger.info(f"Sending password reset email to {email}")
        return f"Password reset email sent to {email}"
    except Exception as exc:
        logger.error(f"Error sending password reset email: {exc}")
        raise self.retry(exc=exc, countdown=60)
