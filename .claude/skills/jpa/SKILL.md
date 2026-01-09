---
name: jpa
description: |
  JPA entities, repositories, and Hibernate ORM patterns for Spring Boot 3.2.5 with Kotlin
  Use when: Creating/modifying entities, repositories, database queries, or handling persistence layer concerns
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# JPA Skill

This project uses Spring Data JPA with Hibernate 6.x on PostgreSQL 14+. All entities are Kotlin data classes with BIGSERIAL IDs, using `FetchType.LAZY` by default and `JOIN FETCH` for N+1 prevention. The repository layer follows Spring Data conventions with custom implementations for complex queries.

## Quick Start

### Entity Definition

```kotlin
@Entity
@Table(name = "wallets")
data class Wallet(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false, unique = true)
    val player: Player,
    
    @Column(nullable = false, precision = 19, scale = 4)
    var balance: BigDecimal = BigDecimal.ZERO,
    
    @Version
    val version: Long = 0,
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
) {
    override fun hashCode(): Int = id?.hashCode() ?: 0
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Wallet) return false
        return id != null && id == other.id
    }
}
```

### Repository Pattern

```kotlin
@Repository
interface PlayerRepository : JpaRepository<Player, Long>, PlayerRepositoryCustom {
    fun findByUsername(username: String): Optional<Player>
    fun existsByEmail(email: String): Boolean
    
    @Query("SELECT p FROM Player p WHERE p.status = 'ACTIVE'")
    fun findActivePlayers(): List<Player>
    
    @Query("""
        SELECT DISTINCT p FROM Player p
        LEFT JOIN FETCH p.wallet
        WHERE p.id = :id
    """)
    fun findByIdWithDetails(@Param("id") id: Long): Optional<Player>
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| ID Generation | BIGSERIAL via IDENTITY | `@GeneratedValue(strategy = GenerationType.IDENTITY)` |
| Lazy Loading | Default for relations | `@ManyToOne(fetch = FetchType.LAZY)` |
| Optimistic Lock | Version field | `@Version val version: Long = 0` |
| Pessimistic Lock | For concurrent updates | `@Lock(LockModeType.PESSIMISTIC_WRITE)` |
| Transaction | Class or method level | `@Transactional(readOnly = true)` |

## Common Patterns

### Preventing N+1 with JOIN FETCH

**When:** Loading entities with associations in a single query

```kotlin
@Query("""
    SELECT p FROM Player p
    JOIN FETCH p.wallet w
    LEFT JOIN FETCH p.addresses
    WHERE p.id = :id
""")
fun findByIdWithDetails(@Param("id") id: Long): Optional<Player>
```

### Atomic Updates Without Load

**When:** High-performance updates avoiding entity load

```kotlin
@Modifying
@Query("""
    UPDATE Wallet w 
    SET w.balance = w.balance + :amount, 
        w.version = w.version + 1
    WHERE w.player.id = :playerId 
    AND w.balance + :amount >= 0
""")
fun updateBalanceAtomic(
    @Param("playerId") playerId: Long, 
    @Param("amount") amount: BigDecimal
): Int  // Returns affected rows
```

## See Also

- [patterns](references/patterns.md) - Entity, repository, and query patterns
- [workflows](references/workflows.md) - Transaction management and testing workflows

## Related Skills

For database migrations and schema changes, see the **postgresql** skill.
For service layer patterns that use JPA, see the **spring-boot** skill.
For Kotlin-specific syntax patterns, see the **kotlin** skill.