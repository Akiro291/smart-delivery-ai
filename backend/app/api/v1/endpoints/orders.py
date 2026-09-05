"""
Orders endpoints.
"""

from decimal import Decimal
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.core.database import get_async_session
from app.db.models.order import OrderStatus
from app.db.models.user import User, UserRole
from app.repositories.order_repo import get_order_by_id, get_orders
from app.schemas.order import Order, OrderCreate, OrderHistoryResponse, OrderUpdate
from app.services.orders_service import get_order_history_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[Order])
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status_filter: str | None = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get orders list with filtering."""
    if current_user.role == UserRole.ADMIN:
        # Admin sees all orders
        status = OrderStatus(status_filter) if status_filter else None
        orders = await get_orders(db, skip, limit, status)
    elif current_user.role == UserRole.COURIER:
        orders = await get_orders(db, skip, limit, courier_id=current_user.id)
    else:
        orders = await get_orders(db, skip, limit, customer_id=current_user.id)
    return orders


@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get order by ID."""
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    # Access control: admin sees all, others only their own orders
    if current_user.role != UserRole.ADMIN and (
        order.customer_id != current_user.id and order.courier_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return order


@router.get("/{order_id}/history", response_model=list[OrderHistoryResponse])
async def get_order_history_endpoint(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get order history timeline."""
    history = await get_order_history_service(
        db=db,
        order_id=order_id,
        current_user_id=current_user.id,
        current_user_role=cast("UserRole", current_user.role),
    )
    if history is None:
        order = await get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return history


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new order."""
    from app.repositories.order_repo import create_order as create_order_repo, create_order_items

    # Never trust the client with the total when line items are provided
    if order_data.items:
        order_total = sum(
            (Decimal(str(item.price)) * item.quantity for item in order_data.items),
            Decimal("0"),
        )
    else:
        order_total = order_data.total_amount

    order = await create_order_repo(
        db,
        {
            "customer_id": current_user.id,
            "from_address": order_data.from_address,
            "to_address": order_data.to_address,
            "total_amount": order_total,
            "description": order_data.description,
            "is_priority": order_data.is_priority,
        },
    )

    if order_data.items:
        await create_order_items(db, order.id, [item.model_dump() for item in order_data.items])

    return order


@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Update an order."""
    from app.repositories.order_repo import update_order as update_order_repo

    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    # Only admin or the order creator can update
    if current_user.role != UserRole.ADMIN and order.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    updated = await update_order_repo(db, order, order_data.model_dump(exclude_unset=True))
    return updated
