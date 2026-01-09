```markdown
# Kotlin Types Reference

Type patterns for data classes, enums, sealed classes, and generics in the casino-b/ codebase.

## Data Classes

### Basic Data Class

```kotlin
data class PlayerDto(
    val id: Long,
    val username: String,
    val email: String,
    val status: PlayerStatus,
    val createdAt: LocalDateTime
) {
    companion object {
        fun from(player: Player) = PlayerDto(
            id = player.id!!,
            username = player.username,
            email = player.email,
            status = player.status,
            createdAt = player.createdAt
        )
    }
}
```

### Data Class with Default Values

```kotlin
data class ProfileUpdateRequest(
    val playerId: Long,
    val documentId: Long,
    val updateFirstName: Boolean = false,
    val updateLastName: Boolean = false,
    val updateDateOfBirth: Boolean = false,
    val adminUserId: Long,
    val reason: String
)
```

### Nested Data Classes

```kotlin
data class ProfileUpdatePreview(
    val playerId: Long,
    val currentProfile: PlayerProfileData,
    val extractedData: ExtractedProfileData,
    val differences: List<ProfileDifference>,
    val canUpdate: Boolean,
    val warnings: List<String>
) {
    data class ProfileDifference(
        val field: String,
        val currentValue: String?,
        val newValue: String?
    )
}
```

## WARNING: Data Classes with JPA Entities

**The Problem:**

```kotlin
// BAD - Data class as JPA entity causes issues
@Entity
data class Player(
    @Id @GeneratedValue
    val id: Long? = null,
    val username: String
)
```

**Why This Breaks:**
1. equals/hashCode includes all fields - breaks JPA identity semantics
2. Lazy-loaded relationships cause unexpected behavior
3. Circular references in toString() cause StackOverflow

**The Fix:**

```kotlin
// GOOD - Regular class with manual equals/hashCode
@Entity
@Table(name = "players")
class Player(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @Column(nullable = false, unique = true)
    val username: String
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Player) return false
        return id != null && id == other.id
    }
    
    override fun hashCode(): Int = id?.hashCode() ?: 0
}
```

**When You Might Be Tempted:**
When you want auto-generated equals/hashCode for entities. Always override manually using ID only.

## Enum Classes

### Basic Enum

```kotlin
enum class PlayerStatus {
    PENDING, ACTIVE, FROZEN, BLOCKED, SUSPENDED, SELF_EXCLUDED, COOLING_OFF
}
```

### Enum with Properties

```kotlin
enum class TransactionType(val isDebit: Boolean) {
    DEPOSIT(false),
    WITHDRAWAL(true),
    BET(true),
    WIN(false),
    BONUS(false),
    REFUND(false);
    
    val isCredit: Boolean get() = !isDebit
}
```

### Enum with Companion Factory

```kotlin
enum class BetType {
    GAME_BET, BONUS_BET, MIXED_BET, FREE_SPIN_BET,
    GAME_WIN, BONUS_WIN, MIXED_WIN, FREE_SPIN_WIN,
    SPORTS_BET, SPORTS_WIN;
    
    companion object {
        fun initialForGameRound(
            isFreeSpin: Boolean = false,
            isBonusOnly: Boolean = false,
            isMixed: Boolean = false
        ): BetType = when {
            isFreeSpin -> FREE_SPIN_BET
            isBonusOnly -> BONUS_BET
            isMixed -> MIXED_BET
            else -> GAME_BET
        }
        
        fun winTypeFor(betType: BetType): BetType = when (betType) {
            GAME_BET -> GAME_WIN
            BONUS_BET -> BONUS_WIN
            MIXED_BET -> MIXED_WIN
            FREE_SPIN_BET -> FREE_SPIN_WIN
            SPORTS_BET -> SPORTS_WIN
            else -> betType
        }
    }
}
```

## Sealed Classes

### Result Pattern

```kotlin
sealed class ValidationResult {
    object Valid : ValidationResult()
    data class Invalid(val errors: List<String>) : ValidationResult()
}

fun validate(request: CreatePlayerRequest): ValidationResult {
    val errors = mutableListOf<String>()
    if (request.email.isBlank()) errors += "Email required"
    if (request.password.length < 8) errors += "Password too short"
    return if (errors.isEmpty()) ValidationResult.Valid 
           else ValidationResult.Invalid(errors)
}
```

### Sealed Interface for ADT

```kotlin
sealed interface PaymentState {
    data class Pending(val checkUrl: String) : PaymentState
    data class Completed(val transactionId: String) : PaymentState
    data class Failed(val code: String, val message: String) : PaymentState
    data class Cancelled(val reason: String) : PaymentState
}
```

## WARNING: Using String Instead of Enum

**The Problem:**

```kotlin
// BAD - Stringly-typed
fun setStatus(status: String) {
    if (status == "active" || status == "ACTIVE") { ... }
}
```

**Why This Breaks:**
1. Typos cause silent bugs ("actve", "ACTIV")
2. No compile-time validation
3. Refactoring misses string literals

**The Fix:**

```kotlin
// GOOD - Type-safe enum
enum class Status { ACTIVE, INACTIVE, PENDING }

fun setStatus(status: Status) {
    when (status) {
        Status.ACTIVE -> { ... }
        Status.INACTIVE -> { ... }
        Status.PENDING -> { ... }
    }
}
```

## Type Aliases

```kotlin
typealias PlayerId = Long
typealias Amount = BigDecimal
typealias GameIds = Set<Long>

fun processPayment(playerId: PlayerId, amount: Amount): TransactionId
```

## Generics

### Generic Repository Interface

```kotlin
interface CrudService<T, ID> {
    fun findById(id: ID): T?
    fun findAll(): List<T>
    fun save(entity: T): T
    fun deleteById(id: ID)
}
```

### Bounded Generics

```kotlin
fun <T : Comparable<T>> findMax(items: List<T>): T? = items.maxOrNull()

inline fun <reified T> parseJson(json: String): T = 
    objectMapper.readValue(json, T::class.java)
```

## Related Skills

- See the **jpa** skill for entity mapping patterns
- See the **spring-boot** skill for DTO validation
```