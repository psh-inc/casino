# Game Provider Integration (Wallet Callbacks + Sync)

This document describes the external game provider integration layer in `casino-b`.
All details are derived from code.

## Source Files

Provider wallet callbacks and security:
- `casino-b/src/main/kotlin/com/casino/core/controller/ProviderCallbackController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderResponseService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderSecurityService.kt`
- `casino-b/src/main/kotlin/com/casino/core/dto/provider/*`
- `casino-b/src/main/kotlin/com/casino/core/filter/GameCallbackLoggingFilter.kt`

Provider management and sync:
- `casino-b/src/main/kotlin/com/casino/core/controller/GameProviderController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/GameProviderSyncController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameProviderService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameProviderSyncService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/sync/*`
- `casino-b/src/main/kotlin/com/casino/core/domain/GameProvider*.kt`

## Callback API Surface

Base path: `/api/v1/provider/{provider}`

Endpoints:
- `POST /authenticate`
- `POST /balance`
- `POST /changebalance`
- `POST /status`
- `POST /cancel`
- `POST /finishround`
- `GET  /ping`

### Request Envelope

All POST endpoints use a wrapper:

- `ProviderApiRequest<T>`
  - `command`
  - `request_timestamp`
  - `hash`
  - `data` (request body specific to endpoint)

Command must match the endpoint name (for example `authenticate`, `balance`, `changebalance`, etc).

### Response Envelope

All responses use `ProviderApiResponse` with a nested `ProviderResponsePayload`:

- `status`: `OK` or `ERROR`
- `response_timestamp`
- `hash`
- `data`: success payload or `ProviderErrorData` (error_code + error_message)

### Headers and Security

Required headers (per code checks in `ProviderCallbackController`):
- `X-Operator-Id` must match configured operator id.
- `X-Authorization` must match expected hash for the command.

Hash logic (see `ProviderSecurityService`):
- `X-Authorization`: SHA1(command + secretKey) or SHA1(command + operatorId + secretKey) depending on `includeOperatorId`.
- Request body `hash`: SHA1(command + request_timestamp + secretKey).
- Response hash: SHA1(status + response_timestamp + secretKey).

Implementation detail from code:
- `ProviderSecurityService.validateAuthorizationHeader` and `validateRequestHash` currently return `true` unconditionally (TODO markers). This means header and body hashes are logged but not enforced at runtime.

## Business Logic by Endpoint

### Authenticate
- Input: `ProviderAuthenticateRequestData(token)`.
- Flow:
  - Fetch game session by token from `GameSessionCacheService`.
  - Validate session is active.
  - Fetch player from `PlayerCacheService`.
  - Reject if player blocked or session invalidated.
  - Balance = real wallet + playable bonus balance.
  - Country is taken from player's primary address; defaults to `XX` if missing.
- Output: `ProviderAuthenticateResponseData` (userId, username, country, displayName, currency, balance).

### Balance
- Input: `ProviderBalanceRequestData(token, user_id, currency_code)`.
- Flow:
  - Validate playerId and currency match.
  - Token is mandatory; validates active session in cache.
  - Balance = real wallet + playable bonus balance.
- Output: `ProviderBalanceResponseData`.

### Change Balance
- Input: `ProviderChangeBalanceRequestData` (transaction_id, round_id, game_id, amount, transaction_type, currency, token, context).
- Idempotency:
  - The combination of `transaction_id` + `providerName` is stored in `ProviderTransaction`.
  - If transaction already exists and the `requestHash` matches, the existing balance is returned.
  - Same transaction id with different data returns error `OP_40`.

Common validations:
- Player exists and not blocked (WIN transactions bypass blocking to avoid stuck payouts).
- Currency matches wallet currency.
- BET requires active session unless it is a promotional free spin.
- WIN/REFUND can be processed without an active session.

Transaction types:
- `BET`:
  - Rejects zero or negative amount.
  - Rejects if game disabled or restricted by active bonuses (unless free spin).
  - Enforces bet limits and session time limits (`BetLimitValidationService`).
  - Splits bet into real + bonus portions, always using real money first.
  - Blocks buy-feature bets that attempt to use bonus funds.
  - Enforces bonus max bet limit for bonus-funded bets.
  - Creates/updates `GameRound` with bet split.
  - Debits real wallet and bonus balance (if needed).
  - Updates deposit wagering progress when eligible.
  - Updates bonus wagering progress based on wagering mode and game contribution factor.
  - Records bet for cumulative bet limit tracking.

- `WIN`:
  - Creates or finds `GameRound` and marks it completed when needed.
  - Uses proportional win distribution based on stored bet split (real vs bonus).
  - Credits real wallet and/or bonus balance accordingly, with fallback to real if bonus credit fails.
  - Triggers wagering completion checks.

- `REFUND`:
  - Credits real wallet (positive amount).
  - If game round exists, marks it as VOIDED.

Free spin handling:
- Free spin transactions are detected by `GameRound.betType` or PROMO-FREESPIN context.
- Free spin BETs do not debit wallet; they create `FREE_SPIN_BET` transactions with zero amount.
- Free spin WINs credit real wallet and update round status.

### Status
- Input: `ProviderTransactionStatusRequestData`.
- Output: `ProviderTransactionStatusResponseData` with status from stored provider transaction.

### Cancel
- Input: `ProviderCancelTransactionRequestData`.
- If transaction not found, returns `CANCELED` to keep provider flows idempotent.
- If transaction exists and status is OK, reverses the transaction by updating wallet balance and marks provider transaction as CANCELED.

### Finish Round
- Input: `ProviderFinishRoundRequestData`.
- Marks the `GameRound` as `COMPLETED` and updates bet type to win type when win amount is positive.
- Idempotent if round already completed.

## Game Round Creation and Bet Types

`ProviderIntegrationService.findOrCreateGameRound`:
- Creates a `GameRound` on BET, or on WIN when a BET did not arrive first (WIN-before-BET race).
- Uses session token if available; otherwise finds most recent active session by player + game.
- Determines initial bet type based on free spin, bonus-only, mixed, or real-money bet.
- Stores real/bonus bet split for proportional win distribution (`OCP-692`).

## Provider Transaction Tracking

`ProviderTransaction` is recorded for each change balance call:
- `providerTransactionId`, `providerName`, `roundId`, `gameId`, `userId`.
- `transactionType` in {BET, WIN, REFUND}.
- `status` in {OK, CANCELED}.
- `originalRequestHash` stored for idempotency.

## Provider Sync (Game List)

`GameProviderSyncService`:
- Implements sync for provider code `TLT`.
- Pulls game list from `PlatformApiService.getAllGames()`.
- Creates categories (slots, tablegames, crashgame) if missing.
- Processes games in batches with `GameBatchProcessor` and `EnhancedSyncProgressTracker`.
- Disables games not present in provider data.
- Updates sync history and triggers async cache refresh.

## Observability

- `GameCallbackLoggingFilter` logs headers/body for provider callbacks under `/api/v1/provider/*`.
- Provider sync history is stored in `GameProviderSyncHistory` with batch and progress data.
