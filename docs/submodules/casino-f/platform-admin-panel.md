# Admin Panel Deep Dive (Code-Derived)

This document describes the admin web app feature set and implementation, derived from code in `casino-f/`.

## Source Files

Routing and navigation:
- `casino-f/src/app/app-routing.module.ts`
- `casino-f/src/app/core/config/navigation.config.ts`

Authentication and security:
- `casino-f/src/app/core/services/auth.service.ts`
- `casino-f/src/app/core/guards/auth.guard.ts`
- `casino-f/src/app/core/interceptors/auth.interceptor.ts`

Realtime and shared services:
- `casino-f/src/app/core/services/bonus-balance-websocket.service.ts`
- `casino-f/src/app/services/deposit-wagering-websocket.service.ts`
- `casino-f/src/app/services/deposit-wagering.service.ts`
- `casino-f/src/app/core/services/notification.service.ts`

Feature services (examples):
- `casino-f/src/app/services/dashboard.service.ts`
- `casino-f/src/app/services/dashboard-facade.service.ts`
- `casino-f/src/app/modules/player-management/players.service.ts`
- `casino-f/src/app/modules/payments/payments.service.ts`
- `casino-f/src/app/modules/refunds/refunds.service.ts`
- `casino-f/src/app/modules/game-management/games.service.ts`
- `casino-f/src/app/services/bonus.service.ts`
- `casino-f/src/app/modules/campaigns/campaigns.service.ts`
- `casino-f/src/app/promotions/services/promotion.service.ts`
- `casino-f/src/app/modules/banners/banners.service.ts`
- `casino-f/src/app/modules/cms/services/content.service.ts`
- `casino-f/src/app/modules/cms-admin/services/cms.service.ts`
- `casino-f/src/app/modules/settings/services/currency.service.ts`
- `casino-f/src/app/core/services/kafka-admin.service.ts`
- `casino-f/src/app/modules/logs-explorer/services/logs-explorer.service.ts`
- `casino-f/src/app/services/reporting/daily-breakdown.service.ts`

## App Shell and Routing

The admin shell uses `MainLayoutComponent` with a guarded route tree.
Primary route groups (`casino-f/src/app/app-routing.module.ts`):
- `/dashboard`
- `/payments`
- `/refunds`
- `/game-management`
- `/player-management`
- `/bonuses`
- `/campaigns`
- `/promotions`
- `/banners`
- `/cms`
- `/admin/cms`
- `/registration-config`
- `/simple-kyc`
- `/settings`
- `/deposit-wagering`
- `/kafka-admin`
- `/logs-explorer`
- `/reporting/daily-breakdown`

Navigation entries are defined in `casino-f/src/app/core/config/navigation.config.ts` and include
player management, fraud detection, payments, reporting, game management, bonuses, campaigns, promotions,
CMS admin, registration config, Simple KYC, logs explorer, Kafka monitoring, and settings.

## Authentication and Session Handling

Auth and guard logic:
- `AuthService` authenticates via `POST {apiUrl}/admin/login`, stores JWT tokens and user info in localStorage,
  and performs periodic token expiry checks.
- `AuthGuard` protects the main route tree and redirects unauthenticated users to `/login`.
- `AuthInterceptor` injects `Authorization: Bearer <token>` on all requests except the login call and logs out
  on HTTP 401 errors.

## Data Transport and Realtime

HTTP transport:
- Services use `HttpClient` with `environment.apiUrl` as the base.
- Filtering and pagination commonly use `HttpParams` in service methods.

Realtime updates:
- Bonus balance websocket: `BonusBalanceWebSocketService` connects via STOMP over SockJS and subscribes to
  `/topic/bonus-balance/{playerId}` and `/topic/combined-balance/{playerId}`.
- Deposit wagering websocket: `DepositWageringWebsocketService` subscribes to
  `/user/{playerId}/queue/deposit-wagering/*` and `/topic/deposit-wagering/events`.
- Event streams are exposed as RxJS Observables for UI consumption.

## Feature Modules and Implementation Notes

