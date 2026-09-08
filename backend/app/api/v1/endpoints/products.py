"""
Products endpoints - admin management and customer catalog.
"""

import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import require_admin
from app.core.config import settings
from app.core.database import get_async_session
from app.db.models.product import Product as ProductModel
from app.repositories.product_repo import (
    create_product,
    delete_product,
    get_product_by_id,
    get_product_count,
    get_products,
    get_products_by_category,
    update_product,
)
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])

# Path to uploads directory (project root)
UPLOADS_DIR = settings.BASE_DIR / "uploads"


@router.get("/", response_model=list[Product])
async def list_products(
    skip: int = Query(0, ge=0, description="Пропуск"),
    limit: int = Query(50, ge=1, le=200, description="Лимит"),
    category: str | None = Query(None, description="Фильтр по категории"),
    available_only: bool = Query(False, description="Только доступные"),
    db: AsyncSession = Depends(get_async_session),
):
    """Получить каталог товаров."""
    products = await get_products(
        db,
        skip=skip,
        limit=limit,
        category=category,
        available_only=available_only,
    )
    return products


@router.get("/categories")
async def list_categories(
    db: AsyncSession = Depends(get_async_session),
):
    """Получить список всех категорий товаров."""
    products = await get_products(db, limit=1000)
    categories = sorted(set(p.category for p in products if p.category))
    return {"categories": categories}


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Получить карточку товара."""
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )
    return product


@router.get("/category/{category}", response_model=list[Product])
async def get_products_by_category_endpoint(
    category: str,
    db: AsyncSession = Depends(get_async_session),
):
    """Получить товары по категории."""
    products = await get_products_by_category(db, category)
    return products


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_async_session),
    admin: object = Depends(require_admin),
):
    """Создать новый товар (только админ)."""
    new_product = await create_product(
        db,
        {
            **product_data.model_dump(),
            "created_by": admin.id,
        },
    )
    return new_product


@router.put("/{product_id}", response_model=Product)
async def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_async_session),
    admin: object = Depends(require_admin),
):
    """Обновить товар (только админ)."""
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )
    updated = await update_product(db, product, product_data.model_dump(exclude_unset=True))
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
    admin: object = Depends(require_admin),
):
    """Удалить товар (только админ)."""
    deleted = await delete_product(db, product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )
    return None


@router.get("/stats/summary")
async def get_product_stats(
    db: AsyncSession = Depends(get_async_session),
    admin: object = Depends(require_admin),
):
    """Статистика по товарам (только админ)."""
    total = await get_product_count(db)
    return {"total_products": total}


@router.post("/{product_id}/image", response_model=Product)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
    admin: object = Depends(require_admin),
):
    """Загрузить изображение для товара (только админ)."""
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Разрешены только изображения",
        )

    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )

    # Validate extension (content-type header is easy to spoof)
    file_extension = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недопустимый формат изображения",
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"

    # Save to uploads folder
    uploads_dir = UPLOADS_DIR / "products"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    file_path = uploads_dir / unique_filename

    # Read file content (with size limit) and save
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Файл слишком большой (максимум 5 МБ)",
        )
    with open(file_path, "wb") as f:
        f.write(contents)

    # Update product with image URL
    image_url = f"/uploads/products/{unique_filename}"
    result = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    db_product = result.scalar_one_or_none()
    if db_product:
        db_product.image_url = image_url
        await db.commit()
        await db.refresh(db_product)
        return Product.model_validate(db_product)

    raise HTTPException(status_code=500, detail="Ошибка при сохранении изображения")


@router.delete("/{product_id}/image", response_model=Product)
async def delete_product_image(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
    admin: object = Depends(require_admin),
):
    """Удалить изображение товара (только админ)."""
    result = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден",
        )

    if product.image_url:
        # Try to delete file
        file_path = UPLOADS_DIR / "products" / os.path.basename(product.image_url)
        if os.path.exists(file_path):
            os.remove(file_path)
        product.image_url = None
        await db.commit()
        await db.refresh(product)
        return Product.model_validate(product)
