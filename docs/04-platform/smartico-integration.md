# Smartico Integration (HTTP + CRM Context)

This document covers Smartico integration endpoints and how Smartico is wired in the backend. For Kafka event schemas and topics, see `smartico-kafka-events.md`.

## Source Files

HTTP endpoints:
- `casino-b/src/main/kotlin/com/casino/core/controller/integration/SmarticoController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/integration/SmarticoIntegrationController.kt`

Security:
- `casino-b/src/main/kotlin/com/casino/core/security/ApiKeyAuthenticationFilter.kt`
- `casino-b/src/main/kotlin/com/casino/core/security/SecurityConfig.kt`

Business logic:
- `casino-b/src/main/kotlin/com/casino/core/service/BonusService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/cache/InMemoryGameCache.kt`

Kafka event publishing:
- `casino-b/src/main/kotlin/com/casino/core/kafka/*`

## Authentication

Smartico endpoints require an API key:
- Header: `X-Smartico-API-Key` (checked in `ApiKeyAuthenticationFilter`).
- Key value is loaded from `smartico.api-key` configuration.

The filter sets an authenticated principal with `ROLE_API` for Smartico requests.

## Smartico Bonus Endpoints

Base path: `/api/v1/smartico`

### GET /bonuses/active
- Returns a list of active bonuses with `bonusId` and `bonusName`.
- Data source: `BonusService.findActiveBonuses()`.

### POST /bonuses/activate
- Body: `ActivateBonusRequest` (bonusId, userId, amount).
- Delegates to `BonusService.activateBonusForSmartivo`.

Business rules from code:
- Zero-wagering bonuses are credited to real balance (withdrawable).
- Wagering bonuses are created as bonus balance with wagering tracking.
- Only ONE active wagering bonus per player.
- Zero-wagering bonuses can be activated even if a wagering bonus is active.

Errors:
- `ValidationException` -> `ACTIVE_BONUS_CONFLICT` (409) or `VALIDATION_ERROR` (400).
- `NotFoundException` -> 404.
- Generic errors -> 500.

### Bonus Schemas (Code-Derived)

#### ActivateBonusRequest

| Field | Type | Notes |
| --- | --- | --- |
| bonusId | number | required |
| userId | number | required |
| amount | number | required, > 0 |

#### ActivateBonusResponse

| Field | Type | Notes |
| --- | --- | --- |
| success | boolean | true on success |
| message | string | human-readable |
| awardId | number? | bonus award id |
| playerId | number | player id |
| bonusId | number | bonus id |
| bonusName | string | bonus name |
| awardedAmount | number | amount awarded |
| currency | string | currency code |
| wageringRequirement | number? | optional |
| expiresAt | string? | ISO date-time |
| depositedToRealBalance | boolean | true for zero-wagering bonuses |

#### ActiveBonusListResponse

| Field | Type | Notes |
| --- | --- | --- |
| bonuses | array | list of SimpleBonusInfo |

#### SimpleBonusInfo

| Field | Type | Notes |
| --- | --- | --- |
| bonusId | number | bonus id |
| bonusName | string | bonus name |

#### ErrorResponse

| Field | Type | Notes |
| --- | --- | --- |
| success | boolean | false |
| message | string | error message |
| error | string | error code |

## Smartico Games Endpoint

Base path: `/api/v1/integration/smartico`

### GET /games
- Returns all games from `InMemoryGameCache` mapped to Smartico format.
- Includes provider info and game categories.
- Builds front-end link as `${spring.frontend.url}/game/{gameId}`.
- Returns empty list if cache not loaded.
- Adds cache headers (`Cache-Control: public, max-age=600`) and response metadata headers.

### Game Schema (Code-Derived)

#### SmarticoGameResponse

| Field | Type | Notes |
| --- | --- | --- |
| id | string | game id |
| name | string | game name |
| link | string | frontend URL |
| image | string? | thumbnail URL |
| enabled | boolean | true for active games |
| game_categories | array | list of SmarticoGameCategoryResponse |
| game_provider | string | provider/vendor name |
| game_provider_id | number? | vendor id |

#### SmarticoGameCategoryResponse

| Field | Type | Notes |
| --- | --- | --- |
| id | number | category id |
| name | string | category name |

## CRM Event Publishing (Overview)

Smartico CRM integration uses Kafka topics defined in `KafkaTopics` and events under `com.casino.core.kafka.events.*`.
Events are published by domain services:
- Player events: `PlayerEventService`
- Payment events: `PaymentEventService`
- Game events: `GameEventService`
- Bonus events: `BonusEventService`
- Sports events: `SportsEventService`
- Compliance events: `ComplianceEventService`
- Engagement events: `EngagementEventService`

See `smartico-kafka-events.md` for full topic list and payload schemas.
