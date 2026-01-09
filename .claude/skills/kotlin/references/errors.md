```markdown
# Kotlin Errors Reference

Exception handling, validation, and error patterns in the casino-b/ codebase.

## Custom Exception Hierarchy

### Base Exception Pattern

```kotlin
@ResponseStatus(HttpStatus.NOT_FOUND)
class NotFoundException(message: String) : RuntimeException(message)

@ResponseStatus(HttpStatus.BAD_REQUEST)
class BadRequestException(message: String) : RuntimeException(message)

@ResponseStatus(HttpStatus.CONFLICT)
class ConflictException(message: String) : RuntimeException(message)

@ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
class LimitExceededException(
    message: String,
    val limitDetails: Map<String, Any?> = emptyMap()
) : RuntimeException(message)
```

### Exception with Context

```kotlin
class PaymentFailedException(
    message: String,
    val paymentId: String,
    val errorCode: String,
    cause: Throwable? = null
) : RuntimeException(message, cause)

// Usage
throw PaymentFailedException(
    message = "Payment processing failed",
    paymentId = payment.id,
    errorCode = "GATEWAY_TIMEOUT",
    cause = e
)
```

## Global Exception Handler

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {
    private val logger = LoggerFactory.getLogger(javaClass)

    @ExceptionHandler(NotFoundException::class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    fun handleNotFound(ex: NotFoundException): ErrorResponse {
        return ErrorResponse(
            status = "ERROR",
            code = "NOT_FOUND",
            message = ex.message ?: "Resource not found"
        )
    }

    @ExceptionHandler(MethodArgumentNotValidException::class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    fun handleValidation(ex: MethodArgumentNotValidException): ErrorResponse {
        val errors = ex.bindingResult.fieldErrors.associate { 
            it.field to (it.defaultMessage ?: "Invalid")
        }
        return ErrorResponse(
            status = "ERROR",
            code = "VALIDATION_FAILED",
            message = "Validation failed",
            details = mapOf("fields" to errors)
        )
    }
}
```

## WARNING: Silent Exception Swallowing

**The Problem:**

```kotlin
// BAD - Catches exception, does nothing
fun processPayment(payment: Payment): Boolean {
    try {
        gateway.process(payment)
        return true
    } catch (e: Exception) {
        return false  // Silent failure - what went wrong?
    }
}
```

**Why This Breaks:**
1. Debugging nightmare - no trace of what failed
2. Masks configuration errors, network issues, bugs
3. Impossible to monitor in production
4. Cannot trigger alerts or retries

**The Fix:**

```kotlin
// GOOD - Log, then handle appropriately
fun processPayment(payment: Payment): PaymentResult {
    return try {
        gateway.process(payment)
        PaymentResult.Success(payment.id)
    } catch (e: PaymentGatewayException) {
        logger.error("Payment failed: ${payment.id}", e)
        PaymentResult.Failed(e.errorCode, e.message ?: "Unknown error")
    } catch (e: Exception) {
        logger.error("Unexpected error processing payment: ${payment.id}", e)
        throw PaymentProcessingException("Failed to process payment", e)
    }
}
```

## Validation Patterns

### Jakarta Bean Validation

```kotlin
data class CreatePlayerRequest(
    @field:NotBlank(message = "Username is required")
    @field:Size(min = 3, max = 50, message = "Username must be 3-50 characters")
    val username: String,
    
    @field:NotBlank(message = "Email is required")
    @field:Email(message = "Invalid email format")
    val email: String,
    
    @field:NotBlank(message = "Password is required")
    @field:Size(min = 8, max = 100, message = "Password must be 8-100 characters")
    val password: String
)
```

### Programmatic Validation with require/check

```kotlin
fun updateThreshold(value: Double, updatedBy: String) {
    require(value in 0.0..1.0) { 
        "Threshold must be between 0 and 1, got: $value" 
    }
    require(updatedBy.isNotBlank()) { 
        "Updater must not be blank" 
    }
    // proceed
}

fun withdraw(amount: BigDecimal) {
    check(status == AccountStatus.ACTIVE) { 
        "Cannot withdraw from ${status} account" 
    }
    check(balance >= amount) { 
        "Insufficient balance: $balance < $amount" 
    }
    // proceed
}
```

## WARNING: Using Exceptions for Flow Control

**The Problem:**

```kotlin
// BAD - Exceptions for expected cases
fun findPlayer(id: Long): Player? {
    return try {
        playerRepository.getById(id)  // throws if not found
    } catch (e: EntityNotFoundException) {
        null
    }
}
```

**Why This Breaks:**
1. Exceptions are expensive - stack trace creation
2. Makes debugging harder (noise in logs)
3. Control flow is obscured
4. Performance impact in hot paths

**The Fix:**

```kotlin
// GOOD - Use Optional or nullable return
fun findPlayer(id: Long): Player? {
    return playerRepository.findById(id).orElse(null)
}

// GOOD - Use sealed class for expected outcomes
sealed class FindResult<out T> {
    data class Found<T>(val value: T) : FindResult<T>()
    object NotFound : FindResult<Nothing>()
}
```

## Kafka Event Error Handling

### Fire-and-Forget Pattern

```kotlin
fun publishPlayerRegistered(player: Player) {
    try {
        val event = PlayerRegisteredEvent(
            eventId = EventBuilder.generateEventId(),
            eventTimestamp = EventBuilder.getCurrentTimestamp(),
            payload = PlayerRegisteredPayload(player.username, player.email)
        )
        eventPublisher.publish(KafkaTopics.PLAYER_REGISTERED, player.id.toString(), event)
        logger.info("Published player registered event: ${player.id}")
    } catch (e: Exception) {
        logger.error("Failed to publish event for player: ${player.id}", e)
        // DON'T throw - event publishing should not break main flow
        // Events go to failed_kafka_events table for retry
    }
}
```

## WARNING: Throwing in Kafka Publishers

**The Problem:**

```kotlin
// BAD - Exception breaks registration
@Transactional
fun registerPlayer(request: RegisterRequest): Player {
    val player = playerRepository.save(Player(...))
    eventPublisher.publish(event)  // Throws on Kafka failure
    return player  // Never reached if Kafka is down
}
```

**Why This Breaks:**
1. Player registration fails when Kafka has transient issues
2. Transaction rolls back - user cannot register
3. Couples core business to messaging infrastructure
4. Single point of failure

**The Fix:**

```kotlin
// GOOD - Async publishing with fallback
@Transactional
fun registerPlayer(request: RegisterRequest): Player {
    val player = playerRepository.save(Player(...))
    
    try {
        asyncEventPublisher.publishAsync(event)
    } catch (e: Exception) {
        logger.error("Event publish failed, saving for retry: ${player.id}", e)
        failedEventRepository.save(FailedKafkaEvent(event, e.message))
    }
    
    return player  // Always returns - registration succeeds
}
```

## Error Response Format

```kotlin
data class ErrorResponse(
    val status: String = "ERROR",
    val code: String,
    val message: String,
    val timestamp: Instant = Instant.now(),
    val details: Map<String, Any?>? = null
)

// Example response:
// {
//   "status": "ERROR",
//   "code": "VALIDATION_FAILED",
//   "message": "Validation failed",
//   "timestamp": "2024-01-15T10:30:00Z",
//   "details": {
//     "fields": { "email": "Invalid email format" }
//   }
// }
```

## Related Skills

- See the **spring-boot** skill for @ControllerAdvice patterns
- See the **kafka** skill for event retry mechanisms
- See the **jpa** skill for repository exception handling
```

I've generated all the Kotlin skill files. Would you like me to create the directory structure and write these files once you grant permission?