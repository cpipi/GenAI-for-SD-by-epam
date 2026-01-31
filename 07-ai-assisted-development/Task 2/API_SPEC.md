# API Specification - Data Validation Module

## Base Information

- **API Version:** 1.0.0
- **Base URL:** `http://localhost:3000/api/v1`
- **Content-Type:** `application/json`
- **Authentication:** Not required (for demo purposes)

---

## Endpoints

### 1. POST /validate

Validates input data against predefined validation rules.

#### Endpoint
```
POST /api/v1/validate
```

#### Description
Validates a single field (email, password, or phone) and returns whether it's valid along with any error messages.

#### Request Headers
```
Content-Type: application/json
```

#### Request Body
```json
{
  "type": "email|password|phone",
  "value": "string"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Type of validation: 'email', 'password', or 'phone' |
| value | string | Yes | The value to validate |

#### Response Format

**Success Response (200 OK):**
```json
{
  "valid": true,
  "errors": []
}
```

**Validation Failed Response (200 OK):**
```json
{
  "valid": false,
  "errors": [
    "Error message 1",
    "Error message 2"
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid request",
  "message": "Type must be one of: email, password, phone"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

#### Examples

**Example 1: Valid Email**
```bash
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "email",
    "value": "user@example.com"
  }'
```

Response:
```json
{
  "valid": true,
  "errors": []
}
```

**Example 2: Invalid Email**
```bash
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "email",
    "value": "invalid-email"
  }'
```

Response:
```json
{
  "valid": false,
  "errors": [
    "Invalid email format",
    "Invalid email domain"
  ]
}
```

**Example 3: Valid Password**
```bash
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "password",
    "value": "SecurePass123!"
  }'
```

Response:
```json
{
  "valid": true,
  "errors": []
}
```

**Example 4: Invalid Password**
```bash
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "password",
    "value": "weak"
  }'
```

Response:
```json
{
  "valid": false,
  "errors": [
    "Password must be at least 8 characters long",
    "Password must contain at least one number",
    "Password must contain at least one special character"
  ]
}
```

**Example 5: Valid Phone**
```bash
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "phone",
    "value": "+1234567890"
  }'
```

Response:
```json
{
  "valid": true,
  "errors": []
}
```

**Example 6: Invalid Phone**
```bash
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "phone",
    "value": "1234567890"
  }'
```

Response:
```json
{
  "valid": false,
  "errors": [
    "Phone number must start with + and country code"
  ]
}
```

---

### 2. GET /validation-rules

Returns all active validation rules from the database.

#### Endpoint
```
GET /api/v1/validation-rules
```

#### Description
Retrieves all validation rules stored in the database, optionally filtered by type.

#### Request Headers
```
Content-Type: application/json
```

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | No | Filter rules by type: 'email', 'password', or 'phone' |
| active | boolean | No | Filter by active status (default: true) |

#### Response Format

**Success Response (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": 1,
      "rule_name": "email_format",
      "rule_type": "email",
      "regex_pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
      "error_message": "Invalid email format",
      "description": "RFC 5322 compliant email format",
      "priority": 1,
      "is_active": true,
      "created_at": "2026-01-31T10:00:00Z",
      "updated_at": "2026-01-31T10:00:00Z"
    }
  ]
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "error": "Database connection failed",
  "message": "Could not retrieve validation rules"
}
```

#### Examples

**Example 1: Get All Rules**
```bash
curl -X GET http://localhost:3000/api/v1/validation-rules
```

Response:
```json
{
  "success": true,
  "count": 14,
  "data": [
    {
      "id": 1,
      "rule_name": "email_required",
      "rule_type": "email",
      "regex_pattern": "^.+$",
      "error_message": "Email is required",
      "description": "Checks if email is not empty",
      "priority": 1,
      "is_active": true,
      "created_at": "2026-01-31T10:00:00Z",
      "updated_at": "2026-01-31T10:00:00Z"
    },
    ...
  ]
}
```

**Example 2: Get Email Rules Only**
```bash
curl -X GET "http://localhost:3000/api/v1/validation-rules?type=email"
```

Response:
```json
{
  "success": true,
  "count": 4,
  "data": [
    {
      "id": 1,
      "rule_name": "email_required",
      "rule_type": "email",
      "regex_pattern": "^.+$",
      "error_message": "Email is required",
      "description": "Checks if email is not empty",
      "priority": 1,
      "is_active": true,
      "created_at": "2026-01-31T10:00:00Z",
      "updated_at": "2026-01-31T10:00:00Z"
    },
    ...
  ]
}
```

**Example 3: Get Password Rules**
```bash
curl -X GET "http://localhost:3000/api/v1/validation-rules?type=password"
```

Response:
```json
{
  "success": true,
  "count": 6,
  "data": [
    {
      "id": 5,
      "rule_name": "password_length_min",
      "rule_type": "password",
      "regex_pattern": "^.{8,}$",
      "error_message": "Password must be at least 8 characters long",
      "description": "Minimum length requirement",
      "priority": 2,
      "is_active": true,
      "created_at": "2026-01-31T10:00:00Z",
      "updated_at": "2026-01-31T10:00:00Z"
    },
    ...
  ]
}
```

---

## Error Codes

| HTTP Code | Error Type | Description |
|-----------|------------|-------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid request parameters or body |
| 404 | Not Found | Endpoint not found |
| 422 | Unprocessable Entity | Valid syntax but semantic errors |
| 500 | Internal Server Error | Server-side error occurred |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## Common Error Messages

### Validation Errors

#### Email Errors
- `Email is required`
- `Invalid email format`
- `Email local part must be between 1 and 64 characters`
- `Invalid email domain`
- `Email contains invalid characters`

#### Password Errors
- `Password is required`
- `Password must be at least 8 characters long`
- `Password must not exceed 128 characters`
- `Password must contain at least one number`
- `Password must contain at least one special character`
- `Password must contain at least one letter`

#### Phone Errors
- `Phone number is required`
- `Phone number must start with + and country code`
- `Phone number must contain between 10 and 15 digits`
- `Phone number contains invalid characters`
- `Invalid phone number format`

---

## Rate Limiting

**Current Implementation:** No rate limiting

**Recommended for Production:**
- 100 requests per minute per IP address
- 1000 requests per hour per IP address
- Response header: `X-RateLimit-Remaining`

---

## Implementation Example (Node.js + Express)

```javascript
const express = require('express');
const { validateEmail, validatePassword, validatePhone } = require('./validation');
const { Pool } = require('pg');

