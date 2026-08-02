"""
Orders endpoints.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
async def list_orders():
    return {"message": "Orders list endpoint - to be implemented"}


@router.get("/{order_id}")
async def get_order(order_id: int):
    return {"message": f"Order {order_id} endpoint - to be implemented"}
