# Kotlin Modules

Package organization and dependency patterns in the casino backend.

## Package Structure

```
com.casino.core/
├── controller/     # REST endpoints (99 files)
├── service/        # Business logic (140 files)
├── repository/     # JPA repositories (114 files)
├── domain/         # JPA entities (109 files)
├── dto/            # Data transfer objects (100 files)
├── config/         # Spring configuration (27 files)
├── security/       # Auth, JWT, guards
├── kafka/          # Event publishing
├── event/          # Domain events
├── scheduler/      # Cron jobs
└── exception/      # Custom exceptions
```

## Layer Dependencies

### WARNING: Circular Dependencies

**The Problem:**

```kotlin
// BAD - ServiceA depends on ServiceB, ServiceB depends on ServiceA
@Service
class PlayerService(private val walletService: WalletService) { }

@Service
class WalletService(private val playerService: PlayerService) { }
// Spring fails: circular dependency
```

**Why This Breaks:**
1. Spring cannot instantiate beans with cycles
2. Indicates poor separation of concerns
3. Hard to test in isolation

**The Fix:**

```kotlin
// GOOD - extract shared logic to third service
@Service
class PlayerService(private val playerRepository: PlayerRepository) { }

@Service
class WalletService(private val walletRepository: WalletRepository) { }

@Service
class PlayerWalletService(
    private val playerService: PlayerService,
    private val walletService: WalletService
) {
    // Coordination logic here
}
```

## Constructor Injection

### WARNING: Field Injection

**The Problem:**

```kotlin
// BAD - field injection
@Service
class PlayerService {
    @Autowired
    private lateinit var repository: PlayerRepository

    @Autowired
    private lateinit var eventPublisher: EventPublisher
}
```

**Why This Breaks:**
1. Cannot create instance without Spring context—untestable
2. Dependencies are hidden—not obvious from constructor
3. `lateinit` can throw if accessed before injection

**The Fix:**

```kotlin
// GOOD - constructor injection
@Service
class PlayerService(
    private val repository: PlayerRepository,
    private val eventPublisher: EventPublisher
) {
    // Dependencies are explicit and immutable
}

// Tests can inject mocks easily
val service = PlayerService(mockRepository, mockPublisher)
```

## Configuration Classes

```kotlin
@Configuration
class CacheConfig {

    @Bean
    fun cacheManager(): CacheManager {
        return CaffeineCacheManager().apply {
            setCaffeine(Caffeine.newBuilder()
                .maximumSize(10_000)
                .expireAfterWrite(5, TimeUnit.SECONDS))
        }
    }
}
```

## Component Scanning

```kotlin
// GOOD - explicit component scanning
@SpringBootApplication
@ComponentScan(basePackages = ["com.casino.core"])
class CasinoApplication

fun main(args: Array<String>) {
    runApplication<CasinoApplication>(*args)
}
```

## Feature Modules

### Encapsulated Feature Package

```
com.casino.core.bonus/
├── BonusController.kt
├── BonusService.kt
├── BonusRepository.kt
├── Bonus.kt (entity)
├── BonusDto.kt
├── BonusCategory.kt (enum)
└── BonusNotFoundException.kt
```

## Internal Visibility

```kotlin
// GOOD - restrict visibility to module
internal class BonusValidator {
    internal fun validate(bonus: Bonus): ValidationResult {
        // Only accessible within same module
    }
}
```

## Companion Objects for Static-Like Behavior

```kotlin
@Entity
@Table(name = "transactions")
data class Transaction(
    @Id val id: Long? = null,
    val amount: BigDecimal,
    val type: TransactionType
) {
    companion object {
        const val TABLE_NAME = "transactions"

        fun deposit(amount: BigDecimal) = Transaction(
            amount = amount,
            type = TransactionType.DEPOSIT
        )

        fun withdrawal(amount: BigDecimal) = Transaction(
            amount = amount,
            type = TransactionType.WITHDRAWAL
        )
    }
}
```

## Integration with Other Skills

For Spring Boot configuration patterns, see the **spring-boot** skill.

For JPA entity mapping, see the **jpa** skill.

For Kafka event module organization, see the **kafka** skill.