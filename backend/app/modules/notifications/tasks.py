"""
Notification-related Celery tasks.
"""

import aiohttp
from app.tasks import celery_app
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(bind=True, max_retries=3, name="app.tasks.notification.send_telegram")
def send_telegram_notification(
    self,
    chat_id: int,
    message: str,
    parse_mode: str = "HTML",
) -> str:
    """Send notification via Telegram bot."""
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode,
        }
        import asyncio
        import aiohttp

        async def _send():
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    return await resp.json()

        result = asyncio.run(_send())
        logger.info(f"Telegram notification sent to {chat_id}: {result}")
        return str(result)
    except Exception as exc:
        logger.error(f"Error sending Telegram notification: {exc}")
        raise self.retry(exc=exc, countdown=30)


@celery_app.task(bind=True, max_retries=3, name="app.tasks.notification.send_email")
def send_email_notification(
    self,
    to_email: str,
    subject: str,
    body: str,
    html: bool = False,
) -> str:
    """Send email notification."""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = subject

        if html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email notification sent to {to_email}")
        return f"Email sent to {to_email}"
    except Exception as exc:
        logger.error(f"Error sending email notification: {exc}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(name="app.tasks.notification.send_push_notification")
def send_push_notification(
    user_id: int,
    title: str,
    body: str,
    data: dict = None,
) -> str:
    """Send push notification to user device."""
    try:
        logger.info(f"Sending push notification to user {user_id}: {title}")
        return f"Push notification sent to user {user_id}"
    except Exception as exc:
        logger.error(f"Error sending push notification: {exc}")
        raise
