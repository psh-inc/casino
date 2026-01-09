---
name: metabase-api
description: Add, manage, and execute SQL scripts in self-hosted Metabase via REST API. Supports creating cards/questions, running queries, and managing collections.
---

# Metabase API Control Skill

This skill enables Claude to interact with a self-hosted Metabase instance through its REST API to create SQL cards (questions), execute queries, and manage resources.

## Prerequisites

Before using this skill, ensure:
1. Metabase instance is accessible (URL)
2. Valid credentials (username/password or API key)
3. Database ID for the target database in Metabase
4. Python 3.7+ with `requests` library installed

## Core Capabilities

### 1. Authentication
Metabase supports two authentication methods:

**Session Token (recommended for temporary use):**
- POST `/api/session` with credentials
- Returns session token valid for 14 days (configurable via MAX_SESSION_AGE env var)
- Use `X-Metabase-Session` header

**API Key (recommended for automation):**
- Use `X-Api-Key` header
- No expiration

### 2. Creating SQL Cards (Questions)

To add a SQL script as a saved question in Metabase:

**Endpoint:** `POST /api/card/`

**Required payload structure:**
```json
{
  "name": "Question Name",
  "display": "table",
  "description": "Optional description",
  "collection_id": null,
  "dataset_query": {
    "database": 1,
    "type": "native",
    "native": {
      "query": "SELECT * FROM users WHERE created_at > '2024-01-01'"
    }
  },
  "visualization_settings": {}
}
```

**Key fields:**
- `database`: Database ID in Metabase (integer)
- `type`: Must be "native" for SQL queries
- `native.query`: The actual SQL query string
- `display`: Visualization type ("table", "bar", "line", "pie", etc.)
- `collection_id`: Target collection ID, or null for root

### 3. Executing Queries

**Run ad-hoc SQL query without saving:**
- Endpoint: `POST /api/dataset/`
- Payload:
```json
{
  "database": 1,
  "type": "native",
  "native": {
    "query": "SELECT COUNT(*) FROM orders"
  }
}
```

**Run saved card query:**
- Endpoint: `POST /api/card/:card-id/query`
- Or: `GET /api/card/:card-id/query/:export-format` (csv, json, xlsx)

### 4. Managing Collections

**List collections:**
- `GET /api/collection/`

**Create collection:**
- `POST /api/collection/`
- Payload: `{"name": "Collection Name", "parent_id": null}`

**Get cards in collection:**
- `GET /api/collection/:id/items`

### 5. Database Operations

**List databases:**
- `GET /api/database/`

**Get database metadata:**
- `GET /api/database/:id/metadata`

## Helper Script Usage

The skill includes `metabase_helper.py` which provides convenient functions:

```python
from metabase_helper import MetabaseClient

# Initialize client
mb = MetabaseClient(
    base_url="https://metabase.example.com",
    username="user@example.com",
    password="password"
    # OR use api_key="your-api-key"
)

# Create a SQL card
card_id = mb.create_card(
    name="Daily Active Users",
    sql_query="SELECT DATE(created_at) as date, COUNT(*) FROM users GROUP BY date",
    database_id=1,
    collection_id=None,
    description="Shows daily user registrations"
)

# Execute ad-hoc query
results = mb.execute_query(
    sql_query="SELECT * FROM products LIMIT 10",
    database_id=1
)

# List all cards
cards = mb.list_cards()

# Get card details
card = mb.get_card(card_id)
```

## Common Workflows

### Creating a New SQL Question
1. Authenticate with Metabase
2. Identify target database ID
3. Prepare SQL query
4. (Optional) Find or create target collection
5. Create card with POST /api/card/
6. Verify creation with GET /api/card/:id

### Bulk SQL Script Import
1. Read SQL scripts from files
2. Parse into individual queries
3. For each query:
   - Extract metadata (name, description from comments)
   - Create card via API
   - Handle errors and log results

### Query Testing Before Saving
1. Execute query via POST /api/dataset/
2. Verify results and performance
3. If successful, create permanent card
4. Add to appropriate collection

## Error Handling

Common HTTP status codes:
- `200/201`: Success
- `400`: Bad request (invalid payload)
- `401`: Authentication failed (invalid/expired token)
- `403`: Forbidden (insufficient permissions)
- `404`: Resource not found
- `500`: Server error

## Security Best Practices

1. **Never hardcode credentials** - use environment variables
2. **Use API keys** for automated scripts instead of session tokens
3. **Implement token refresh** logic for long-running applications
4. **Validate SQL queries** before sending to prevent injection
5. **Use HTTPS** for all API communication
6. **Store tokens securely** and never commit to version control

## Advanced Features

### Parameterized Queries
Use template tags in SQL:
```sql
SELECT * FROM orders 
WHERE created_at > {{start_date}} 
  AND created_at < {{end_date}}
```

### Query Variables
Field filter variables for dynamic filtering:
```json
{
  "native": {
    "query": "SELECT * FROM orders WHERE status = {{status}}",
    "template-tags": {
      "status": {
        "type": "text",
        "id": "unique-id",
        "name": "status",
        "display-name": "Order Status"
      }
    }
  }
}
```

## Troubleshooting

**Issue:** 401 Unauthorized
- Solution: Regenerate session token or verify API key

**Issue:** Card not appearing in UI
- Solution: Check collection_id, ensure user has permissions

**Issue:** Query timeout
- Solution: Optimize SQL, increase timeout settings in Metabase

**Issue:** Invalid database ID
- Solution: List databases with GET /api/database/ to find correct ID

## References

- Official Metabase API docs: `https://your-metabase-instance.com/api/docs`
- API documentation: `/docs/api-documentation.md` in Metabase repo
- Community wiki: GitHub metabase/metabase Wiki

## Implementation Notes

When implementing Metabase operations:
1. Always validate inputs before API calls
2. Use meaningful names and descriptions for cards
3. Organize cards into collections for better management
4. Test queries before creating cards
5. Handle rate limits (session creation is rate-limited)
6. Cache session tokens to avoid re-authentication
7. Log all API operations for auditing