const app = express();
const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

app.use(express.json());

// POST /validate endpoint
app.post('/api/v1/validate', async (req, res) => {
  try {
    const { type, value } = req.body;

    if (!type || !value) {
      return res.status(400).json({
        error: 'Invalid request',
        message: 'Both type and value are required'
      });
    }

    let result;
    switch (type) {
      case 'email':
        result = validateEmail(value);
        break;
      case 'password':
        result = validatePassword(value);
        break;
      case 'phone':
        result = validatePhone(value);
        break;
      default:
        return res.status(400).json({
          error: 'Invalid request',
          message: 'Type must be one of: email, password, phone'
        });
    }

    res.json(result);
  } catch (error) {
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

// GET /validation-rules endpoint
app.get('/api/v1/validation-rules', async (req, res) => {
  try {
    const { type, active = 'true' } = req.query;
    
    let query = 'SELECT * FROM validation_rules WHERE is_active = $1';
    const params = [active === 'true'];

    if (type) {
      query += ' AND rule_type = $2 ORDER BY priority';
      params.push(type);
    } else {
      query += ' ORDER BY rule_type, priority';
    }

    const result = await pool.query(query, params);

    res.json({
      success: true,
      count: result.rows.length,
      data: result.rows
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Database connection failed',
      message: error.message
    });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

---

## Testing with Postman

### Import Collection

Create a Postman collection with the following structure:

1. **Validate Email (Valid)**
   - Method: POST
   - URL: `{{base_url}}/validate`
   - Body: `{"type": "email", "value": "test@example.com"}`

2. **Validate Email (Invalid)**
   - Method: POST
   - URL: `{{base_url}}/validate`
   - Body: `{"type": "email", "value": "invalid"}`

3. **Validate Password (Valid)**
   - Method: POST
   - URL: `{{base_url}}/validate`
   - Body: `{"type": "password", "value": "Secure123!"}`

4. **Validate Phone (Valid)**
   - Method: POST
   - URL: `{{base_url}}/validate`
   - Body: `{"type": "phone", "value": "+1234567890"}`

5. **Get All Rules**
   - Method: GET
   - URL: `{{base_url}}/validation-rules`

6. **Get Email Rules**
   - Method: GET
   - URL: `{{base_url}}/validation-rules?type=email`

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-31 | Initial API specification |
