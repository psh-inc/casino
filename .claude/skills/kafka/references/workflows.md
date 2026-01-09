# Kafka Workflows

## Failure Handling & Recovery

### How Failures Are Handled

```
Service → ResilientAsyncEventPublisher → Circuit Breaker → Kafka
                    ↓ (on failure)
            FailedKafkaEvent table → Retry Job (1min) → DLQ (after 3 retries)
```

1. **Circuit Breaker**: Opens after 50% failure rate, prevents cascading failures
2. **Database Storage**: Failed events stored to `failed_kafka_events` table
3. **Automatic Retry**: `FailedEventRetryService` runs every minute
4. **Dead Letter Queue**: After max retries, events go to `{topic}.dlq`

### Circuit Breaker States

| State | Behavior |
|-------|----------|
| CLOSED | Normal operation, all publishes go to Kafka |
| OPEN | Kafka unavailable, events stored to DB immediately |
| HALF_OPEN | Testing recovery, limited requests allowed |

### Exponential Backoff Schedule

```kotlin
// Attempt 0: retry in 1 minute
// Attempt 1: retry in 5 minutes
// Attempt 2: retry in 15 minutes
// Attempt 3+: retry in 60 minutes (then DLQ)
private fun calculateNextRetry(attemptCount: Int): LocalDateTime {
    val delayMinutes = when (attemptCount) {
        0 -> 1L
        1 -> 5L
        2 -> 15L
        else -> 60L
    }
    return LocalDateTime.now().plusMinutes(delayMinutes)
}
```

---

## WARNING: Silent Event Loss

**The Problem:**

```kotlin
// BAD - If storeFailures=false, events disappear
kafka:
  fallback:
    store-failures: false  # DANGEROUS
```

**Why This Breaks:**
1. Events published during Kafka outage are lost permanently
2. No audit trail of what happened
3. Data inconsistency between systems (player exists but Smartico doesn't know)

**The Fix:**

```yaml
# GOOD - Always store failures (default)
kafka:
  fallback:
    store-failures: true
  retry:
    max-attempts: 3
```

---

## WARNING: Not Using Partition Key

**The Problem:**

```kotlin
// BAD - Events for same player may arrive out of order
eventPublisher.publish(
    topic = KafkaTopics.PLAYER_STATUS_CHANGED,
    key = UUID.randomUUID().toString(),  // Random key = random partition
    event = event
)
```

**Why This Breaks:**
1. Events for same player go to different partitions
2. No ordering guarantee: STATUS_CHANGED might arrive before REGISTERED
3. Consumer sees inconsistent state

**The Fix:**

```kotlin
// GOOD - Use player ID as key for ordering
eventPublisher.publish(
    topic = KafkaTopics.PLAYER_STATUS_CHANGED,
    key = player.id.toString(),  // Same player = same partition = ordered
    event = event
)
```

---

## Monitoring & Health Checks

### Publisher Statistics

```kotlin
// Get current publisher state
val stats = resilientAsyncEventPublisher.getPublisherStats()
// Returns: asyncEnabled, storeFailures, circuitBreakerState, threadPool stats
```

### Retry Service Statistics

```kotlin
// Get retry queue status
val retryStats = failedEventRetryService.getRetryStats()
// Returns: pending, resolved, dlq, dlqFailed counts
```

### Key Metrics (Micrometer)

| Metric | Description |
|--------|-------------|
| `kafka.events.published{status=success}` | Successful publishes |
| `kafka.events.published{status=error}` | Failed publishes |
| `kafka.publish.latency` | Publish latency distribution |
| `kafka.circuit_breaker.open` | Circuit breaker open events |
| `kafka.events.stored_for_retry` | Events stored for retry |
| `kafka.retry.success` | Successful retries |
| `kafka.dlq.sent` | Events sent to DLQ |

---

## Consumer Pattern

Basic consumer implementation (see `Consumer.kt`):

```kotlin
@Service
class MyConsumer {
    private val logger = LoggerFactory.getLogger(javaClass)

    @KafkaListener(
        id = "myConsumer",
        topics = ["topic_name"],
        groupId = "springboot-group-1",
        autoStartup = "true"
    )
    fun listen(
        value: String?,
        @Header(KafkaHeaders.RECEIVED_TOPIC) topic: String?,
        @Header(KafkaHeaders.RECEIVED_KEY) key: String?
    ) {
        logger.info("Consumed from {}: key={}, value={}", topic, key, value)
        // Process message...
    }
}
```

---

## Adding New Event Types

### Step 1: Add Topic Constant

```kotlin
// In KafkaTopics.kt
object KafkaTopics {
    const val MY_NEW_EVENT = "casino.domain.my-action.v1"
}
```

### Step 2: Create Event Classes

```kotlin
// In kafka/events/mydomain/MyNewEvent.kt
data class MyNewEvent(
    override val eventId: String,
    override val eventType: String = KafkaTopics.MY_NEW_EVENT,
    override val eventTimestamp: String,
    override val brandId: String,
    override val userId: String,
    override val metadata: EventMetadata,
    val payload: MyNewEventPayload
) : BaseEvent(eventId, eventType, eventTimestamp, eventVersion, brandId, userId, null, metadata)

data class MyNewEventPayload(
    val field1: String,
    val field2: BigDecimal,
    // Smartico required fields
    val userExtId: String,
    val extBrandId: String,
    val dtUpdate: String
)
```

### Step 3: Create Event Service

```kotlin
@Service
class MyDomainEventService(
    private val eventPublisher: EventPublisher,
    private val metadataBuilder: EventMetadataBuilder
) {
    @Value("\${app.brand-id}")
    private lateinit var brandId: String
    
    private val logger = LoggerFactory.getLogger(javaClass)

    fun publishMyNewEvent(entity: MyEntity) {
        try {
            val event = MyNewEvent(
                eventId = EventBuilder.generateEventId(),
                eventTimestamp = EventBuilder.getCurrentTimestamp(),
                brandId = brandId,
                userId = entity.playerId.toString(),
                metadata = metadataBuilder.build(entity),
                payload = MyNewEventPayload(/* ... */)
            )
            
            eventPublisher.publish(KafkaTopics.MY_NEW_EVENT, entity.playerId.toString(), event)
            logger.info("Published MyNewEvent for entity: {}", entity.id)
        } catch (e: Exception) {
            logger.error("Failed to publish MyNewEvent: {}", entity.id, e)
        }
    }
}
```

---

## Testing Kafka Events

For unit tests, mock the `EventPublisher` interface. See the **spring-boot** skill for MockK patterns.

```kotlin
@Test
fun `should publish player registered event`() {
    val eventPublisher = mockk<EventPublisher>(relaxed = true)
    val service = PlayerEventService(eventPublisher, metadataBuilder)
    
    service.publishPlayerRegistered(testPlayer)
    
    verify { 
        eventPublisher.publish(
            topic = KafkaTopics.PLAYER_REGISTERED,
            key = testPlayer.id.toString(),
            event = any<PlayerRegisteredEvent>()
        )
    }
}
```