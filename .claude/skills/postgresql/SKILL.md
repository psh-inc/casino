---
name: postgresql
description: |
  PostgreSQL database design, Flyway migrations, and JPA queries for the casino platform.
  Use when: Creating or modifying database tables, writing migrations, designing entities,
  writing repository queries, or troubleshooting data layer issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# PostgreSQL Skill

PostgreSQL 14+ is the primary datastore for the casino platform. This project uses Flyway for migrations, Spring Data JPA for ORM, and follows strict conventions: BIGSERIAL for all IDs, TIMESTAMP WITH TIME ZONE for dates, DECIMAL(19,4) for money. The **jpa** skill covers entity mapping in detail.

## Quick Start

### Migration Creation

```sql
-- V20250106150000__add_player_loyalty.sql
ALTER TABLE players ADD COLUMN loyalty_tier VARCHAR(20) DEFAULT 'BRONZE';
CREATE INDEX idx_players_loyalty_tier ON players(loyalty_tier);
```

### Entity Definition

```kotlin
@Entity
@Table(name = "players")
data class Player(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @Column(nullable = false, precision = 19, scale = 4)
    var balance: BigDecimal = BigDecimal.ZERO,
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
)
```

### Repository Query

```kotlin
@Query("""
    SELECT COALESCE(SUM(t.amount), 0) FROM Transaction t
    WHERE t.wallet.player.id = :playerId AND t.type = :type
""")
fun sumByPlayerIdAndType(playerId: Long, type: TransactionType): BigDecimal?
```

## Key Concepts

| Concept | SQL Type | Kotlin Type |
|---------|----------|-------------|
| Primary Key | `BIGSERIAL` | `Long?` |
| Money | `DECIMAL(19,4)` | `BigDecimal` |
| Timestamp | `TIMESTAMP WITH TIME ZONE` | `LocalDateTime` |
| JSON | `JSONB` | `Map<String, Any>` |
| Version | `BIGINT` | `@Version Long` |

## Common Patterns

### Atomic Balance Update

**When:** Concurrent wallet modifications

```kotlin
@Modifying
@Query("""
    UPDATE Wallet w SET w.balance = w.balance + :amount, w.version = w.version + 1
    WHERE w.player.id = :playerId AND w.version = :version AND w.balance + :amount >= 0
""")
fun updateBalanceWithVersion(playerId: Long, amount: BigDecimal, version: Long): Int
```

### Partial Index

**When:** Filtering on common status values

```sql
CREATE INDEX idx_wallets_active ON wallets(player_id) WHERE status = 'ACTIVE';
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **jpa** skill for entity mapping and repository patterns
- See the **kotlin** skill for BigDecimal handling and data classes
- See the **spring-boot** skill for transaction management