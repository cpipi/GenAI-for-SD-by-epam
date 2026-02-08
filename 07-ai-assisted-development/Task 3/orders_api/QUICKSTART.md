# Quick Start Guide

## Run the API

```powershell
cd "g:\EPAM\GenAI-for-SD-by-epam\07-ai-assisted-development\Task 3\orders_api"
.\.venv312\Scripts\activate
uvicorn app.main:app --reload
```

Open browser: http://127.0.0.1:8000/docs

## Run Tests

```powershell
.\.venv312\Scripts\pytest -v --cov=app --cov-report=term-missing
```

## Example API Calls

### Get orders (first page)
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/orders?page=1&limit=10" -Method GET
```

### Create order
```powershell
$body = @{
    customer_name = "John Doe"
    status = "paid"
    amount = 199.99
    currency = "USD"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/orders" -Method POST -Body $body -ContentType "application/json"
```

### Filter orders
```powershell
# By status
Invoke-WebRequest -Uri "http://127.0.0.1:8000/orders?status=paid&limit=20"

# By amount range
Invoke-WebRequest -Uri "http://127.0.0.1:8000/orders?min_amount=100&max_amount=500"

# By date range
Invoke-WebRequest -Uri "http://127.0.0.1:8000/orders?start_date=2024-11-01&end_date=2025-12-31"
```

### Get single order
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/orders/1" -Method GET
```

### Get statistics
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/stats/summary" -Method GET
```

## Project Files

- **README.md** - Full documentation
- **COPILOT_METRICS_REPORT.md** - Copilot usage metrics
- **PROJECT_SUMMARY.md** - Project overview and assessment
- **app/** - API source code
- **tests/** - Test suite
