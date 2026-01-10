# Admin Frontend Features and Implementation (Code-Derived)

Admin UI code lives in `casino-f/src/app`.

## Auth and Shell

- Login route: `/login` uses `AuthService`.
- Tokens are stored in localStorage (`access_token` + expiry).
- `AuthGuard` protects main routes.
- Main layout: `MainLayoutComponent`.

Code:
- `casino-f/src/app/core/services/auth.service.ts`
- `casino-f/src/app/core/guards/auth.guard.ts`
- `casino-f/src/app/app-routing.module.ts`

## Navigation and Feature Map

Navigation is defined in:
- `casino-f/src/app/core/config/navigation.config.ts`

Primary modules and routes:
- Dashboard: `/dashboard`
- Player management: `/player-management/*`
- Payments: `/payments/*`
- Refunds: `/refunds/*`
- Game management: `/game-management/*`
- Bonuses: `/bonuses/*`
- Campaigns: `/campaigns/*`
- Promotions: `/promotions/*`
- Banners: `/banners/*`
- CMS: `/cms/*`
- CMS Admin: `/admin/cms/*`
- Registration config: `/registration-config/*`
- Simple KYC: `/simple-kyc/*`
- Settings (currencies): `/settings/*`
- Deposit wagering: `/deposit-wagering/*`
- Kafka admin: `/kafka-admin/*`
- Logs explorer: `/logs-explorer/*`
- Reporting: `/reporting/daily-breakdown`

## Module-by-Module Implementation Notes

### Player Management

Routes and components:
- Player list, create, details
- Login history
- Fraud detection dashboard
- Duplicate accounts and suspicious activity

Code:
- `casino-f/src/app/modules/player-management/player-management-routing.module.ts`

Backend mapping:
- `PlayerAdminController`, `LoginHistoryAdminController`, `PlayerCommentController`

### Game Management

Routes and components:
- Game list, create/edit, details
- Providers, vendors, categories
- Country restrictions and game availability

Code:
- `casino-f/src/app/modules/game-management/game-management-routing.module.ts`

Backend mapping:
- `GameAdminController`, `GameProviderController`, `VendorController`, `GameCategoryController`, `CountryAvailabilityRestrictionAdminController`, `GameAvailabilityRestrictionAdminController`

### Payments and Refunds

- Payments list and details
- Refund handling

Backend mapping:
- `PaymentAdminController`, `RefundAdminController`, `TransactionAdminController`

### Bonuses

- Bonus list and creation
- Advanced bonus flows and management
- Bonus balance views and analytics

Backend mapping:
- `AdminBonusController`, `BonusManagementController`, `AdvancedBonusController`, `BonusBalanceController`, `BonusAnalyticsController`

### Campaigns (Free Spins)

- List, create, cancel campaigns
- Vendor limits and presets

Frontend service:
- `casino-f/src/app/modules/campaigns/campaigns.service.ts`

Backend mapping:
- `CampaignAdminController`

### Promotions and Banners

- Promotions list/create
- Banner management

Backend mapping:
- `PromotionController`, `AdminBannerController`, `BannerController`

### CMS and CMS Admin

- Page configuration, widgets, translations
- Public and admin CMS endpoints

Backend mapping:
- `PageConfigurationAdminController`, `WidgetAdminController`, `TranslationAdminController`

### Registration Config

- Dynamic registration field configuration and preview

Backend mapping:
- `RegistrationConfigController`, `PublicRegistrationController`

### Simple KYC

- Dashboard and pending reviews
- Verification instructions

Backend mapping:
- `AdminSimpleKycController`, `PlayerSimpleKycController`

### Deposit Wagering

- Wagering requirements and progress
- WebSocket updates for deposit wagering

Backend mapping:
- `DepositWageringController`, `DepositWageringWebSocketController`

### Kafka Admin and Logs Explorer

- Kafka monitoring, failed events, metrics
- HTTP request log explorer

Backend mapping:
- `KafkaAdminController`, `LogsExplorerController`

## Shared Services

Key shared services:
- Balance and wagering APIs: `core/services/balance.service.ts`
- Bonus balance websocket: `core/services/bonus-balance-websocket.service.ts`
- Kafka admin monitoring: `core/services/kafka-admin.service.ts`

