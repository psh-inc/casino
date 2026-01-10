# BetBy Sports Betting Integration

This document covers the BetBy sportsbook integration in `casino-b`. It includes inbound BetBy API callbacks, wallet operations for players, and outbound BetBy External API calls. All details are derived from code.

## Source Files

Inbound BetBy API:
- `casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByController.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/service/BetByApiService.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/validation/BetByRequestValidator.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/dto/request/*`
- `casino-b/src/main/kotlin/com/casino/core/sports/dto/response/*`

BetBy wallet for authenticated players:
- `casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByWalletController.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/service/BetByWalletService.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/service/BetByTransactionService.kt`

BetBy JWT and crypto:
- `casino-b/src/main/kotlin/com/casino/core/sports/service/BetByJwtService.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/service/BetByPartnerJwtService.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/config/BetByIntegrationConfig.kt`

External API (outbound):
- `casino-b/src/main/kotlin/com/casino/core/sports/client/BetByExternalApiClient.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/service/BetByExternalApiIntegrationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/sports/config/BetByExternalApiResilienceConfig.kt`

## Inbound BetBy API (Webhook-Style)

Base path: `/api/v1/sport/betby`

Endpoints (each accepts `{ "payload": "<jwt>" }`):
- `GET /ping` -> returns `{"timestamp": <unix>}`
- `POST /bet/make` and `/bet_make` -> BET_MAKE
- `POST /bet/win` and `/bet_win` -> BET_WIN
- `POST /bet/lost` and `/bet_lost` -> BET_LOST
- `POST /bet/refund` and `/bet_refund` -> BET_REFUND
- `POST /bet/discard` and `/bet_discard` -> BET_DISCARD
- `POST /bet/rollback` and `/bet_rollback` -> BET_ROLLBACK
- `POST /bet/commit` and `/bet_commit` -> BET_COMMIT
- `POST /bet/settlement` and `/bet_settlement` -> BET_SETTLEMENT
- `POST /player-segment` and `/player_segment` -> PLAYER_SEGMENT
- `POST /status` -> STATUS

### Authentication and Payload Encryption

Incoming requests contain a JWT string in `payload`. The service decrypts and parses the payload with `BetByJwtService`:
- Private key loaded from `betby.private-key-path` (EC or RSA PEM).
- ES256 tokens are verified with the private key.
- RS256 tokens are parsed without signature verification (payload is decoded directly).

This means the integration accepts RS256 payloads without signature verification in current code.

### Request Validation

`BetByRequestValidator` enforces:
- Supported currencies: USD, EUR, GBP, CAD, AUD.
- Amount bounds: min 0.01 (positive bets), max 100000.
- Maximum selections per bet: 20.
- Max transaction id length: 100.

### Amount Units

All monetary amounts from BetBy requests are in subunits.
`CurrencySubunitConverter` converts subunits to `BigDecimal` and back for responses.

### Core Business Logic (BetByApiService)

- Idempotency: Transactions are checked by `BetByTransactionService` before processing.
- Player validation: player must exist before funds are deducted.
- Bonus handling:
  - Standard bonus bets (FREEBET_REFUND, FREEBET_FREEMONEY, COMBOBOOST): no wallet debit.
  - NO_RISK bonus bets: real money is debited, but funds can be refunded if bet loses.
  - Bonus processing uses `BetByBonusService` and records usage for analytics.
- Wallet handling:
  - Real money bets call `BetByWalletService.deductBetAmount`.
  - Wins and refunds credit the wallet.
- Sports bet persistence:
  - `BetBySportsBetService` creates `SportsBet` records for history.
- CRM event publishing:
  - `SportsEventService` publishes `SportsBetPlacedEvent` and `SportsBetSettledEvent` for Smartico.

### Settlement and Rollback

- BET_SETTLEMENT can credit wins or process refunds based on status.
- BET_ROLLBACK reverses prior transactions.
- BET_DISCARD and BET_COMMIT support two-phase betting flows.

## BetBy Wallet API (Customer Auth)

Base path: `/api/v1/sports/wallet`

Endpoints:
- `GET /balance` -> returns real + bonus balances.
- `GET /balance/check` -> checks if a bet amount is affordable.
- `GET /transactions` -> paginated history.
- `GET /transactions/stats` -> summary statistics.
- `POST /reserve` -> optional fund reservation (60s TTL).
- `POST /release/{reservationId}` -> release reservation.

Implementation detail:
- `BetByWalletController.extractPlayerId` derives playerId from username hash as a placeholder. This may be replaced with real mapping from auth user to player id.

## BetBy External API (Outbound)

External API calls use `BetByExternalApiClient`:
- Requests are sent as `{ "payload": "<jwt>" }`.
- JWT is signed by `BetByPartnerJwtService` using configured private key.
- Headers include `X-BRAND-ID`.

External API endpoints supported:
1. `GET /api/v1/external_api/ping`
2. `POST /api/v1/external_api/player/details`
3. `POST /api/v1/external_api/player/segment`
4. `POST /api/v1/external_api/bonus/templates`
5. `POST /api/v1/external_api/bonus/template`
6. `POST /api/v1/external_api/bonus/player_bonuses`
7. `POST /api/v1/external_api/bonus/bonus`
8. `POST /api/v1/external_api/bonus/mass_give_bonus`
9. `POST /api/v1/external_api/bonus/revoke_bonus`

Resilience:
- Circuit breaker + retry configured in `BetByExternalApiResilienceConfig`.
- Failure thresholds, backoff, and open state timing are configurable.

Caching:
- Bonus templates cached for 1 hour.
- Player segments and player bonuses cached for 5 minutes.

## Player Segment Sync

`PlayerSegmentSyncService` updates `Player.sportsSegmentName` and `sportsCcfScore`:
- Webhook segment updates are applied unless the player has a manual override.
- Sync can also pull segment data from the external API.
- Segment changes are logged in `SportsPlayerSegmentHistory`.

## Configuration Keys (Code Defaults)

From `BetByIntegrationConfig` and services:
- `betby.api.url` (default `https://api.betby.com`)
- `betby.api.key`, `betby.api.secret`
- `betby.operator.id`, `betby.operator.brand.id`
- `betby.brand-id`
- `betby.private-key-path`
- `betby.external-api.url` (default `https://external-api.invisiblesport.com`)
- External API JWT algorithm via `betby.external-api.jwt-alg` (RS256 or ES256)
