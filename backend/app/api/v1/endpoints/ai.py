"""
AI endpoints.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/predict")
async def predict():
    return {"message": "AI prediction endpoint - to be implemented"}
