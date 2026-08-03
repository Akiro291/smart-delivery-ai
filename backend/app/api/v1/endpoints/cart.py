"""
Cart endpoints - customer shopping cart.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.schemas.cart import CartItemCreate, CartItemWithProduct, OrderItemCreate
from app.repositories.cart_repo import (
    get_cart_items,
    get_cart_item_by_product,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
    clear_cart,
    get_cart_total,
)
from app.repositories.product_repo import get_product_by_id
from app.db.models.product import Product
from app.api.v1.dependencies import get_current_user, require_customer

router = APIRouter(prefix="/cart", tags=["cart"])


def _enrich_cart_items(db: AsyncSession, items) -> list:
    """Add product details to cart items."""
    result = []
    for item in items:
        product = None
        for p in [item.product_id]:
            p_obj = None
            # We'll handle this differently in the endpoint
            pass
    return result


@router.get("/", response_model=list)
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
            enriched.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_name": product.name,
                "product_price": product.price,
                "product_image_url": product.image_url,
                "subtotal": product.price * item.quantity,
            })
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
    
    cart_item = await add_to_cart(
        db, current_user.id, item_data.product_id, item_data.quantity
    )
    
    return {
        "message": "Товар добавлен в корзину",
        "cart_item_id": cart_item.id,
        "quantity": cart_item.quantity,
    }


@router.put("/{cart_item_id}", response_model=dict)
async def update_cart_item_endpoint(
    cart_item_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: object = Depends(require_customer),
):
    """Обновить количество товара в корзине."""
    if quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Количество должно быть больше 0",
        )
    
    cart_item = await update_cart_item(db, cart_item_id, quantity)
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
    removed = await remove_from_cart(db, cart_item_id)
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
    from_address: str,
    to_address: str,
    description: str = None,
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
    
    # Calculate total
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
        
        subtotal = product.price * cart_item.quantity
        total += subtotal
        
        order_items_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": cart_item.quantity,
            "price": product.price,
        })
    
    # Create order
    from app.repositories.order_repo import create_order, create_order_items
    
    order = await create_order(db, {
        "customer_id": current_user.id,
        "from_address": from_address,
        "to_address": to_address,
        "total_amount": total,
        "description": description,
    })
    
    # Create order items
    await create_order_items(db, order.id, order_items_data)
    
    # Clear cart
    await clear_cart(db, current_user.id)
    
    return {
        "message": "Заказ успешно оформлен",
        "order_id": order.id,
        "total": total,
    }
