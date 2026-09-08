"""
Statistics schemas.
"""

from pydantic import BaseModel


class OrderStatsResponse(BaseModel):
    """Order statistics for dashboards."""

    total: int
    by_status: dict[str, int]
    completed_revenue: float
    active: int
