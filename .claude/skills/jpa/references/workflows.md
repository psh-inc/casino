# JPA Workflows Reference

This document covers transaction management, testing, and common development workflows.

## Transaction Management

### Service Layer Transactions

Apply `@Transactional` at class level for write operations:

```kotlin
@Service
@Transactional  // All methods are transactional by default
class WalletService(
    private val walletRepository: WalletRepository,
    private val transactionRepository: TransactionRepository
) {
    // This inherits class-level @Transactional (read-write)
    fun createWallet(player: Player, currency: String): Wallet {
        return walletRepository.save(Wallet(player = player, currency = currency))
    }

    // Override for read-only optimization
    @Transactional(readOnly = true)
    fun getWalletByPlayerId(playerId: Long): Wallet {
        return walletRepository.findByPlayerId(playerId)
            .orElseThrow { ResourceNotFoundException("Wallet not found") }
    }
}
```

---

### WARNING: Transaction Propagation Issues

**The Problem:**

```kotlin
// BAD - Internal call bypasses proxy, no transaction!
@Service
class PlayerService {
    fun createPlayerWithWallet(request: CreateRequest) {
        createPlayer(request)  // Direct call - NOT transactional!
    }
    
    @Transactional
    fun createPlayer(request: CreateRequest) { ... }
}
```

**Why This Breaks:**
1. Spring AOP proxies only intercept external calls
2. Internal method calls bypass the proxy entirely
3. No rollback on failure, data inconsistency

**The Fix:**

```kotlin
// GOOD - Single transactional method or inject self
@Service
@Transactional
class PlayerService {
    fun createPlayerWithWallet(request: CreateRequest) {
        // Everything in one transactional method
        val player = playerRepository.save(...)
        val wallet = walletRepository.save(...)
    }
}
```

**When You Might Be Tempted:**
When refactoring large methods into smaller ones - keep transaction boundaries in mind.

---

## Atomic Update Pattern

For high-concurrency updates, bypass entity loading:

```kotlin
@Modifying
@Query("""
    UPDATE Wallet w 
    SET w.balance = w.balance + :amount, 
        w.version = w.version + 1,
        w.updatedAt = CURRENT_TIMESTAMP
    WHERE w.player.id = :playerId 
    AND w.balance + :amount >= 0
    AND w.status = 'ACTIVE'
""")
fun updateBalanceAtomic(
    @Param("playerId") playerId: Long, 
    @Param("amount") amount: BigDecimal
): Int  // Returns 1 if updated, 0 if failed

// Usage
val updated = walletRepository.updateBalanceAtomic(playerId, amount)
if (updated == 0) {
    throw InsufficientFundsException("Balance update failed")
}
```

---

## Repository Testing Workflow

### Integration Test Setup with Testcontainers

```kotlin
@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class PlayerRepositoryTest {
    @Autowired
    private lateinit var playerRepository: PlayerRepository

    @Autowired
    private lateinit var entityManager: TestEntityManager

    companion object {
        @Container
        @JvmStatic
        val postgresContainer = PostgreSQLContainer("postgres:14-alpine")
            .withDatabaseName("casino_test")

        @JvmStatic
        @DynamicPropertySource
        fun properties(registry: DynamicPropertyRegistry) {
            registry.add("spring.datasource.url", postgresContainer::getJdbcUrl)
            registry.add("spring.datasource.username", postgresContainer::getUsername)
            registry.add("spring.datasource.password", postgresContainer::getPassword)
        }
    }

    @BeforeEach
    fun cleanup() {
        playerRepository.deleteAll()
        entityManager.clear()  // Clear persistence context
    }

    @Test
    fun `findByUsername should return player when exists`() {
        // Given
        val player = playerRepository.save(createTestPlayer())
        entityManager.flush()
        entityManager.clear()  // Force re-read from DB

        // When
        val result = playerRepository.findByUsername("testuser")

        // Then
        result.isPresent shouldBe true
        result.get().username shouldBe "testuser"
    }
}
```

---

### WARNING: Missing flush/clear in Tests

**The Problem:**

```kotlin
// BAD - Entity still in persistence context, not testing DB
@Test
fun `test finds player`() {
    val player = playerRepository.save(createPlayer())
    // Player is still cached in first-level cache!
    val found = playerRepository.findById(player.id!!)  // Returns cached, not from DB
}
```

**Why This Breaks:**
1. Hibernate returns cached entity, not testing actual query
2. Lazy loading issues hidden by cache
3. Tests pass but production fails

**The Fix:**

```kotlin
// GOOD - Clear cache to force DB read
@Test
fun `test finds player`() {
    val player = playerRepository.save(createPlayer())
    entityManager.flush()   // Write to DB
    entityManager.clear()   // Clear cache
    
    val found = playerRepository.findById(player.id!!)  // Reads from DB
}
```

---

## BigDecimal Handling

### WARNING: Creating BigDecimal from Double

**The Problem:**

```kotlin
// BAD - Precision loss!
val amount = BigDecimal(123.45)  // Actually 123.4500000000000028421709...
```

**Why This Breaks:**
1. Double cannot represent 123.45 exactly in binary
2. Financial calculations accumulate errors
3. Balance mismatches in reports

**The Fix:**

```kotlin
// GOOD - String constructor preserves precision
val amount = BigDecimal("123.45")

// Comparisons
if (amount.compareTo(BigDecimal.ZERO) > 0) { ... }  // NOT == or !=
```

---

## JPQL vs Native Query Decision

| Use Case | Approach |
|----------|----------|
| Simple lookups | Derived query methods |
| Entity with associations | JPQL with JOIN FETCH |
| Complex dynamic filters | Criteria API |
| Database-specific features | Native query |
| Bulk updates | `@Modifying` JPQL |

### JPQL Example

```kotlin
@Query("""
    SELECT p FROM Player p
    WHERE p.status = :status
    AND p.createdAt BETWEEN :from AND :to
    ORDER BY p.createdAt DESC
""")
fun findByStatusInDateRange(
    @Param("status") status: PlayerStatus,
    @Param("from") from: LocalDateTime,
    @Param("to") to: LocalDateTime
): List<Player>
```

### Native Query Example

```kotlin
@Query(
    value = """
        SELECT * FROM players 
        WHERE EXTRACT(MONTH FROM date_of_birth) = :month 
        AND EXTRACT(DAY FROM date_of_birth) = :day
        AND status = 'ACTIVE'
    """,
    nativeQuery = true
)
fun findByBirthdayNative(
    @Param("month") month: Int,
    @Param("day") day: Int
): List<Player>
```

---

## Modifying Query Pattern

For bulk updates that don't need to load entities:

```kotlin
@Modifying
@Query("UPDATE Player p SET p.status = :status WHERE p.id IN :ids")
fun updateStatusBatch(
    @Param("ids") ids: List<Long>,
    @Param("status") status: PlayerStatus
): Int

// IMPORTANT: Clear cache after @Modifying queries
@Transactional
fun suspendPlayers(playerIds: List<Long>) {
    playerRepository.updateStatusBatch(playerIds, PlayerStatus.SUSPENDED)
    entityManager.clear()  // Entities in memory are now stale
}
```

---

## Related Skills

For PostgreSQL-specific features and migrations, see the **postgresql** skill.
For Spring transaction configuration and service patterns, see the **spring-boot** skill.
For writing repository tests with Kotest, see the **jasmine** skill (test patterns apply).