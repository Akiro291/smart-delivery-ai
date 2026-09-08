"""
Notification event service: create in-app notifications and dispatch
email/telegram via Celery when configured.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models.notification import Notification, NotificationStatus, NotificationType
from app.db.models.user import User

logger = get_logger(__name__)


def _external_channel_configured(channel: NotificationType) -> bool:
    if channel == NotificationType.EMAIL:
        return bool(settings.SMTP_USER and settings.SMTP_PASSWORD)
    if channel == NotificationType.TELEGRAM:
        return bool(settings.TELEGRAM_BOT_TOKEN)
    return False


async def notify_user(
    db: AsyncSession,
    user: User,
    title: str,
    message: str,
    *,
    email: bool = False,
    telegram: bool = False,
) -> Notification:
    """Create an in-app notification; queue external delivery when configured.

    External channels are best-effort: a missing broker/token never fails the request.
    """
    notification = Notification(
        user_id=user.id,
        type=NotificationType.PUSH,
        status=NotificationStatus.PENDING,
        title=title,
        message=message[:1000],
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)

    if email and _external_channel_configured(NotificationType.EMAIL):
        _queue_external(
            "app.tasks.notification.send_email",
            {"to_email": user.email, "subject": title, "body": message},
        )
    if telegram and _external_channel_configured(NotificationType.TELEGRAM):
        _queue_external(
            "app.tasks.notification.send_telegram",
            {"chat_id": user.id, "message": f"{title}\n{message}"},
        )
    return notification


def _queue_external(task_name: str, kwargs: dict) -> None:
    try:
        from app.tasks import celery_app

        celery_app.send_task(task_name, kwargs=kwargs)
    except Exception as exc:  # pragma: no cover - broker failure path
        logger.warning(f"Could not queue task {task_name}: {exc}")


async def notify_order_status_change(
    db: AsyncSession,
    order,
    new_status_value: str,
    actor: User | None = None,
) -> None:
    """Notify the customer (and courier if assigned) about an order status change."""
    from app.repositories.user_repo import get_user_by_id

    titles = {
        "CONFIRMED": "Заказ подтверждён",
        "ASSIGNED": "Назначен курьер",
        "IN_PROGRESS": "Заказ в пути",
        "COMPLETED": "Заказ доставлен",
        "CANCELLED": "Заказ отменён",
    }
    title = titles.get(new_status_value, "Статус заказа обновлён")
    message = f"Заказ #{order.id}: статус изменён на {new_status_value}."

    customer = await get_user_by_id(db, order.customer_id)
    if customer:
        await notify_user(db, customer, title, message, email=True)

    if order.courier_id:
        courier = await get_user_by_id(db, order.courier_id)
        if courier and (not actor or actor.id != courier.id):
            await notify_user(db, courier, title, message)
