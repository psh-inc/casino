# Reporting, Analytics, and Statistics

This document describes reporting, analytics, and statistics modules in `casino-b` based on code.

## Source Files

Reporting API:
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/ReportingController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/TimeSeriesController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/DailyBreakdownController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/ReportingExportController.kt`

Analytics API:
- `casino-b/src/main/kotlin/com/casino/core/controller/analytics/GameAnalyticsController.kt`

Reporting services:
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ReportingService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/TimeSeriesService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/DailyBreakdownService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ReportingExportService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ReportingAggregationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ProviderAggregationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/GameDailyStatisticsService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/PlayerDailyStatisticsService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/UnifiedAggregationOrchestrator.kt`
- `casino-b/src/main/kotlin/com/casino/core/config/ReportingCacheConfig.kt`

Dashboard analytics:
- `casino-b/src/main/kotlin/com/casino/core/service/DashboardAnalyticsService.kt`

Player statistics:
- `casino-b/src/main/kotlin/com/casino/core/service/PlayerStatisticsService.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/admin/PlayerStatisticsController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/cache/PlayerStatisticsCacheService.kt`

## Reporting API Endpoints

Base path: `/api/v1/reporting`

- `GET /dashboard` -> `DashboardMetrics`
- `GET /providers` -> provider metrics
- `GET /rankings` -> top players by ranking type and period
- `GET /vendors/{vendorId}` -> vendor metrics
- `GET /ftd` -> first-time depositor metrics
- `GET /ftd/conversion` -> registration to deposit conversion rate
- `GET /ftd/cohort` -> cohort analysis by registration month
- `POST /cache/refresh` -> refresh cached reporting data
- `GET /realtime` -> last-hour real-time metrics
- `GET /summary` -> summary stats for last 30 days
- `POST /recalculate` -> recompute reporting data for a date range

Authorization: `ADMIN`, `OPERATOR`, or `ANALYST` roles unless otherwise noted.

## Time Series API

Base path: `/api/v1/reporting/timeseries`

- `GET /{metric}` -> time series data by granularity
- `GET /{metric}/compare` -> current vs previous period
- `POST /multi` -> multi-metric time series
- `GET /deposits/by-provider` -> time series of deposits (currently uses general deposits series)
- `GET /withdrawals/by-provider` -> time series of withdrawals (currently uses general withdrawals series)
- `GET /ggr/by-vendor` -> time series of GGR (currently uses general GGR series)
- `GET /metrics` -> list of available metrics
- `GET /granularities` -> list of available granularities

## Daily Breakdown API

Base path: `/api/v1/reporting/daily-breakdown`

- `GET /` -> daily metrics with optional summary and comparison
- `GET /summary-cards` -> dashboard summary cards
- `POST /export` -> CSV or Excel export
- `POST /recalculate` -> recalculate daily breakdown
- `GET /available-metrics` -> metric taxonomy (financial, gaming, player, bonus, session)
- `GET /date/{date}` -> breakdown for a single date

## Export API

Base path: `/api/v1/reporting/export`

- `GET /dashboard/excel` -> Excel export
- `GET /timeseries/csv` -> CSV export for a metric
- `GET /rankings/csv` -> CSV export of rankings
- `GET /comprehensive/json` -> JSON export of report pack
- `POST /schedule` -> schedules report generation (currently returns mock response)
- `GET /formats` -> supported export formats
- `GET /history` -> export history (currently returns mock response)

## Analytics API

Base paths:
- `/api/admin/analytics/games`
- `/api/admin/analytics/providers`

Endpoints:
- `GET /{gameId}` -> game analytics for date range, optional country
- `GET /best-performing` -> best games by metric (rtp, players, bets)
- `POST /{gameId}/generate` -> compute analytics for a game
- `POST /generate-all` -> compute analytics for all games

Provider analytics:
- `GET /{providerId}` -> provider analytics by date range
- `GET /best-performing` -> top providers by metric
- `POST /{providerId}/generate` -> compute provider analytics
- `POST /generate-all` -> compute analytics for all providers

## Reporting Data Flow and Aggregation

- `ReportingService` reads from reporting tables and caches results in Redis (via `ReportingCacheService`).
- `GameDailyStatisticsService` aggregates daily and hourly game stats and logs anomalies (extreme RTP, negative GGR, inconsistent counts).
- `PlayerDailyStatisticsService` aggregates per-player daily statistics.
- `ProviderAggregationService` aggregates provider-level performance.
- `UnifiedAggregationOrchestrator` runs aggregated jobs for reporting.

Key computed metrics:
- GGR = total bets - total wins.
- NGR derived from GGR minus bonuses and adjustments (stored in daily summary tables).
- Provider metrics include deposit/withdraw counts and net flow.
- FTD metrics include count, total, average, conversion rate, and cohort analysis.

Reporting cache keys use `ReportingCacheKeyBuilder` and TTLs from `ReportingCacheConfig`:
- `reporting:dashboard`
- `reporting:timeseries`
- `reporting:providers`
- `reporting:rankings`
- `reporting:summary`
- `reporting:vendors`

## Dashboard Analytics (Admin)

`DashboardAnalyticsService` composes admin dashboard metrics:
- Deposit and withdrawal metrics with status breakdown.
- Revenue metrics and charts by period presets.
- Chart categories from reporting repositories.
- Uses `DashboardAnalyticsRepository` queries plus reporting summary tables.

## Player Statistics

`PlayerStatisticsService` maintains per-player statistics by period:
- Periods: DAILY, MONTHLY, YEARLY, LIFETIME.
- Updates on DEPOSIT, WITHDRAWAL, GAME_BET, GAME_WIN transactions.
- Tracks totals, counts, largest amounts, first/last dates.
- Uses `PlayerStatisticsCacheService` for caching and aggregates.

`PlayerStatisticsController` endpoints:
- `GET /api/v1/admin/player-statistics` (by player, currency, period)
- `GET /api/v1/admin/player-statistics/aggregate`
- `GET /api/v1/admin/player-statistics/by-currencies`
- `GET /api/v1/admin/player-statistics/verification-stats`
- `GET /api/v1/admin/player-statistics/top-players`
- `POST /api/v1/admin/player-statistics/cleanup`

## Monitoring and Stats Endpoints

Administrative stats endpoints in other modules (examples):
- Cache stats: `CacheAdminController`, `WalletMetricsController`
- Kafka monitoring: `KafkaAdminController`
- Aggregation monitoring: `AggregationMonitoringController`
- Logs statistics: `LogsExplorerController`
- Refund statistics: `RefundAdminController`

These endpoints are documented in controller files listed in `docs/04-platform/module-inventory.md`.
