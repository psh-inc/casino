# PostgreSQL Patterns Reference

## Data Types

### WARNING: Using SERIAL Instead of BIGSERIAL

**The Problem:**

```sql
-- BAD - SERIAL maxes out at 2.1 billion rows
CREATE TABLE transactions (id SERIAL PRIMARY KEY);
```

**Why This Breaks:**
1. SERIAL is 32-bit signed integer (max 2,147,483,647)
2. High-volume tables (transactions, game rounds) easily exceed this
3. Recovery requires schema migration with downtime

**The Fix:**

```sql
-- GOOD - BIGSERIAL handles 9.2 quintillion rows
CREATE TABLE transactions (id BIGSERIAL PRIMARY KEY);
```

**When You Might Be Tempted:**
Copying schemas from tutorials or small-scale projects. Always use BIGSERIAL.

---

### WARNING: TIMESTAMP Without Time Zone

**The Problem:**

```sql
-- BAD - Ambiguous timezone, causes bugs across regions
CREATE TABLE events (occurred_at TIMESTAMP NOT NULL);
```

**Why This Breaks:**
1. No timezone context stored—interpretation varies by client
2. DST transitions cause duplicate or missing timestamps
3. Distributed systems disagree on actual time

**The Fix:**

```sql
-- GOOD - Explicit UTC storage
CREATE TABLE events (occurred_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW());
```

---

### WARNING: Using FLOAT/DOUBLE for Money

**The Problem:**

```sql
-- BAD - Binary floating point loses precision
CREATE TABLE wallets (balance FLOAT NOT NULL);
```

**Why This Breaks:**
1. `0.1 + 0.2 = 0.30000000000000004` in binary floating point
2. Rounding errors accumulate across transactions
3. Financial audits fail with penny discrepancies

**The Fix:**

```sql
-- GOOD - Exact decimal arithmetic
CREATE TABLE wallets (balance DECIMAL(19,4) NOT NULL DEFAULT 0);
```

---

## Index Patterns

### Composite Index for Pagination

```sql
-- Optimizes: WHERE player_id = ? ORDER BY created_at DESC LIMIT 20
CREATE INDEX idx_transactions_player_created 
ON transactions(player_id, created_at DESC);
```

### Partial Index for Status Filtering

```sql
-- Only indexes active records, smaller and faster
CREATE INDEX idx_bonuses_active 
ON bonuses(player_id) WHERE status = 'ACTIVE';
```

### Covering Index for Query Performance

```sql
-- Includes columns to avoid table lookup
CREATE INDEX idx_players_email_status 
ON players(email) INCLUDE (status, created_at);
```

---

## Foreign Key Patterns

### Standard Reference

```sql
CREATE TABLE wallets (
    id BIGSERIAL PRIMARY KEY,
    player_id BIGINT NOT NULL REFERENCES players(id),
    CONSTRAINT fk_wallets_player FOREIGN KEY (player_id) REFERENCES players(id)
);
```

### Cascade Delete for Audit Tables

```sql
-- Child records deleted when parent removed
CREATE TABLE player_audit (
    id BIGSERIAL PRIMARY KEY,
    player_id BIGINT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);
```

### Set Null for Optional References

```sql
-- Orphan children rather than delete
ALTER TABLE bonuses 
ADD CONSTRAINT fk_bonus_parent
FOREIGN KEY (parent_id) REFERENCES bonuses(id) ON DELETE SET NULL;
```

---

## JSONB Usage

### Entity Mapping

```kotlin
@Entity
data class KycDocument(
    @Type(JsonType::class)
    @Column(name = "metadata", columnDefinition = "JSONB")
    var metadata: Map<String, Any>? = null
)
```

### Native Query on JSONB

```sql
-- Query nested JSON fields
SELECT * FROM kyc_documents 
WHERE metadata->>'documentType' = 'PASSPORT';

-- Check array contains value
SELECT * FROM game_configs 
WHERE features @> '["bonus_buy"]';
```

---

## Check Constraints

### Enum Validation

```sql
CREATE TABLE payments (
    status VARCHAR(20) NOT NULL 
    CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED'))
);
```

### Range Validation

```sql
CREATE TABLE bonuses (
    wagering_multiplier DECIMAL(5,2) NOT NULL CHECK (wagering_multiplier >= 1),
    max_bonus DECIMAL(19,4) CHECK (max_bonus > 0)
);
```