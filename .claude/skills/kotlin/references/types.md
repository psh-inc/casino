# Kotlin Types

Type system patterns and best practices for the casino backend.

## Data Classes

### WARNING: Mutable Properties in Data Classes

**The Problem:**

```kotlin
// BAD - mutable data class
data class PlayerDto(
    var id: Long,
    var username: String,
    var balance: BigDecimal
)
```

**Why This Breaks:**
1. DTOs should be immutable—unexpected mutations cause bugs
2. Breaks hashCode/equals contract if used in collections
3. Thread safety issues in concurrent contexts

**The Fix:**

```kotlin
// GOOD - immutable with val
data class PlayerDto(
    val id: Long,
    val username: String,
    val balance: BigDecimal
)

// If you need to "modify", use copy()
val updated = playerDto.copy(balance = newBalance)
```

## Nullable Types

### Nullable vs Non-Nullable Design

```kotlin
// GOOD - entity ID nullable before persistence
@Entity
data class Player(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,  // null until saved

    @Column(nullable = false)
    val username: String,  // never null

    val nickname: String? = null  // optional field
)
```

### DTO Nullability

```kotlin
// GOOD - response DTO with non-null ID (already persisted)
data class PlayerResponse(
    val id: Long,  // guaranteed after fetch
    val username: String,
    val nickname: String?,  // may be null
    val lastLoginAt: LocalDateTime?  // may be null
)

// GOOD - request DTO with nullable optional fields
data class UpdatePlayerRequest(
    val nickname: String? = null,  // only update if provided
    val locale: String? = null
)
```

## Enums

### Enum with Properties

```kotlin
enum class PlayerStatus(val canPlay: Boolean, val canWithdraw: Boolean) {
    PENDING(false, false),
    ACTIVE(true, true),
    FROZEN(false, false),
    BLOCKED(false, false),
    SUSPENDED(false, false),
    SELF_EXCLUDED(false, false),
    COOLING_OFF(false, true);

    fun isRestricted(): Boolean = !canPlay || !canWithdraw
}
```

### WARNING: String-Based Type Discrimination

**The Problem:**

```kotlin
// BAD - stringly typed
fun processReward(type: String, amount: BigDecimal) {
    when (type) {
        "MONEY" -> processMoney(amount)
        "FREE_SPINS" -> processFreeSpins(amount)
        else -> throw IllegalArgumentException("Unknown type")
    }
}
```

**Why This Breaks:**
1. No compile-time safety—typos cause runtime errors
2. Refactoring doesn't catch all usages
3. No IDE autocomplete support

**The Fix:**

```kotlin
// GOOD - use enum
enum class RewardType {
    MONEY, FREE_SPINS, SPORTS_BONUS
}

fun processReward(type: RewardType, amount: BigDecimal) {
    when (type) {
        RewardType.MONEY -> processMoney(amount)
        RewardType.FREE_SPINS -> processFreeSpins(amount)
        RewardType.SPORTS_BONUS -> processSportsBonus(amount)
    }
}
```

## BigDecimal Handling

### WARNING: Creating BigDecimal from Double

**The Problem:**

```kotlin
// BAD - precision loss
val amount = BigDecimal(123.45)  // Actually 123.4500000000000028421...
val rate = BigDecimal(0.1)       // Not exactly 0.1
```

**Why This Breaks:**
1. Double cannot represent decimals exactly
2. Financial calculations accumulate errors
3. €99.99 may become €99.98999999

**The Fix:**

```kotlin
// GOOD - from String
val amount = BigDecimal("123.45")
val rate = BigDecimal("0.1")

// GOOD - use constants
val zero = BigDecimal.ZERO
val one = BigDecimal.ONE
```

### BigDecimal Comparisons

```kotlin
// GOOD - compareTo for value comparison
fun isPositive(amount: BigDecimal): Boolean =
    amount.compareTo(BigDecimal.ZERO) > 0

// GOOD - signum for sign check
fun getBalanceStatus(balance: BigDecimal): String = when (balance.signum()) {
    1 -> "Positive"
    0 -> "Zero"
    -1 -> "Negative"
    else -> error("Impossible")
}
```

## Type Aliases

```kotlin
// GOOD - meaningful aliases for complex types
typealias PlayerId = Long
typealias TransactionId = String
typealias CurrencyCode = String

// GOOD - function type aliases
typealias PlayerValidator = (Player) -> ValidationResult
typealias TransactionMapper = (Transaction) -> TransactionDto
```

## Generic Types

```kotlin
// GOOD - generic response wrapper
data class ApiResponse<T>(
    val status: String,
    val data: T?,
    val error: String? = null
) {
    companion object {
        fun <T> success(data: T) = ApiResponse("SUCCESS", data)
        fun <T> error(message: String) = ApiResponse<T>("ERROR", null, message)
    }
}
```