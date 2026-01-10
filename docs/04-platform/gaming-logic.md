# Gaming Logic (Code-Derived)

This section documents game lifecycle, launch, callbacks, and round accounting logic from backend services.

## Core Entities

Key entities in `casino-b/src/main/kotlin/com/casino/core/domain`:
- `Game`, `GameProvider`, `Vendor`, `GameCategory`
- `GameSession` (sessionUuid, mode, totals)
- `GameLaunchTransaction` (launchUrl, token, device, geo)
- `GameRound` (roundId, bet/win amounts, betType, status)
- `ProviderTransaction` (idempotency for provider callbacks)
- `GameAvailabilityRestriction`, `CountryAvailabilityRestriction`, `PlayerGameRestriction`

## Game Launch Pipeline

Primary path: `GameLaunchController` -> `GameLaunchService`

Steps in `GameLaunchService.launchGame()`:
1. Load player by username and validate status:
   - BLOCKED, SUSPENDED, FROZEN, SELF_EXCLUDED, COOLING_OFF are blocked.
2. Enforce email verification for gameplay if configured:
   - Grace period hours from `ComplianceSettingsService`.
   - Logs `ComplianceEventType.PAYMENT_BLOCKED_NO_EMAIL_VERIFICATION`.
3. Geo-detect country from IP via `GeoLocationService`.
4. Apply country and game availability restrictions via `GameAvailabilityService`.
5. Enforce session time limit by checking recent completed sessions.
6. Create `GameLaunchTransaction` and `GameSession` records.
7. Build launch URL:
   - Base host from provider or operator config.
   - Query params include mode, game_id, token, currency, language, operator_id, homeurl, session_id, device, player_id, username, RTP and bet overrides.

Relevant code:
- `casino-b/src/main/kotlin/com/casino/core/service/GameLaunchService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameAvailabilityService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameRestrictionService.kt`

## Session Management

- Active sessions are stored in `GameSession` and `GameLaunchTransaction`.
- `forceEndActiveSessionsForPlayer()` terminates active sessions and invalidates cache.
- Session keep-alive updates the launch transaction timestamp.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/GameLaunchService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/cache/GameSessionCacheService.kt`

## Availability and Restriction Logic

Availability uses a precedence model:
1. Game-specific country restriction
2. Global country restriction
3. Default allow

Player-specific restrictions are checked separately:
- `GameRestrictionService.isGameAvailableForPlayer()` checks global enable + player restriction.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/GameAvailabilityService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameRestrictionService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/CountryAvailabilityRestrictionService.kt`

## Provider Wallet Callback Logic (ChangeBalance)

Primary path: `ProviderCallbackController` -> `ProviderIntegrationService`.

Key rules:
- Idempotency: provider transaction ID + request hash.
- Transaction types: BET, WIN, REFUND.
- Token required for BET (unless PROMO-FREESPIN). WIN/REFUND can be tokenless.
- Game restrictions applied only for BET and non-free-spin.
- Bet limit validation and session time limits enforced before debit.
- Real money is always spent first; bonus balance used only if needed.
- Bonus max bet limit applies when bonus funds used.
- Buy-feature bets are rejected if bonus funds are involved.
- Wagering contribution uses game contribution factor and wagering mode.

Code:
- `casino-b/src/main/kotlin/com/casino/core/controller/ProviderCallbackController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/WinDistributionService.kt`

## Game Round and Win Accounting

Two parallel paths exist:

1) Provider Wallet Callbacks
- `ProviderIntegrationService` creates or updates `GameRound` for bet/win.
- `GameRoundService` marks rounds as PENDING on bet and COMPLETED on win.

2) Generic Game Callbacks
- `GameCallbackService.processGameRound()` handles bet and win in one call.
- Calculates bet split (real vs bonus) before creating `GameRound`.
- Uses `WinDistributionService` for proportional win split:\n  - `realWin = winAmount * (realBet / (realBet + bonusBet))`\n  - `bonusWin = winAmount - realWin` (rounding remainder to bonus).

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/GameRoundService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameCallbackService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/WinDistributionService.kt`

## Free Spins Handling

Free spins can be driven by external campaigns:
- Provider context `reason` includes PROMO-FREESPIN.
- Campaign code is validated against local `PlayerFreeSpinsAward` records.
- Free spin BET transactions do not debit wallet; win credits are tracked.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/FreeSpinsCallbackService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/BonusLogicService.kt`

## Game Discovery and Catalog

- `GameDiscoveryService` provides featured, popular, new, and filtered search results.
- Availability filters are applied per country using `GameAvailabilityService`.
- Provider, category, and vendor catalogs are managed by admin controllers and services.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/GameDiscoveryService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameProviderService.kt`

## Caching and Sync

- `InMemoryGameCache` stores game list snapshots.
- Sync endpoints exist for provider/game catalog refresh.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/cache/InMemoryGameCache.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/GameProviderSyncController.kt`
