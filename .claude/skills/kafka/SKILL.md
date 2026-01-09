---
name: kafka
description: |
  Apache Kafka event publishing with circuit breaker, failure recovery, and Smartico CRM integration.
  Use when: publishing domain events, consuming messages, handling event failures, or integrating with Smartico.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Kafka Skill

This project uses **Apache Kafka** (Confluent Cloud) for event-driven architecture with zero data loss guarantees. The implementation features a resilient async publisher with circuit breaker protection, automatic retry with exponential backoff, and dead letter queue handling.

**Key Architecture Decision:** Events never break the main business flow. All publishing is fire-and-forget with database-backed failure storage for automatic retry.

## Quick Start

### Fire-and-Forget Publishing (Recommended)

```kotlin
@Service
class PlayerService(
    private val playerEventService: PlayerEventService
) {
    fun registerPlayer(player: Player) {
        // Business logic completes regardless of Kafka state
        playerEventService.publishPlayerRegistered(player)
    }
}
```

### Publishing with Confirmation

```kotlin
eventPublisher.publishAsync(topic, key, event)
    .thenAccept { result ->
        logger.info("Published: partition={}, offset={}", 
            result.recordMetadata.partition(),
            result.recordMetadata.offset())
    }
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Topics | Versioned domain events | `casino.player.registered.v1` |
| Keys | Partition routing (userId) | `player.id.toString()` |
| Circuit Breaker | Fail-fast when Kafka down | 50% failure threshold |
| Failed Events | Database-backed retry | `failed_kafka_events` table |
| DLQ | Final failure destination | `{topic}.dlq` suffix |

## Common Patterns

### Creating a New Event Service

**When:** Adding event publishing for a new domain

```kotlin
@Service
class PaymentEventService(
    private val eventPublisher: EventPublisher,
    private val metadataBuilder: EventMetadataBuilder
) {
    fun publishDepositCompleted(deposit: Deposit) {
        try {
            val event = DepositEvent(
                eventId = EventBuilder.generateEventId(),
                eventTimestamp = EventBuilder.getCurrentTimestamp(),
                brandId = brandId,
                userId = deposit.playerId.toString(),
                metadata = metadataBuilder.build(),
                payload = DepositPayload(...)
            )
            eventPublisher.publish(
                topic = KafkaTopics.PAYMENT_DEPOSIT_COMPLETED,
                key = deposit.playerId.toString(),
                event = event
            )
        } catch (e: Exception) {
            logger.error("Failed to publish deposit event", e)
            // NEVER throw - event publishing must not break main flow
        }
    }
}
```

### Adding a New Topic

**When:** Introducing a new event type

```kotlin
// In KafkaTopics.kt
object KafkaTopics {
    // New topic (follow naming: casino.{domain}.{action}.v{version})
    const val LOYALTY_TIER_UPGRADED = "casino.loyalty.tier-upgraded.v1"
}
```

## See Also

- [patterns](references/patterns.md) - Publishing patterns, event design, error handling
- [workflows](references/workflows.md) - Retry mechanism, monitoring, troubleshooting

## Related Skills

- See the **spring-boot** skill for service layer patterns and configuration
- See the **kotlin** skill for Kotlin-specific syntax and patterns
- See the **jpa** skill for the `FailedKafkaEvent` entity and repository patterns
- See the **postgresql** skill for the `failed_kafka_events` migration