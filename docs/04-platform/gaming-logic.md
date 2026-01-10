# Gaming Logic (Code-Derived)

This section documents game lifecycle, launch, callbacks, betting, and wallet interactions.
All details are derived from code.

## Source Files

- `casino-b/src/main/kotlin/com/casino/core/service/GameLaunchService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameCallbackService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/GameRoundService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/WinDistributionService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/HighPerformanceWalletService.kt`

## Core Entities

- `Game`, `GameProvider`, `Vendor`, `GameCategory`
- `GameSession` (sessionUuid, mode, totals)
- `GameLaunchTransaction` (launchUrl, token, device, geo)
- `GameRound` (roundId, bet/win amounts, betType, status, bet split)
- `ProviderTransaction` (idempotency for provider callbacks)

## Game Launch Pipeline

`GameLaunchService.launchGame()`:
1. Validate player status (BLOCKED/SUSPENDED/SELF_EXCLUDED/COOLING_OFF are blocked).
2. Enforce email verification if configured (`ComplianceSettingsService`).
3. Geo-detect country from IP (`GeoLocationService`).
4. Apply game availability and restriction rules.
5. Enforce session time limits.
6. Create `GameLaunchTransaction` + `GameSession`.
7. Build launch URL with provider/operator params.

## Bet and Win Handling (Generic Game Callbacks)

`GameCallbackService.processGameRound()`:

### Bet Deduction

Algorithm (`calculateAndDeductBet`):
- Real money is used first.
- Bonus balances are used FIFO (oldest bonus first).
- Funding source recorded as `FundingSource.REAL_MONEY`, `BONUS_MONEY`, or `MIXED`.
- If real balance is fully depleted during the bet, `BalanceTransitionService.notifyRealBalanceDepleted()` is triggered.

Application (`applyBetDeduction`):
- Real balance is debited via `WalletService.updateBalanceByAmount()`.
- Bonus balances are reduced via `BonusBalanceService.deductFromBalance()`.
- Bonus cache is invalidated in `HighPerformanceWalletService`.

### GameRound Creation

`GameRound` stores:
- `realBetAmount` and `bonusBetAmount` (OCP-692) for proportional wins.
- `betType` derived from funding source (`BONUS_BET`, `MIXED_BET`, or `GAME_BET`).

### Win Distribution

`WinDistributionService.calculateProportionalDistribution()`:
- Splits win by `realBetAmount` vs `bonusBetAmount`.
- Credits bonus portion to bonus balance if active bonus exists.
- Fallback: bonus portion credited to real wallet if no active bonus.

### Transactions

- GAME_BET and GAME_WIN transactions record `balanceBefore` and `balanceAfter`.
- Funding source is stored in transaction record.

### Kafka Events

- Bet placed, win awarded, and round completed events are published to Kafka via `GameEventService`.

## Provider Wallet Callbacks (Primary Casino Flow)

`ProviderIntegrationService` handles `/changebalance`:

- Idempotency: provider transaction ID + request hash.
- BET processing:
  - Validates session, player status, bet limits, and game restrictions.
  - Splits bet into real + bonus (real first).
  - Debits real balance via `HighPerformanceWalletService.updateBalance(TransactionType.GAME_BET)`.
  - Debits bonus via `HighPerformanceWalletService.updateBonusBalance()`.
  - Updates deposit wagering for real portion (unless bonus mode is DEPOSIT_PLUS_BONUS).
  - Updates bonus wagering via `updateBonusWagering()` based on wagering mode.
- WIN processing:
  - Uses `WinDistributionService` to split win.
  - Credits real balance and/or bonus balance.
  - Falls back to real balance if bonus credit fails.
- REFUND processing:
  - Credits real balance and marks round VOIDED.

## Deposit and Bonus Wagering Sync

- Deposit wagering updates are performed via `DepositWageringService.updateWageringProgress()`.
- Bonus wagering updates occur via `HighPerformanceWalletService.updateBonusWagering()` or `WageringService` (GameRoundCompletedEvent).
- Wagering modes:
  - `BONUS_ONLY`: only bonus portion counts.
  - `DEPOSIT_PLUS_BONUS`: full bet counts (bonus + deposit).

## Free Spins

- Free spin BET does not debit wallet.
- Free spin WIN credits real wallet.
- Free spin tracking is handled via `PlayerFreeSpinsAward`.

## Idempotency and Consistency

- Provider wallet callbacks are idempotent by provider transaction ID and request hash.
- Generic callbacks store `GameCallbackLog` for audit.
- Game rounds are created or updated even if WIN arrives before BET (WIN-before-BET race).

