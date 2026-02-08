# Orders Management API

A REST API for managing orders with pagination and filtering capabilities, built with FastAPI and SQLite.

## Features

- ✅ Create new orders (POST /orders)
- ✅ List orders with pagination (GET /orders)
- ✅ Filter by status, amount range, and date range
- ✅ SQLite database with 50 pre-seeded orders
- ✅ 15 comprehensive test cases with 80%+ coverage
- ✅ Input validation using Pydantic

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: SQLite3
- **Testing**: pytest, httpx
- **Python**: 3.12+

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment**
   ```bash
   python -m venv .venv312
   ```

3. **Activate the virtual environment**
   - Windows: `.venv312\Scripts\activate`
   - macOS/Linux: `source .venv312/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive API documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### POST /orders

Create a new order.

**Request body:**
```json
{
  "customer_name": "Alice",
  "status": "paid",
  "amount": 120.5,
  "currency": "USD",
  "created_at": "2025-01-10"
}
```

**Status values:** `pending`, `paid`, `shipped`, `cancelled`

**Response:** `201 Created`
```json
{
  "id": 51,
  "customer_name": "Alice",
  "status": "paid",
  "amount": 120.5,
  "currency": "USD",
  "created_at": "2025-01-10"
}
```

### GET /orders

List orders with pagination and optional filters.

**Query Parameters:**
- `page` (default: 1) - Page number
- `limit` (default: 10, max: 100) - Items per page
- `status` - Filter by order status
- `min_amount` - Minimum order amount
- `max_amount` - Maximum order amount
- `start_date` - Start date (YYYY-MM-DD)
- `end_date` - End date (YYYY-MM-DD)

**Example requests:**

```bash
# Get first page with 10 items
GET /orders?page=1&limit=10

# Filter paid orders
GET /orders?status=paid&limit=20

# Filter by amount range
GET /orders?min_amount=100&max_amount=1000

# Filter by date range
GET /orders?start_date=2024-11-01&end_date=2025-12-31

# Combined filters
GET /orders?status=shipped&min_amount=50&max_amount=500&page=1&limit=20
```

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "customer_name": "Customer 1",
      "status": "paid",
      "amount": 1234.56,
      "currency": "USD",
      "created_at": "2024-11-15"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 50,
  "total_pages": 5
}
```

## Database

The API uses SQLite for data storage. The database file (`orders.db`) is created automatically in the `app/` directory.

**Custom database path:**
Set the `ORDERS_DB_PATH` environment variable:
```bash
# Windows
set ORDERS_DB_PATH=path\to\orders.db

# macOS/Linux
export ORDERS_DB_PATH=path/to/orders.db
```

**Seed data:**
50 sample orders are automatically created on first startup.

## Testing

Run all tests:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=app --cov-report=term-missing
```

Run specific test file:
```bash
pytest tests/test_orders.py -v
```

### Test Coverage

The test suite includes 15 test cases covering:
- ✅ Order creation with valid data
- ✅ Validation errors (invalid status, negative amount)
- ✅ Pagination (page/limit parameters)
- ✅ Status filtering
- ✅ Amount range filtering
- ✅ Date range filtering
- ✅ Combined filters
- ✅ Edge cases (invalid date range, out-of-range pages, limit validation)

Target: **80%+ code coverage**

## Project Structure

```
orders_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and endpoints
│   ├── db.py            # Database operations
│   ├── schemas.py       # Pydantic models
│   ├── seed.py          # Database seeding script
│   └── orders.db        # SQLite database (auto-created)
├── tests/
│   ├── __init__.py
│   └── test_orders.py   # Test cases
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Development

**Manual database seeding:**
```bash
python -m app.seed
```

**Clear and reseed database:**
Delete `app/orders.db` and restart the server.

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `400 Bad Request` - Invalid query parameters (e.g., start_date > end_date)
- `422 Unprocessable Entity` - Validation errors in request body

## License

This project is created for educational purposes as part of the AI-Assisted Development course.
