from __future__ import annotations

import os
import random
import sqlite3
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

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


def _build_orders_filter_clause(
    *,
    status: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> Tuple[str, List[Any]]:
    """Build WHERE SQL clause and parameter list for orders filters."""
    where_clauses: List[str] = []
    params: List[Any] = []

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

    return where_sql, params


def _rows_to_order_dicts(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convert SQLite rows to simple order dictionaries."""
    return [
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
    """List orders with pagination and filtering."""
    where_sql, params = _build_orders_filter_clause(
        status=status,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date,
    )

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

    items = _rows_to_order_dicts(rows)
    return items, total


def get_order_by_id(order_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a single order by its ID or return None if it does not exist."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, customer_name, status, amount, currency, created_at FROM orders WHERE id = ?",
            (order_id,),
        )
        row = cursor.fetchone()

    if not row:
        return None

    return {
        "id": row["id"],
        "customer_name": row["customer_name"],
        "status": row["status"],
        "amount": row["amount"],
        "currency": row["currency"],
        "created_at": row["created_at"],
    }


def get_order_stats() -> Dict[str, Any]:
    """Return aggregate statistics for all orders."""
    with get_connection() as conn:
        # Total orders and total amount
        cursor = conn.execute("SELECT COUNT(*), SUM(amount) FROM orders")
        total_count, total_amount = cursor.fetchone()

        # Breakdown by status
        cursor = conn.execute(
            "SELECT status, COUNT(*) as count, SUM(amount) as total FROM orders GROUP BY status"
        )
        status_breakdown = [
            {
                "status": row["status"],
                "count": row["count"],
                "total": round(row["total"], 2),
            }
            for row in cursor.fetchall()
        ]

    return {
        "total_orders": total_count,
        "total_amount": round(total_amount or 0, 2),
        "status_breakdown": status_breakdown,
    }
