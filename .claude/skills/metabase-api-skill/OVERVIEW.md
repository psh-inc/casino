# Metabase API Skill - Overview

## What is This?

A comprehensive Claude Code skill for managing SQL scripts and questions in self-hosted Metabase via REST API. This skill enables Claude to programmatically create, execute, and manage SQL cards (questions) in your Metabase instance.

## Directory Structure

```
metabase-api-skill/
├── SKILL.md              # Main skill definition (for Claude)
├── README.md             # Usage documentation
├── INSTALL.md            # Installation guide
├── CLAUDE.md             # Claude Code integration instructions
├── requirements.txt      # Python dependencies
├── .env.example          # Environment configuration template
├── .gitignore           # Git ignore rules
├── metabase_helper.py   # Core Python API client
├── metabase_cli.py      # Command-line interface tool
└── examples.py          # Example usage scripts
```

## Key Components

### 1. SKILL.md
The main skill definition that Claude reads. Contains:
- Complete API reference
- Authentication methods
- Request/response formats
- Best practices
- Troubleshooting guide

### 2. metabase_helper.py
Python client library providing:
- `MetabaseClient` class for API interactions
- Authentication management (API key or session token)
- Methods for all common operations:
  - `create_card()` - Create SQL questions
  - `execute_query()` - Run ad-hoc queries
  - `list_cards()` - List all cards
  - `create_collection()` - Organize cards
  - `bulk_create_cards()` - Import multiple queries
  - And many more...

### 3. metabase_cli.py
Command-line tool for easy operations:
```bash
# List databases
metabase_cli.py databases

# Create a card
metabase_cli.py create "Query Name" \
  --database-id 1 --sql "SELECT * FROM users"

# Import SQL files
metabase_cli.py import "queries/*.sql" --database-id 1

# Execute query
metabase_cli.py query --database-id 1 \
  --sql "SELECT COUNT(*) FROM orders" --show-results
```

### 4. examples.py
Demonstrates all features:
- Listing resources
- Creating cards with various configurations
- Executing queries
- Managing collections
- Complex SQL examples
- Error handling

## Capabilities

### Core Features
✓ Create SQL cards (questions) in Metabase
✓ Execute ad-hoc queries without saving
✓ Manage collections for organization
✓ Bulk import SQL files
✓ Update existing cards
✓ Delete cards
✓ List all resources (databases, cards, collections)
✓ Get detailed information about specific resources

### Authentication
✓ API Key (recommended for automation)
✓ Username/Password (session-based)
✓ Session token (manual management)
✓ Automatic token refresh

### Advanced Features
✓ Parameterized queries with template tags
✓ Custom visualization settings
✓ Field filters for dashboards
✓ Export query results (JSON, CSV, XLSX)
✓ Database metadata access
✓ Batch operations

## Use Cases

### 1. Single Query Creation
**Scenario:** User has a SQL query and wants to save it in Metabase

```python
mb.create_card(
    name="Daily Revenue",
    sql_query="SELECT DATE(created_at), SUM(total) FROM orders GROUP BY 1",
    database_id=1
)
```

### 2. Bulk SQL Import
**Scenario:** User has a folder of SQL files to import

```bash
metabase_cli.py import "analytics/*.sql" \
  --database-id 1 \
  --collection-id 5
```

### 3. Query Testing
**Scenario:** Test query before creating permanent card

```python
# Test first
result = mb.execute_query(sql_query, database_id=1)
if result['status'] == 'completed':
    # Then save
    mb.create_card(name="Tested Query", sql_query=sql_query, database_id=1)
```

### 4. Organization & Management
**Scenario:** Organize queries into logical collections

```python
# Create collection structure
analytics = mb.create_collection(name="Analytics")
reports = mb.create_collection(name="Reports", parent_id=analytics['id'])

# Add queries to collections
mb.create_card(
    name="Revenue Report",
    sql_query=query,
    database_id=1,
    collection_id=reports['id']
)
```

