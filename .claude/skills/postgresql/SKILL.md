---
name: postgresql
description: |
  PostgreSQL 14+ database design, Flyway migrations, and JPA queries for the casino platform.
  Use when: Creating or modifying database tables, writing migrations, designing entities,
  writing repository queries, or troubleshooting data layer issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# PostgreSQL Skill

PostgreSQL 14+ is the primary database for this casino platform, accessed via Spring Data JPA with Hibernate. All financial operations use `NUMERIC(19,4)` for precision, IDs are `BIGSERIAL`, and timestamps use `TIMESTAMP WITH TIME ZONE`. Flyway manages migrations with out-of-order support enabled.

## Quick Start

### Create a Migration

```sql
-- V20260110120000__add_player_preferences.sql
CREATE TABLE player_preferences (
    id BIGSERIAL PRIMARY KEY,
    player_id BIGINT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    notification_email BOOLEAN NOT NULL DEFAULT true,
    notification_sms BOOLEAN NOT NULL DEFAULT false,
    preferred_currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_player_preferences_player_id ON player_preferences(player_id);
```

### Map Entity to Table

```kotlin
@Entity
@Table(name = "player_preferences")
data class PlayerPreferences(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false)
    val player: Player,
    
    @Column(name = "preferred_currency", nullable = false, length = 3)
    var preferredCurrency: String = "EUR",
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
)
```

## Key Concepts

| SQL Type | Kotlin Type | Usage |
|----------|-------------|-------|
| `BIGSERIAL` | `Long` | All primary keys |
| `NUMERIC(19,4)` | `BigDecimal` | Money, balances, amounts |
| `TIMESTAMP WITH TIME ZONE` | `LocalDateTime` | All datetime fields |
| `UUID` | `UUID` | External references, tokens |
| `TEXT` | `String` | Long content, descriptions |
| `JSONB` | `String`/Custom | Structured flexible data |

## Common Patterns

### Prevent N+1 with JOIN FETCH

**When:** Loading entities with relationships

```kotlin
@Query("""
    SELECT DISTINCT p FROM Player p
    LEFT JOIN FETCH p.wallet
    LEFT JOIN FETCH p.addresses
    WHERE p.id = :id
""")
fun findByIdWithDetails(@Param("id") id: Long): Optional<Player>
```

### Aggregate with COALESCE

**When:** Summing values that might be null

```kotlin
@Query("""
    SELECT COALESCE(SUM(t.amount), 0)
    FROM Transaction t
    WHERE t.wallet.player.id = :playerId
    AND t.type = :type
    AND t.status = 'COMPLETED'
""")
fun sumByPlayerIdAndType(
    @Param("playerId") playerId: Long,
    @Param("type") type: TransactionType
): BigDecimal
```

## See Also

- [patterns](references/patterns.md) - Schema design, indexing, query patterns
- [workflows](references/workflows.md) - Migration workflow, testing, deployment

## Related Skills

- See the **jpa** skill for entity mapping and repository patterns
- See the **spring-boot** skill for transaction management and configuration
- See the **kotlin** skill for data class patterns with JPA