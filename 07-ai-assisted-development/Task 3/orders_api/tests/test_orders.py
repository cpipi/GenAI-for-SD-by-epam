import uuid

import httpx
import pytest

from app.main import app


@pytest.fixture
async def async_client(monkeypatch, tmp_path):
    """Create an async test client with isolated database"""
    db_path = tmp_path / f"orders_{uuid.uuid4().hex}.db"
    monkeypatch.setenv("ORDERS_DB_PATH", str(db_path))

    from app.db import init_db, seed_db
    init_db()
    seed_db()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.anyio
async def test_seeded_orders_count(async_client):
    """Test that 50 orders are seeded on startup"""
    response = await async_client.get("/orders", params={"limit": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 50
    assert len(data["items"]) == 50


@pytest.mark.anyio
async def test_create_order_success(async_client):
    """Test creating a new order successfully"""
    payload = {
        "customer_name": "Alice",
        "status": "paid",
        "amount": 120.5,
        "currency": "USD",
        "created_at": "2025-01-10",
    }
    response = await async_client.post("/orders", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["customer_name"] == "Alice"
    assert body["status"] == "paid"
    assert body["currency"] == "USD"


@pytest.mark.anyio
async def test_create_order_invalid_status(async_client):
    """Test creating an order with invalid status"""
    payload = {
        "customer_name": "Bob",
        "status": "unknown",
        "amount": 99.99,
        "currency": "EUR",
    }
    response = await async_client.post("/orders", json=payload)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_order_invalid_amount(async_client):
    """Test creating an order with negative amount"""
    payload = {
        "customer_name": "Bob",
        "status": "paid",
        "amount": -10,
        "currency": "EUR",
    }
    response = await async_client.post("/orders", json=payload)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_pagination_page_limit(async_client):
    """Test pagination with page and limit parameters"""
    response = await async_client.get("/orders", params={"page": 2, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["limit"] == 10
    assert len(data["items"]) == 10


@pytest.mark.anyio
async def test_pagination_limit_cap(async_client):
    """Test that limit respects maximum allowed value"""
    response = await async_client.get("/orders", params={"limit": 100})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 50


@pytest.mark.anyio
async def test_filter_status(async_client):
    """Test filtering orders by status"""
    response = await async_client.get("/orders", params={"status": "paid", "limit": 100})
    assert response.status_code == 200
    data = response.json()
    assert all(item["status"] == "paid" for item in data["items"])


@pytest.mark.anyio
async def test_filter_min_amount(async_client):
    """Test filtering orders by minimum amount"""
    response = await async_client.get("/orders", params={"min_amount": 1000, "limit": 100})
    assert response.status_code == 200
    data = response.json()
    assert all(item["amount"] >= 1000 for item in data["items"])


@pytest.mark.anyio
async def test_filter_max_amount(async_client):
    """Test filtering orders by maximum amount"""
    response = await async_client.get("/orders", params={"max_amount": 50, "limit": 100})
    assert response.status_code == 200
    data = response.json()
    assert all(item["amount"] <= 50 for item in data["items"])


@pytest.mark.anyio
async def test_filter_date_range(async_client):
    """Test filtering orders by date range"""
    response = await async_client.get(
        "/orders",
        params={"start_date": "2024-11-01", "end_date": "2025-12-31", "limit": 100},
    )
    assert response.status_code == 200
    data = response.json()
    assert all("2024-11-01" <= item["created_at"] <= "2025-12-31" for item in data["items"])


@pytest.mark.anyio
async def test_filter_combined(async_client):
    """Test combining multiple filters"""
    response = await async_client.get(
        "/orders",
        params={"status": "shipped", "min_amount": 100, "max_amount": 2000, "limit": 100},
    )
    assert response.status_code == 200
    data = response.json()
    assert all(item["status"] == "shipped" for item in data["items"])
    assert all(100 <= item["amount"] <= 2000 for item in data["items"])


@pytest.mark.anyio
async def test_start_date_after_end_date(async_client):
    """Test validation error when start_date is after end_date"""
    response = await async_client.get(
        "/orders",
        params={"start_date": "2025-12-31", "end_date": "2025-01-01"},
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_page_out_of_range_returns_empty(async_client):
    """Test that requesting a page beyond available data returns empty list"""
    response = await async_client.get("/orders", params={"page": 999, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []


@pytest.mark.anyio
async def test_invalid_limit_validation(async_client):
    """Test that limit exceeding maximum is rejected"""
    response = await async_client.get("/orders", params={"limit": 1000})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_order_by_id(async_client):
    """Test retrieving a single order by ID"""
    response = await async_client.get("/orders/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "customer_name" in data


@pytest.mark.anyio
async def test_get_order_not_found(async_client):
    """Test 404 when order doesn't exist"""
    response = await async_client.get("/orders/9999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_stats_summary(async_client):
    """Test statistics summary endpoint"""
    response = await async_client.get("/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_orders" in data
    assert "total_amount" in data
    assert "status_breakdown" in data
    assert data["total_orders"] == 50


@pytest.mark.anyio
async def test_min_amount_greater_than_max_amount(async_client):
    """Test validation when min_amount > max_amount"""
    response = await async_client.get(
        "/orders",
        params={"min_amount": 1000, "max_amount": 100},
    )
    assert response.status_code == 400