### 5. CI/CD Integration
**Scenario:** Deploy queries as part of deployment pipeline

```yaml
# GitHub Actions example
- name: Deploy Metabase Queries
  run: |
    python metabase_cli.py import "sql/*.sql" \
      --database-id ${{ secrets.DB_ID }}
```

## Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your Metabase URL and credentials
```

### 3. Test
```bash
python metabase_cli.py databases
```

### 4. Use with Claude Code
Just ask Claude:
- "Add this SQL query to Metabase"
- "Import all SQL files from the queries folder"
- "Create a collection called Analytics and add these queries"

Claude will use this skill automatically!

## API Quick Reference

```python
from metabase_helper import MetabaseClient

mb = MetabaseClient(base_url=url, api_key=key)

# Create
card = mb.create_card(name, sql_query, database_id)
collection = mb.create_collection(name)

# Read
databases = mb.list_databases()
cards = mb.list_cards()
card = mb.get_card(card_id)

# Execute
result = mb.execute_query(sql_query, database_id)
result = mb.run_card_query(card_id)

# Update
mb.update_card(card_id, name="New Name", sql_query="NEW SQL")

# Delete
mb.delete_card(card_id)

# Bulk
mb.bulk_create_cards(cards_list, database_id, collection_id)
```

## Configuration

Set these environment variables:

```env
METABASE_URL=https://metabase.example.com
METABASE_API_KEY=your-api-key

# OR use username/password
METABASE_USERNAME=user@example.com
METABASE_PASSWORD=password
```

## Error Handling

All operations raise `MetabaseError` on failure:

```python
from metabase_helper import MetabaseError

try:
    card = mb.create_card(...)
except MetabaseError as e:
    print(f"Error: {e}")
```

## Security Best Practices

1. ✓ Use API keys over username/password
2. ✓ Never commit `.env` file
3. ✓ Use HTTPS for all connections
4. ✓ Rotate API keys regularly
5. ✓ Limit API key permissions
6. ✓ Validate SQL queries before execution
7. ✓ Use environment variables for credentials

## Requirements

- Python 3.7+
- `requests` library
- `python-dotenv` library
- Self-hosted Metabase instance
- Valid Metabase credentials

## Integration with Claude Code

When this skill is installed in Claude Code, Claude can:

1. **Understand Metabase context** - Knows how to work with Metabase API
2. **Execute operations** - Can create, update, delete cards
3. **Handle authentication** - Manages session tokens and API keys
4. **Provide guidance** - Suggests best practices and error solutions
5. **Automate workflows** - Can batch process SQL files

Claude will automatically use this skill when you mention:
- "Metabase"
- "Create a SQL card"
- "Add query to Metabase"
- "Import SQL scripts"
- Similar database/BI tool operations

## Extending the Skill

To add new capabilities:

1. Add methods to `MetabaseClient` in `metabase_helper.py`
2. Add CLI commands to `metabase_cli.py`
3. Update documentation in `SKILL.md`
4. Add examples to `examples.py`

Example new method:

```python
def your_new_feature(self, param):
    """Your new feature description"""
    return self._make_request("GET", f"/api/your-endpoint/{param}")
```

## Support & Documentation

- **Full API docs:** See `SKILL.md`
- **Usage examples:** See `README.md` and `examples.py`
- **Installation:** See `INSTALL.md`
- **Claude integration:** See `CLAUDE.md`
- **Metabase API:** `https://your-metabase.com/api/docs`

## Version Information

- **Skill version:** 1.0.0
- **Metabase API:** Compatible with v0.32+
- **Python:** 3.7+
- **Claude Code:** Compatible with current version

## License

MIT License - Free to use and modify

## Contributors

Created for use with Claude Code and self-hosted Metabase instances.

---

**Ready to use!** Start with `INSTALL.md` for setup instructions.
