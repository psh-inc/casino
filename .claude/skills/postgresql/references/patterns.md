# PostgreSQL Patterns Reference

## Schema Design Patterns

### Primary Keys: BIGSERIAL Only

NEVER use `SERIAL`. The 32-bit limit (~2B) seems huge until you're migrating a production database.

```sql
-- GOOD - 64-bit, future-proof
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    -- ...
);

-- BAD - 32-bit limit, migration nightmare
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,  -- DON'T
    -- ...
);
```

### Financial Columns: NUMERIC(19,4)

```sql
-- GOOD - 19 digits, 4 decimal places for sub-cent precision
balance NUMERIC(19,4) NOT NULL DEFAULT 0,
bonus_balance NUMERIC(19,4) NOT NULL DEFAULT 0,

-- BAD - precision loss, rounding errors
balance FLOAT NOT NULL DEFAULT 0,  -- NEVER for money
balance DECIMAL(10,2),              -- Too small for large transactions
```

### Timestamps: Always WITH TIME ZONE

```sql
-- GOOD - timezone-aware, prevents production bugs
created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
last_login_at TIMESTAMP WITH TIME ZONE,

-- BAD - timezone confusion in distributed systems
created_at TIMESTAMP NOT NULL DEFAULT NOW(),  -- Which timezone?
```

### UUID for External References

```sql
-- Use for public-facing identifiers, transaction references
transaction_uuid UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
session_uuid UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
```

## Indexing Patterns

### WARNING: Missing Indices on Foreign Keys

**The Problem:**

PostgreSQL does NOT auto-create indices on foreign keys. Every FK without an index is a full table scan waiting to happen.

```sql
-- BAD - FK without index
ALTER TABLE transactions ADD CONSTRAINT fk_wallet 
    FOREIGN KEY (wallet_id) REFERENCES wallets(id);
-- Queries filtering by wallet_id will be SLOW
```

**Why This Breaks:**
1. Joins become O(n) instead of O(log n)
2. Cascade deletes lock entire tables
3. Reports timeout as data grows

**The Fix:**

```sql
-- GOOD - always index FKs
CREATE INDEX idx_transactions_wallet_id ON transactions(wallet_id);
ALTER TABLE transactions ADD CONSTRAINT fk_wallet 
    FOREIGN KEY (wallet_id) REFERENCES wallets(id);
```

### Covering Indices for Read-Heavy Queries

```sql
-- Include non-key columns to avoid table lookups
CREATE INDEX idx_covering_player_stats 
ON player_statistics(player_id, currency, period_type) 
INCLUDE (total_deposits, total_wagered, deposit_count);
```

### Partial Indices for Filtered Queries

```sql
-- Index only active records - smaller, faster
CREATE INDEX idx_stats_aggregation 
ON player_statistics(period_type, currency, period_start) 
WHERE period_type IN ('DAILY', 'MONTHLY');

-- Index only pending transactions
CREATE INDEX idx_pending_transactions 
ON transactions(created_at) 
WHERE status = 'PENDING';
```

### Composite Indices: Column Order Matters

```sql
-- GOOD - most selective column first
CREATE INDEX idx_transactions_lookup 
ON transactions(wallet_id, type, created_at);

-- BAD - status has low cardinality
CREATE INDEX idx_transactions_lookup 
ON transactions(status, wallet_id, created_at);  -- Won't help most queries
```

## Query Patterns

### Prevent N+1 with JOIN FETCH

```kotlin
// BAD - triggers N+1 queries
val players = playerRepository.findAll()
players.forEach { it.wallet }  // Each access = 1 query

// GOOD - single query with join
@Query("""
    SELECT DISTINCT p FROM Player p
    LEFT JOIN FETCH p.wallet
    WHERE p.status = :status
""")
fun findByStatusWithWallet(@Param("status") status: PlayerStatus): List<Player>
```

### Batch Operations with @Modifying

```kotlin
// GOOD - single UPDATE statement
@Modifying
@Query("""
    UPDATE Player p 
    SET p.lastActivityAt = :timestamp 
    WHERE p.id IN :playerIds
""")
fun updateLastActivityBatch(
    @Param("playerIds") playerIds: List<Long>,
    @Param("timestamp") timestamp: LocalDateTime
): Int

// BAD - N separate updates
playerIds.forEach { id ->
    playerRepository.findById(id).ifPresent { 
        it.lastActivityAt = timestamp
        playerRepository.save(it)  // N queries!
    }
}
```

### Dynamic Queries with Criteria API

```kotlin
// For complex filtering where JPQL becomes unwieldy
class GameRepositoryImpl : GameRepositoryCustom {
    @PersistenceContext
    private lateinit var entityManager: EntityManager

    override fun findByDynamicCriteria(
        providerIds: List<Long>,
        minRtp: BigDecimal?,
        hasJackpot: Boolean?
    ): Page<Game> {
        val cb = entityManager.criteriaBuilder
        val cq = cb.createQuery(Game::class.java)
        val root = cq.from(Game::class.java)
        
        val predicates = mutableListOf<Predicate>()
        
        if (providerIds.isNotEmpty()) {
            predicates.add(root.get<Long>("providerId").`in`(providerIds))
        }
        
        minRtp?.let {
            predicates.add(cb.ge(root.get("rtp"), it))
        }
        
        cq.where(*predicates.toTypedArray())
        // ...
    }
}
```

## Anti-Patterns

### WARNING: BigDecimal from Double

**The Problem:**

```kotlin
// BAD - precision loss from floating point
val amount = BigDecimal(123.45)  // Actually 123.4500000000000028...
```

**Why This Breaks:**
1. Financial calculations become incorrect
2. Audit trails show wrong amounts
3. Regulatory compliance failures

**The Fix:**

```kotlin
// GOOD - exact decimal representation
val amount = BigDecimal("123.45")
val zero = BigDecimal.ZERO
```

### WARNING: Comparing BigDecimal with ==

**The Problem:**

```kotlin
// BAD - compares scale, not value
if (amount == BigDecimal.ZERO) { ... }  // 0.00 != 0
```

**The Fix:**

```kotlin
// GOOD - compares mathematical value
if (amount.compareTo(BigDecimal.ZERO) == 0) { ... }
```