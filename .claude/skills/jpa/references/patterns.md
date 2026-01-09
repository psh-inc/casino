# JPA Patterns Reference

Entity, relationship, and query patterns for the casino platform.

## Entity Patterns

### Standard Entity Structure

```kotlin
@Entity
@Table(name = "wallets")
data class Wallet(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,

    @Column(nullable = false, precision = 19, scale = 4)
    var balance: BigDecimal = BigDecimal.ZERO,

    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),

    @Column(name = "updated_at", nullable = false)
    var updatedAt: LocalDateTime = LocalDateTime.now(),

    @Version
    var version: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false)
    val player: Player
) {
    override fun hashCode(): Int = id?.hashCode() ?: 0
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Wallet) return false
        return id != null && id == other.id
    }
}
```

### WARNING: BigDecimal from Double

**The Problem:**

```kotlin
// BAD - Precision loss from floating-point representation
val amount = BigDecimal(123.45)  // Actually stores 123.4500000000000028421...
```

**Why This Breaks:**
1. Financial calculations become incorrect (off by fractions of cents)
2. Comparisons fail unexpectedly
3. Audit trails show wrong amounts

**The Fix:**

```kotlin
// GOOD - Exact decimal representation
val amount = BigDecimal("123.45")
val zero = BigDecimal.ZERO

// Comparison (NEVER use == or !=)
if (amount.compareTo(BigDecimal.ZERO) > 0) { ... }
```

**When You Might Be Tempted:**
Quick calculations or tests where you think precision doesn't matter. It always matters for money.

---

### WARNING: Using EnumType.ORDINAL

**The Problem:**

```kotlin
// BAD - Position-based storage
@Enumerated(EnumType.ORDINAL)
val status: PlayerStatus  // Stores 0, 1, 2...
```

**Why This Breaks:**
1. Adding enum value in middle shifts all subsequent values
2. Old data points to wrong statuses
3. Data corruption across entire table

**The Fix:**

```kotlin
// GOOD - Name-based storage
@Enumerated(EnumType.STRING)
val status: PlayerStatus  // Stores "ACTIVE", "BLOCKED"...
```

**When You Might Be Tempted:**
Trying to save storage space. String enums use ~10 bytes vs 4 for ordinal. Not worth the risk.

---

## Relationship Patterns

### OneToOne (Player ↔ Wallet)

```kotlin
// Player.kt - Owner side
@OneToOne(mappedBy = "player", cascade = [CascadeType.ALL], fetch = FetchType.LAZY)
val wallet: Wallet? = null

// Wallet.kt - Inverse side
@OneToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "player_id", nullable = false, unique = true)
val player: Player
```

### OneToMany (Wallet → Transactions)

```kotlin
// Wallet.kt - Parent
@OneToMany(mappedBy = "wallet", cascade = [CascadeType.ALL], fetch = FetchType.LAZY)
val transactions: List<Transaction> = emptyList()

// Transaction.kt - Child
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "wallet_id", nullable = false)
val wallet: Wallet
```

### ManyToMany (Game ↔ Categories)

```kotlin
@ManyToMany(fetch = FetchType.LAZY)
@JoinTable(
    name = "game_category_mappings",
    joinColumns = [JoinColumn(name = "game_id")],
    inverseJoinColumns = [JoinColumn(name = "category_id")]
)
val categories: Set<GameCategory> = emptySet()
```

---

## Query Patterns

### JPQL with Optional Parameters

```kotlin
@Query("""
    SELECT p FROM Player p
    WHERE p.cellxpertToken IS NOT NULL
    AND (COALESCE(:dateFrom, p.createdAt) <= p.createdAt)
    AND (COALESCE(:dateTo, p.createdAt) >= p.createdAt)
    ORDER BY p.createdAt ASC
""")
fun findPlayersForCellxpert(
    @Param("dateFrom") dateFrom: LocalDateTime?,
    @Param("dateTo") dateTo: LocalDateTime?
): List<Player>
```

### Aggregation Queries

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
): BigDecimal?
```

### WARNING: N+1 Query Problem

**The Problem:**

```kotlin
// BAD - Loads wallet separately for each player
val players = playerRepository.findByStatus(PlayerStatus.ACTIVE)
players.forEach { println(it.wallet?.balance) }  // N+1 queries!
```

**Why This Breaks:**
1. 1 query for players + N queries for wallets
2. 1000 players = 1001 database roundtrips
3. Response times grow linearly with data

**The Fix:**

```kotlin
// GOOD - Single query with JOIN FETCH
@Query("""
    SELECT DISTINCT p FROM Player p
    LEFT JOIN FETCH p.wallet
    WHERE p.status = 'ACTIVE'
""")
fun findActivePlayersWithWallet(): List<Player>
```

**When You Might Be Tempted:**
Simple loops where you access lazy-loaded properties. Always check query logs in development.

---

## JSON Storage Pattern

For complex objects that don't need querying:

```kotlin
@Column(name = "deposit_limits", columnDefinition = "text")
val depositLimitsJson: String? = null

val depositLimits: Map<String, BigDecimal>?
    get() = depositLimitsJson?.let {
        try {
            objectMapper.readValue<Map<String, BigDecimal>>(it)
        } catch (e: Exception) {
            null
        }
    }
```

## ElementCollection Pattern

For simple sets of values:

```kotlin
@ElementCollection
@CollectionTable(
    name = "bonus_country_whitelist",
    joinColumns = [JoinColumn(name = "bonus_id")]
)
@Column(name = "country_code")
val countryWhitelist: Set<String> = emptySet()
```