# Kafka Workflows

## Event Flow Architecture

```
Service → EventService → ResilientAsyncEventPublisher → Circuit Breaker → Kafka
                                    ↓ (on failure)
                         FailedKafkaEvent (DB) → FailedEventRetryService → DLQ
```

## Retry Mechanism Workflow

### How Automatic Retry Works

1. **Initial Failure**: Publisher fails → Event stored in `failed_kafka_events` table
2. **Exponential Backoff**: Retry scheduled with increasing delays
3. **Scheduled Job**: `FailedEventRetryService` runs every 60 seconds
4. **Success**: Event published → marked `RESOLVED`
5. **Max Retries Exceeded**: Event sent to Dead Letter Queue

### Retry Schedule

| Attempt | Delay | Cumulative Wait |
|---------|-------|-----------------|
| 1 | 1 minute | 1 minute |
| 2 | 5 minutes | 6 minutes |
| 3 | 15 minutes | 21 minutes |
| 4+ | 60 minutes | ~1.5 hours |

### Failed Event Statuses

```kotlin
// In FailedKafkaEvent entity
status: String // PENDING → RESOLVED | DLQ | DLQ_FAILED
```

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| `PENDING` | Awaiting retry | Automatic |
| `RESOLVED` | Successfully retried | None |
| `DLQ` | Sent to Dead Letter Queue | Review in DLQ topic |
| `DLQ_FAILED` | **CRITICAL** - DLQ send failed | Manual intervention |

---

## Monitoring Workflow

### Health Check Endpoint

```
GET /actuator/health/kafka
```

Response when healthy:
```json
{
  "status": "UP",
  "details": {
    "circuitBreakerState": "CLOSED",
    "pendingEvents": 0,
    "dlqFailedEvents": 0
  }
}
```

Response when degraded:
```json
{
  "status": "DEGRADED",
  "details": {
    "circuitBreakerState": "OPEN",
    "pendingEvents": 1500,
    "oldestPendingAge": "2 hours"
  }
}
```

### Key Metrics to Monitor

```
kafka.events.published{topic, status}      # Counter: success/error by topic
kafka.publish.latency{topic}               # Timer: publish duration
kafka.events.errors{topic, error_type}     # Counter: errors by type
kafka.circuit_breaker.open{topic}          # Counter: circuit breaker trips
kafka.events.stored_for_retry{topic}       # Counter: events saved to DB
kafka.retry.attempts{topic}                # Counter: retry attempts
kafka.retry.success{topic}                 # Counter: successful retries
kafka.dlq.sent{topic}                      # Counter: events sent to DLQ
```

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| `pending_events` | > 1000 | > 5000 |
| `oldest_pending_age` | > 1 hour | > 4 hours |
| `circuit_breaker_state` | HALF_OPEN | OPEN > 5 min |
| `dlq_failed_count` | > 0 | > 0 (immediate) |

---

## WARNING: Not Monitoring DLQ_FAILED Events

**The Problem:**

```kotlin
// Events stuck in DLQ_FAILED status = data loss risk
val criticalEvents = failedEventRepository.countByStatus("DLQ_FAILED")
// If this is > 0 and nobody notices...
```

**Why This Breaks:**
1. Events that failed to reach DLQ are effectively lost
2. No automatic recovery mechanism exists
3. Compliance/audit issues if critical events disappear

**The Fix:**

```kotlin
// Add monitoring and alerting
@Scheduled(fixedRate = 60000)
fun checkForCriticalFailures() {
    val dlqFailed = failedEventRepository.countByStatus("DLQ_FAILED")
    if (dlqFailed > 0) {
        alertService.sendCriticalAlert(
            "Kafka DLQ_FAILED events detected: $dlqFailed events require manual intervention"
        )
    }
}
```

---

## Troubleshooting Workflow

### Problem: Events Not Publishing

1. **Check circuit breaker state:**
```kotlin
val stats = resilientAsyncEventPublisher.getPublisherStats()
// circuitBreakerState: OPEN means Kafka is down
```

2. **Check thread pool:**
```kotlin
// stats.threadPool.queueSize > 9000 = backpressure
// stats.threadPool.activeCount = 50 = all threads busy
```

3. **Check failed events table:**
```sql
SELECT status, COUNT(*) FROM failed_kafka_events GROUP BY status;
-- PENDING count increasing = Kafka consistently down
```

### Problem: High Latency in Event Publishing

1. **Check batch settings** in `KafkaProducerConfig`:
   - `batch.size`: 32768 (32KB)
   - `linger.ms`: 10ms
   
2. **Check network/Confluent Cloud status**

3. **Check for slow consumers** causing backpressure

### Problem: Events in DLQ

1. **Read DLQ topic:**
```bash
kafka-console-consumer --bootstrap-server $KAFKA_BROKERS \
  --topic casino.player.registered.v1.dlq --from-beginning
```

2. **Analyze failure reasons:**
```sql
SELECT last_error, COUNT(*) 
FROM failed_kafka_events 
WHERE status = 'DLQ'
GROUP BY last_error;
```

3. **Reprocess if needed:** Manual intervention required

---

## Adding New Event Types Workflow

### Step 1: Define Topic Constant

```kotlin
// KafkaTopics.kt
const val LOYALTY_POINTS_EARNED = "casino.loyalty.points-earned.v1"
```

### Step 2: Create Event Classes

```kotlin
// LoyaltyPointsEarnedEvent.kt
class LoyaltyPointsEarnedEvent(
    eventId: String,
    eventTimestamp: String,
    brandId: String,
    userId: String,
    metadata: EventMetadata,
    val payload: LoyaltyPointsEarnedPayload
) : BaseEvent(...)

data class LoyaltyPointsEarnedPayload(
    val points: Int,
    val reason: String,
    val source: String
)
```

### Step 3: Create Event Service

```kotlin
@Service
class LoyaltyEventService(
    private val eventPublisher: EventPublisher,
    private val metadataBuilder: EventMetadataBuilder
) {
    fun publishPointsEarned(player: Player, points: Int, reason: String) {
        try {
            val event = LoyaltyPointsEarnedEvent(...)
            eventPublisher.publish(
                topic = KafkaTopics.LOYALTY_POINTS_EARNED,
                key = player.id.toString(),
                event = event
            )
        } catch (e: Exception) {
            logger.error("Failed to publish loyalty event", e)
        }
    }
}
```

### Step 4: Call from Business Logic

```kotlin
@Service
class LoyaltyService(
    private val loyaltyEventService: LoyaltyEventService
) {
    fun awardPoints(player: Player, points: Int) {
        // Business logic first
        loyaltyRepository.addPoints(player.id, points)
        
        // Then publish event (never blocks or throws)
        loyaltyEventService.publishPointsEarned(player, points, "game_win")
    }
}
```