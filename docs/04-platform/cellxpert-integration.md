# Cellxpert Affiliate Integration

This document covers Cellxpert affiliate tracking integration in `casino-b`. All details are derived from code.

## Source Files

- `casino-b/src/main/kotlin/com/casino/core/controller/CellxpertController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/CellxpertService.kt`
- `casino-b/src/main/kotlin/com/casino/core/dto/CellxpertDtos.kt`
- `casino-b/src/main/kotlin/com/casino/core/security/ApiKeyAuthenticationFilter.kt`
- `casino-b/src/main/kotlin/com/casino/core/scheduler/CellxpertActivityRefreshScheduler.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/CellxpertConfig.kt`
- `casino-b/src/main/kotlin/com/casino/core/domain/CellxpertSyncLog.kt`

## Authentication

- API key header: `X-Cellxpert-API-Key`.
- Key is validated by `ApiKeyAuthenticationFilter` against a SHA-256 hash stored in `CellxpertConfig` in the database.
- If configuration is missing, requests return `503 Cellxpert integration not configured`.

Endpoints are protected by `@PreAuthorize("hasAuthority('CELLXPERT_API') or hasAuthority('ADMIN')")`.

## API Endpoints

Base path: `/api/v1/cellxpert`

### GET /players
Returns players with Cellxpert tracking tokens.

Filters (all optional unless noted):
- `registrationDateFrom`, `registrationDateTo` (ISO 8601 date-time)
- `lastModifiedDateFrom`, `lastModifiedDateTo` (ISO 8601 date-time)
- `playerId` (overrides date filters)
- `affId`

Response: list of `CellxpertPlayerResponse`.

Key response fields:
- player_id, CXD, AffId, Status
- RegistrationDate, LastModifiedDate
- ISOCountry, UserIPAddress
- FirstDepositDate, FirstDepositAmount, FirstDepositCurrency
- TotalDepositAmount, DepositCount
- TotalWithdrawalAmount, WithdrawalCount
- NetDeposit, PrimaryCurrency

### GET /transactions
Returns deposits, withdrawals, and chargebacks for commission calculations.

Required filters:
- `transactionDateFrom`, `transactionDateTo` (ISO 8601 date-time)
Optional:
- `playerId`

Response: list of `CellxpertTransactionResponse`.

Transaction mapping rules:
- Only transactions for players with `cellxpertToken` are included.
- Withdrawals are negative amounts.
- `transaction_type` is mapped from internal `TransactionType`.

### GET /activities
Returns aggregated daily betting activity (GGR) using a materialized view.

Required filters:
- `activityCloseDateFrom`, `activityCloseDateTo` (YYYY-MM-DD)
Optional:
- `playerId`

Response: list of `CellxpertActivityResponse`:
- activity_date
- bets, bonus, revenue, stake
- activity_currency

Data source:
- SQL query against `cellxpert_player_daily_activity` view.

### GET /health
Returns integration status plus recent sync logs.

### POST /refresh-activities
Triggers a refresh of the Cellxpert activity materialized view.

## Sync Logging

`CellxpertSyncLog` tracks syncs with:
- syncType (players/transactions/activities)
- syncStartTime, syncEndTime
- recordsSynced
- status, errorMessage

`CellxpertService.logSync` writes logs after each request.

## Scheduler

`CellxpertActivityRefreshScheduler` refreshes the activity view every 5 minutes.
This is important because Cellxpert can poll activities frequently.

## Tracking Token Capture

- `cellxpertToken` is stored on `Player` and captured during registration.
- DTOs also support `cellxpert_token` in lead creation flows.
