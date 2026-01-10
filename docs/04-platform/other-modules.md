# Other Platform Modules (Code Inventory)

This document lists additional platform modules not covered in the deeper dives. It is derived from controller and service names in the codebase. For full endpoint lists, see `docs/04-platform/module-inventory.md`.

## Content and CMS

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/cms/MenuConfigurationAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/cms/PageConfigurationAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/cms/PageConfigurationPublicController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/cms/PageLocaleOverrideAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/cms/WidgetAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PublicCmsController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/CMSBannerController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/CMSStaticPageController.kt`

Features indicated by code:
- Admin management of menus, pages, widgets, and localized overrides.
- Public CMS endpoints for page configuration and cache stats.
- Banner management for CMS-driven content.

## Media and Assets

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/MediaController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/MediaUploadController.kt`

Features indicated by code:
- Media upload and retrieval endpoints.

## Translations and Localization

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/TranslationAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/TranslationKeyAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/TranslationPublicController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/LocaleAdminController.kt`

Features indicated by code:
- Translation key management and public translation retrieval.
- Locale administration for UI localization.

## Responsible Gambling and KYC

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/responsible/PlayerLimitController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/responsible/SelfExclusionController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/admin/AdminSimpleKycController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/player/PlayerSimpleKycController.kt`

Features indicated by code:
- Player deposit/loss/bet limits and statistics.
- Self-exclusion flows for players and admins.
- Simple KYC management and statistics.

## Promotions, Bonuses, and Campaigns

Controllers (non-exhaustive):
- `casino-b/src/main/kotlin/com/casino/core/controller/BonusManagementController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/BonusOfferController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PromotionController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/AdvancedBonusController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/AdminBonusController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/BonusAnalyticsController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/FreeSpinsController.kt`

Features indicated by code:
- Bonus lifecycle management, offers, and promotions.
- Bonus analytics and free spins management.

## Games, Recommendations, and Favorites

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/GameController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/GameDiscoveryController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/recommendation/GameRecommendationController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/FavoritesController.kt`

Features indicated by code:
- Game listing, discovery, and recommendations.
- Favorites management and stats.

## Payments and Cashier

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/PaymentAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PaymentMethodAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PublicCashierController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PaymentWebhookController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/CashierWebhookController.kt`

Features indicated by code:
- Payment method and provider administration.
- Cashier flows and webhook ingestion.

## Admin Monitoring and Operations

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/admin/CacheAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/admin/AggregationMonitoringController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/admin/KafkaAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/LogsExplorerController.kt`

Features indicated by code:
- Cache statistics and cache warm/evict operations.
- Aggregation job monitoring.
- Kafka retry statistics and failure monitoring.
- Log exploration and statistics.

## Customer Account and Security

Controllers:
- `casino-b/src/main/kotlin/com/casino/core/controller/AuthController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PublicAuthController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PasswordResetController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/TwoFactorAuthController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/EmailVerificationController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/PhoneVerificationController.kt`

Features indicated by code:
- Authentication, password reset, 2FA, and verification flows.
