# Metabase API Patterns

## Card Creation Patterns

### Native SQL Card with Parameters

**When:** Creating reusable reports with user-configurable filters

```bash
curl -X POST https://metabase.example.com/api/card \
  -H "Content-Type: application/json" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}" \
  -d '{
    "name": "CellExpert Player Metrics",
    "dataset_query": {
      "type": "native",
      "native": {
        "query": "SELECT p.username, ps.total_deposit_amount, ps.deposit_count, ps.net_deposit FROM players p JOIN player_statistics ps ON p.id = ps.player_id WHERE p.affiliate_code = {{affiliate_code}} AND ps.updated_at >= {{start_date}}::timestamp",
        "template-tags": {
          "affiliate_code": {"type": "text", "name": "affiliate_code", "display-name": "Affiliate Code"},
          "start_date": {"type": "date", "name": "start_date", "display-name": "Start Date"}
        }
      },
      "database": 1
    },
    "display": "table",
    "collection_id": 10
  }'
```

### WARNING: Raw String Interpolation in Queries

**The Problem:**

```bash
# BAD - SQL injection vulnerability
query="SELECT * FROM players WHERE username = '${USER_INPUT}'"
```

**Why This Breaks:**
1. SQL injection attacks can compromise entire database
2. Bypasses Metabase's parameter sanitization
3. Violates casino platform security requirements

**The Fix:**

```bash
# GOOD - Use template tags for parameters
{
  "native": {
    "query": "SELECT * FROM players WHERE username = {{username}}",
    "template-tags": {
      "username": {"type": "text", "name": "username", "display-name": "Username"}
    }
  }
}
```

## Query Optimization Patterns

### Aggregation Queries for Reporting

**When:** Building affiliate or transaction reports

```sql
-- Efficient aggregation for CellExpert feed
SELECT 
    p.id as player_id,
    p.affiliate_code,
    MIN(t.created_at) FILTER (WHERE t.type = 'DEPOSIT') as first_deposit_date,
    SUM(t.amount) FILTER (WHERE t.type = 'DEPOSIT') as total_deposits,
    COUNT(*) FILTER (WHERE t.type = 'DEPOSIT') as deposit_count,
    SUM(t.amount) FILTER (WHERE t.type = 'WITHDRAWAL') as total_withdrawals
FROM players p
LEFT JOIN transactions t ON p.id = t.player_id
WHERE p.created_at >= {{start_date}}::timestamp
GROUP BY p.id, p.affiliate_code
```

### WARNING: Missing Index Hints

**The Problem:**

```sql
-- BAD - Full table scan on large transactions table
SELECT * FROM transactions WHERE player_id = 12345 ORDER BY created_at DESC
```

**Why This Breaks:**
1. Metabase queries timeout on large datasets
2. Degrades database performance for production workloads
3. CellExpert sync jobs fail with timeouts

**The Fix:**

```sql
-- GOOD - Query uses indexed columns
SELECT id, type, amount, created_at 
FROM transactions 
WHERE player_id = 12345 
  AND created_at >= NOW() - INTERVAL '90 days'
ORDER BY created_at DESC 
LIMIT 100
```

See the **postgresql** skill for index optimization strategies.

## Error Handling Patterns

### Check Card Execution Status

```bash
# Get card query results with error handling
response=$(curl -s -w "\n%{http_code}" -X POST \
  "https://metabase.example.com/api/card/${CARD_ID}/query" \
  -H "X-Metabase-Session: ${SESSION_TOKEN}")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" != "200" ]; then
  echo "ERROR: Query failed with status $http_code"
  echo "$body" | jq '.message // .error'
  exit 1
fi
```

### Session Expiration Handling

```bash
# Re-authenticate on 401
if [ "$http_code" = "401" ]; then
  SESSION_TOKEN=$(curl -s -X POST https://metabase.example.com/api/session \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"${MB_USER}\", \"password\": \"${MB_PASS}\"}" | jq -r '.id')
  # Retry original request
fi
```

## Integration with Casino Platform

### Kotlin Service for Metabase API

```kotlin
@Service
class MetabaseService(
    @Value("\${metabase.url}") private val baseUrl: String,
    @Value("\${metabase.username}") private val username: String,
    @Value("\${metabase.password}") private val password: String,
    private val restTemplate: RestTemplate
) {
    private var sessionToken: String? = null

    fun executeQuery(cardId: Long, parameters: Map<String, Any> = emptyMap()): List<Map<String, Any>> {
        ensureAuthenticated()
        val response = restTemplate.postForObject(
            "$baseUrl/api/card/$cardId/query",
            HttpEntity(parameters, createHeaders()),
            MetabaseQueryResponse::class.java
        )
        return response?.data?.rows ?: emptyList()
    }

    private fun ensureAuthenticated() {
        if (sessionToken == null) {
            val response = restTemplate.postForObject(
                "$baseUrl/api/session",
                mapOf("username" to username, "password" to password),
                SessionResponse::class.java
            )
            sessionToken = response?.id
        }
    }

    private fun createHeaders() = HttpHeaders().apply {
        set("X-Metabase-Session", sessionToken)
    }
}
```

See the **spring-boot** skill for RestTemplate configuration patterns.