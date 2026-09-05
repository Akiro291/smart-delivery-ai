"""
Seed script to populate database with sample products.
Run with: python -m app.seed_data
"""

import asyncio
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_factory
from sqlalchemy import text


# Sample products with images from picsum.photos (real placeholder images)
SAMPLE_PRODUCTS = [
    # ELECTRONICS
    {
        "name": "MacBook Pro 14\"",
        "description": "Мощный ноутбук для профессионалов с чипом M3 Pro",
        "price": 199990.0,
        "category": "Электроника",
        "image_url": "https://picsum.photos/seed/macbook/400/400",
        "is_available": True,
        "stock_quantity": 15,
    },
    {
        "name": "iPhone 15 Pro",
        "description": "Флагманский смартфон Apple с титановым корпусом",
        "price": 129990.0,
        "category": "Электроника",
        "image_url": "https://picsum.photos/seed/iphone/400/400",
        "is_available": True,
        "stock_quantity": 30,
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "description": "Премиальный смартфон с AI-функциями и S Pen",
        "price": 119990.0,
        "category": "Электроника",
        "image_url": "https://picsum.photos/seed/samsung/400/400",
        "is_available": True,
        "stock_quantity": 25,
    },
    {
        "name": "AirPods Pro 2",
        "description": "Беспроводные наушники с активным шумоподавлением",
        "price": 24990.0,
        "category": "Электроника",
        "image_url": "https://picsum.photos/seed/airpods/400/400",
        "is_available": True,
        "stock_quantity": 50,
    },
    {
        "name": "iPad Air",
        "description": "Легкий и мощный планшет для работы и творчества",
        "price": 59990.0,
        "category": "Электроника",
        "image_url": "https://picsum.photos/seed/ipad/400/400",
        "is_available": True,
        "stock_quantity": 20,
    },
    {
        "name": "PlayStation 5",
        "description": "Игровая консоль нового поколения",
        "price": 49990.0,
        "category": "Электроника",
        "image_url": "https://picsum.photos/seed/playstation/400/400",
        "is_available": True,
        "stock_quantity": 10,
    },
    
    # CLOTHING
    {
        "name": "Зимняя куртка North Face",
        "description": "Теплая куртка для экстремальных условий",
        "price": 18990.0,
        "category": "Одежда",
        "image_url": "https://picsum.photos/seed/jacket/400/400",
        "is_available": True,
        "stock_quantity": 40,
    },
    {
        "name": "Кроссовки Nike Air Max",
        "description": "Легкие кроссовки для бега и повседневной носки",
        "price": 12990.0,
        "category": "Одежда",
        "image_url": "https://picsum.photos/seed/nike/400/400",
        "is_available": True,
        "stock_quantity": 60,
    },
    {
        "name": "Джинсы Levi's 501",
        "description": "Классические джинсы прямого кроя",
        "price": 8990.0,
        "category": "Одежда",
        "image_url": "https://picsum.photos/seed/levis/400/400",
        "is_available": True,
        "stock_quantity": 75,
    },
    {
        "name": "Худи Adidas Originals",
        "description": "Уютное худи с классическим логотипом",
        "price": 6990.0,
        "category": "Одежда",
        "image_url": "https://picsum.photos/seed/hoodie/400/400",
        "is_available": True,
        "stock_quantity": 80,
    },
    
    # HOME & KITCHEN
    {
        "name": "Робот-пылесос Xiaomi",
        "description": "Умный пылесос с функцией влажной уборки",
        "price": 32990.0,
        "category": "Дом и кухня",
        "image_url": "https://picsum.photos/seed/vacuum/400/400",
        "is_available": True,
        "stock_quantity": 20,
    },
    {
        "name": "Кофемашина DeLonghi",
        "description": "Автоматическая кофемашина с капучинатором",
        "price": 45990.0,
        "category": "Дом и кухня",
        "image_url": "https://picsum.photos/seed/coffee/400/400",
        "is_available": True,
        "stock_quantity": 12,
    },
    {
        "name": "Набор ножей Zwilling",
        "description": "Премиальный набор кухонных ножей из нержавеющей стали",
        "price": 15990.0,
        "category": "Дом и кухня",
        "image_url": "https://picsum.photos/seed/knives/400/400",
        "is_available": True,
        "stock_quantity": 25,
    },
    {
        "name": "Блендер Bosch",
        "description": "Многофункциональный блендер для смузи и супов",
        "price": 8990.0,
        "category": "Дом и кухня",
        "image_url": "https://picsum.photos/seed/blender/400/400",
        "is_available": True,
        "stock_quantity": 35,
    },
    
    # BEAUTY & HEALTH
    {
        "name": "Фен Dyson Supersonic",
        "description": "Профессиональный фен с умным контролем температуры",
        "price": 39990.0,
        "category": "Красота и здоровье",
        "image_url": "https://picsum.photos/seed/hairdryer/400/400",
        "is_available": True,
        "stock_quantity": 18,
    },
    {
        "name": "Электробритва Philips",
        "description": "Ротационная бритва с 5 головками",
        "price": 11990.0,
        "category": "Красота и здоровье",
        "image_url": "https://picsum.photos/seed/razor/400/400",
        "is_available": True,
        "stock_quantity": 45,
    },
    {
        "name": "Набор косметики L'Oreal",
        "description": "Подарочный набор уходовой косметики",
        "price": 7990.0,
        "category": "Красота и здоровье",
        "image_url": "https://picsum.photos/seed/cosmetics/400/400",
        "is_available": True,
        "stock_quantity": 55,
    },
    
    # SPORT & OUTDOORS
    {
        "name": "Гантели разборные 20кг",
        "description": "Набор гантелей для домашних тренировок",
        "price": 6990.0,
        "category": "Спорт",
        "image_url": "https://picsum.photos/seed/dumbbells/400/400",
        "is_available": True,
        "stock_quantity": 30,
    },
    {
        "name": "Коврик для йоги",
        "description": "Профессиональный коврик с антискользящим покрытием",
        "price": 2990.0,
        "category": "Спорт",
        "image_url": "https://picsum.photos/seed/yoga/400/400",
        "is_available": True,
        "stock_quantity": 65,
    },
    {
        "name": "Велосипед горный Trek",
        "description": "Горный велосипед для бездорожья",
        "price": 89990.0,
        "category": "Спорт",
        "image_url": "https://picsum.photos/seed/bicycle/400/400",
        "is_available": True,
        "stock_quantity": 8,
    },
    {
        "name": "Спальный туристический",
        "description": "Легкий спальный мешок для походов",
        "price": 5990.0,
        "category": "Спорт",
        "image_url": "https://picsum.photos/seed/camping/400/400",
        "is_available": True,
        "stock_quantity": 22,
    },
    
    # BOOKS & STATIONERY
    {
        "name": "Atomic Habits - James Clear",
        "description": "Книга о формировании привычек",
        "price": 890.0,
        "category": "Книги",
        "image_url": "https://picsum.photos/seed/book1/400/400",
        "is_available": True,
        "stock_quantity": 100,
    },
    {
        "name": "Набор ручек Pilot",
        "description": "Набор гелевых ручек разных цветов",
        "price": 990.0,
        "category": "Книги и канцелярия",
        "image_url": "https://picsum.photos/seed/pens/400/400",
        "is_available": True,
        "stock_quantity": 150,
    },
    {
        "name": "Ежедневник Moleskine",
        "description": "Классический ежедневник формата A5",
        "price": 1990.0,
        "category": "Книги и канцелярия",
        "image_url": "https://picsum.photos/seed/diary/400/400",
        "is_available": True,
        "stock_quantity": 80,
    },
    
    # GROCERIES
    {
        "name": "Кофе в зернах Lavazza 1кг",
        "description": "Итальянский кофе из 100% арабики",
        "price": 1290.0,
        "category": "Продукты",
        "image_url": "https://picsum.photos/seed/coffeebeans/400/400",
        "is_available": True,
        "stock_quantity": 120,
    },
    {
        "name": "Чай Greenfield Assam",
        "description": "Черный листовой чай высшего качества",
        "price": 390.0,
        "category": "Продукты",
        "image_url": "https://picsum.photos/seed/tea/400/400",
        "is_available": True,
        "stock_quantity": 200,
    },
    {
        "name": "Шоколад Lindt 85%",
        "description": "Горький шоколад премиум-класса",
        "price": 490.0,
        "category": "Продукты",
        "image_url": "https://picsum.photos/seed/chocolate/400/400",
        "is_available": True,
        "stock_quantity": 150,
    },
    {
        "name": "Оливковое масло Extra Virgin",
        "description": "Холодный отжим, Испания, 500мл",
        "price": 890.0,
        "category": "Продукты",
        "image_url": "https://picsum.photos/seed/oliveoil/400/400",
        "is_available": True,
                "stock_quantity": 90,
    },
    
    # ACCESSORIES
    {
        "name": "Рюкзак Samsonite",
        "description": "Городской рюкзак с отделением для ноутбука",
        "price": 9990.0,
        "category": "Аксессуары",
        "image_url": "https://picsum.photos/seed/backpack/400/400",
        "is_available": True,
        "stock_quantity": 35,
    },
    {
        "name": "Солнцезащитные очки Ray-Ban",
        "description": "Классические авиаторы с UV-защитой",
        "price": 14990.0,
        "category": "Аксессуары",
        "image_url": "https://picsum.photos/seed/sunglasses/400/400",
        "is_available": True,
        "stock_quantity": 28,
    },
    {
        "name": "Умные часы Apple Watch",
        "description": "Фитнес-трекер и уведомления на запястье",
        "price": 32990.0,
        "category": "Аксессуары",
        "image_url": "https://picsum.photos/seed/smartwatch/400/400",
        "is_available": True,
        "stock_quantity": 20,
    },
    {
        "name": "Портативная колонка JBL",
        "description": "Водонепроницаемая Bluetooth-колонка",
        "price": 7990.0,
        "category": "Аксессуары",
        "image_url": "https://picsum.photos/seed/speaker/400/400",
        "is_available": True,
        "stock_quantity": 42,
    },
]


async def seed_products():
    """Insert sample products into database using raw SQL."""
    async with async_session_factory() as session:
        # Check if products already exist
        result = await session.execute(text("SELECT COUNT(*) FROM products"))
        count = result.scalar()
        
        if count > 0:
            print(f"Database already has {count} products. Skipping seed.")
            await session.close()
            return
        
        print("Seeding products with raw SQL...")
        
        for i, product_data in enumerate(SAMPLE_PRODUCTS, 1):
            try:
                await session.execute(text("""
                    INSERT INTO products (name, description, price, image_url, category, is_available, stock_quantity)
                    VALUES (:name, :description, :price, :image_url, :category, :is_available, :stock_quantity)
                """), product_data)
                await session.commit()
                print(f"  [{i}/{len(SAMPLE_PRODUCTS)}] Created: {product_data['name']} (${product_data['price']})")
            except Exception as e:
                print(f"  [ERROR] Failed to create '{product_data['name']}': {e}")
                await session.rollback()
        
        await session.close()
        print(f"\n✅ Successfully seeded {len(SAMPLE_PRODUCTS)} products!")


if __name__ == "__main__":
    print("=" * 60)
    print("Smart Delivery AI - Product Seeder")
    print("=" * 60)
    asyncio.run(seed_products())
