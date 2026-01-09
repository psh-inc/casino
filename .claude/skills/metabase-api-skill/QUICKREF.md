# Metabase API Skill - Quick Reference Card

## Installation
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

## Environment Setup
```env
METABASE_URL=https://your-metabase.com
METABASE_API_KEY=your-api-key
```

## CLI Commands

### View Resources
```bash
metabase_cli.py databases              # List databases
metabase_cli.py cards                  # List all cards
metabase_cli.py collections            # List collections
metabase_cli.py get <card-id>          # Get card details
```

### Create Resources
```bash
# Create card from SQL string
metabase_cli.py create "Card Name" \
  --database-id 1 \
  --sql "SELECT * FROM users"

# Create card from file
metabase_cli.py create "Card Name" \
  --database-id 1 \
  --sql-file query.sql \
  --collection-id 5

# Create collection
metabase_cli.py create-collection "Collection Name" \
  --description "Description"
```

### Execute Queries
```bash
# Run query
metabase_cli.py query \
  --database-id 1 \
  --sql "SELECT COUNT(*) FROM orders" \
  --show-results

# Run from file
metabase_cli.py query \
  --database-id 1 \
  --sql-file query.sql \
  --show-results
```

### Bulk Operations
```bash
# Import all SQL files
metabase_cli.py import "queries/*.sql" \
  --database-id 1 \
  --collection-id 5
```

### Delete
```bash
metabase_cli.py delete <card-id>       # Delete card
metabase_cli.py delete <card-id> -f    # Force delete (no confirm)
```

## Python API

### Initialize Client
```python
from metabase_helper import MetabaseClient
import os

mb = MetabaseClient(
    base_url=os.getenv('METABASE_URL'),
    api_key=os.getenv('METABASE_API_KEY')
)
```

### Create Card
```python
card = mb.create_card(
    name="Query Name",
    sql_query="SELECT * FROM users",
    database_id=1,
    collection_id=5,  # Optional
    description="Query description"  # Optional
)
# Returns: {'id': 123, 'name': 'Query Name', ...}
```

### Execute Query
```python
result = mb.execute_query(
    sql_query="SELECT COUNT(*) FROM orders",
    database_id=1
)
# Returns: {'data': {'rows': [[42]], 'cols': [...]}, ...}
```

### List Resources
```python
databases = mb.list_databases()
cards = mb.list_cards()
collections = mb.list_collections()
```

### Get Details
```python
card = mb.get_card(card_id)
metadata = mb.get_database_metadata(database_id)
items = mb.get_collection_items(collection_id)
```

### Update Card
```python
mb.update_card(
    card_id=123,
    name="New Name",
    sql_query="NEW SQL",
    description="Updated"
)
```

### Create Collection
```python
collection = mb.create_collection(
    name="Analytics",
    description="Analytics queries",
    parent_id=None  # Or parent collection ID
)
```

### Bulk Create
```python
cards = [
    {"name": "Q1", "query": "SELECT 1", "description": "First"},
    {"name": "Q2", "query": "SELECT 2", "description": "Second"}
]

results = mb.bulk_create_cards(
    cards=cards,
    database_id=1,
    collection_id=5
)
```

### Delete Card
```python
mb.delete_card(card_id)
```

### Run Saved Card
```python
result = mb.run_card_query(card_id)
# Or export as CSV
csv_data = mb.run_card_query(card_id, export_format="csv")
```

## Common Patterns

### Test Query Before Saving
```python
# Test
result = mb.execute_query(sql_query, database_id=1)
print(f"Rows: {len(result['data']['rows'])}")

# If OK, save
if result['status'] == 'completed':
    card = mb.create_card(name, sql_query, database_id)
```

### Import SQL Files
```python
import glob

sql_files = glob.glob("queries/*.sql")
for sql_file in sql_files:
    with open(sql_file, 'r') as f:
        sql = f.read()
    
    name = os.path.basename(sql_file).replace('.sql', '')
    mb.create_card(name, sql, database_id=1)
```

### Organize into Collections
```python
# Create collection
coll = mb.create_collection(name="Reports")

# Add queries
mb.create_card(
    name="Query 1",
    sql_query="SELECT 1",
    database_id=1,
    collection_id=coll['id']
)
```

## Error Handling
```python
from metabase_helper import MetabaseError

try:
    card = mb.create_card(...)
except MetabaseError as e:
    print(f"Error: {e}")
```

## Authentication Methods

### API Key (Recommended)
```python
mb = MetabaseClient(
    base_url="https://metabase.example.com",
    api_key="your-api-key"
)
```

### Username/Password
```python
mb = MetabaseClient(
    base_url="https://metabase.example.com",
    username="user@example.com",
    password="password"
)
```

### Session Token
```python
mb = MetabaseClient(
    base_url="https://metabase.example.com",
    session_token="existing-token"
)
```

## Files Reference

| File | Purpose |
|------|---------|
| SKILL.md | Complete API reference for Claude |
| README.md | Usage documentation and examples |
| INSTALL.md | Installation instructions |
| CLAUDE.md | Claude Code integration guide |
| OVERVIEW.md | High-level overview |
| metabase_helper.py | Python API client library |
| metabase_cli.py | Command-line tool |
| examples.py | Example usage scripts |
| requirements.txt | Python dependencies |
| .env.example | Environment template |

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200/201 | Success |
| 400 | Bad request (invalid data) |
| 401 | Unauthorized (invalid auth) |
| 403 | Forbidden (no permission) |
| 404 | Not found |
| 500 | Server error |

## Tips

- Use `--json` flag for raw JSON output
- Use `-v` flag for verbose output
- Test queries with `query` command first
- Organize cards in collections
- Use meaningful names and descriptions
- Validate SQL before creating cards

## Getting Help

```bash
metabase_cli.py --help              # General help
metabase_cli.py create --help       # Command-specific help
python examples.py                  # Run examples
```

---

**Quick Start:** `INSTALL.md` → `examples.py` → Start using!
