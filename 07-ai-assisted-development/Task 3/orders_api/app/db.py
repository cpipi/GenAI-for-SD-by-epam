from __future__ import annotations

import os
import random
import sqlite3
from datetime import date, timedelta
from typing import Any, Dict, List, Tuple

from .schemas import OrderCreate, OrderStatus

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")


def _db_path() -> str:
    """Get database path from environment or use default"""
    return os.getenv("ORDERS_DB_PATH", DEFAULT_DB_PATH)


def get_connection() -> sqlite3.Connection:
    """Create a database connection with row factory"""
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database schema"""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                status TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def clear_db() -> None:
    """Clear all orders from the database"""
    with get_connection() as conn:
        conn.execute("DELETE FROM orders")
        conn.commit()


def seed_db(count: int = 50) -> None:
    """Seed the database with sample orders"""
    with get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM orders")
        existing = cursor.fetchone()[0]
        if existing > 0:
            return

        random.seed(42)
        statuses = [s.value for s in OrderStatus]
        currencies = ["USD", "EUR", "KZT"]
        base_date = date.today() - timedelta(days=120)

        for i in range(count):
            created = base_date + timedelta(days=random.randint(0, 120))
            conn.execute(
                """
                INSERT INTO orders (customer_name, status, amount, currency, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    f"Customer {i + 1}",
                    random.choice(statuses),
                    round(random.uniform(10, 5000), 2),
                    random.choice(currencies),
                    created.isoformat(),
                ),
            )
        conn.commit()


def create_order(order: OrderCreate) -> Dict[str, Any]:
    """Create a new order in the database"""
    created_at = (order.created_at or date.today()).isoformat()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO orders (customer_name, status, amount, currency, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                order.customer_name,
                order.status.value,
                order.amount,
                order.currency.upper(),
                created_at,
            ),
        )
        order_id = cursor.lastrowid
        conn.commit()

    return {
        "id": order_id,
        "customer_name": order.customer_name,
        "status": order.status.value,
        "amount": order.amount,
        "currency": order.currency.upper(),
        "created_at": created_at,
    }


def list_orders(
    *,
    status: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = 1,
    limit: int = 10,
) -> Tuple[List[Dict[str, Any]], int]:
    """List orders with pagination and filtering"""
    where_clauses: List[str] = []
    params: List[Any] = []

    # Build WHERE clause based on filters
    if status:
        where_clauses.append("status = ?")
        params.append(status)
    if min_amount is not None:
        where_clauses.append("amount >= ?")
        params.append(min_amount)
    if max_amount is not None:
        where_clauses.append("amount <= ?")
        params.append(max_amount)
    if start_date:
        where_clauses.append("created_at >= ?")
        params.append(start_date.isoformat())
    if end_date:
        where_clauses.append("created_at <= ?")
        params.append(end_date.isoformat())

    where_sql = ""
    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)

    offset = (page - 1) * limit

    with get_connection() as conn:
        # Get total count
        count_cursor = conn.execute(
            f"SELECT COUNT(*) FROM orders{where_sql}", params
        )
        total = count_cursor.fetchone()[0]

        # Get paginated results
        cursor = conn.execute(
            f"""
            SELECT id, customer_name, status, amount, currency, created_at
            FROM orders{where_sql}
            ORDER BY id ASC
            LIMIT ? OFFSET ?
            """,
            [*params, limit, offset],
        )
        rows = cursor.fetchall()

    items = [
        {
            "id": row["id"],
            "customer_name": row["customer_name"],
            "status": row["status"],
            "amount": row["amount"],
            "currency": row["currency"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]
    return items, total
