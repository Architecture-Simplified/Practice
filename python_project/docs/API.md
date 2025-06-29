# API Documentation

## Overview

This document describes the API endpoints and usage for the Python Project.

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

### API Key Authentication
```http
Authorization: Bearer YOUR_API_KEY
```

### Example Request
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://your-domain.com/api/v1/endpoint
```

## Endpoints

### Health Check
Check if the API is running.

**GET** `/health`

#### Response
```json
{
    "status": "healthy",
    "timestamp": "2025-06-30T10:00:00Z",
    "version": "1.0.0"
}
```

### Data Endpoints

#### Get All Items
Retrieve all items with optional filtering.

**GET** `/items`

##### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Number of items to return (default: 10) |
| `offset` | integer | No | Number of items to skip (default: 0) |
| `filter` | string | No | Filter criteria |

##### Example Request
```bash
curl "http://localhost:8000/api/v1/items?limit=5&offset=0"
```

##### Response
```json
{
    "items": [
        {
            "id": 1,
            "name": "Item 1",
            "description": "Description of item 1",
            "created_at": "2025-06-30T10:00:00Z"
        }
    ],
    "total": 100,
    "limit": 5,
    "offset": 0
}
```

#### Get Item by ID
Retrieve a specific item by its ID.

**GET** `/items/{id}`

##### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Item ID |

##### Response
```json
{
    "id": 1,
    "name": "Item 1",
    "description": "Description of item 1",
    "created_at": "2025-06-30T10:00:00Z",
    "updated_at": "2025-06-30T10:00:00Z"
}
```

#### Create Item
Create a new item.

**POST** `/items`

##### Request Body
```json
{
    "name": "New Item",
    "description": "Description of the new item"
}
```

##### Response
```json
{
    "id": 2,
    "name": "New Item",
    "description": "Description of the new item",
    "created_at": "2025-06-30T10:00:00Z",
    "updated_at": "2025-06-30T10:00:00Z"
}
```

#### Update Item
Update an existing item.

**PUT** `/items/{id}`

##### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Item ID |

##### Request Body
```json
{
    "name": "Updated Item",
    "description": "Updated description"
}
```

##### Response
```json
{
    "id": 1,
    "name": "Updated Item",
    "description": "Updated description",
    "created_at": "2025-06-30T10:00:00Z",
    "updated_at": "2025-06-30T10:00:00Z"
}
```

#### Delete Item
Delete an item by ID.

**DELETE** `/items/{id}`

##### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Item ID |

##### Response
```json
{
    "message": "Item deleted successfully"
}
```

## Error Handling

### Error Response Format
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": "Additional error details"
    }
}
```

### HTTP Status Codes
| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

### Common Errors

#### Validation Error
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "name": ["This field is required"],
            "email": ["Invalid email format"]
        }
    }
}
```

#### Not Found Error
```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Item with ID 999 not found"
    }
}
```

## Rate Limiting

- Rate limit: 1000 requests per hour per API key
- Rate limit headers are included in responses:
  - `X-RateLimit-Limit`: Request limit per hour
  - `X-RateLimit-Remaining`: Requests remaining in current window
  - `X-RateLimit-Reset`: Time when rate limit resets (Unix timestamp)

## Pagination

Large datasets are paginated using offset-based pagination:

```json
{
    "items": [...],
    "pagination": {
        "total": 1000,
        "limit": 20,
        "offset": 40,
        "has_next": true,
        "has_prev": true,
        "next_url": "/api/v1/items?limit=20&offset=60",
        "prev_url": "/api/v1/items?limit=20&offset=20"
    }
}
```

## SDK Examples

### Python
```python
import requests

# Configure API client
API_BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Get all items
response = requests.get(f"{API_BASE_URL}/items", headers=headers)
items = response.json()

# Create new item
new_item = {
    "name": "New Item",
    "description": "Item description"
}
response = requests.post(f"{API_BASE_URL}/items", json=new_item, headers=headers)
created_item = response.json()
```

### JavaScript
```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
const API_KEY = 'your-api-key';

const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
};

// Get all items
fetch(`${API_BASE_URL}/items`, { headers })
    .then(response => response.json())
    .then(data => console.log(data));

// Create new item
const newItem = {
    name: 'New Item',
    description: 'Item description'
};

fetch(`${API_BASE_URL}/items`, {
    method: 'POST',
    headers,
    body: JSON.stringify(newItem)
})
.then(response => response.json())
.then(data => console.log(data));
```

## Webhooks

Configure webhooks to receive notifications about events:

### Webhook Events
- `item.created` - New item created
- `item.updated` - Item updated
- `item.deleted` - Item deleted

### Webhook Payload
```json
{
    "event": "item.created",
    "timestamp": "2025-06-30T10:00:00Z",
    "data": {
        "id": 1,
        "name": "New Item",
        "description": "Item description"
    }
}
```

## Testing

Use the provided test endpoints to verify your integration:

**GET** `/test/echo` - Echo back request data
**POST** `/test/webhook` - Test webhook endpoint

## Support

For API support:
- Check the [FAQ](./FAQ.md)
- Create an issue on GitHub
- Contact support: api-support@example.com
