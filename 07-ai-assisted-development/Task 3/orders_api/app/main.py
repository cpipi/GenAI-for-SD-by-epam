from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, HTTPException, Query

from .db import create_order, init_db, list_orders, seed_db
from .schemas import OrderCreate, OrderListResponse, OrderOut, OrderStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed data on startup"""
    init_db()
    seed_db()
    yield


app = FastAPI(title="Orders Management API", version="1.0.0", lifespan=lifespan)


@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order_endpoint(order: OrderCreate) -> OrderOut:
    """
    Create a new order.
    
    - **customer_name**: Name of the customer (1-100 characters)
    - **status**: Order status (pending, paid, shipped, cancelled)
    - **amount**: Order amount (must be positive)
    - **currency**: Currency code (3 characters, e.g., USD, EUR)
    - **created_at**: Order creation date (optional, defaults to today)
    """
    created = create_order(order)
    return OrderOut(**created)


@app.get("/orders", response_model=OrderListResponse)
def list_orders_endpoint(
    status: OrderStatus | None = None,
    min_amount: float | None = Query(default=None, ge=0),
    max_amount: float | None = Query(default=None, ge=0),
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
) -> OrderListResponse:
    """
    Get orders with pagination and filtering.
    
    Query parameters:
    - **status**: Filter by order status
    - **min_amount**: Minimum order amount
    - **max_amount**: Maximum order amount
    - **start_date**: Filter orders from this date (YYYY-MM-DD)
    - **end_date**: Filter orders until this date (YYYY-MM-DD)
    - **page**: Page number (starts at 1)
    - **limit**: Items per page (1-100)
    """
    # Validate date range
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400, detail="start_date cannot be after end_date"
        )

    # Validate amount range
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(
            status_code=400, detail="min_amount cannot be greater than max_amount"
        )

    items, total = list_orders(
        status=status.value if status else None,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date,
        page=page,
        limit=limit,
    )

    total_pages = max(1, (total + limit - 1) // limit)

    return OrderListResponse(
        items=[OrderOut(**item) for item in items],
        page=page,
        limit=limit,
        total=total,
        total_pages=total_pages,
    )


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order_endpoint(order_id: int) -> OrderOut:
    """
    Get a single order by ID.
    
    - **order_id**: The unique identifier of the order
    """
    from .db import get_connection
    
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, customer_name, status, amount, currency, created_at FROM orders WHERE id = ?",
            (order_id,)
        )
        row = cursor.fetchone()
        
    if not row:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return OrderOut(
        id=row["id"],
        customer_name=row["customer_name"],
        status=row["status"],
        amount=row["amount"],
        currency=row["currency"],
        created_at=row["created_at"],
    )


@app.get("/stats/summary")
def get_stats_summary():
    """
    Get summary statistics for all orders.
    
    Returns total count, total amount, and breakdown by status.
    """
    from .db import get_connection
    
    with get_connection() as conn:
        # Total orders
        cursor = conn.execute("SELECT COUNT(*), SUM(amount) FROM orders")
        total_count, total_amount = cursor.fetchone()
        
        # Breakdown by status
        cursor = conn.execute(
            "SELECT status, COUNT(*) as count, SUM(amount) as total FROM orders GROUP BY status"
        )
        status_breakdown = [
            {"status": row["status"], "count": row["count"], "total": round(row["total"], 2)}
            for row in cursor.fetchall()
        ]
    
    return {
        "total_orders": total_count,
        "total_amount": round(total_amount or 0, 2),
        "status_breakdown": status_breakdown,
    }
