```markdown
# Kotlin Patterns Reference

Idiomatic Kotlin patterns used in the casino-b/ backend codebase.

## Null Safety Patterns

### Safe Call Chain with Elvis

```kotlin
// GOOD - Chained safe calls with fallback
val balance = player?.wallet?.balance ?: BigDecimal.ZERO
val country = player.addresses.firstOrNull { it.addressType == AddressType.RESIDENTIAL }?.country

// BAD - Unsafe access that crashes on null
val balance = player!!.wallet!!.balance  // DON'T
```

### let for Nullable Transformation

```kotlin
// GOOD - Transform only when non-null
maxAmount?.let { max ->
    if (calculated > max) max else calculated
} ?: calculated

// BAD - Verbose null check
if (maxAmount != null) {
    if (calculated > maxAmount) maxAmount else calculated
} else {
    calculated
}
```

## Scope Functions

### apply for Object Configuration

```kotlin
// GOOD - Configure object in-place
val player = Player().apply {
    username = request.username
    email = request.email
    status = PlayerStatus.PENDING
}

// Use when: Building/configuring objects
```

### also for Side Effects

```kotlin
// GOOD - Perform side effect, return original
val saved = repository.save(entity).also {
    logger.info("Created entity: ${it.id}")
    eventPublisher.publish(EntityCreatedEvent(it))
}
```

### run for Scoped Computation

```kotlin
// GOOD - Compute value with receiver
val result = player.run {
    val fullName = "$firstName $lastName"
    PlayerSummary(id, fullName, status)
}
```

## WARNING: Overusing Non-Null Assertion (!!)

**The Problem:**

```kotlin
// BAD - Crashes at runtime if null
val playerId = player.id!!
val wallet = walletRepository.findByPlayerId(id)!!
```

**Why This Breaks:**
1. NullPointerException at runtime defeats Kotlin's null safety
2. No compiler protection for edge cases
3. Fails silently in production when data is unexpectedly null

**The Fix:**

```kotlin
// GOOD - Handle null explicitly
val playerId = player.id ?: throw IllegalStateException("Player not persisted")
val wallet = walletRepository.findByPlayerId(id)
    ?: throw NotFoundException("Wallet not found for player: $id")
```

**When You Might Be Tempted:**
When you're "sure" the value exists (after a save, in a transaction). Always handle explicitly.

## Collection Patterns

### map with Data Transformation

```kotlin
val dtos = entities.map { entity ->
    EntityDto(
        id = entity.id!!,
        name = entity.name,
        createdAt = entity.createdAt
    )
}
```

### filter with Predicate

```kotlin
val activeGames = games.filter { game ->
    game.status == GameStatus.ACTIVE &&
    gameAvailabilityService.isGameAvailable(game.id, countryCode)
}
```

### groupBy for Categorization

```kotlin
val transactionsByType = transactions.groupBy { it.type }
val depositTotal = transactionsByType[TransactionType.DEPOSIT]
    ?.sumOf { it.amount } ?: BigDecimal.ZERO
```

### sumOf for Aggregation

```kotlin
val totalLocked = lockedDeposits.sumOf { it.lockedAmount }
val playerCount = segments.sumOf { it.playerIds.size }
```

## WARNING: Mutating Collections In-Place

**The Problem:**

```kotlin
// BAD - Mutating shared list
val games = gameRepository.findAll()
games.removeIf { !it.isActive }  // Modifies underlying collection
```

**Why This Breaks:**
1. JPA collections may be hibernate proxies - mutation causes issues
2. Shared references see unexpected changes
3. Thread-safety problems in concurrent contexts

**The Fix:**

```kotlin
// GOOD - Create new filtered list
val activeGames = gameRepository.findAll().filter { it.isActive }
```

## When Expression Patterns

### Exhaustive When with Sealed Classes

```kotlin
sealed class PaymentResult {
    data class Success(val transactionId: String) : PaymentResult()
    data class Failed(val reason: String) : PaymentResult()
    data class Pending(val checkUrl: String) : PaymentResult()
}

// Compiler enforces all cases handled
fun process(result: PaymentResult): String = when (result) {
    is PaymentResult.Success -> "Completed: ${result.transactionId}"
    is PaymentResult.Failed -> "Failed: ${result.reason}"
    is PaymentResult.Pending -> "Check: ${result.checkUrl}"
}
```

### When with Smart Cast

```kotlin
val amount = responseBody["amount"]?.let {
    when (it) {
        is Number -> BigDecimal(it.toString())
        is String -> BigDecimal(it)
        else -> BigDecimal.ONE
    }
} ?: BigDecimal.ONE
```

## Validation Patterns

### require for Preconditions

```kotlin
fun updateThreshold(value: Double, updatedBy: String) {
    require(value in 0.0..1.0) { "Threshold must be between 0 and 1" }
    require(updatedBy.isNotBlank()) { "Updater required" }
    // proceed with update
}
```

### check for State Invariants

```kotlin
fun withdraw(amount: BigDecimal) {
    check(status == AccountStatus.ACTIVE) { "Account must be active" }
    check(balance >= amount) { "Insufficient funds" }
    // proceed with withdrawal
}
```

## Related Skills

- See the **spring-boot** skill for @Transactional patterns
- See the **jpa** skill for repository query methods
```