"""
Application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.endpoints import ai, auth, cart, delivery, notifications, orders, products, users, ws
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


# Unified error response format: {"detail": ..., "code": ...}
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail), "code": exc.status_code},
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "code": status.HTTP_500_INTERNAL_SERVER_ERROR},
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
app.include_router(ws.router, prefix="/api/v1", tags=["websocket"])

# Create uploads directory before mounting static files
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Serve static files from uploads
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
