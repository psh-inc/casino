# JPA Patterns Reference

This document covers entity design, repository patterns, and query optimization for the casino platform.

## Entity Design Patterns

### Standard Entity Structure

Every entity in this codebase follows this pattern:

```kotlin
@Entity
@Table(name = "players")
data class Player(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,  // BIGSERIAL in PostgreSQL
    
    @Column(nullable = false, unique = true)
    val username: String,
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),
    
    @Enumerated(EnumType.STRING)
    val status: PlayerStatus = PlayerStatus.PENDING,
    
    @OneToOne(mappedBy = "player", fetch = FetchType.LAZY)
    val wallet: Wallet? = null
) {
    // REQUIRED: Override to prevent stack overflow in bidirectional relations
    override fun hashCode(): Int = id?.hashCode() ?: 0
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Player) return false
        return id != null && id == other.id
    }
}
```

---

### WARNING: EAGER Fetch on Collections

**The Problem:**

```kotlin
// BAD - Loads ALL transactions every time wallet is loaded
@OneToMany(mappedBy = "wallet", fetch = FetchType.EAGER)
val transactions: List<Transaction> = emptyList()
```

**Why This Breaks:**
1. Performance disaster: Loading 10 wallets loads potentially thousands of transactions
2. Cartesian product with multiple EAGER collections causes memory explosion
3. Cannot control when data is loaded - always fetched even when not needed

**The Fix:**

```kotlin
// GOOD - Lazy by default, fetch when needed with JOIN FETCH
@OneToMany(mappedBy = "wallet", fetch = FetchType.LAZY)
val transactions: List<Transaction> = emptyList()
```

**When You Might Be Tempted:**
When you get `LazyInitializationException` - but the fix is JOIN FETCH, not EAGER.

---

### WARNING: Missing equals/hashCode in Bidirectional Relations

**The Problem:**

```kotlin
// BAD - Default data class equals/hashCode includes all fields
@Entity
data class Player(
    @Id val id: Long? = null,
    @OneToOne(mappedBy = "player") val wallet: Wallet? = null
)
// Causes StackOverflowError: Player.hashCode -> Wallet.hashCode -> Player.hashCode...
```

**Why This Breaks:**
1. Stack overflow on any `toString()`, `hashCode()`, or `equals()` call
2. Sets and Maps containing entities fail silently
3. Hibernate dirty checking breaks completely

**The Fix:**

```kotlin
// GOOD - ID-based equality that breaks circular reference
override fun hashCode(): Int = id?.hashCode() ?: 0
override fun equals(other: Any?): Boolean {
    if (this === other) return true
    if (other !is Player) return false
    return id != null && id == other.id
}
override fun toString(): String = "Player(id=$id, username=$username)"
```

---

## Repository Patterns

### Derived Query Methods

Spring Data generates queries from method names:

```kotlin
interface PlayerRepository : JpaRepository<Player, Long> {
    fun findByUsername(username: String): Optional<Player>
    fun findByEmailContainingIgnoreCase(email: String, pageable: Pageable): Page<Player>
    fun existsByEmail(email: String): Boolean
    fun countByStatus(status: PlayerStatus): Long
    fun findByStatusAndEmailVerified(status: PlayerStatus, verified: Boolean): List<Player>
}
```

### Custom Repository Implementation

For complex queries, use the custom repository pattern:

```kotlin
// 1. Define interface
interface GameRepositoryCustom {
    fun findGamesByAdvancedCriteria(
        query: String?, providerIds: List<Long>, pageable: Pageable
    ): Page<Game>
}

// 2. Implement with EntityManager
@Repository
class GameRepositoryImpl : GameRepositoryCustom {
    @PersistenceContext
    private lateinit var entityManager: EntityManager

    override fun findGamesByAdvancedCriteria(...): Page<Game> {
        val cb = entityManager.criteriaBuilder
        val cq = cb.createQuery(Game::class.java)
        val root = cq.from(Game::class.java)
        // Build dynamic query...
    }
}

// 3. Extend in main repository
interface GameRepository : JpaRepository<Game, Long>, GameRepositoryCustom
```

---

### WARNING: N+1 Query Problem

**The Problem:**

```kotlin
// BAD - Triggers N additional queries for wallet
val players = playerRepository.findAll()  // 1 query
players.forEach { player ->
    println(player.wallet?.balance)  // N queries!
}
```

**Why This Breaks:**
1. 100 players = 101 queries (1 + 100 lazy loads)
2. Database connection pool exhaustion under load
3. Response times scale linearly with data size

**The Fix:**

```kotlin
// GOOD - Single query with JOIN FETCH
@Query("""
    SELECT p FROM Player p
    JOIN FETCH p.wallet
    WHERE p.status = 'ACTIVE'
""")
fun findActivePlayersWithWallet(): List<Player>
```

**When You Might Be Tempted:**
When code looks clean iterating over collections - profile SQL logs first.

---

## ElementCollection Pattern

For simple value collections without separate entity:

```kotlin
@Entity
data class Bonus(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @ElementCollection
    @CollectionTable(
        name = "bonus_country_whitelist", 
        joinColumns = [JoinColumn(name = "bonus_id")]
    )
    @Column(name = "country_code")
    val countryWhitelist: Set<String> = emptySet()
)
```

This creates a separate table `bonus_country_whitelist` automatically.

---

## Optimistic vs Pessimistic Locking

### Optimistic Locking (Default)

```kotlin
@Entity
data class Wallet(
    @Version
    val version: Long = 0,
    var balance: BigDecimal
)

// Usage in service
@Transactional
fun updateBalance(walletId: Long, amount: BigDecimal) {
    val wallet = walletRepository.findById(walletId).orElseThrow()
    wallet.balance += amount
    // Version auto-incremented, throws OptimisticLockException on conflict
}
```

### Pessimistic Locking (For High Contention)

```kotlin
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("SELECT w FROM Wallet w WHERE w.player.id = :playerId")
fun findByPlayerIdWithLock(@Param("playerId") playerId: Long): Optional<Wallet>
```

Use pessimistic locking for wallet balance updates where conflicts are frequent.