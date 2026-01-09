# Claude Code Usage Instructions

## For Claude Code

When a user asks you to work with Metabase, follow these steps:

### Setup (First Time Only)

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   - Ask user for Metabase URL, credentials
   - Create `.env` file from `.env.example`
   - Set appropriate values

3. **Verify Connection:**
   ```bash
   python metabase_cli.py databases
   ```

### Common Tasks

#### Creating a SQL Card

**User says:** "Add this SQL query to Metabase"

```bash
python metabase_cli.py create "Query Name" \
  --database-id 1 \
  --sql "SELECT * FROM users LIMIT 10" \
  --description "Description here"
```

Or from file:
```bash
python metabase_cli.py create "Query Name" \
  --database-id 1 \
  --sql-file query.sql
```

#### Bulk Import SQL Files

**User says:** "Import all SQL files from the queries folder"

```bash
python metabase_cli.py import "queries/*.sql" --database-id 1
```

#### Execute Query Without Saving

**User says:** "Run this query and show me the results"

```bash
python metabase_cli.py query \
  --database-id 1 \
  --sql "SELECT COUNT(*) FROM orders" \
  --show-results
```

#### Organize Into Collections

**User says:** "Create a collection for analytics queries"

```bash
# Create collection
python metabase_cli.py create-collection "Analytics" \
  --description "Analytics queries"

# Then create cards in that collection
python metabase_cli.py create "Revenue Query" \
  --database-id 1 \
  --collection-id 5 \
  --sql "SELECT SUM(amount) FROM orders"
```

### Python API Usage

For more complex operations, use the Python API directly:

```python
from metabase_helper import MetabaseClient
import os

mb = MetabaseClient(
    base_url=os.getenv('METABASE_URL'),
    api_key=os.getenv('METABASE_API_KEY')
)

# Create card
card = mb.create_card(
    name="Custom Query",
    sql_query="SELECT * FROM users",
    database_id=1
)
```

### Decision Tree

**User wants to:**
- **Add ONE SQL query** → Use `metabase_cli.py create`
- **Add MULTIPLE SQL files** → Use `metabase_cli.py import`
- **Test query first** → Use `metabase_cli.py query`
- **Complex workflow** → Write Python script using `metabase_helper`
- **See what's available** → Use `databases`, `cards`, `collections` commands

### Common Patterns

#### Pattern 1: SQL File → Metabase Card
```python
# Read SQL file
with open('query.sql', 'r') as f:
    sql = f.read()

# Create card
mb.create_card(
    name="Query from file",
    sql_query=sql,
    database_id=1
)
```

#### Pattern 2: Organize Multiple Queries
```python
# Create collection
coll = mb.create_collection(name="Reports")

# Add queries to collection
queries = [
    {"name": "Q1", "query": "SELECT 1"},
    {"name": "Q2", "query": "SELECT 2"}
]

mb.bulk_create_cards(
    cards=queries,
    database_id=1,
    collection_id=coll['id']
)
```

#### Pattern 3: Test Then Save
```python
# Test query first
result = mb.execute_query(sql_query, database_id=1)
print(f"Query returned {len(result['data']['rows'])} rows")

# If successful, create card
if result['status'] == 'completed':
    mb.create_card(name="Tested Query", sql_query=sql_query, database_id=1)
```

### Error Handling

Always wrap operations in try-except:

```python
from metabase_helper import MetabaseError

try:
    card = mb.create_card(...)
except MetabaseError as e:
    print(f"Failed: {e}")
    # Suggest fixes to user
```

### Tips for Claude Code

1. **Always validate inputs** before making API calls
2. **Show URLs** for created resources
3. **Use meaningful names** for cards
4. **Test queries** with `execute_query()` first
5. **Handle errors gracefully** and explain to user
6. **Organize with collections** for better management

### Quick Reference

```bash
# List resources
metabase_cli.py databases        # Show databases
metabase_cli.py cards            # Show all cards
metabase_cli.py collections      # Show collections

# Get details
metabase_cli.py get <card-id>    # Card details

# Create resources
metabase_cli.py create ...       # New card
metabase_cli.py create-collection ... # New collection

# Execute
metabase_cli.py query ...        # Run query

# Bulk operations
metabase_cli.py import ...       # Import SQL files

# Delete
metabase_cli.py delete <card-id> # Delete card
```

### Examples Reference

Run the examples script to see all features:
```bash
python examples.py
```

This will demonstrate:
- Listing resources
- Creating cards
- Executing queries
- Managing collections
- Complex SQL
- Error handling
