---
name: jpa
description: |
  JPA entities, repositories, and Hibernate ORM patterns for Spring Boot 3.2.5 with Kotlin
  Use when: Creating/modifying entities, repositories, database queries, or handling persistence layer concerns
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# JPA Skill - Casino Platform

JPA/Hibernate patterns for the casino platform backend. This codebase uses Kotlin data classes with Spring Data JPA, PostgreSQL, and strict conventions for financial data handling.

## Quick Start

### Entity with ID and Auditing

```kotlin
@Entity
@Table(name = "transactions")
data class Transaction(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,

    @Column(nullable = false, precision = 19, scale = 4)
    val amount: BigDecimal,

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    var status: TransactionStatus,

    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),

    @Column(name = "updated_at", nullable = false)
    var updatedAt: LocalDateTime = LocalDateTime.now(),

    @Version
    var version: Long = 0
)
```

### Repository with JOIN FETCH

```kotlin
interface PlayerRepository : JpaRepository<Player, Long> {
    fun findByUsername(username: String): Optional<Player>

    @Query("""
        SELECT DISTINCT p FROM Player p
        LEFT JOIN FETCH p.wallet
        WHERE p.status = 'ACTIVE'
    """)
    fun findActivePlayersWithWallet(): List<Player>
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| ID Type | Always BIGSERIAL | `@GeneratedValue(strategy = GenerationType.IDENTITY)` |
| Money | BigDecimal from String | `BigDecimal("123.45")` not `BigDecimal(123.45)` |
| Dates | LocalDateTime, UTC | `LocalDateTime.now(ZoneOffset.UTC)` |
| Enums | STRING not ORDINAL | `@Enumerated(EnumType.STRING)` |
| Locking | Optimistic | `@Version var version: Long = 0` |
| Lazy Loading | Default for relations | `fetch = FetchType.LAZY` |

## Common Patterns

### Preventing N+1 Queries

**When:** Loading entities with their relationships

```kotlin
// BAD - N+1 queries
val players = repo.findByStatus(ACTIVE)
players.forEach { it.wallet?.balance }  // Separate query per player!

// GOOD - Single query with JOIN FETCH
@Query("SELECT p FROM Player p LEFT JOIN FETCH p.wallet WHERE p.status = 'ACTIVE'")
fun findActivePlayersWithWallet(): List<Player>
```

### Bulk Updates with @Modifying

**When:** Updating multiple records without loading entities

```kotlin
@Modifying
@Query("""
    UPDATE Player p SET 
        p.status = :status, 
        p.updatedAt = CURRENT_TIMESTAMP 
    WHERE p.lastActivityAt < :threshold
""")
fun deactivateInactivePlayers(
    @Param("status") status: PlayerStatus,
    @Param("threshold") threshold: LocalDateTime
): Int
```

## See Also

- [patterns](references/patterns.md) - Entity, relationship, and query patterns
- [workflows](references/workflows.md) - Common development workflows

## Related Skills

- See the **spring-boot** skill for service layer patterns and transactions
- See the **postgresql** skill for Flyway migrations and database design
- See the **kotlin** skill for Kotlin-specific JPA considerations