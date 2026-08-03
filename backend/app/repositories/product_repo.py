"""
Product repository with CRUD operations.
"""

from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product


async def get_products(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    available_only: bool = False,
) -> List[Product]:
    """Get list of products with filtering."""
    query = select(Product)
    
    if category:
        query = query.where(Product.category == category)
    
    if available_only:
        query = query.where(Product.is_available == True)  # noqa
    
    query = query.offset(skip).limit(limit).order_by(Product.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
    """Get product by ID."""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def get_products_by_category(
    db: AsyncSession, category: str
) -> List[Product]:
    """Get products by category."""
    result = await db.execute(
        select(Product)
        .where(Product.category == category, Product.is_available == True)
        .order_by(Product.created_at.desc())
    )
    return list(result.scalars().all())


async def create_product(db: AsyncSession, product_data: dict) -> Product:
    """Create a new product."""
    product = Product(**product_data)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(
    db: AsyncSession, product: Product, product_data: dict
) -> Product:
    """Update product fields."""
    for field, value in product_data.items():
        if value is not None and hasattr(product, field):
            setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: int) -> bool:
    """Delete a product."""
    product = await get_product_by_id(db, product_id)
    if product:
        await db.delete(product)
        await db.commit()
    return bool(product)


async def get_product_count(db: AsyncSession) -> int:
    """Get total product count."""
    result = await db.execute(func.count(Product.id))
    return result.scalar_one()
