# Module Inventory (Code-Derived)

This inventory enumerates backend and frontend modules from the codebase.

## Backend Package Structure

Top-level packages under `com.casino.core`:
- `annotation`
- `cache`
- `callback`
- `campaigns`
- `config`
- `controller`
- `converter`
- `domain`
- `dto`
- `entity`
- `event`
- `exception`
- `filter`
- `init`
- `kafka`
- `repository`
- `scheduler`
- `security`
- `service`
- `specification`
- `sports`
- `tools`
- `util`
- `validator`

Sports sub-packages under `com.casino.core.sports`:
- `client`
- `config`
- `controller`
- `domain`
- `dto`
- `exception`
- `filter`
- `repository`
- `security`
- `serialization`
- `service`
- `util`
- `validation`

## Backend HTTP Controllers

Controllers by source file:

```text
casino-b/src/main/kotlin/com/casino/core/controller/AdminBannerController.kt:AdminBannerController
casino-b/src/main/kotlin/com/casino/core/controller/AdminBonusController.kt:AdminBonusController
casino-b/src/main/kotlin/com/casino/core/controller/AdminController.kt:AdminController
casino-b/src/main/kotlin/com/casino/core/controller/AdminWageringManagementController.kt:AdminWageringManagementController
casino-b/src/main/kotlin/com/casino/core/controller/AdvancedBonusController.kt:AdvancedBonusController
casino-b/src/main/kotlin/com/casino/core/controller/AuthController.kt:AuthController
casino-b/src/main/kotlin/com/casino/core/controller/BalanceWebSocketController.kt:BalanceWebSocketController
casino-b/src/main/kotlin/com/casino/core/controller/BannerController.kt:PublicBannerController
casino-b/src/main/kotlin/com/casino/core/controller/BonusAnalyticsController.kt:BonusAnalyticsController
casino-b/src/main/kotlin/com/casino/core/controller/BonusBalanceController.kt:BonusBalanceController
casino-b/src/main/kotlin/com/casino/core/controller/BonusLifecycleTestController.kt:BonusLifecycleTestController
casino-b/src/main/kotlin/com/casino/core/controller/BonusManagementController.kt:BonusManagementController
casino-b/src/main/kotlin/com/casino/core/controller/BonusOfferController.kt:BonusOfferController
casino-b/src/main/kotlin/com/casino/core/controller/BonusSelectionController.kt:BonusSelectionController
casino-b/src/main/kotlin/com/casino/core/controller/BonusTestController.kt:BonusTestController
casino-b/src/main/kotlin/com/casino/core/controller/CMSBannerController.kt:CMSBannerController
casino-b/src/main/kotlin/com/casino/core/controller/CMSPromotionalBlockController.kt:CMSPromotionalBlockController
casino-b/src/main/kotlin/com/casino/core/controller/CMSStaticPageController.kt:CMSStaticPageController
casino-b/src/main/kotlin/com/casino/core/controller/CashierWebhookController.kt:CashierWebhookController
casino-b/src/main/kotlin/com/casino/core/controller/CellxpertController.kt:CellxpertController
casino-b/src/main/kotlin/com/casino/core/controller/ContentController.kt:ContentController
casino-b/src/main/kotlin/com/casino/core/controller/ContentTypeController.kt:ContentTypeController
casino-b/src/main/kotlin/com/casino/core/controller/CountryAvailabilityRestrictionAdminController.kt:CountryAvailabilityRestrictionAdminController
casino-b/src/main/kotlin/com/casino/core/controller/CustomerBonusController.kt:CustomerBonusController
casino-b/src/main/kotlin/com/casino/core/controller/CustomerPortalController.kt:CustomerPortalController
casino-b/src/main/kotlin/com/casino/core/controller/CustomerResponsibleGamblingController.kt:CustomerResponsibleGamblingController
casino-b/src/main/kotlin/com/casino/core/controller/DepositWageringController.kt:DepositWageringController
casino-b/src/main/kotlin/com/casino/core/controller/DepositWageringWebSocketController.kt:DepositWageringWebSocketController
casino-b/src/main/kotlin/com/casino/core/controller/EmailVerificationController.kt:EmailVerificationController
casino-b/src/main/kotlin/com/casino/core/controller/FavoritesController.kt:FavoritesController
casino-b/src/main/kotlin/com/casino/core/controller/FreeSpinsController.kt:FreeSpinsController
casino-b/src/main/kotlin/com/casino/core/controller/GameAdminController.kt:GameAdminController
casino-b/src/main/kotlin/com/casino/core/controller/GameAvailabilityRestrictionAdminController.kt:GameAvailabilityRestrictionAdminController
casino-b/src/main/kotlin/com/casino/core/controller/GameCallbackController.kt:GameCallbackController
casino-b/src/main/kotlin/com/casino/core/controller/GameCategoryController.kt:GameCategoryAdminController
casino-b/src/main/kotlin/com/casino/core/controller/GameCategoryController.kt:GameCategoryController
casino-b/src/main/kotlin/com/casino/core/controller/GameController.kt:GameController
casino-b/src/main/kotlin/com/casino/core/controller/GameCountryConfigAdminController.kt:GameCountryConfigAdminPanelController
casino-b/src/main/kotlin/com/casino/core/controller/GameCountryConfigController.kt:GameCountryConfigController
casino-b/src/main/kotlin/com/casino/core/controller/GameDiscoveryController.kt:GameDiscoveryController
casino-b/src/main/kotlin/com/casino/core/controller/GameLaunchController.kt:GameLaunchController
casino-b/src/main/kotlin/com/casino/core/controller/GameLaunchController.kt:GameSessionAdminController
casino-b/src/main/kotlin/com/casino/core/controller/GameLaunchController.kt:GameSessionController
casino-b/src/main/kotlin/com/casino/core/controller/GameLaunchController.kt:PublicGameLaunchController
casino-b/src/main/kotlin/com/casino/core/controller/GameLimitsController.kt:GameLimitsController
casino-b/src/main/kotlin/com/casino/core/controller/GameProviderController.kt:GameProviderAdminController
casino-b/src/main/kotlin/com/casino/core/controller/GameProviderController.kt:GameProviderController
casino-b/src/main/kotlin/com/casino/core/controller/GameProviderSyncController.kt:GameProviderSyncController
casino-b/src/main/kotlin/com/casino/core/controller/GameRestrictionController.kt:GameRestrictionController
casino-b/src/main/kotlin/com/casino/core/controller/KafkaTestController.kt.disabled:KafkaTestController
casino-b/src/main/kotlin/com/casino/core/controller/LayoutPublicController.kt:LayoutPublicController
casino-b/src/main/kotlin/com/casino/core/controller/LegacyGameCallbackController.kt:LegacyGameCallbackController
casino-b/src/main/kotlin/com/casino/core/controller/LocaleAdminController.kt:LocaleAdminController
casino-b/src/main/kotlin/com/casino/core/controller/LoginHistoryAdminController.kt:LoginHistoryAdminController
casino-b/src/main/kotlin/com/casino/core/controller/LogsExplorerController.kt:LogsExplorerController
casino-b/src/main/kotlin/com/casino/core/controller/MediaController.kt:MediaController
casino-b/src/main/kotlin/com/casino/core/controller/MediaUploadController.kt:MediaUploadController
casino-b/src/main/kotlin/com/casino/core/controller/PasswordResetController.kt:PasswordResetController
casino-b/src/main/kotlin/com/casino/core/controller/PaymentAdminController.kt:PaymentAdminController
casino-b/src/main/kotlin/com/casino/core/controller/PaymentMethodAdminController.kt:PaymentMethodAdminController
casino-b/src/main/kotlin/com/casino/core/controller/PaymentMethodController.kt:PaymentMethodController
casino-b/src/main/kotlin/com/casino/core/controller/PaymentWebhookController.kt:PaymentWebhookController
casino-b/src/main/kotlin/com/casino/core/controller/PhoneVerificationController.kt:PhoneVerificationController
casino-b/src/main/kotlin/com/casino/core/controller/PlayerAdminController.kt:PlayerAdminController
casino-b/src/main/kotlin/com/casino/core/controller/PlayerBonusRestrictionController.kt:PlayerBonusRestrictionController
casino-b/src/main/kotlin/com/casino/core/controller/PlayerCashierRestrictionController.kt:PlayerCashierRestrictionController
casino-b/src/main/kotlin/com/casino/core/controller/PlayerCommentController.kt:PlayerCommentController
casino-b/src/main/kotlin/com/casino/core/controller/PlayerController.kt:PlayerController
casino-b/src/main/kotlin/com/casino/core/controller/PromotionController.kt:PromotionController
casino-b/src/main/kotlin/com/casino/core/controller/ProviderCallbackController.kt:ProviderCallbackController
casino-b/src/main/kotlin/com/casino/core/controller/PublicAuthController.kt:PublicAuthController
casino-b/src/main/kotlin/com/casino/core/controller/PublicBonusController.kt:PublicBonusController
casino-b/src/main/kotlin/com/casino/core/controller/PublicCashierController.kt:PublicCashierController
casino-b/src/main/kotlin/com/casino/core/controller/PublicCmsController.kt:PublicCmsController
casino-b/src/main/kotlin/com/casino/core/controller/PublicGameController.kt:PublicGameController
casino-b/src/main/kotlin/com/casino/core/controller/PublicRegistrationController.kt:PublicRegistrationController
casino-b/src/main/kotlin/com/casino/core/controller/PublicVendorController.kt:PublicVendorController
casino-b/src/main/kotlin/com/casino/core/controller/RefundAdminController.kt:RefundAdminController
casino-b/src/main/kotlin/com/casino/core/controller/TestController.kt:TestController
casino-b/src/main/kotlin/com/casino/core/controller/TestOptimizedController.kt:TestOptimizedController
casino-b/src/main/kotlin/com/casino/core/controller/TestTranslationController.kt:TestTranslationController
casino-b/src/main/kotlin/com/casino/core/controller/TransactionAdminController.kt:TransactionAdminController
casino-b/src/main/kotlin/com/casino/core/controller/TranslationAdminController.kt:TranslationAdminController
casino-b/src/main/kotlin/com/casino/core/controller/TranslationKeyAdminController.kt:TranslationKeyAdminController
casino-b/src/main/kotlin/com/casino/core/controller/TranslationPublicController.kt:TranslationPublicController
casino-b/src/main/kotlin/com/casino/core/controller/TwoFactorAuthController.kt:TwoFactorAuthController
casino-b/src/main/kotlin/com/casino/core/controller/VendorController.kt:VendorController
casino-b/src/main/kotlin/com/casino/core/controller/WageringController.kt:WageringController
casino-b/src/main/kotlin/com/casino/core/controller/WageringWebSocketController.kt:WageringWebSocketController
casino-b/src/main/kotlin/com/casino/core/controller/WalletCacheDemoController.kt:WalletCacheDemoController
casino-b/src/main/kotlin/com/casino/core/controller/WalletController.kt:WalletController
casino-b/src/main/kotlin/com/casino/core/controller/admin/AdminGameController.kt:AdminGameController
casino-b/src/main/kotlin/com/casino/core/controller/admin/AdminPlayerStatusController.kt:AdminPlayerStatusController
casino-b/src/main/kotlin/com/casino/core/controller/admin/AdminPlayerTagController.kt:AdminPlayerTagController
casino-b/src/main/kotlin/com/casino/core/controller/admin/AdminSimpleKycController.kt:AdminSimpleKycController
casino-b/src/main/kotlin/com/casino/core/controller/admin/AggregationMonitoringController.kt:AggregationMonitoringController
casino-b/src/main/kotlin/com/casino/core/controller/admin/CacheAdminController.kt:CacheAdminController
casino-b/src/main/kotlin/com/casino/core/controller/admin/CellxpertAdminController.kt:CellxpertAdminController
casino-b/src/main/kotlin/com/casino/core/controller/admin/ComplianceSettingsController.kt:ComplianceSettingsController
casino-b/src/main/kotlin/com/casino/core/controller/admin/CurrencyAdminController.kt:CurrencyAdminController
casino-b/src/main/kotlin/com/casino/core/controller/admin/DashboardController.kt:DashboardController
casino-b/src/main/kotlin/com/casino/core/controller/admin/KafkaAdminController.kt:KafkaAdminController
casino-b/src/main/kotlin/com/casino/core/controller/admin/KafkaDataPopulationController.kt.disabled:KafkaDataPopulationController
casino-b/src/main/kotlin/com/casino/core/controller/admin/PlayerProfileUpdateController.kt:PlayerProfileUpdateController
casino-b/src/main/kotlin/com/casino/core/controller/admin/PlayerStatisticsController.kt:PlayerStatisticsController
casino-b/src/main/kotlin/com/casino/core/controller/admin/RegistrationConfigController.kt:RegistrationConfigController
casino-b/src/main/kotlin/com/casino/core/controller/admin/ReportingManagementController.kt:ReportingManagementController
casino-b/src/main/kotlin/com/casino/core/controller/admin/SmarticoTestDataController.kt:SmarticoTestDataController
casino-b/src/main/kotlin/com/casino/core/controller/admin/TestDataController.kt:TestDataController
casino-b/src/main/kotlin/com/casino/core/controller/admin/TestGamingDataController.kt:TestGamingDataController
casino-b/src/main/kotlin/com/casino/core/controller/admin/WalletCacheTestController.kt:WalletCacheTestController
casino-b/src/main/kotlin/com/casino/core/controller/admin/WalletMetricsController.kt:WalletMetricsController
casino-b/src/main/kotlin/com/casino/core/controller/admin/WidgetTranslationController.kt:WidgetTranslationController
casino-b/src/main/kotlin/com/casino/core/controller/analytics/GameAnalyticsController.kt:GameAnalyticsController
casino-b/src/main/kotlin/com/casino/core/controller/analytics/GameAnalyticsController.kt:ProviderAnalyticsController
casino-b/src/main/kotlin/com/casino/core/controller/cms/MenuConfigurationAdminController.kt:MenuConfigurationAdminController
casino-b/src/main/kotlin/com/casino/core/controller/cms/PageConfigurationAdminController.kt:PageConfigurationAdminController
casino-b/src/main/kotlin/com/casino/core/controller/cms/PageConfigurationPublicController.kt:PageConfigurationPublicController
casino-b/src/main/kotlin/com/casino/core/controller/cms/PageLocaleOverrideAdminController.kt:PageLocaleOverrideAdminController
casino-b/src/main/kotlin/com/casino/core/controller/cms/WidgetAdminController.kt:WidgetAdminController
casino-b/src/main/kotlin/com/casino/core/controller/customer/CustomerPaymentController.kt:CustomerPaymentController
casino-b/src/main/kotlin/com/casino/core/controller/demo/MultilanguageDemoController.kt:MultilanguageDemoController
casino-b/src/main/kotlin/com/casino/core/controller/demo/SignupConfigCacheDemoController.kt:SignupConfigCacheDemoController
casino-b/src/main/kotlin/com/casino/core/controller/integration/SmarticoController.kt:SmarticoController
casino-b/src/main/kotlin/com/casino/core/controller/integration/SmarticoIntegrationController.kt:SmarticoIntegrationController
casino-b/src/main/kotlin/com/casino/core/controller/player/PlayerProfileFieldController.kt:PlayerProfileFieldController
casino-b/src/main/kotlin/com/casino/core/controller/player/PlayerProfilePictureController.kt:PlayerProfilePictureController
casino-b/src/main/kotlin/com/casino/core/controller/player/PlayerSimpleKycController.kt:PlayerSimpleKycController
casino-b/src/main/kotlin/com/casino/core/controller/publicApi/OptimizedPublicGameController.kt:OptimizedPublicGameController
casino-b/src/main/kotlin/com/casino/core/controller/publicApi/V3PublicGameController.kt:V3PublicGameController
casino-b/src/main/kotlin/com/casino/core/controller/recommendation/GameRecommendationController.kt:GameRecommendationController
casino-b/src/main/kotlin/com/casino/core/controller/reporting/DailyBreakdownController.kt:DailyBreakdownController
casino-b/src/main/kotlin/com/casino/core/controller/reporting/ReportingController.kt:ReportingController
casino-b/src/main/kotlin/com/casino/core/controller/reporting/ReportingExportController.kt:ReportingExportController
casino-b/src/main/kotlin/com/casino/core/controller/reporting/TimeSeriesController.kt:TimeSeriesController
casino-b/src/main/kotlin/com/casino/core/controller/responsible/PlayerLimitController.kt:AdminLimitController
casino-b/src/main/kotlin/com/casino/core/controller/responsible/PlayerLimitController.kt:PlayerLimitController
casino-b/src/main/kotlin/com/casino/core/controller/responsible/SelfExclusionController.kt:AdminSelfExclusionController
casino-b/src/main/kotlin/com/casino/core/controller/responsible/SelfExclusionController.kt:SelfExclusionController
casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByAdminController.kt:BetByAdminController
casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByController.kt:BetByController
casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByExternalApiTestController.kt:BetByDebugController
casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByExternalApiTestController.kt:BetByExternalApiTestController
casino-b/src/main/kotlin/com/casino/core/sports/controller/BetByWalletController.kt:BetByWalletController
casino-b/src/main/kotlin/com/casino/core/sports/controller/BonusAdminController.kt:BonusAdminController
casino-b/src/main/kotlin/com/casino/core/sports/controller/SportsAuthController.kt:SportsAuthController
```

## Admin Frontend Modules

Modules under `casino-f/src/app/modules`:

```text
banners
campaigns
cms
cms-admin
dashboard
deposit-wagering
game-management
kafka-admin
logs-explorer
payments
player-management
refunds
registration-config
reporting
settings
simple-kyc
```

Key route configs:
- `casino-f/src/app/app-routing.module.ts`
- `casino-f/src/app/core/config/navigation.config.ts`

## Customer Frontend Features

Features under `casino-customer-f/src/app/features`:

```text
account
affiliate
ai-game-finder
auth
cms-page
contact
games
home
kyc
promotions
responsible-gambling
sports
wallet
widget-demo
```

Additional modules under `casino-customer-f/src/app/modules`:

```text
game-page
promotions
```

Key route configs:
- `casino-customer-f/src/app/app.routes.ts`
- `casino-customer-f/src/app/features/account/account.routes.ts`
