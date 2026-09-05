"""
Cart endpoints - customer shopping cart.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import require_customer
from app.core.database import get_async_session
from app.repositories.cart_repo import (
    add_to_cart,
    clear_cart,
    get_cart_items,
    get_cart_total,
    remove_from_cart,
    update_cart_item,
)
from app.repositories.product_repo import get_product_by_id
from app.schemas.cart import CartItemCreate

router = APIRouter(prefix="/cart", tags=["cart"])


class CheckoutRequest(BaseModel):
    from_address: str
    to_address: str
    description: str | None = None


@router.get("/", response_model=list[dict])
async def get_cart(
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Получить содержимое корзины."""
    items = await get_cart_items(db, current_user.id)

    enriched = []
    for item in items:
        product = await get_product_by_id(db, item.product_id)
        if product:
            enriched.append(
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "product_name": product.name,
                    "product_price": product.price,
                    "product_image_url": product.image_url,
                    "subtotal": product.price * item.quantity,
                }
            )
    return enriched


@router.get("/summary")
async def get_cart_summary(
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Получить сводку корзины (количество и сумма)."""
    summary = await get_cart_total(db, current_user.id)
    items = await get_cart_items(db, current_user.id)
    summary["items_count"] = len(items)
    return summary


@router.post("/add", response_model=dict)
async def add_to_cart_endpoint(
    item_data: CartItemCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Добавить товар в корзину."""
    product = await get_product_by_id(db, item_data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )
    if not product.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Товар недоступен",
        )

    cart_item = await add_to_cart(db, current_user.id, item_data.product_id, item_data.quantity)

    return {
        "message": "Товар добавлен в корзину",
        "cart_item_id": cart_item.id,
        "quantity": cart_item.quantity,
    }


@router.put("/{cart_item_id}", response_model=dict)
async def update_cart_item_endpoint(
    cart_item_id: int,
    quantity: int = Query(..., ge=1),
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Обновить количество товара в корзине."""
    cart_item = await update_cart_item(db, cart_item_id, quantity, current_user.id)
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар в корзине не найден",
        )
    return {"message": "Количество обновлено", "quantity": cart_item.quantity}


@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart_endpoint(
    cart_item_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Удалить товар из корзины."""
    removed = await remove_from_cart(db, cart_item_id, current_user.id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар в корзине не найден",
        )


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart_endpoint(
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Очистить корзину."""
    await clear_cart(db, current_user.id)


@router.post("/checkout", response_model=dict)
async def checkout(
    body: CheckoutRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Оформить заказ из корзины."""
    cart_items = await get_cart_items(db, current_user.id)
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Корзина пуста",
        )

    # Calculate total and capture prices at checkout time
    total = 0.0
    order_items_data = []

    for cart_item in cart_items:
        product = await get_product_by_id(db, cart_item.product_id)
        if not product:
            continue
        if not product.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товар '{product.name}' недоступен",
            )

        # Capture price at checkout time to prevent race conditions
        captured_price = float(product.price)
        subtotal = captured_price * cart_item.quantity
        total += subtotal

        order_items_data.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "quantity": cart_item.quantity,
                "price": captured_price,
            }
        )

    # Create order
    from app.repositories.order_repo import create_order, create_order_items

    order = await create_order(
        db,
        {
            "customer_id": current_user.id,
            "from_address": body.from_address,
            "to_address": body.to_address,
            "total_amount": total,
            "description": body.description,
        },
    )

    # Create order items
    await create_order_items(db, order.id, order_items_data)

    # Clear cart
    await clear_cart(db, current_user.id)

    return {
        "message": "Заказ успешно оформлен",
        "order_id": order.id,
        "total": total,
    }