These services implement STOMP WebSocket subscriptions and call backend REST endpoints.

## Service Inventory (All Service Files)

```text
casino-f/src/app/components/bonus/bonus-form/bonus-form-state.service.ts
casino-f/src/app/core/services/auth.service.ts
casino-f/src/app/core/services/balance.service.ts
casino-f/src/app/core/services/bonus-balance-websocket.service.ts
casino-f/src/app/core/services/kafka-admin.service.ts
casino-f/src/app/core/services/navigation-search.service.ts
casino-f/src/app/core/services/notification.service.ts
casino-f/src/app/core/services/player-statistics.service.ts
casino-f/src/app/core/services/wagering-management.service.ts
casino-f/src/app/core/services/wagering-requirements.service.ts
casino-f/src/app/modules/banners/banners.service.ts
casino-f/src/app/modules/campaigns/campaigns.service.ts
casino-f/src/app/modules/cms-admin/pages/page-configuration-form/page-configuration-form-state.service.ts
casino-f/src/app/modules/cms-admin/services/cms.service.ts
casino-f/src/app/modules/cms-admin/translations/services/translation-management.service.ts
casino-f/src/app/modules/cms-admin/widgets/widget-edit/services/widget-form-factory.service.ts
casino-f/src/app/modules/cms/services/content-type.service.ts
casino-f/src/app/modules/cms/services/content.service.ts
casino-f/src/app/modules/cms/services/media.service.ts
casino-f/src/app/modules/dashboard/dashboard.service.ts
casino-f/src/app/modules/game-management/categories.service.ts
casino-f/src/app/modules/game-management/game-availability.service.ts
casino-f/src/app/modules/game-management/game-restriction.service.ts
casino-f/src/app/modules/game-management/games.service.ts
casino-f/src/app/modules/game-management/providers.service.ts
casino-f/src/app/modules/game-management/services/sync-progress.service.ts
casino-f/src/app/modules/game-management/vendors.service.ts
casino-f/src/app/modules/logs-explorer/services/logs-explorer.service.ts
casino-f/src/app/modules/payments/payments.service.ts
casino-f/src/app/modules/player-management/login-history.service.ts
casino-f/src/app/modules/player-management/media-upload.service.ts
casino-f/src/app/modules/player-management/player-bonus-restriction.service.ts
casino-f/src/app/modules/player-management/player-cashier-restriction.service.ts
casino-f/src/app/modules/player-management/player-comment.service.ts
casino-f/src/app/modules/player-management/player-responsible-gambling.service.ts
casino-f/src/app/modules/player-management/player-tag.service.ts
casino-f/src/app/modules/player-management/players.service.ts
casino-f/src/app/modules/refunds/refunds.service.ts
casino-f/src/app/modules/registration-config/services/registration-config.service.ts
casino-f/src/app/modules/settings/services/compliance-settings.service.ts
casino-f/src/app/modules/settings/services/currency.service.ts
casino-f/src/app/modules/simple-kyc/services/simple-kyc.service.ts
casino-f/src/app/promotions/services/promotion.service.ts
casino-f/src/app/services/bonus.service.ts
casino-f/src/app/services/dashboard-facade.service.ts
casino-f/src/app/services/dashboard.service.ts
casino-f/src/app/services/deposit-wagering-websocket.service.ts
casino-f/src/app/services/deposit-wagering.service.ts
casino-f/src/app/services/export.service.ts
casino-f/src/app/services/game-filter.service.ts
casino-f/src/app/services/game-limits.service.ts
casino-f/src/app/services/media.service.ts
casino-f/src/app/services/public-game.service.ts
casino-f/src/app/services/reporting.service.ts
casino-f/src/app/services/reporting/daily-breakdown.service.ts
casino-f/src/app/services/sports-bonus-template.service.ts
casino-f/src/app/services/vendor.service.ts
casino-f/src/app/shared/services/language.service.ts
casino-f/src/app/shared/ui/ui-dialog.service.ts
casino-f/src/app/shared/ui/ui-toast.service.ts
```
