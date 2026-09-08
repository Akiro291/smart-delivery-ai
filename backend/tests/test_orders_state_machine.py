"""Tests for the order state machine and order repository helpers."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order, OrderStatus
from app.db.models.user import User, UserRole
from app.repositories.order_repo import (
    assign_courier,
    create_order,
    get_order_stats,
    update_order_status,
)
from app.services.orders_service import (
    ALLOWED_TRANSITIONS,
    can_view_order,
    is_transition_allowed,
)


def _make_user(email: str, role: UserRole) -> User:
    return User(email=email, hashed_password="test", role=role)


async def _make_order(db: AsyncSession, user: User) -> Order:
    order = await create_order(
        db,
        {
            "customer_id": user.id,
            "from_address": "A",
            "to_address": "B",
            "total_amount": "100.00",
        },
    )
    return order


@pytest.mark.asyncio
async def test_valid_transitions(db_session: AsyncSession):
    customer = _make_user("sm_c1@example.com", UserRole.CUSTOMER)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)

    order = await _make_order(db_session, customer)
    assert order.status == OrderStatus.PENDING

    updated = await update_order_status(db_session, order.id, OrderStatus.CONFIRMED)
    assert updated is not None
    assert updated.status == OrderStatus.CONFIRMED


@pytest.mark.asyncio
async def test_invalid_transition_rejected(db_session: AsyncSession):
    customer = _make_user("sm_c2@example.com", UserRole.CUSTOMER)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)

    order = await _make_order(db_session, customer)
    # PENDING -> COMPLETED is forbidden
    result = await update_order_status(db_session, order.id, OrderStatus.COMPLETED)
    assert result is None


@pytest.mark.asyncio
async def test_terminal_states_are_frozen(db_session: AsyncSession):
    for terminal in (OrderStatus.COMPLETED, OrderStatus.CANCELLED):
        assert ALLOWED_TRANSITIONS[terminal] == set()
        assert not is_transition_allowed(terminal, OrderStatus.PENDING)


@pytest.mark.asyncio
async def test_assign_courier_moves_to_assigned(db_session: AsyncSession):
    customer = _make_user("sm_c3@example.com", UserRole.CUSTOMER)
    courier = _make_user("sm_k3@example.com", UserRole.COURIER)
    db_session.add_all([customer, courier])
    await db_session.commit()
    await db_session.refresh(customer)
    await db_session.refresh(courier)

    order = await _make_order(db_session, customer)
    updated = await assign_courier(db_session, order, courier.id, assigned_by=1)
    assert updated.courier_id == courier.id
    assert updated.status == OrderStatus.ASSIGNED


@pytest.mark.asyncio
async def test_can_view_order_permissions():
    order = Order(
        customer_id=1,
        status=OrderStatus.PENDING,
        from_address="A",
        to_address="B",
        total_amount=100,
    )
    order.customer_id = 1
    assert can_view_order(UserRole.CUSTOMER, 1, order)
    assert not can_view_order(UserRole.CUSTOMER, 2, order)
    assert can_view_order(UserRole.ADMIN, 999, order)
    assert can_view_order(UserRole.MANAGER, 999, order)


@pytest.mark.asyncio
async def test_order_stats(db_session: AsyncSession):
    customer = _make_user("sm_c5@example.com", UserRole.CUSTOMER)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)

    await _make_order(db_session, customer)
    await _make_order(db_session, customer)

    stats = await get_order_stats(db_session)
    assert stats["total"] >= 2
    assert stats["by_status"].get("PENDING", 0) >= 2
    assert "completed_revenue" in stats
    assert "active" in stats