### Dashboard and Analytics
- Routes: `/dashboard`.
- Services: `dashboard.service.ts` calls `/v1/admin/dashboard/*` endpoints for metrics, time series, and rankings.
- `dashboard-facade.service.ts` composes filter state, auto-refresh (5 min), and provides cached Observable streams.

### Player Management
- Routes: `/player-management/*`.
- `players.service.ts` provides CRUD, search, wallet/transactions/history, status updates, manual deposits,
  bonus balance details, wagering transactions, and KYC-related data.
- Supporting services cover tags, comments, cashier restrictions, responsible gambling, and bonus restrictions.

### Fraud Detection
- Routes: `/player-management/fraud-detection/*`.
- UI modules show dashboards, duplicate accounts, and suspicious activity views.

### Payments and Refunds
- Routes: `/payments/*`, `/refunds/*`.
- `payments.service.ts` calls `/admin/payments` with filters (status, method, amount, date, player, provider).
- `refunds.service.ts` supports list/create/approve/reject/process, including statistics.

### Game Management
- Routes: `/game-management/*`.
- `games.service.ts` manages game CRUD, filters, ranks, and bulk updates.
- Providers, vendors, categories, availability, and restrictions are handled by
  `providers.service.ts`, `vendors.service.ts`, `categories.service.ts`, and `game-availability.service.ts`.

### Bonuses
- Routes: `/bonuses/*`.
- `bonus.service.ts` maps backend bonus models to frontend form structures and back to API requests.
- Supports multi-currency limits, reward mapping, campaign mappings for free spins, and schedule configuration.
- `bonus-form-state.service.ts` manages complex form state across sections.

### Campaigns
- Routes: `/campaigns/*`.
- `campaigns.service.ts` drives list/create/detail screens and campaign metadata management.

### Promotions and Banners
- Routes: `/promotions/*`, `/banners/*`.
- `promotion.service.ts` and `banners.service.ts` handle CRUD and metadata for public-facing promotions.

### CMS and CMS Admin
- Routes: `/cms/*` (content/editor), `/admin/cms/*` (admin CMS management).
- `content.service.ts`, `content-type.service.ts`, and `media.service.ts` support content editing, scheduling,
  and media asset handling.
- `cms.service.ts` provides admin page/widget management; translation tools live under
  `translations` modules and `translation-management.service.ts`.

### Registration Config
- Routes: `/registration-config/*`.
- `registration-config.service.ts` manages field definitions, collection points, and preview configuration.

### Simple KYC
- Routes: `/simple-kyc/*`.
- `simple-kyc.service.ts` loads dashboard stats and player queues by status.

### Settings and Compliance
- Routes: `/settings/*`.
- `currency.service.ts` handles currency CRUD and status toggles.
- `compliance-settings.service.ts` is used for compliance-related configuration screens.

### Deposit Wagering (Admin)
- Routes: `/deposit-wagering/*`.
- `deposit-wagering.service.ts` provides admin CRUD and progress controls for wagering requirements,
  plus live status aggregation for players.
- `deposit-wagering-websocket.service.ts` provides realtime updates and notifications.

### Kafka Monitoring
- Routes: `/kafka-admin/*`.
- `kafka-admin.service.ts` uses `/v1/admin/kafka/*` endpoints for health, metrics, failed events,
  bulk actions, and retry statistics.

### Logs Explorer
- Routes: `/logs-explorer/*`.
- `logs-explorer.service.ts` queries `/v1/admin/logs` with filters, pagination, and CSV export.

### Reporting (Daily Breakdown)
- Route: `/reporting/daily-breakdown`.
- `daily-breakdown.service.ts` calls `/api/v1/reporting/daily-breakdown` for analytics
  and `ReportingExportService`-backed exports.

## Information Movement Patterns

- REST is the default integration path (HTTP + JSON) using `HttpClient`.
- Filtering and pagination are handled via `HttpParams` (page/size/sort/filters).
- Realtime updates use STOMP over SockJS and are scoped per-player via topic naming conventions.
- Complex workflows (bonuses, dashboard analytics) use mapping layers to reconcile backend DTOs
  with admin UI form structures and filters.
