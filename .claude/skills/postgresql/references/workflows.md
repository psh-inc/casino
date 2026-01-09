# PostgreSQL Workflows Reference

## Migration Workflow

### Step 1: Create Migration File

```bash
# Naming: V{YYYYMMddHHmmss}__{description}.sql
touch casino-b/src/main/resources/db/migration/V20250106150000__add_player_vip_status.sql
```

### Step 2: Write Idempotent DDL

```sql
-- Use IF NOT EXISTS / IF EXISTS for safety
ALTER TABLE players ADD COLUMN IF NOT EXISTS vip_level VARCHAR(20);

CREATE INDEX IF NOT EXISTS idx_players_vip_level ON players(vip_level);

-- For drops, check existence
DROP INDEX IF EXISTS idx_players_old_status;
```

### Step 3: Run Migration

```bash
./gradlew flywayMigrate
# Or automatically on bootRun with flyway.enabled=true
```

### WARNING: Modifying Existing Migrations

**The Problem:**

```sql
-- BAD - Editing V1__initial_schema.sql after it ran
-- Changes checksum, breaks Flyway validation
```

**Why This Breaks:**
1. Flyway checksums each migration file
2. Production database has original checksum stored
3. Mismatch = deployment failure

**The Fix:**

```sql
-- GOOD - Create new migration for changes
-- V20250106160000__fix_player_column.sql
ALTER TABLE players ALTER COLUMN email TYPE VARCHAR(255);
```

---

## Entity-First vs Migration-First

### Migration-First (Recommended)

```sql
-- 1. Write migration
ALTER TABLE players ADD COLUMN phone_verified BOOLEAN DEFAULT FALSE;
```

```kotlin
// 2. Update entity to match
@Column(name = "phone_verified")
var phoneVerified: Boolean = false
```

### Entity-First (Development Only)

```yaml
# application.yml - NEVER in production
spring:
  jpa:
    hibernate:
      ddl-auto: update  # Creates missing columns
```

---

## Query Optimization Workflow

### Step 1: Identify Slow Query

```kotlin
// Enable SQL logging in application.yml
logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql: TRACE
```

### Step 2: Analyze with EXPLAIN

```sql
EXPLAIN ANALYZE
SELECT * FROM transactions 
WHERE wallet_id = 123 AND created_at > '2025-01-01'
ORDER BY created_at DESC LIMIT 20;
```

### Step 3: Add Appropriate Index

```sql
-- Based on EXPLAIN output
CREATE INDEX CONCURRENTLY idx_transactions_wallet_created
ON transactions(wallet_id, created_at DESC);
```

**Note:** `CONCURRENTLY` avoids table locks in production.

---

## Locking Strategies

### Optimistic Locking (Default)

```kotlin
@Entity
data class Wallet(
    @Version
    var version: Long = 0,
    
    var balance: BigDecimal = BigDecimal.ZERO
)

// Service catches OptimisticLockException and retries
```

### Pessimistic Locking (High Contention)

```kotlin
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("SELECT w FROM Wallet w WHERE w.player.id = :playerId")
fun findByPlayerIdWithLock(playerId: Long): Wallet?
```

### Atomic Update (Best for Counters)

```kotlin
@Modifying
@Query("""
    UPDATE Wallet w SET w.balance = w.balance + :amount
    WHERE w.id = :walletId AND w.balance + :amount >= 0
""")
fun addBalance(walletId: Long, amount: BigDecimal): Int
```

---

## Connection Pool Tuning

### HikariCP Configuration

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20        # Match CPU cores * 2-4
      minimum-idle: 5
      connection-timeout: 30000    # 30 seconds
      idle-timeout: 600000         # 10 minutes
      max-lifetime: 1800000        # 30 minutes
```

### WARNING: Pool Exhaustion

**The Problem:**

```kotlin
// BAD - Long-running transaction holds connection
@Transactional
fun generateReport(): Report {
    val data = repository.findAll()  // Quick
    return pdfGenerator.create(data) // Slow, 30+ seconds
}
```

**Why This Breaks:**
1. Connection held during PDF generation
2. Other requests queue waiting for connections
3. Pool exhausted = application hangs

**The Fix:**

```kotlin
// GOOD - Separate read from processing
fun generateReport(): Report {
    val data = fetchData()  // Short transaction
    return pdfGenerator.create(data)  // No transaction
}

@Transactional(readOnly = true)
fun fetchData(): List<ReportData> = repository.findAll()
```

---

## Bulk Operations

### Batch Insert Pattern

```kotlin
@Modifying
@Query(value = """
    INSERT INTO transactions (wallet_id, amount, type, created_at)
    SELECT unnest(:walletIds), unnest(:amounts), :type, NOW()
""", nativeQuery = true)
fun bulkInsert(walletIds: List<Long>, amounts: List<BigDecimal>, type: String)
```

### Batch Update Pattern

```kotlin
// Use JPA batch settings
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true
```

---

## Database Backup Verification

```bash
# Verify backup integrity
pg_restore --list backup.dump | head -20

# Test restore to scratch database
createdb casino_test
pg_restore -d casino_test backup.dump

# Run smoke tests
psql casino_test -c "SELECT COUNT(*) FROM players;"
```