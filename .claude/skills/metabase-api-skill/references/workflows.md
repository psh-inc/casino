# Metabase API Workflows

## Dashboard Automation Workflow

### Step 1: Create Collection Structure

```bash
# Create parent collection for casino reports
curl -X POST https://metabase.example.com/api/collection \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{"name": "Casino Reports", "color": "#509EE3"}'

# Create sub-collection for affiliate reports
curl -X POST https://metabase.example.com/api/collection \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{"name": "CellExpert Affiliate", "parent_id": 15, "color": "#88BF4D"}'
```

### Step 2: Create Dashboard

```bash
curl -X POST https://metabase.example.com/api/dashboard \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{
    "name": "CellExpert Daily Overview",
    "collection_id": 16,
    "parameters": [
      {"name": "Date Range", "slug": "date_range", "type": "date/range", "default": "past30days"}
    ]
  }'
```

### Step 3: Add Cards to Dashboard

```bash
# Add existing card to dashboard
curl -X POST https://metabase.example.com/api/dashboard/5/cards \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{
    "cardId": 42,
    "row": 0,
    "col": 0,
    "size_x": 6,
    "size_y": 4,
    "parameter_mappings": [
      {"parameter_id": "date_range", "card_id": 42, "target": ["variable", ["template-tag", "start_date"]]}
    ]
  }'
```

## Report Generation Workflow

### Export Query Results

```bash
# Export as CSV
curl -X POST "https://metabase.example.com/api/card/${CARD_ID}/query/csv" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -o report.csv

# Export as JSON
curl -X POST "https://metabase.example.com/api/card/${CARD_ID}/query/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -o report.json
```

### WARNING: Large Dataset Exports

**The Problem:**

```bash
# BAD - No pagination for large exports
curl -X POST "https://metabase.example.com/api/dataset/csv" \
  -d '{"query": "SELECT * FROM transactions"}'  # Millions of rows
```

**Why This Breaks:**
1. Request times out after default 30 seconds
2. Memory exhaustion on Metabase server
3. Incomplete data exports without warning

**The Fix:**

```bash
# GOOD - Paginate large exports
for offset in $(seq 0 100000 500000); do
  curl -X POST "https://metabase.example.com/api/dataset/csv" \
    -H "X-Metabase-Session: ${SESSION_TOKEN}" \
    -d "{
      \"database\": 1,
      \"type\": \"native\",
      \"native\": {\"query\": \"SELECT * FROM transactions ORDER BY id LIMIT 100000 OFFSET ${offset}\"}
    }" >> full_export.csv
done
```

## Scheduled Report Workflow

### Create Pulse (Scheduled Email)

```bash
curl -X POST https://metabase.example.com/api/pulse \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{
    "name": "Daily Affiliate Summary",
    "cards": [{"id": 42, "include_csv": true}],
    "channels": [{
      "channel_type": "email",
      "schedule_type": "daily",
      "schedule_hour": 8,
      "recipients": [{"email": "affiliates@casino.com"}]
    }],
    "collection_id": 16
  }'
```

## Database Connection Management

### List Available Databases

```bash
curl -X GET https://metabase.example.com/api/database \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" | jq '.data[] | {id, name, engine}'
```

### Sync Database Schema

**When:** After Flyway migrations add new tables

```bash
curl -X POST "https://metabase.example.com/api/database/1/sync_schema" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}"
```

### WARNING: Stale Schema Cache

**The Problem:**

```sql
-- Query fails: column "category" does not exist
SELECT category, COUNT(*) FROM bonuses GROUP BY category
```

**Why This Breaks:**
1. Metabase caches schema metadata
2. New columns from migrations not visible
3. Users see confusing error messages

**The Fix:**

```bash
# After running Flyway migrations, trigger schema sync
./gradlew flywayMigrate && \
curl -X POST "https://metabase.example.com/api/database/1/sync_schema" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}"
```

## Cleanup and Maintenance

### Archive Unused Cards

```bash
# Find cards not viewed in 90 days
curl -X GET "https://metabase.example.com/api/card?f=recent&model_id=1" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" | \
  jq '[.[] | select(.last_query_start < (now - 7776000 | todate))] | .[].id' | \
  xargs -I {} curl -X PUT "https://metabase.example.com/api/card/{}" \
    -H "X-Metabase-Session: ${SESSION_TOKEN}" \
    -d '{"archived": true}'
```

### Backup Card Definitions

```bash
# Export all cards as JSON for version control
curl -X GET "https://metabase.example.com/api/card" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" | \
  jq '.[] | {id, name, dataset_query, display, visualization_settings}' > cards_backup.json
```