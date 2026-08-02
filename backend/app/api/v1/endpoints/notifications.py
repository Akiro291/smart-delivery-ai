"""
Notifications endpoints.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/")
async def list_notifications():
    return {"message": "Notifications list endpoint - to be implemented"}
