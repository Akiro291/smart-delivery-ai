"""
Cart repository with CRUD operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order_item import CartItem
from app.db.models.product import Product


async def get_cart_items(db: AsyncSession, user_id: int) -> list[CartItem]:
    """Get all cart items for a user."""
    result = await db.execute(select(CartItem).where(CartItem.user_id == user_id).order_by(CartItem.created_at.desc()))
    return list(result.scalars().all())


async def get_cart_item_by_product(db: AsyncSession, user_id: int, product_id: int) -> CartItem | None:
    """Get cart item for user and product."""
    result = await db.execute(
        select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id,
        )
    )
    return result.scalar_one_or_none()


async def add_to_cart(db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItem:
    """Add product to cart or update quantity if exists."""
    existing = await get_cart_item_by_product(db, user_id, product_id)

    if existing:
        existing.quantity += quantity
        await db.commit()
        await db.refresh(existing)
        return existing

    cart_item = CartItem(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
    )
    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return cart_item


async def update_cart_item(db: AsyncSession, cart_item_id: int, quantity: int, user_id: int) -> CartItem | None:
    """Update cart item quantity (only if the item belongs to user)."""
    result = await db.execute(select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == user_id))
    cart_item = result.scalar_one_or_none()
    if cart_item:
        cart_item.quantity = quantity
        await db.commit()
        await db.refresh(cart_item)
    return cart_item


async def remove_from_cart(db: AsyncSession, cart_item_id: int, user_id: int) -> bool:
    """Remove item from cart (only if the item belongs to user)."""
    result = await db.execute(select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == user_id))
    cart_item = result.scalar_one_or_none()
    if cart_item:
        await db.delete(cart_item)
        await db.commit()
        return True
    return False


async def clear_cart(db: AsyncSession, user_id: int) -> int:
    """Remove all items from user's cart. Returns count of removed items."""
    result = await db.execute(select(CartItem).where(CartItem.user_id == user_id))
    items = list(result.scalars().all())
    for item in items:
        await db.delete(item)
    await db.commit()
    return len(items)


async def get_cart_total(db: AsyncSession, user_id: int) -> dict:
    """Get cart total with items and sum."""
    result = await db.execute(
        select(CartItem, Product).join(Product, CartItem.product_id == Product.id).where(CartItem.user_id == user_id)
    )
    items_with_products = result.all()

    total = 0.0
    for cart_item, product in items_with_products:
        total += product.price * cart_item.quantity

    return {
        "items_count": len(items_with_products),
        "total": total,
    }
