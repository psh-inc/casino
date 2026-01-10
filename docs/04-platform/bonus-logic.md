# Bonus Logic (Code-Derived)

This section documents bonus lifecycle, eligibility, wagering, free spins, and wallet interactions.
All details are derived from code.

## Source Files

Core bonus logic:
- `casino-b/src/main/kotlin/com/casino/core/service/BonusService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/BonusBalanceService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/BonusEligibilityService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/WageringService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/DepositWageringService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/HighPerformanceWalletService.kt`

Entities:
- `casino-b/src/main/kotlin/com/casino/core/domain/Bonus.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/BonusReward.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/PlayerBonusAward.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/PlayerBonusBalance.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/BonusDepositAssociation.kt`

## Core Entities

- `Bonus` and `BonusReward` define types, limits, wagering mode, and contribution factors.
- `PlayerBonusAward` tracks bonus issuance and status.
- `PlayerBonusBalance` tracks bonus funds and wagering progress.
- `BonusDepositAssociation` preserves deposit wagering data when DEPOSIT_PLUS_BONUS replaces deposit wagering.

## Eligibility Rules

Eligibility is enforced in `BonusEligibilityService` and includes:
- Bonus active status and schedule window.
- Player restrictions and segmentation.
- Currency and country rules.
- KYC and category-specific checks.
- Deposit constraints and payment method constraints.
- Bonus subtype rules (SIGN_UP, RELOAD, NTH_DEPOSIT, etc).

## Bonus Creation and Activation

`BonusService`:
- Validates category/reward compatibility.
- Creates `BonusReward` entries and free spins configs.
- Activation types: `AUTOMATIC`, `MANUAL_CLAIM`, `DEPOSIT_SELECTION`.

## Bonus Balance Creation

`BonusBalanceService.createBonusBalance()`:
- Resolves wagering mode via `BonusWageringModeResolver`.
- Wagering base:
  - `BONUS_ONLY`: bonus amount
  - `DEPOSIT_PLUS_BONUS`: bonus amount + deposit amount
- Cancels active deposit wagering if mode is DEPOSIT_PLUS_BONUS.
- Locks deposit amount in `PlayerBonusBalance.lockedDepositAmount`.
- Records `BonusDepositAssociation` to restore deposit wagering if bonus is forfeited.
- Invalidates bonus cache after transaction commit (OCP-671).

## Bonus Wagering Progress

### Event-driven (GameRoundCompletedEvent)

`WageringService.processGameRoundWagering()`:
- Processes only if funding source is not REAL_MONEY.
- Applies game contribution factors from `BonusReward`.
- Creates `WageringTransaction` records.
- Updates `PlayerBonusBalance.wageringCompleted` and caps at requirement.
- Publishes WebSocket notifications and milestones.

### Provider Wallet Callbacks

`ProviderIntegrationService.processBetTransactionCached()`:
- Updates bonus wagering through `HighPerformanceWalletService.updateBonusWagering()`.
- Wagering mode handling:
  - `BONUS_ONLY`: only bonus portion counts.
  - `DEPOSIT_PLUS_BONUS`: full bet counts.
- On completion, calls `BonusBalanceService.checkAndCompleteWagering()`.

### Completion and Conversion

`BonusBalanceService.checkAndCompleteWagering()`:
- Releases locked deposit.
- Credits real wallet using `TransactionType.BONUS_CONVERSION`.
- Sets bonus balance to zero and marks award `COMPLETED`.
- Invalidates bonus cache after commit.

## Bonus Balance Debits and Credits

`HighPerformanceWalletService.updateBonusBalance()`:
- BONUS debit: FIFO by creation time.
- BONUS credit: adds to oldest active bonus balance.
- BONUS convert: credits real wallet and zeroes bonus balances.
- BONUS expire: deactivates and zeros balance.

`BonusBalanceService.deductFromBalance()`:
- Used in `GameCallbackService` for bonus bet deductions.

## Bonus Bet Limits

`BonusBalanceService.validateBonusBetLimit()`:
- Enforced when a bet uses bonus funds.
- Violations produce WebSocket notifications and `BonusBetLimitExceededException`.

## Deposit Wagering Interaction

- When DEPOSIT_PLUS_BONUS is activated, active deposit wagering is cancelled.
- When bonus is forfeited, deposit wagering can be restored using `BonusDepositAssociation` and `DepositWageringService.createDepositWageringFromAssociation()`.

## Free Spins

Free spins are tracked independently of wallet balance:
- Awards stored in `PlayerFreeSpinsAward`.
- `FreeSpinsCallbackService` tracks spins used and total winnings.
- Free spin bets do not debit wallet; wins are credited to real balance.

## CRM (Smartico) Interaction

Smartico bonus activation endpoints:
- `/api/v1/smartico/bonuses/active`
- `/api/v1/smartico/bonuses/activate`

Zero-wagering bonuses can be credited directly to wallet; wagering bonuses create bonus balances.

## Wallet and Transaction Types

Bonus-related transaction types:
- `BONUS_BET`, `BONUS_WIN`, `BONUS_CONVERSION`, `BONUS_EXPIRED`, `BONUS_AWARDED`

Wallet updates occur through:
- `HighPerformanceWalletService.updateBonusBalance()`
- `WalletService.credit()` for bonus conversion

