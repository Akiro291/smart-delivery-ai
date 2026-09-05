"""
Application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import ai, auth, cart, delivery, notifications, orders, products, users
from app.core.config import settings
from app.core.database import close_engine
from app.core.logging import get_logger

logger = get_logger(__name__)

# Path to uploads directory (project root)
UPLOADS_DIR = settings.BASE_DIR / "uploads"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    logger.info("Starting Smart Delivery AI Platform")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # Create uploads directory
    (UPLOADS_DIR / "products").mkdir(parents=True, exist_ok=True)
    logger.info(f"Uploads directory: {UPLOADS_DIR}")

    yield

    # Shutdown
    logger.info("Shutting down Smart Delivery AI Platform")
    await close_engine()


app = FastAPI(
    title="Smart Delivery AI Platform",
    description="SaaS-платформа управления доставкой с модульной архитектурой",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Smart Delivery AI Platform",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include API routes
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
app.include_router(notifications.router, prefix="/api/v1", tags=["notifications"])
app.include_router(ai.router, prefix="/api/v1", tags=["ai"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(cart.router, prefix="/api/v1", tags=["cart"])
app.include_router(delivery.router, prefix="/api/v1", tags=["delivery"])

# Create uploads directory before mounting static files
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Serve static files from uploads
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
