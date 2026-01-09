# Kotlin Error Handling

Exception handling patterns for the casino backend.

## Custom Exceptions

### Domain-Specific Exceptions

```kotlin
// GOOD - meaningful exception hierarchy
sealed class CasinoException(message: String) : RuntimeException(message)

class PlayerNotFoundException(playerId: Long) :
    CasinoException("Player not found: $playerId")

class InsufficientBalanceException(
    val available: BigDecimal,
    val required: BigDecimal
) : CasinoException("Insufficient balance: available=$available, required=$required")

class BonusNotEligibleException(reason: String) :
    CasinoException("Player not eligible for bonus: $reason")
```

### Exception with Error Codes

```kotlin
enum class ErrorCode(val httpStatus: Int) {
    PLAYER_NOT_FOUND(404),
    INSUFFICIENT_BALANCE(400),
    BONUS_EXPIRED(400),
    VALIDATION_FAILED(422),
    INTERNAL_ERROR(500)
}

class ApiException(
    val code: ErrorCode,
    override val message: String
) : RuntimeException(message)
```

## WARNING: Silent Exception Swallowing

**The Problem:**

```kotlin
// BAD - exception silently ignored
fun processPayment(request: PaymentRequest): PaymentResult {
    try {
        return paymentGateway.process(request)
    } catch (e: Exception) {
        return PaymentResult.failure() // No logging, no context
    }
}
```

**Why This Breaks:**
1. No audit trail when issues occur
2. Debugging is impossible—failure cause unknown
3. May hide critical errors (database down, network issues)

**The Fix:**

```kotlin
// GOOD - log with context, rethrow or handle explicitly
fun processPayment(request: PaymentRequest): PaymentResult {
    return try {
        paymentGateway.process(request)
    } catch (e: PaymentGatewayException) {
        logger.error("Payment failed for player ${request.playerId}: ${e.message}", e)
        PaymentResult.failure(e.errorCode, e.message)
    } catch (e: Exception) {
        logger.error("Unexpected error processing payment: ${request.playerId}", e)
        throw PaymentProcessingException("Payment failed unexpectedly", e)
    }
}
```

## WARNING: Catching Generic Exception

**The Problem:**

```kotlin
// BAD - catches everything including system errors
try {
    processTransaction()
} catch (e: Exception) {
    handleError(e)
}
```

**Why This Breaks:**
1. Catches `OutOfMemoryError`, `InterruptedException`
2. May swallow errors that should crash the application
3. No differentiation between recoverable and fatal errors

**The Fix:**

```kotlin
// GOOD - catch specific exceptions
try {
    processTransaction()
} catch (e: InsufficientBalanceException) {
    return TransactionResult.insufficientFunds(e.available)
} catch (e: PlayerNotFoundException) {
    return TransactionResult.playerNotFound()
} catch (e: DatabaseException) {
    logger.error("Database error during transaction", e)
    throw ServiceUnavailableException("Please try again later")
}
```

## Result Pattern

### Using Kotlin Result

```kotlin
// GOOD - explicit success/failure without exceptions
fun validatePlayer(playerId: Long): Result<Player> {
    val player = playerRepository.findById(playerId).orElse(null)
        ?: return Result.failure(PlayerNotFoundException(playerId))

    if (player.status == PlayerStatus.BLOCKED) {
        return Result.failure(PlayerBlockedException(playerId))
    }

    return Result.success(player)
}

// Usage
validatePlayer(playerId)
    .onSuccess { player -> processBonus(player) }
    .onFailure { error -> logger.warn("Validation failed: ${error.message}") }
```

### Sealed Class for Detailed Results

```kotlin
sealed class WithdrawalResult {
    data class Success(val transactionId: String) : WithdrawalResult()
    data class InsufficientFunds(val available: BigDecimal) : WithdrawalResult()
    data class PlayerBlocked(val reason: String) : WithdrawalResult()
    data class LimitExceeded(val dailyLimit: BigDecimal) : WithdrawalResult()
}

fun processWithdrawal(request: WithdrawalRequest): WithdrawalResult {
    val player = playerRepository.findById(request.playerId)
        ?: return WithdrawalResult.PlayerBlocked("Player not found")

    val wallet = walletRepository.findByPlayerId(request.playerId)
    if (wallet.balance < request.amount) {
        return WithdrawalResult.InsufficientFunds(wallet.balance)
    }

    // Process...
    return WithdrawalResult.Success(transactionId)
}
```

## Exception in Kafka Events

### WARNING: Throwing in Event Publishers

**The Problem:**

```kotlin
// BAD - exception breaks main transaction
fun createPlayer(request: CreatePlayerRequest): Player {
    val player = playerRepository.save(Player(username = request.username))
    eventPublisher.publish(PlayerCreatedEvent(player)) // May throw
    return player // Never reached if publish fails
}
```

**Why This Breaks:**
1. Player created but not returned—inconsistent state
2. Event publishing is secondary to main operation
3. Kafka unavailability shouldn't break player creation

**The Fix:**

```kotlin
// GOOD - fire-and-forget with logging
fun createPlayer(request: CreatePlayerRequest): Player {
    val player = playerRepository.save(Player(username = request.username))
    try {
        eventPublisher.publish(PlayerCreatedEvent(player))
    } catch (e: Exception) {
        logger.error("Failed to publish player created event: ${player.id}", e)
        // Event will be retried via FailedKafkaEvent mechanism
    }
    return player
}
```

See the **kafka** skill for event publishing patterns.

## Global Exception Handler

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    private val logger = LoggerFactory.getLogger(javaClass)

    @ExceptionHandler(PlayerNotFoundException::class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    fun handlePlayerNotFound(e: PlayerNotFoundException): ErrorResponse {
        return ErrorResponse(
            status = "ERROR",
            code = "PLAYER_NOT_FOUND",
            message = e.message ?: "Player not found"
        )
    }

    @ExceptionHandler(MethodArgumentNotValidException::class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    fun handleValidation(e: MethodArgumentNotValidException): ErrorResponse {
        val errors = e.bindingResult.fieldErrors
            .associate { it.field to (it.defaultMessage ?: "Invalid") }
        return ErrorResponse(
            status = "ERROR",
            code = "VALIDATION_FAILED",
            message = "Validation failed",
            details = mapOf("fields" to errors)
        )
    }

    @ExceptionHandler(Exception::class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    fun handleUnexpected(e: Exception): ErrorResponse {
        logger.error("Unexpected error", e)
        return ErrorResponse(
            status = "ERROR",
            code = "INTERNAL_ERROR",
            message = "An unexpected error occurred"
        )
    }
}
```

See the **spring-boot** skill for controller advice patterns.