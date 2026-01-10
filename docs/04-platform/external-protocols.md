# External Provider Communication Protocols (Code-Derived)

This document lists external provider integrations and the concrete protocols implemented in code.

## Summary Table

| Integration | Direction | Auth | Transport | Code Reference |
| --- | --- | --- | --- | --- |
| Game Provider Wallet API | Inbound | X-Operator-Id + X-Authorization + request hash | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/controller/ProviderCallbackController.kt` |
| Game Provider Callbacks | Inbound | None in controller (provider-level auth not enforced) | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/controller/GameCallbackController.kt` |
| Legacy Game Provider Callbacks | Inbound | None in controller (provider-level auth not enforced) | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/controller/LegacyGameCallbackController.kt` |
| Operator / Platform API | Outbound | SHA1 + X-Operator-Id | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/service/ApiHttpClient.kt` |
| Campaigns API (Free Spins) | Outbound | SHA1 + X-Operator-Id | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/campaigns/client/CampaignsApiClient.kt` |
| Payment Provider (Cashier) | Outbound + Inbound | Bearer token + webhook signature | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/service/PaymentProviderService.kt` |
| Payment Webhook (Legacy) | Inbound | None in controller | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/controller/PaymentWebhookController.kt` |
| Payment Balance (Legacy) | Inbound | None in controller | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/controller/PaymentWebhookController.kt` |
| Smartico CRM | Inbound + Kafka | API key header + Kafka events | HTTP JSON + Kafka | `casino-b/src/main/kotlin/com/casino/core/controller/integration/SmarticoController.kt` |
| Cellxpert Affiliate | Inbound | API key header (SHA-256 hash) | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/controller/CellxpertController.kt` |
| BetBy Sports API | Inbound | JWT payload | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByController.kt` |
| BetBy External API | Outbound | JWT payload + X-BRAND-ID | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/sports/client/BetByExternalApiClient.kt` |
| GeoLocation | Outbound | Public API | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/service/GeoLocationService.kt` |
| Currency Exchange | Outbound | Public API | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/service/CurrencyExchangeService.kt` |
| Email (SendGrid) | Outbound | SendGrid API key | HTTP JSON | `casino-b/src/main/kotlin/com/casino/core/service/EmailService.kt` |
| SMS (Twilio) | Outbound | Twilio credentials | HTTP API | `casino-b/src/main/kotlin/com/casino/core/service/sms/TwilioSmsProvider.kt` |
| AI Providers | Outbound | API keys | HTTP JSON / SDK | `casino-b/src/main/kotlin/com/casino/core/service/ai/*.kt` |
| OpenSearch | Outbound | HTTP client | HTTP | `casino-b/src/main/kotlin/com/casino/core/config/OpenSearchConfig.kt` |

## Game Provider Wallet API (Inbound)

Endpoints:
- `POST /api/v1/provider/{provider}/authenticate`
- `POST /api/v1/provider/{provider}/balance`
- `POST /api/v1/provider/{provider}/changebalance`
- `POST /api/v1/provider/{provider}/status`
- `POST /api/v1/provider/{provider}/cancel`
- `POST /api/v1/provider/{provider}/finishround`
- `GET  /api/v1/provider/{provider}/ping`

Request wrapper (all commands):
- `ProviderApiRequest<T>` with `command`, `request_timestamp`, `hash`, `data`

Headers:
- `X-Operator-Id` must match configured operator id.
- `X-Authorization` must match SHA1 of command with secret (see below).

Hashing rules in `ProviderSecurityService`:
- Authorization hash: `SHA1(command + secretKey)` in the current controller path.
- A `SHA1(command + operatorId + secretKey)` variant exists but is not used by `ProviderCallbackController`.
- Request hash: `SHA1(command + request_timestamp + secretKey)`
- Response hash: `SHA1(status + response_timestamp + secretKey)`

Security note:
- `validateAuthorizationHeader()` and `validateRequestHash()` log mismatches but return `true`. Only header presence and operatorId match are enforced.

Key payloads:
- `ProviderChangeBalanceRequestData` includes `token`, `user_id`, `transaction_type`, `transaction_id`, `round_id`, `round_finished`, `game_id`, `currency_code`, `amount`, `transaction_timestamp`, `context`.
- `context` may include `campaign_code` and `reason` (used for PROMO-FREESPIN).

## Game Provider Callbacks (Inbound)

Endpoints in `GameCallbackController`:
- `POST /api/callbacks/game-round`
- `POST /api/callbacks/balance`
- `POST /api/callbacks/error`
- `POST /api/callbacks/jackpot`
- `POST /api/callbacks/session-recovery`
- `POST /api/callbacks/session-transfer`
- `GET  /api/callbacks/ping`

Payloads in `GameCallbackDto.kt`:
- `GameResultRequest`, `BalanceUpdateRequest`, `GameErrorRequest`, `JackpotWinRequest`, `SessionRecoveryRequest`, `SessionTransferRequest`.

### GameResultRequest

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string | required |
| gameId | string | required |
| roundId | string? | optional |
| playerId | number? | optional |
| betAmount | number | required, positive |
| winAmount | number | required |
| currency | string | required |
| roundStartTime | string? | optional (ISO date-time) |
| roundEndTime | string? | optional (ISO date-time) |
| roundStatus | string | default "COMPLETED" |
| gameData | object? | optional |
| providerTransactionId | string? | optional |
| deviceInfo | string? | optional |
| additionalInfo | object? | optional |

### GameResultResponse

| Field | Type | Notes |
| --- | --- | --- |
| transactionId | string | internal transaction id |
| sessionId | string | session id |
| status | string | OK/ERROR (service-defined) |
| balance | number | current balance |
| timestamp | string | ISO date-time |
| message | string? | optional |
| additionalData | object? | optional |

### BalanceUpdateRequest

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string | required |
| gameId | string | required |
| playerId | number? | optional |
| amount | number | required |
| currency | string | required |
| transactionType | string | required |
| roundId | string? | optional |
| providerTransactionId | string? | optional |
| reason | string? | optional |
| deviceInfo | string? | optional |

### BalanceUpdateResponse

| Field | Type | Notes |
| --- | --- | --- |
| transactionId | string | internal transaction id |
| sessionId | string | session id |
| balanceBefore | number | balance before update |
| balanceAfter | number | balance after update |
| status | string | OK/ERROR (service-defined) |
| timestamp | string | ISO date-time |
| message | string? | optional |

### GameErrorRequest

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string? | optional |
| gameId | string? | optional |
| playerId | number? | optional |
| errorCode | string | required |
| errorMessage | string? | optional |
| errorData | object? | optional |
| roundId | string? | optional |
| deviceInfo | string? | optional |
| severity | string | default "ERROR" |

### JackpotWinRequest

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string | required |
| gameId | string | required |
| playerId | number? | optional |
| amount | number | required, positive |
| currency | string | required |
| jackpotType | string | required |
| roundId | string? | optional |
| providerTransactionId | string? | optional |
| jackpotId | string? | optional |
| jackpotLevel | string? | optional |
| deviceInfo | string? | optional |

### JackpotWinResponse

| Field | Type | Notes |
| --- | --- | --- |
| transactionId | string | internal transaction id |
| sessionId | string | session id |
| jackpotType | string | jackpot type |
| amount | number | jackpot amount |
| newBalance | number | balance after credit |
| status | string | OK/ERROR (service-defined) |
| timestamp | string | ISO date-time |
| message | string? | optional |

### SessionRecoveryRequest

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string | required |
| playerId | number? | optional |
| deviceId | string? | optional |
| deviceInfo | string? | optional |
| browserInfo | string? | optional |
| ipAddress | string? | optional |

### SessionRecoveryResponse

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string | session id |
| status | string | OK/ERROR (service-defined) |
| gameState | string? | optional |
| balance | number | current balance |
| lastRoundId | string? | optional |
| recoveryToken | string | recovery token |
| resumeUrl | string? | optional |
| timestamp | string | ISO date-time |
| expiresAt | string | ISO date-time |

### SessionTransferRequest

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string | required |
| playerId | number? | optional |
| newDeviceId | string | required |
| previousDeviceId | string? | optional |
| deviceInfo | string? | optional |
| browserInfo | string? | optional |
| ipAddress | string? | optional |

### SessionTransferResponse

| Field | Type | Notes |
| --- | --- | --- |
| sessionId | string | session id |
| status | string | OK/ERROR (service-defined) |
| transferToken | string | transfer token |
| resumeUrl | string | resume URL |
| gameState | string? | optional |
| balance | number | current balance |
| timestamp | string | ISO date-time |
| expiresAt | string | ISO date-time |

## Legacy Game Provider Callbacks (Inbound)

Base path: `/api/callbacks/legacy`

Endpoints:
- `POST /game-round`
- `POST /balance`
- `POST /error`
- `POST /jackpot`

Payloads:
- All endpoints accept `Map<String, Any>` and are handled by `GameLaunchService` as legacy formats.

## Operator / Platform API (Outbound)

There are two outbound patterns implemented in `ApiHttpClient`:

1) Operator API (command-based POST):
- Body contains `command`, `request_timestamp`, `hash`, and `data`.
- `hash = SHA1(command + request_timestamp + dataString + secretKey)` via `HashUtil`.
- Headers: `X-Operator-Id`, `X-Authorization = secretKey`.

2) Platform API (game list/reporting):
- Auth header: `X-Authorization = SHA1(operation + operatorId + secretKey)`.
- Header: `X-Operator-Id = operatorId`.
- Optional `X-Vendor-Id` for hand history requests.

Code references:
- `casino-b/src/main/kotlin/com/casino/core/service/ApiHttpClient.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/PlatformApiService.kt`
- `casino-b/src/main/kotlin/com/casino/core/config/OperatorApiConfig.kt`

## Campaigns API (Outbound)

Purpose: Free spins campaign management with external PLATFORM.

Auth headers added by `CampaignsApiRestTemplateConfig`:
- `X-Authorization = SHA1("campaigns" + operatorId + secretKey)`
- `X-Operator-Id = operatorId`

Endpoints (base path is configured):
- `/api/generic/campaigns/vendors`
- `/api/generic/campaigns/vendors/limits`
- `/api/generic/campaigns/list`
- `/api/generic/campaigns/{campaign_code}`
- `/api/generic/campaigns/create`
- `/api/generic/campaigns/cancel`
- `/api/generic/campaigns/players/add`
- `/api/generic/campaigns/players/remove`

Resilience:
- Circuit breaker and retry via Resilience4j and `RetryTemplate`.

## Payment Provider (Cashier) - Outbound + Inbound

Outbound (initiate session) in `PaymentProviderService`:
- `POST /api/v1/auth/client/login` with `client_id` and `client_secret`
- `POST /api/v1/cashier/initiate-session` with customer info and URLs
- Authorization: Bearer token from login

Inbound webhook in `CashierWebhookController`:
- `POST /api/payment/cashier/hook`
- Headers: `x-webhook-signature`, `x-webhook-request-id`, `x-webhook-timestamp`
- Signature: HMAC-SHA256 over `timestamp + requestId + body` (see `WebhookSignatureService`)
- Signature mismatches are logged, but requests are still processed.

### Cashier Webhook Payload (PaymentWebhookDto)

| Field | Type | Notes |
| --- | --- | --- |
| transactionId | string | required |
| paymentId | string | required |
| customerEmail | string? | optional |
| type | string | PAYMENT (deposit) or PAYOUT (withdrawal) |
| status | string | payment/payout status (see `PaymentWebhookStatus`) |
| amount | number | required |
| currency | string | required |
| customerName | string? | optional |
| billingAddress | string? | optional |
| billingCity | string? | optional |
| billingState | string? | optional |
| billingPostalCode | string? | optional |
| billingCountry | string? | optional |
| errorCode | string? | optional |
| errorMessage | string? | optional |
| cardBrand | string? | optional |
| cardLastFour | string? | optional |
| paymentMethod | string | required |
| paymentProvider | string | required |
| createdAt | string | required (ISO date-time) |
| updatedAt | string | required (ISO date-time) |
| completedAt | string? | optional (ISO date-time) |
| cashierSessionId | string | required |
| eventType | string | event type (e.g., payment.created) |
| eventTimestamp | string | required (ISO date-time) |

## Payment Webhook (Legacy)

Inbound in `PaymentWebhookController`:
- `POST /api/payment/hook` expects `type` in `payment.successful|payment.failed|payment.cancelled`.
- Creates deposit transactions on success.
- `GET /api/payment/player/balance` returns wallet balance for `customerId` (no auth in controller).

### PaymentWebhookData

| Field | Type | Notes |
| --- | --- | --- |
| type | string | `payment.successful` / `payment.failed` / `payment.cancelled` |
| sessionId | string? | optional |
| transactionId | string? | optional |
| customerId | string? | optional (player id as string) |
| amount | string? | optional (decimal string) |
| currency | string? | optional |
| paymentMethod | string? | optional |
| paymentProviderId | string? | optional |
| status | string? | optional |
| failureReason | string? | optional |
| timestamp | string? | optional (ISO date-time) |
| metadata | object? | optional |

### PaymentWebhookResponse

| Field | Type | Notes |
| --- | --- | --- |
| status | string | success/error |
| message | string | human-readable |

### PlayerBalanceResponse

| Field | Type | Notes |
| --- | --- | --- |
| customerId | string | requested customer id |
| balance | string | balance as string |
| currency | string | wallet currency |

## Smartico CRM

Inbound HTTP:
- `/api/v1/smartico/bonuses/active`
- `/api/v1/smartico/bonuses/activate`
- API key header: `X-Smartico-API-Key` validated in `ApiKeyAuthenticationFilter`.

Outbound to Smartico (via Kafka):
- Player events, payment events, game events, sports events.
- Topics under `casino.*` are published for CRM consumption.

## Cellxpert Affiliate

Inbound HTTP:
- `/api/v1/cellxpert/players`
- `/api/v1/cellxpert/transactions`
- `/api/v1/cellxpert/activities`

Auth:
- API key header `X-Cellxpert-API-Key`, validated by SHA-256 hash stored in DB.

## BetBy Sports API (Inbound)

Endpoints:
- `/api/v1/sport/betby/ping`
- `/api/v1/sport/betby/bet/make|bet_make`
- `/api/v1/sport/betby/bet/win|bet_win`
- `/api/v1/sport/betby/bet/lost|bet_lost`
- `/api/v1/sport/betby/bet/refund|bet_refund`
- `/api/v1/sport/betby/bet/discard|bet_discard`
- `/api/v1/sport/betby/bet/rollback|bet_rollback`
- `/api/v1/sport/betby/bet/commit|bet_commit`
- `/api/v1/sport/betby/bet/settlement|bet_settlement`

Payload:
- Body contains `{ payload: "<jwt>" }` which is parsed/verified by `BetByJwtService` (JWT is signed, not encrypted).

## BetBy External API (Outbound)

Protocol:
- Header: `X-BRAND-ID`
- Body: `{ "payload": "<jwt>" }`
- JWT contains `iss`, `aud`, `iat`, `exp`, `nbf`, `payload`.

Endpoints:
- `/api/v1/external_api/ping`
- `/api/v1/external_api/player/details`
- `/api/v1/external_api/player/segment`
- `/api/v1/external_api/bonus/templates`
- `/api/v1/external_api/bonus/template`
- `/api/v1/external_api/bonus/player_bonuses`
- `/api/v1/external_api/bonus/bonus`
- `/api/v1/external_api/bonus/mass_give_bonus`
- `/api/v1/external_api/bonus/revoke_bonus`

## GeoLocation

Outbound API calls:
- `https://ipapi.co/{ip}/json/`
- `https://ipinfo.io/{ip}/json`

Cache:
- In-memory cache with 60 minute TTL, fallback to mock data for private IPs.

## Currency Exchange

Outbound API:
- `https://api.frankfurter.app`

Features:
- Cached latest rates, fallback rates when API unavailable.

## Email and SMS

Email:
- SendGrid via `EmailService` using `sendgrid.api-key`.

SMS:
- Twilio via `TwilioSmsProvider` with `account-sid`, `auth-token`, `phone-number`.

## AI Providers

- Claude via Anthropic SDK (`ClaudeAIProvider`).
- Gemini via HTTP (`GeminiAIProvider`).

## OpenSearch

- Configured via `OpenSearchConfig` with Apache HTTP transport.
