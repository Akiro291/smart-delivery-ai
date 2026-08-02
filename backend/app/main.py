"""
Application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import users, orders, notifications, ai, auth
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Smart Delivery AI Platform",
    description="AI-powered delivery management platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG,
)

# Configure CORS
if settings.DEBUG:
    origins = ["*"]
else:
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting Smart Delivery AI Platform")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down Smart Delivery AI Platform")


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
