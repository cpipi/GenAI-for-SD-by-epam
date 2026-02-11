from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Order status enumeration"""
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    customer_name: str = Field(..., min_length=1, max_length=100)
    status: OrderStatus
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    created_at: Optional[date] = None


class OrderOut(BaseModel):
    """Schema for order response"""
    id: int
    customer_name: str
    status: OrderStatus
    amount: float
    currency: str
    created_at: date


class OrderListResponse(BaseModel):
    """Schema for paginated order list response"""
    items: List[OrderOut]
    page: int
    limit: int
    total: int
    total_pages: int
