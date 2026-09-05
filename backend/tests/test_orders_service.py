import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, UserRole
from app.db.models.order import Order, OrderStatus
from app.db.models.order_history import OrderHistory
from app.services.orders_service import get_order_history_service
from app.schemas.order import OrderHistoryResponse


@pytest.mark.asyncio
async def test_get_order_history_service_returns_history(db_session: AsyncSession):
    customer = User(email="hist1@example.com", hashed_password="test", role=UserRole.CUSTOMER)
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

    result = await get_order_history_service(
        db=db_session,
        order_id=order.id,
        current_user_id=customer.id,
        current_user_role=UserRole.CUSTOMER,
    )
    assert len(result) == 1
    assert isinstance(result[0], OrderHistoryResponse)
    assert result[0].to_status == OrderStatus.PENDING
    assert result[0].order_id == order.id


@pytest.mark.asyncio
async def test_get_order_history_service_returns_empty_for_unauthorized_user(db_session: AsyncSession):
    customer = User(email="hist2@example.com", hashed_password="test", role=UserRole.CUSTOMER)
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
    )
    db_session.add(history)
    await db_session.commit()

    result = await get_order_history_service(
        db=db_session,
        order_id=order.id,
        current_user_id=9999,
        current_user_role=UserRole.CUSTOMER,
    )
    assert result is None


@pytest.mark.asyncio
async def test_get_order_history_service_returns_none_for_missing_order(db_session: AsyncSession):
    result = await get_order_history_service(
        db=db_session,
        order_id=9999,
        current_user_id=1,
        current_user_role=UserRole.ADMIN,
    )
    assert result is None


@pytest.mark.asyncio
async def test_get_order_history_service_allows_admin(db_session: AsyncSession):
    customer = User(email="hist3@example.com", hashed_password="test", role=UserRole.CUSTOMER)
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
    )
    db_session.add(history)
    await db_session.commit()

    result = await get_order_history_service(
        db=db_session,
        order_id=order.id,
        current_user_id=1,
        current_user_role=UserRole.ADMIN,
    )
    assert len(result) == 1
