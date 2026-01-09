---
name: kafka
description: |
  Apache Kafka event publishing with circuit breaker, failure recovery, and Smartico CRM integration.
  Use when: publishing domain events, consuming messages, handling event failures, or integrating with Smartico.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Kafka Skill

This project uses Kafka via Confluent Cloud for event-driven architecture. The primary use case is publishing domain events (player, payment, game, bonus) to Smartico CRM. Key features: resilient async publishing with circuit breaker, automatic failure recovery via database storage, and structured event schema.

**CRITICAL**: Event publishing should NEVER break the main business flow. Always use fire-and-forget pattern and catch exceptions.

## Quick Start

### Publishing Events (Fire-and-Forget)

```kotlin
// GOOD - Non-blocking, resilient publish
@Service
class PlayerService(
    private val playerEventService: PlayerEventService
) {
    fun registerPlayer(player: Player) {
        // Business logic first
        val savedPlayer = repository.save(player)
        
        // Publish event (never blocks, never throws)
        playerEventService.publishPlayerRegistered(savedPlayer)
    }
}
```

### Event Service Pattern

```kotlin
@Service
class MyEventService(
    private val eventPublisher: EventPublisher,  // ResilientAsyncEventPublisher injected
    private val metadataBuilder: EventMetadataBuilder
) {
    fun publishMyEvent(entity: MyEntity) {
        try {
            val event = MyEvent(
                eventId = EventBuilder.generateEventId(),
                eventTimestamp = EventBuilder.getCurrentTimestamp(),
                brandId = brandId,
                userId = entity.playerId.toString(),
                metadata = metadataBuilder.build(entity),
                payload = MyEventPayload(/* ... */)
            )
            
            eventPublisher.publish(
                topic = KafkaTopics.MY_TOPIC,
                key = entity.playerId.toString(),  // Partition key for ordering
                event = event
            )
        } catch (e: Exception) {
            logger.error("Failed to publish event: {}", entity.id, e)
            // DON'T THROW - event failures must not break business logic
        }
    }
}
```

## Key Concepts

| Concept | Usage | Location |
|---------|-------|----------|
| Topic constants | `KafkaTopics.PLAYER_REGISTERED` | `kafka/constants/KafkaTopics.kt` |
| Event base class | Extend `BaseEvent` for all events | `kafka/events/base/BaseEvent.kt` |
| Event builder | `EventBuilder.generateEventId()` | `kafka/events/base/EventBuilder.kt` |
| Publisher | Inject `EventPublisher` interface | `kafka/publisher/EventPublisher.kt` |
| Circuit breaker | Auto-managed, stores failures to DB | `kafka/config/KafkaCircuitBreakerConfig.kt` |
| Failed events | `FailedKafkaEvent` entity | `domain/kafka/FailedKafkaEvent.kt` |

## Event Structure

All events must follow this schema for Smartico CRM compatibility:

```kotlin
data class MyEvent(
    override val eventId: String,          // UUID
    override val eventType: String,        // "casino.domain.action.v1"
    override val eventTimestamp: String,   // ISO-8601 UTC
    override val brandId: String,          // From app.brand-id
    override val userId: String,           // Partition key
    override val metadata: EventMetadata,
    val payload: MyEventPayload
) : BaseEvent(eventId, eventType, eventTimestamp, brandId, userId, metadata)
```

## See Also

- [patterns](references/patterns.md) - Publishing patterns, event structure, anti-patterns
- [workflows](references/workflows.md) - Failure handling, retry mechanism, monitoring

## Related Skills

- See the **kotlin** skill for Kotlin syntax and idioms
- See the **spring-boot** skill for Spring configuration
- See the **jpa** skill for `FailedKafkaEvent` entity patterns