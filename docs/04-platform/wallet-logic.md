# Wallet and Payment Logic (Code-Derived)

This section documents wallet operations, payment flows, and withdrawable balance computation.

## Core Entities

- `Wallet` - player balance and currency.
- `Transaction` - wallet credits/debits (deposit, withdrawal, bet, win, adjustments).
- `Payment` and `PaymentTransaction` - payment provider lifecycle.
- `DepositWageringRequirement` and `DepositWageringTransaction` - deposit wagering lock state.

Code references:
- `casino-b/src/main/kotlin/com/casino/core/domain/Wallet.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/Transaction.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/Payment.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/PaymentTransaction.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/DepositWageringRequirement.kt`

## Wallet Service Operations

`WalletService` provides core debit/credit and withdrawal logic.

Credit flow:
- Optional bonus forfeiture on new deposit (`removeActiveBonusesOnDeposit`).
- Pessimistic lock on wallet (`findByPlayerIdWithLock`).
- Persist `Transaction` and publish balance update.

Debit flow:
- Pessimistic lock on wallet.
- Withdrawals validate withdrawable balance (see below).
- Persist `Transaction` and publish balance update.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/WalletService.kt`

## High-Performance Wallet Service

`HighPerformanceWalletService` handles game-time balance changes:
- Multi-layer caching (Caffeine + Redis + DB).
- Atomic balance updates with retries on optimistic locking.
- Emits `BalanceUpdateEvent` and combined balance events for WebSocket consumers.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/HighPerformanceWalletService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/BalanceCacheService.kt`

## Withdrawable Balance Algorithm

`WithdrawableBalanceCalculator` enforces locked funds logic:

Rules:
1. If active bonus wagering mode is `DEPOSIT_PLUS_BONUS`, withdrawable balance is zero.
2. If any active deposit wagering requirements exist, withdrawable balance is zero.
3. Otherwise, withdrawable balance equals wallet balance.

Locked funds breakdown includes:
- Deposit wagering locked amount (binary lock).
- Bonus locked deposit (for DEPOSIT_PLUS_BONUS bonuses).

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/WithdrawableBalanceCalculator.kt`

## Deposit Wagering Logic

`DepositWageringService` creates and updates wagering requirements:
- New deposit wagering may merge with an existing active requirement.
- Wagering requirement = depositAmount * wageringMultiplier (+ remaining old).
- Wagering completion is tracked in `DepositWageringTransaction`.
- Completion emits events and WebSocket notifications.

Key behaviors:
- Binary lock: full deposit locked until wagering completes (no partial unlocks).
- Merge behavior: existing active requirement is marked REPLACED and remaining wagering is carried over, capped to new requirement.
- Auto-close wagering when wallet falls below threshold.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/DepositWageringService.kt`

## Payment Provider and Webhook Processing

Payment provider session creation:
- `PaymentProviderService` authenticates with client id/secret.
- Initiates cashier session and returns `cashierUrl`.

Webhook processing:
- `PaymentWebhookService` updates status based on webhook.
- Completed deposits credit wallet and publish events.
- Status transitions are validated via `PaymentStatusTransitionService`.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/PaymentProviderService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/PaymentWebhookService.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/CashierWebhookController.kt`

## Compliance Gates for Wallet Actions

- Deposits are blocked when email verification is required and grace period expired.
- KYC checks are enforced for deposit and withdrawal flows.
- Compliance events are logged via `ComplianceService`.

Code:
- `casino-b/src/main/kotlin/com/casino/core/service/PaymentService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/ComplianceSettingsService.kt`

## WebSocket and Realtime Updates

Balance updates are published via:
- `BalanceWebSocketController`
- `WageringWebSocketController`
- `DepositWageringWebSocketController`

These controllers broadcast updates consumed by both admin and customer frontends.

Code:
- `casino-b/src/main/kotlin/com/casino/core/controller/BalanceWebSocketController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/WageringWebSocketController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/DepositWageringWebSocketController.kt`
