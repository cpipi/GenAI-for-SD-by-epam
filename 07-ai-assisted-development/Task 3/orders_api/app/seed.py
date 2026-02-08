from __future__ import annotations

from .db import init_db, seed_db


def run() -> None:
    """Initialize database and seed sample orders"""
    init_db()
    seed_db()
    print("Database initialized and seeded with 50 orders")


if __name__ == "__main__":
    run()
