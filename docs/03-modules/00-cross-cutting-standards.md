# Cross-Cutting Standards

These standards apply to all modules.

## Data and persistence

- IDs use BIGSERIAL (PostgreSQL) and Long (Kotlin).
- Monetary values use BigDecimal from String (no double).
- Dates use TIMESTAMP WITH TIME ZONE (UTC).

## API and DTOs

- Controllers are annotated with @RestController and versioned paths.
- DTOs are used for request/response payloads.
- Validation via Jakarta validation annotations.

## Security

- JWT bearer auth for API requests.
- Never store passwords unhashed (BCrypt/Argon2).
- Parameterized queries only (JPA).

## Caching

- Multi-level caching: Caffeine (L1) + Redis (L2).
- Cache keys standardized via CacheKeyGenerator.

## Eventing

- Kafka topics defined in KafkaTopics.kt.
- Failed events stored for retry and DLQ routing.
