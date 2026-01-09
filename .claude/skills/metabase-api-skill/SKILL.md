---
name: metabase-api-skill
description: |
  Add, manage, and execute SQL scripts in self-hosted Metabase via REST API.
  Supports creating cards/questions, running queries, and managing collections.
  Use when: Creating Metabase dashboards programmatically, automating report generation,
  managing SQL questions/cards via API, or integrating Metabase with the casino platform.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Metabase API Skill

This skill covers programmatic interaction with Metabase's REST API for the casino platform. Use it for creating SQL-based cards (questions), managing collections, running ad-hoc queries, and automating dashboard creation. The casino platform uses Metabase for affiliate reporting (CellExpert metrics), player analytics, and transaction reporting.

## Quick Start

### Authentication

```bash
# Get session token
curl -X POST https://metabase.example.com/api/session \
  -H "Content-Type: application/json" \
  -d '{"username": "admin@casino.com", "password": "secret"}'

# Response: {"id": "session-token-here"}
```

### Create a SQL Card

```bash
curl -X POST https://metabase.example.com/api/card \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{
    "name": "Player Deposits by Currency",
    "dataset_query": {
      "type": "native",
      "native": {
        "query": "SELECT currency, SUM(amount) as total FROM transactions WHERE type = '\''DEPOSIT'\'' GROUP BY currency",
        "template-tags": {}
      },
      "database": 1
    },
    "display": "bar",
    "visualization_settings": {},
    "collection_id": 5
  }'
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Card | A saved question/query | SQL or GUI-based query |
| Collection | Folder for organizing cards | `collection_id: 5` |
| Database | Connected data source | PostgreSQL casino DB |
| Dashboard | Container for multiple cards | Player Overview |
| Template Tags | Parameterized queries | `{{player_id}}` |

## Common Patterns

### Execute Ad-hoc Query

**When:** Running one-off queries for debugging or data exploration

```bash
curl -X POST https://metabase.example.com/api/dataset \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{
    "database": 1,
    "type": "native",
    "native": {
      "query": "SELECT * FROM players WHERE id = {{player_id}}",
      "template-tags": {
        "player_id": {"type": "number", "name": "player_id", "display-name": "Player ID"}
      }
    },
    "parameters": [{"type": "number", "target": ["variable", ["template-tag", "player_id"]], "value": 12345}]
  }'
```

### List Collections

**When:** Finding where to place new cards

```bash
curl -X GET https://metabase.example.com/api/collection \
  -H "X-Metabase-Session: ${SESSION_TOKEN}"
```

## See Also

- [patterns](references/patterns.md) - Card creation, query optimization, error handling
- [workflows](references/workflows.md) - Dashboard automation, report scheduling

## Related Skills

- See the **postgresql** skill for SQL query optimization and schema design
- See the **spring-boot** skill for backend API integration with Metabase