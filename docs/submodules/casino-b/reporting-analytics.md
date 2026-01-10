# Reporting and Analytics Deep Dive (Code-Derived)

This document describes the reporting and analytics subsystem in the backend, derived from code in `casino-b/`.

## Source Files

Core reporting services:
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ReportingService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ReportingAggregationService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/UnifiedAggregationOrchestrator.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/DailyBreakdownService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/TimeSeriesService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ReportingExportService.kt`

Analytics services:
- `casino-b/src/main/kotlin/com/casino/core/service/DashboardAnalyticsService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/analytics/GameAnalyticsService.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/analytics/ProviderAnalyticsService.kt`

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/ReportingController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/DailyBreakdownController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/ReportingExportController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/reporting/TimeSeriesController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/admin/ReportingManagementController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/admin/AggregationMonitoringController.kt`

Caching:
- `casino-b/src/main/kotlin/com/casino/core/config/ReportingCacheConfig.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/reporting/ReportingCacheService.kt`

## Reporting Aggregation Pipeline

`ReportingAggregationService` is the core aggregator for daily summaries:
- Aggregates deposits, withdrawals, gaming bets/wins, bonus issuance/wagering, sessions, jackpots, and player metrics.
- Computes derived KPIs such as GGR, NGR, RTP, hold, ARPU, win frequency, average bet, and conversion rates.
- Converts monetary values to EUR for consistent reporting (uses `CurrencyRateLoggingService`).
- Writes into `ReportingDailySummary` via `ReportingDailySummaryRepository`.

`UnifiedAggregationOrchestrator` runs the daily job (00:00 UTC) and coordinates:
- Daily summary aggregation (`ReportingAggregationService.aggregateForDate`).
- Player daily statistics (`PlayerDailyStatisticsService.aggregateForDate`).
- Game daily statistics (`GameDailyStatisticsService.aggregateForDate`).
- Provider aggregations (`ProviderAggregationService` for payment and game providers).
- Circuit breaker with execution logging via `AggregationJobExecutionRepository`.

## Reporting Queries and Caching

`ReportingService` is the read-layer for reporting APIs:
- Dashboard metrics (`getDashboardMetrics`) over a date range with previous-period comparison.
- Provider metrics (`getProviderMetrics`) aggregated by provider name.
- Player rankings by ranking type and period.
- Vendor metrics (`getVendorMetrics`) for provider/aggregator performance.
- FTD metrics via `FirstTimeDepositorService`.
- Daily summary fetch and cache refresh.

`ReportingCacheConfig` defines Redis caches and TTLs:
- `reporting:dashboard`, `reporting:timeseries`, `reporting:providers`, `reporting:rankings`,
  `reporting:summary`, `reporting:vendors`.
- Cache keys are constructed via `ReportingCacheKeyBuilder`.

## Daily Breakdown Reporting

`DailyBreakdownService`:
- Produces `DailyBreakdownResponse` with row-level daily metrics and optional summary/comparison sections.
- Supports sorting and range limits with validation.
- Can trigger recalculation for date ranges by calling `ReportingAggregationService.aggregateForDate`.

`DailyBreakdownController` exposes:
- `/api/v1/reporting/daily-breakdown` for fetch and export.
- `/api/v1/reporting/daily-breakdown/recalculate` for admin-triggered recalculation.

## Dashboard Analytics APIs

`DashboardAnalyticsService` provides the admin dashboard metrics used in the admin UI:
- Deposits, withdrawals, revenue (GGR/NGR), time-series charts, and player/gaming/bonus analytics.
- Status breakdowns by payment method.
- Player rankings (top depositors/winners/losers).

Endpoints are exposed in `DashboardController` under `/v1/admin/dashboard/*`.

## Game and Provider Analytics

`GameAnalyticsService`:
- Computes per-game metrics (sessions, bets, wins, RTP, average bet, session duration).
- Supports daily aggregation per game, by country, and top lists (RTP, popularity).

`ProviderAnalyticsService`:
- Computes provider metrics (active games, sessions, bets, wins, RTP, error counts, uptime approximation).
- Uses callback logs to derive error counts.

## Export and Management Operations

Export endpoints:
- `ReportingExportController` exposes `/api/v1/reporting/export/*` for JSON/CSV/Excel exports.
- Daily breakdown export uses `ReportingExportService`.

Admin controls:
- `ReportingManagementController` triggers recalculation for date ranges or specific days.
- `AggregationMonitoringController` exposes job executions, status, and circuit breaker state.

## Information Movement Summary

- Aggregation is batch-oriented and scheduled daily via `UnifiedAggregationOrchestrator`.
- Reporting reads are served from pre-aggregated tables with Redis caching.
- Admin APIs expose analytics and exports; recalc endpoints allow reprocessing on demand.
- Analytics services (game/provider) compute daily records using sessions, rounds, and callback logs.
