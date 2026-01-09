# Kafka Patterns

## Event Publishing Patterns

### Pattern 1: Fire-and-Forget (Recommended)

Use for most event publishing scenarios. Never blocks calling thread.

```kotlin
// GOOD - Fire and forget
fun publishPlayerRegistered(player: Player) {
    try {
        val event = PlayerRegisteredEvent(
            eventId = EventBuilder.generateEventId(),
            eventTimestamp = EventBuilder.getCurrentTimestamp(),
            brandId = brandId,
            userId = player.id.toString(),
            metadata = metadataBuilder.build(player),
            payload = PlayerRegisteredPayload(/* ... */)
        )
        
        // Returns immediately - background thread handles publish
        eventPublisher.publish(
            topic = KafkaTopics.PLAYER_REGISTERED,
            key = player.id.toString(),
            event = event
        )
        
        logger.info("Published player registered event: {}", player.id)
    } catch (e: Exception) {
        logger.error("Failed to publish event: {}", player.id, e)
        // NEVER throw from event publisher
    }
}
```

### Pattern 2: Async with Confirmation

Use when you need to chain operations after successful publish.

```kotlin
// Wait for confirmation when needed
eventPublisher.publishAsync(topic, key, event)
    .whenComplete { result, error ->
        if (error == null) {
            logger.info("Published to partition {}", result.recordMetadata.partition())
        } else {
            logger.error("Publish failed", error)
        }
    }
```

### Pattern 3: Batch Publishing

Use for high-throughput scenarios like bulk imports.

```kotlin
val events = players.map { player ->
    player.id.toString() to createRegistrationEvent(player)
}
eventPublisher.publishBatch(KafkaTopics.PLAYER_REGISTERED, events)
```

---

## WARNING: Throwing Exceptions from Event Publishers

**The Problem:**

```kotlin
// BAD - Exception breaks main business flow
fun registerPlayer(request: RegisterRequest): Player {
    val player = playerRepository.save(createPlayer(request))
    eventPublisher.publish(topic, player.id.toString(), event) // Can throw!
    return player  // Never reached if Kafka is down
}
```

**Why This Breaks:**
1. Player registration fails when Kafka is unavailable
2. User sees error even though player was saved to database
3. Data inconsistency: player exists but no event was published
4. Cascading failures across the system during Kafka outages

**The Fix:**

```kotlin
// GOOD - Wrap in try-catch, never propagate
fun registerPlayer(request: RegisterRequest): Player {
    val player = playerRepository.save(createPlayer(request))
    try {
        playerEventService.publishPlayerRegistered(player)
    } catch (e: Exception) {
        logger.error("Event publish failed for player {}", player.id, e)
        // ResilientAsyncEventPublisher stores to DB automatically
    }
    return player
}
```

**When You Might Be Tempted:**
When you want guaranteed event delivery. Instead, rely on the `FailedKafkaEvent` retry mechanism.

---

## WARNING: Using Legacy Synchronous Publisher

**The Problem:**

```kotlin
// BAD - Blocks for 5 seconds per publish
@Service
class MyService(
    @Qualifier("legacyEventPublisher")  // DON'T inject this
    private val eventPublisher: EventPublisher
)
```

**Why This Breaks:**
1. Blocks calling thread for up to 5 seconds per event
2. No circuit breaker protection
3. Failed events are lost permanently
4. Can crash application if Kafka is down during high traffic

**The Fix:**

```kotlin
// GOOD - Default injection gives ResilientAsyncEventPublisher
@Service
class MyService(
    private val eventPublisher: EventPublisher  // @Primary is ResilientAsyncEventPublisher
)
```

---

## WARNING: Hardcoded Topic Names

**The Problem:**

```kotlin
// BAD - Magic strings
eventPublisher.publish("casino.player.registered.v1", key, event)
```

**Why This Breaks:**
1. Typos cause silent failures (messages go to wrong topic)
2. No compile-time checking
3. Difficult to refactor or audit topic usage

**The Fix:**

```kotlin
// GOOD - Use constants
eventPublisher.publish(KafkaTopics.PLAYER_REGISTERED, key, event)
```

---

## Event Structure Best Practices

### Partition Key Selection

Always use `userId` (or `playerId`) as partition key for event ordering:

```kotlin
// GOOD - All events for a player go to same partition (ordered)
eventPublisher.publish(
    topic = KafkaTopics.PLAYER_STATUS_CHANGED,
    key = player.id.toString(),  // Partition key
    event = event
)
```

### Event ID Generation

```kotlin
// GOOD - UUID for deduplication
val eventId = EventBuilder.generateEventId()  // UUID.randomUUID().toString()

// GOOD - ISO-8601 timestamps
val timestamp = EventBuilder.getCurrentTimestamp()  // Instant.now().toString()
```

### Smartico CRM Required Fields

Events sent to Smartico must include these fields:

```kotlin
data class SmarticoEventPayload(
    val userExtId: String,        // player.id
    val extBrandId: String,       // brandId from config
    val dtUpdate: String,         // ISO-8601 timestamp
    val coreAccountStatus: String // Mapped via SmarticoStatusMapper
)
```

---

## Topic Naming Convention

Format: `casino.{domain}.{action}.{version}`

| Domain | Examples |
|--------|----------|
| player | `casino.player.registered.v1`, `casino.player.status-changed.v1` |
| payment | `casino.payment.deposit-completed.v1`, `casino.payment.withdrawal-created.v1` |
| game | `casino.game.bet-placed.v1`, `casino.game.round-completed.v1` |
| bonus | `casino.bonus.activated.v1`, `casino.bonus.wagering-updated.v1` |
| compliance | `casino.compliance.kyc-approved.v1`, `casino.compliance.self-excluded.v1` |
| sports | `casino.sports.bet-placed.v1`, `casino.sports.bet-settled.v1` |

See `KafkaTopics.kt` for complete list.