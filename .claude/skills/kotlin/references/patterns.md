# Kotlin Patterns

Idiomatic Kotlin patterns used throughout the casino-b backend.

## Scope Functions

### apply - Object Configuration

```kotlin
// GOOD - configure object during construction
val player = Player().apply {
    username = request.username
    email = request.email
    status = PlayerStatus.PENDING
}
```

### let - Null-Safe Transformations

```kotlin
// GOOD - transform nullable value
val displayName = player.nickname?.let { "@$it" } ?: player.username

// GOOD - execute block only if non-null
player.referralCode?.let { code ->
    referralService.processReferral(code, player.id!!)
}
```

### also - Side Effects

```kotlin
// GOOD - logging or side effects without changing value
return bonusRepository.save(bonus).also {
    logger.info("Created bonus: ${it.id}")
    eventPublisher.publishBonusCreated(it)
}
```

## Collection Operations

### WARNING: Mutating Collections

**The Problem:**

```kotlin
// BAD - mutating input list
fun processPlayers(players: List<Player>) {
    (players as MutableList).add(newPlayer) // ClassCastException risk
}
```

**Why This Breaks:**
1. Caller may pass immutable list, causing runtime exception
2. Violates function contract—side effects are unexpected
3. Concurrent modification if list is shared

**The Fix:**

```kotlin
// GOOD - return new collection
fun processPlayers(players: List<Player>): List<Player> {
    return players + newPlayer
}
```

### Filter and Map Chains

```kotlin
// GOOD - readable chain operations
val activePlayerEmails = players
    .filter { it.status == PlayerStatus.ACTIVE }
    .filter { it.emailVerified }
    .map { it.email }
    .distinct()
```

### groupBy for Aggregation

```kotlin
// GOOD - group transactions by currency
val transactionsByCurrency = transactions.groupBy { it.currency }
    .mapValues { (_, txs) -> txs.sumOf { it.amount } }
```

## Null Safety Patterns

### WARNING: Overusing !! (Not-Null Assertion)

**The Problem:**

```kotlin
// BAD - crashes if null
val playerId = player.id!!
val balance = wallet!!.balance!!
```

**Why This Breaks:**
1. NPE at runtime defeats Kotlin's null safety
2. No information about why null occurred
3. Cascading failures are hard to debug

**The Fix:**

```kotlin
// GOOD - explicit handling with meaningful error
val playerId = player.id
    ?: throw IllegalStateException("Player must be persisted before use")

// GOOD - safe call with default
val balance = wallet?.balance ?: BigDecimal.ZERO
```

### Elvis Operator for Defaults

```kotlin
// GOOD - provide sensible defaults
val locale = player.locale ?: "en"
val limit = request.limit ?: 20
val currency = wallet?.currency ?: defaultCurrency
```

## Extension Functions

### Domain-Specific Extensions

```kotlin
// GOOD - add behavior to existing types
fun Player.isEligibleForBonus(): Boolean {
    return status == PlayerStatus.ACTIVE &&
           !allBonusesRestricted &&
           kycStatus == SimpleKycStatus.VERIFIED
}

// Usage
if (player.isEligibleForBonus()) {
    applyBonus(player)
}
```

### String Extensions

```kotlin
// GOOD - reusable string utilities
fun String.toSlug(): String = this
    .lowercase()
    .replace(Regex("[^a-z0-9]+"), "-")
    .trim('-')
```

## Sealed Classes for State

```kotlin
// GOOD - exhaustive when expressions
sealed class PaymentResult {
    data class Success(val transactionId: String) : PaymentResult()
    data class Failure(val error: String, val code: String) : PaymentResult()
    object Pending : PaymentResult()
}

fun handlePayment(result: PaymentResult): String = when (result) {
    is PaymentResult.Success -> "Transaction: ${result.transactionId}"
    is PaymentResult.Failure -> "Error: ${result.error}"
    PaymentResult.Pending -> "Processing..."
    // Compiler ensures all cases handled
}
```

## Companion Object Factory Methods

```kotlin
data class PlayerDto(
    val id: Long,
    val username: String,
    val status: PlayerStatus
) {
    companion object {
        fun from(player: Player): PlayerDto = PlayerDto(
            id = player.id!!,
            username = player.username,
            status = player.status
        )
    }
}
```