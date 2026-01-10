# Bonus Logic (Code-Derived)

This section documents bonus lifecycle, eligibility, wagering, and free spins.

## Core Entities

- `Bonus`, `BonusReward`, `BonusActivation`, `BonusSchedule`
- `PlayerBonusAward`, `PlayerBonusBalance`, `BonusConversion`
- `BonusFreeSpinsConfig`, `BonusFreeSpinsCampaignMapping`, `PlayerFreeSpinsAward`
- `BonusDepositAssociation`

Code:
- `casino-b/src/main/kotlin/com/casino/core/domain/Bonus.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/BonusReward.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/PlayerBonusAward.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/PlayerBonusBalance.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/BonusFreeSpinsConfig.kt`

## Eligibility Rules

Eligibility is enforced in `BonusEligibilityService`.

Checks include:
- Bonus active status.
- Player bonus restrictions (all bonuses or specific bonus).
- Currency compatibility (bonus eligible currencies).
- Country whitelist and blacklist.
- KYC requirements and category-specific KYC checks.
- Affiliate and segment targeting.
- Sign-up code requirements.
- Bonus subtype constraints:
  - SIGN_UP requires no prior deposits.
  - RELOAD requires existing deposits.
  - NTH_DEPOSIT requires a specific deposit number.
- Schedule restrictions with timezone support.
- Deposit constraints (minimum deposit and payment methods).

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/BonusEligibilityService.kt`

## Bonus Creation and Activation

`BonusService` handles creation and activation:
- Validates category vs reward compatibility.
- Writes multi-currency limits for max bet, min termination, and max win.
- Creates `BonusReward` entries and free spins configs.
- Activation types: `AUTOMATIC`, `MANUAL_CLAIM`, `DEPOSIT_SELECTION`.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/BonusService.kt`

## Bonus Balance and Wagering

`BonusBalanceService` manages bonus balances:

- `BONUS_ONLY` wagering:
  - Wagering base is bonus amount.
- `DEPOSIT_PLUS_BONUS` wagering:
  - Wagering base is bonus + deposit.
  - Cancels active deposit wagering requirements.
  - Locks deposit amount until wagering completes.
- Wagering requirement formula: `wageringRequirement = wageringBase * wageringMultiplier`.

Wagering completion:
- Converts bonus balance to real money via `WalletService.credit`.
- Updates award status to COMPLETED.
- Invalidates bonus cache and emits WebSocket updates.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/BonusBalanceService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/WageringService.kt`

## Bonus Wagering Updates During Gameplay

`ProviderIntegrationService.processBetTransactionCached()`:
- Calculates bet split between real and bonus funds.
- Determines if wagering should be updated based on mode and contribution factor.
- Updates wagering via `HighPerformanceWalletService.updateBonusWagering()`.
- When wagering is complete, calls `BonusBalanceService.checkAndCompleteWagering()`.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/HighPerformanceWalletService.kt`

## Bonus Bet Limits

Bonus bet limits are validated when bonus funds are used:
- `BonusBalanceService.validateBonusBetLimit`.
- Bet limit violations trigger WebSocket notifications.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/BonusBalanceService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`

## Free Spins and Campaigns

Free spins can be awarded by:
- Bonus rewards in `BonusService`.
- External campaigns via Campaigns API.

Free spin tracking:
- `FreeSpinsCallbackService` increments `spinsUsed` and tracks `totalWinnings`.
- Max win caps are enforced per award.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/BonusLogicService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/FreeSpinsService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/FreeSpinsCallbackService.kt`

## CRM and Smartico Integration

- Smartico can activate bonuses via `/api/v1/smartico/bonuses/activate`.
- Zero-wagering bonuses are deposited to real balance; wagering bonuses create bonus balance.

Code:
- `casino-b/src/main/kotlin/com/casino/core/controller/integration/SmarticoController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/BonusService.kt`
