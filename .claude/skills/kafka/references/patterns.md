# Kafka Patterns

## Event Publishing Patterns

### Pattern 1: Domain Event Service

Each domain has a dedicated event service that encapsulates event creation and publishing.

```kotlin
@Service
class BonusEventService(
    private val eventPublisher: EventPublisher,
    private val metadataBuilder: EventMetadataBuilder
) {
    @Value("\${app.brand-id}")
    private lateinit var brandId: String

    fun publishBonusActivated(bonus: Bonus, player: Player) {
        try {
            val event = BonusActivatedEvent(
                eventId = EventBuilder.generateEventId(),
                eventTimestamp = EventBuilder.getCurrentTimestamp(),
                brandId = brandId,
                userId = player.id.toString(),
                metadata = metadataBuilder.build(player),
                payload = BonusActivatedPayload(
                    bonusId = bonus.id.toString(),
                    bonusType = bonus.type.name,
                    amount = bonus.amount.toPlainString()
                )
            )
            eventPublisher.publish(
                topic = KafkaTopics.BONUS_ACTIVATED,
                key = player.id.toString(),
                event = event
            )
            logger.info("Published bonus activated: bonusId={}", bonus.id)
        } catch (e: Exception) {
            logger.error("Failed to publish bonus event", e)
            // Don't throw - event failures must not break business logic
        }
    }
}
```

### Pattern 2: High-Frequency Event Batching

For events that fire rapidly (e.g., wagering updates), batch them to reduce Kafka load.

```kotlin
@Service
class BonusEventService(...) {
    private val wageringBatch = ConcurrentHashMap<Long, WageringContribution>()

    fun addWageringContribution(playerId: Long, contribution: BigDecimal) {
        wageringBatch.merge(playerId, WageringContribution(playerId, contribution)) { old, new ->
            old.copy(total = old.total + new.total)
        }
    }

    @Scheduled(fixedRate = 10000) // Every 10 seconds
    fun flushWageringBatches() {
        if (wageringBatch.isEmpty()) return
        
        val batch = HashMap(wageringBatch)
        wageringBatch.clear()
        
        batch.forEach { (playerId, contribution) ->
            publishWageringUpdateImmediate(playerId, contribution)
        }
    }
}
```

---

## WARNING: Throwing Exceptions in Event Publishers

**The Problem:**

```kotlin
// BAD - Exception breaks the main business flow
fun publishPlayerRegistered(player: Player) {
    val event = createEvent(player)
    eventPublisher.publish(topic, key, event) // If this fails...
    throw RuntimeException("Failed to publish") // ...registration breaks!
}
```

**Why This Breaks:**
1. Player registration fails even though database save succeeded
2. User sees error despite account being created
3. Inconsistent state: player exists but no Kafka event

**The Fix:**

```kotlin
// GOOD - Log error but never throw
fun publishPlayerRegistered(player: Player) {
    try {
        val event = createEvent(player)
        eventPublisher.publish(topic, key, event)
        logger.info("Published player registered: {}", player.id)
    } catch (e: Exception) {
        logger.error("Failed to publish player event: {}", player.id, e)
        // Event stored to database by ResilientAsyncEventPublisher
        // Automatic retry will handle it
    }
}
```

**When You Might Be Tempted:**
When you want to ensure "all or nothing" semantics. Instead, rely on the resilient publisher's database fallback and automatic retry.

---

## WARNING: Using Synchronous/Blocking Publisher

**The Problem:**

```kotlin
// BAD - Blocks thread for up to 5 seconds per publish
@Qualifier("legacyEventPublisher")
private val eventPublisher: LegacyKafkaEventPublisher

fun publishEvent(event: Event) {
    eventPublisher.publish(topic, key, event) // Blocks calling thread!
}
```

**Why This Breaks:**
1. HTTP request thread blocked waiting for Kafka acknowledgment
2. Response latency increases by 100-5000ms per event
3. Thread pool exhaustion under load
4. No circuit breaker protection

**The Fix:**

```kotlin
// GOOD - Use the default async publisher (automatically injected)
@Service
class MyEventService(
    private val eventPublisher: EventPublisher // Injects ResilientAsyncEventPublisher
) {
    fun publishEvent(event: Event) {
        eventPublisher.publish(topic, key, event) // Returns immediately
    }
}
```

**When You Might Be Tempted:**
When you need confirmation that the event was published. Use `publishAsync()` with `.thenAccept()` instead.

---

## WARNING: Hardcoding Topic Names

**The Problem:**

```kotlin
// BAD - Topic name scattered across codebase
eventPublisher.publish("casino.player.registered.v1", key, event)
```

**Why This Breaks:**
1. Topic rename requires finding all usages
2. Typos cause silent failures (messages go nowhere)
3. No compile-time safety

**The Fix:**

```kotlin
// GOOD - Centralized topic constants
eventPublisher.publish(KafkaTopics.PLAYER_REGISTERED, key, event)

// In KafkaTopics.kt
object KafkaTopics {
    const val PLAYER_REGISTERED = "casino.player.registered.v1"
}
```

---

## Event Structure Pattern

All events extend `BaseEvent` with consistent structure:

```kotlin
class PlayerRegisteredEvent(
    eventId: String,
    eventTimestamp: String,
    brandId: String,
    userId: String,
    metadata: EventMetadata,
    val payload: PlayerRegisteredPayload
) : BaseEvent(
    eventId = eventId,
    eventType = KafkaTopics.PLAYER_REGISTERED,
    eventTimestamp = eventTimestamp,
    brandId = brandId,
    userId = userId,
    metadata = metadata
)

data class PlayerRegisteredPayload(
    val username: String,
    val email: String,
    val firstName: String?,
    val lastName: String?,
    // ... domain-specific fields
)
```

## Topic Naming Convention

Follow this pattern: `casino.{domain}.{action}.v{version}`

| Domain | Examples |
|--------|----------|
| player | `casino.player.registered.v1`, `casino.player.status-changed.v1` |
| payment | `casino.payment.deposit-completed.v1`, `casino.payment.withdrawal-created.v1` |
| bonus | `casino.bonus.activated.v1`, `casino.bonus.wagering-updated.v1` |
| game | `casino.game.session-started.v1`, `casino.game.bet-placed.v1` |
| sports | `casino.sports.bet-placed.v1`, `casino.sports.bet-settled.v1` |
| compliance | `casino.compliance.kyc-submitted.v1` |