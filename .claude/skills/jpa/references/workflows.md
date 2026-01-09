# JPA Workflows Reference

Common development workflows for JPA in the casino platform.

## Creating a New Entity

### Step 1: Define Entity Class

```kotlin
@Entity
@Table(name = "payment_methods")
data class PaymentMethod(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,

    @Column(nullable = false, length = 100)
    val name: String,

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    val type: PaymentMethodType,

    @Column(nullable = false)
    var enabled: Boolean = true,

    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(),

    @Column(name = "updated_at", nullable = false)
    var updatedAt: LocalDateTime = LocalDateTime.now()
) {
    override fun hashCode(): Int = id?.hashCode() ?: 0
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is PaymentMethod) return false
        return id != null && id == other.id
    }
}
```

### Step 2: Create Flyway Migration

See the **postgresql** skill for migration details. File naming: `V{timestamp}__add_payment_methods.sql`

```sql
CREATE TABLE payment_methods (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payment_methods_type ON payment_methods(type);
```

### Step 3: Create Repository

```kotlin
@Repository
interface PaymentMethodRepository : JpaRepository<PaymentMethod, Long> {
    fun findByType(type: PaymentMethodType): List<PaymentMethod>
    fun findByEnabledTrue(): List<PaymentMethod>
    fun existsByNameIgnoreCase(name: String): Boolean
}
```

---

## Adding a Relationship

### Adding ManyToOne (Transaction → PaymentMethod)

**Step 1: Update Entity**

```kotlin
@Entity
@Table(name = "transactions")
data class Transaction(
    // ... existing fields ...

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "payment_method_id")
    val paymentMethod: PaymentMethod? = null
)
```

**Step 2: Migration**

```sql
ALTER TABLE transactions
ADD COLUMN payment_method_id BIGINT REFERENCES payment_methods(id);

CREATE INDEX idx_transactions_payment_method ON transactions(payment_method_id);
```

---

## Custom Repository Implementation

For complex queries beyond JPQL:

### Step 1: Define Custom Interface

```kotlin
interface GameRepositoryCustom {
    fun findByAdvancedCriteria(
        query: String?,
        providerIds: List<Long>,
        pageable: Pageable
    ): Page<Game>
}
```

### Step 2: Implement with Criteria API

```kotlin
@Repository
class GameRepositoryImpl : GameRepositoryCustom {
    @PersistenceContext
    private lateinit var entityManager: EntityManager

    override fun findByAdvancedCriteria(
        query: String?,
        providerIds: List<Long>,
        pageable: Pageable
    ): Page<Game> {
        val cb = entityManager.criteriaBuilder
        val cq = cb.createQuery(Game::class.java)
        val root = cq.from(Game::class.java)

        val predicates = mutableListOf<Predicate>()

        query?.let {
            predicates.add(
                cb.like(cb.lower(root.get("name")), "%${it.lowercase()}%")
            )
        }

        if (providerIds.isNotEmpty()) {
            predicates.add(root.get<Long>("provider").get<Long>("id").`in`(providerIds))
        }

        cq.where(*predicates.toTypedArray())

        val results = entityManager.createQuery(cq)
            .setFirstResult(pageable.offset.toInt())
            .setMaxResults(pageable.pageSize)
            .resultList

        // Count query
        val countQuery = cb.createQuery(Long::class.java)
        val countRoot = countQuery.from(Game::class.java)
        countQuery.select(cb.count(countRoot))
        if (predicates.isNotEmpty()) {
            countQuery.where(*predicates.toTypedArray())
        }
        val total = entityManager.createQuery(countQuery).singleResult

        return PageImpl(results, pageable, total)
    }
}
```

### Step 3: Extend Main Repository

```kotlin
@Repository
interface GameRepository : JpaRepository<Game, Long>, GameRepositoryCustom {
    // Simple queries here
    fun findByStatus(status: GameStatus): List<Game>
}
```

---

## WARNING: Missing Pagination on Large Queries

**The Problem:**

```kotlin
// BAD - Loads all players into memory
@Query("SELECT p FROM Player p WHERE p.status = 'ACTIVE'")
fun findAllActive(): List<Player>  // 100,000+ records = OOM
```

**Why This Breaks:**
1. OutOfMemoryError in production
2. Slow response times even if it succeeds
3. Database connection held too long

**The Fix:**

```kotlin
// GOOD - Paginated results
fun findByStatus(status: PlayerStatus, pageable: Pageable): Page<Player>

// Usage
val page = repo.findByStatus(PlayerStatus.ACTIVE, PageRequest.of(0, 100))
```

**When You Might Be Tempted:**
Export features, reports, or "get all" APIs. Always paginate or stream.

---

## Testing Repositories

Use `@DataJpaTest` for repository tests:

```kotlin
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class PlayerRepositoryTest {
    @Autowired
    private lateinit var playerRepository: PlayerRepository

    @Autowired
    private lateinit var entityManager: TestEntityManager

    @Test
    fun `findByUsername returns player when exists`() {
        val player = Player(username = "testuser", email = "test@example.com")
        entityManager.persistAndFlush(player)

        val found = playerRepository.findByUsername("testuser")

        assertThat(found).isPresent
        assertThat(found.get().username).isEqualTo("testuser")
    }
}
```

---

## Debugging JPA Queries

Enable SQL logging in `application.yml`:

```yaml
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        
logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
```

Check for N+1 queries by counting SQL statements in logs.