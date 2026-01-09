# Metabase API Skill for Claude Code

A comprehensive skill for managing SQL scripts and questions in self-hosted Metabase via REST API.

## Quick Start

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   export METABASE_URL="https://your-metabase.com"
   export METABASE_USERNAME="your-email@example.com"
   export METABASE_PASSWORD="your-password"
   # OR use API key (recommended)
   export METABASE_API_KEY="your-api-key"
   ```

3. **Test connection:**
   ```bash
   python metabase_helper.py
   ```

### Using with Claude Code

Once installed as a skill, Claude Code can:
- Create SQL questions/cards in Metabase
- Execute queries and retrieve results
- Manage collections and organize cards
- Bulk import SQL scripts
- Update existing cards

## Basic Usage

### Python API

```python
from metabase_helper import MetabaseClient

# Initialize client
mb = MetabaseClient(
    base_url="https://metabase.example.com",
    api_key="your-api-key"
)

# Create a SQL card
card = mb.create_card(
    name="Daily Active Users",
    sql_query="""
        SELECT 
            DATE(created_at) as date,
            COUNT(DISTINCT user_id) as active_users
        FROM events
        WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    """,
    database_id=1,
    description="Shows daily active users for the last 30 days"
)

print(f"Card created: {mb.base_url}/question/{card['id']}")
```

### Common Tasks

#### List Available Databases
```python
databases = mb.list_databases()
for db in databases:
    print(f"{db['name']} (ID: {db['id']})")
```

#### Execute Query Without Saving
```python
results = mb.execute_query(
    sql_query="SELECT COUNT(*) as total FROM users",
    database_id=1
)
print(f"Total users: {results['data']['rows'][0][0]}")
```

#### Organize Cards in Collections
```python
# Create a collection
collection = mb.create_collection(
    name="Analytics Reports",
    description="All analytics-related queries"
)

# Create cards in the collection
mb.create_card(
    name="Revenue by Month",
    sql_query="SELECT DATE_TRUNC('month', order_date) as month, SUM(total) FROM orders GROUP BY month",
    database_id=1,
    collection_id=collection['id']
)
```

#### Bulk Import SQL Scripts
```python
cards_to_create = [
    {
        "name": "Active Users Count",
        "query": "SELECT COUNT(*) FROM users WHERE active = true",
        "description": "Total active users"
    },
    {
        "name": "Revenue Today",
        "query": "SELECT SUM(amount) FROM orders WHERE DATE(created_at) = CURRENT_DATE",
        "description": "Today's revenue"
    }
]

results = mb.bulk_create_cards(
    cards=cards_to_create,
    database_id=1,
    collection_id=collection['id']
)
```

## Advanced Usage

### Parameterized Queries

Create cards with parameters for dashboard filters:

```python
query = """
SELECT 
    status,
    COUNT(*) as count,
    AVG(total) as avg_amount
FROM orders
WHERE created_at >= {{start_date}}
  AND created_at <= {{end_date}}
GROUP BY status
"""

# Note: Template tags configuration would need to be added to the payload
# See SKILL.md for detailed template-tags structure
```

### Error Handling

```python
from metabase_helper import MetabaseError

try:
    card = mb.create_card(
        name="Test Query",
        sql_query="SELECT * FROM nonexistent_table",
        database_id=1
    )
except MetabaseError as e:
    print(f"Error creating card: {e}")
```

### Working with Multiple Environments

```python
# Production
prod_mb = MetabaseClient(
    base_url="https://metabase-prod.example.com",
    api_key=os.getenv('METABASE_PROD_KEY')
)

# Staging
staging_mb = MetabaseClient(
    base_url="https://metabase-staging.example.com",
    api_key=os.getenv('METABASE_STAGING_KEY')
)

# Clone cards from staging to production
staging_cards = staging_mb.list_cards()
for card in staging_cards:
    if card['collection_id'] == STAGING_COLLECTION_ID:
        card_data = staging_mb.get_card(card['id'])
        prod_mb.create_card(
            name=card_data['name'],
            sql_query=card_data['dataset_query']['native']['query'],
            database_id=PROD_DATABASE_ID
        )
```

## Example Scripts

### Import SQL Files

```python
import os
import glob
from metabase_helper import MetabaseClient

mb = MetabaseClient(
    base_url=os.getenv('METABASE_URL'),
    api_key=os.getenv('METABASE_API_KEY')
)

# Read all SQL files from a directory
sql_files = glob.glob("queries/*.sql")

for sql_file in sql_files:
    with open(sql_file, 'r') as f:
        sql_content = f.read()
    
    # Extract name from filename
    name = os.path.splitext(os.path.basename(sql_file))[0].replace('_', ' ').title()
    
    # Create card
    mb.create_card(
        name=name,
        sql_query=sql_content,
        database_id=1,
        description=f"Imported from {sql_file}"
    )
```

### Export Cards to SQL Files

```python
import os
from metabase_helper import MetabaseClient

mb = MetabaseClient(
    base_url=os.getenv('METABASE_URL'),
    api_key=os.getenv('METABASE_API_KEY')
)

cards = mb.list_cards()
os.makedirs("exported_queries", exist_ok=True)

for card in cards:
    card_detail = mb.get_card(card['id'])
    if card_detail['dataset_query']['type'] == 'native':
        query = card_detail['dataset_query']['native']['query']
        filename = f"exported_queries/{card['id']}_{card['name'].replace(' ', '_')}.sql"
        
        with open(filename, 'w') as f:
            f.write(f"-- Card: {card['name']}\n")
            f.write(f"-- ID: {card['id']}\n")
            f.write(f"-- Description: {card.get('description', 'N/A')}\n\n")
            f.write(query)
        
        print(f"Exported: {filename}")
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
METABASE_URL=https://metabase.example.com
METABASE_API_KEY=your-api-key-here
# OR
METABASE_USERNAME=user@example.com
METABASE_PASSWORD=your-password

# Optional
METABASE_DEFAULT_DATABASE_ID=1
METABASE_DEFAULT_COLLECTION_ID=5
```

Load with:

```python
from dotenv import load_dotenv
load_dotenv()

mb = MetabaseClient(
    base_url=os.getenv('METABASE_URL'),
    api_key=os.getenv('METABASE_API_KEY')
)
```

## API Reference

See `SKILL.md` for complete API documentation including:
- All available endpoints
- Request/response formats
- Error handling
- Security best practices
- Advanced features

## Troubleshooting

### Authentication Issues

**Problem:** 401 Unauthorized
```python
# Solution: Refresh session token
mb._authenticate()
```

**Problem:** API key not working
```
# Verify API key is set correctly
import os
print(os.getenv('METABASE_API_KEY'))
```

### Query Errors

**Problem:** SQL syntax error
```python
# Test query first
try:
    result = mb.execute_query(sql_query, database_id)
    print("Query valid:", result['data']['rows'])
except MetabaseError as e:
    print("Query error:", e)
```

### Rate Limiting

Session creation is rate-limited. Use API keys for automation or cache session tokens:

```python
# Cache token
mb = MetabaseClient(base_url=url, username=user, password=pwd)
token = mb.session_token

# Reuse token
mb_reused = MetabaseClient(base_url=url, session_token=token)
```

## Contributing

To extend this skill:
1. Add new methods to `MetabaseClient` class
2. Update `SKILL.md` with new capabilities
3. Add examples to this README

## License

MIT License - Feel free to use and modify as needed.
