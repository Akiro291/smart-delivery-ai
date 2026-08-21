import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.db.models.user import User, UserRole
from app.db.models.order import Order, OrderStatus
from app.db.models.order_history import OrderHistory
from app.api.v1.endpoints.orders import get_order_history_endpoint
from app.schemas.order import OrderHistoryResponse


@pytest.mark.asyncio
async def test_get_order_history_endpoint_returns_history(db_session: AsyncSession):
    customer = User(email="api1@example.com", hashed_password="test", role=UserRole.CUSTOMER)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)

    order = Order(
        customer_id=customer.id,
        status=OrderStatus.PENDING,
        from_address="A",
        to_address="B",
        total_amount=100,
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    history = OrderHistory(
        order_id=order.id,
        from_status=None,
        to_status=OrderStatus.PENDING,
        changed_by=customer.id,
        notes="created",
    )
    db_session.add(history)
    await db_session.commit()
    await db_session.refresh(history)

    current_user = User(id=customer.id, role=UserRole.CUSTOMER)
    result = await get_order_history_endpoint(
        order_id=order.id,
        db=db_session,
        current_user=current_user,
    )
    assert len(result) == 1
    assert isinstance(result[0], OrderHistoryResponse)
    assert result[0].to_status == OrderStatus.PENDING


@pytest.mark.asyncio
async def test_get_order_history_endpoint_raises_404_for_missing_order(db_session: AsyncSession):
    current_user = User(id=1, role=UserRole.ADMIN)
    with pytest.raises(HTTPException) as exc_info:
        await get_order_history_endpoint(
            order_id=9999,
            db=db_session,
            current_user=current_user,
        )
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_order_history_endpoint_raises_403_for_unauthorized(db_session: AsyncSession):
    customer = User(email="api2@example.com", hashed_password="test", role=UserRole.CUSTOMER)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)

    order = Order(
        customer_id=customer.id,
        status=OrderStatus.PENDING,
        from_address="A",
        to_address="B",
        total_amount=100,
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    current_user = User(id=9999, role=UserRole.CUSTOMER)
    with pytest.raises(HTTPException) as exc_info:
        await get_order_history_endpoint(
            order_id=order.id,
            db=db_session,
            current_user=current_user,
        )
    assert exc_info.value.status_code == 403
