"""
AI service: prediction + chat assistant.

Two providers behind a common interface:
- HeuristicAIService: rule/average-based, no external dependencies (default).
- OpenAIAIService: uses OpenAI API when OPENAI_API_KEY is configured.
"""

from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models.delivery_tracking import DeliveryTracking
from app.db.models.order import Order, OrderStatus
from app.db.models.user import User

logger = get_logger(__name__)

# Rough baseline: average courier delivery time in minutes per status
_BASE_ESTIMATES = {
    "PENDING": 90,
    "CONFIRMED": 75,
    "ASSIGNED": 60,
    "IN_PROGRESS": 30,
}


class AIServiceBase(ABC):
    """Base class for AI services."""

    @abstractmethod
    async def predict_delivery_time(
        self,
        db: AsyncSession,
        order: Order,
    ) -> dict:
        """Predict delivery time (minutes) for an order."""

    @abstractmethod
    async def chat(self, db: AsyncSession, user: User, message: str) -> dict:
        """Answer a user chat message."""


class HeuristicAIService(AIServiceBase):
    """Deterministic heuristics: history averages + priority adjustments."""

    async def predict_delivery_time(self, db: AsyncSession, order: Order) -> dict:
        base = _BASE_ESTIMATES.get(order.status.value, 60)

        # Priority orders arrive sooner
        if order.is_priority:
            base = int(base * 0.7)

        # Blend with historical average for completed orders
        result = await db.execute(
            select(DeliveryTracking.estimated_delivery_time)
            .join(Order, Order.id == DeliveryTracking.order_id)
            .where(Order.status == OrderStatus.COMPLETED)
        )
        history = [m for m in result.scalars().all() if m]
        if history:
            avg = sum(history) / len(history)
            base = int(0.5 * base + 0.5 * avg)

        return {
            "order_id": order.id,
            "estimated_minutes": base,
            "provider": "heuristic",
        }

    async def chat(self, db: AsyncSession, user: User, message: str) -> dict:
        text = message.lower()
        user_orders = select(Order).where(Order.customer_id == user.id).order_by(Order.created_at.desc())
        result = await db.execute(user_orders.limit(5))
        orders = list(result.scalars().all())
        active = [o for o in orders if o.status not in (OrderStatus.COMPLETED, OrderStatus.CANCELLED)]

        if any(k in text for k in ("заказ", "order", "доставк", "delivery")):
            if active:
                o = active[0]
                return {
                    "reply": (f"Ваш заказ #{o.id} сейчас в статусе {o.status.value}. Адрес доставки: {o.to_address}."),
                    "provider": "heuristic",
                }
            return {"reply": "У вас нет активных заказов. Создайте заказ в каталоге.", "provider": "heuristic"}
        if any(k in text for k in ("привет", "здравствуй", "hello", "hi")):
            return {
                "reply": "Здравствуйте! Я помощник Smart Delivery. Могу рассказать о ваших заказах.",
                "provider": "heuristic",
            }
        return {
            "reply": "Я могу рассказать о статусе ваших заказов. Напишите «статус заказа».",
            "provider": "heuristic",
        }


class OpenAIAIService(AIServiceBase):
    """OpenAI-backed provider with heuristic fallback."""

    def __init__(self) -> None:
        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def predict_delivery_time(self, db: AsyncSession, order: Order) -> dict:
        fallback = await HeuristicAIService().predict_delivery_time(db, order)
        try:
            prompt = (
                f"Оцени время доставки в минутах одним числом. "
                f"Статус: {order.status.value}, приоритетный: {bool(order.is_priority)}, "
                f"откуда: {order.from_address}, куда: {order.to_address}. "
                f"Эвристическая оценка: {fallback['estimated_minutes']} минут."
            )
            response = await self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.2,
            )
            raw = (response.choices[0].message.content or "").strip()
            minutes = int("".join(ch for ch in raw if ch.isdigit())[:4] or fallback["estimated_minutes"])
            return {"order_id": order.id, "estimated_minutes": minutes, "provider": "openai"}
        except Exception as exc:  # pragma: no cover - API failure path
            logger.warning(f"OpenAI prediction failed, using heuristic: {exc}")
            return fallback

    async def chat(self, db: AsyncSession, user: User, message: str) -> dict:
        # Context: user's recent orders
        result = await db.execute(
            select(Order).where(Order.customer_id == user.id).order_by(Order.created_at.desc()).limit(5)
        )
        orders = list(result.scalars().all())
        context = (
            "\n".join(f"Заказ #{o.id}: статус {o.status.value}, адрес {o.to_address}" for o in orders) or "Заказов нет."
        )
        try:
            response = await self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты — ассистент сервиса доставки Smart Delivery. "
                            "Отвечай кратко на русском. Данные о заказах клиента:\n" + context
                        ),
                    },
                    {"role": "user", "content": message},
                ],
                max_tokens=300,
                temperature=0.5,
            )
            reply = (response.choices[0].message.content or "").strip()
            return {"reply": reply, "provider": "openai"}
        except Exception as exc:  # pragma: no cover - API failure path
            logger.warning(f"OpenAI chat failed, using heuristic: {exc}")
            return await HeuristicAIService().chat(db, user, message)


def get_ai_service() -> AIServiceBase:
    """Choose provider: OpenAI if a real key is configured, else heuristics."""
    if settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("your-"):
        try:
            return OpenAIAIService()
        except Exception as exc:  # pragma: no cover - client init failure
            logger.warning(f"OpenAI init failed: {exc}")
    return HeuristicAIService()
