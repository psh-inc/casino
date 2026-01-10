# CRM, Affiliate, and Player Operations (Code-Derived)

This section covers player operations, CRM integrations, segmentation, and affiliate flows.

## Player Operations and Admin Actions

Core player capabilities:
- Create and manage players, addresses, and wallet.
- Update status and record status history.
- Add internal comments and tags.
- Apply game and bonus restrictions.

Key controllers:
- `PlayerAdminController`, `PlayerController`
- `AdminPlayerStatusController`, `AdminPlayerTagController`
- `PlayerCommentController`, `PlayerProfileUpdateController`
- `PlayerBonusRestrictionController`, `PlayerGameRestriction` endpoints

Key services:
- `PlayerService` (registration, updates, statistics)
- `SessionTrackingService` and `LoginHistoryService`

## KYC and Responsible Gambling

KYC operations:
- Simple KYC endpoints for player and admin (`PlayerSimpleKycController`, `AdminSimpleKycController`).
- KYC schedules for document expiry, reminders, and audits (`kyc.scheduler` in `application.yml`).

Responsible gambling:
- Limits (deposit, loss, wager, session time).
- Self-exclusion and cooling-off periods.
- Session time limit enforcement at game launch and provider bet time.

Code:
- `casino-b/src/main/kotlin/com/casino/core/controller/responsible/PlayerLimitController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/responsible/SelfExclusionController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/responsible/*`

## Smartico CRM Integration

Inbound API (bonus operations):
- `/api/v1/smartico/bonuses/active`
- `/api/v1/smartico/bonuses/activate`

API key authentication:
- `X-Smartico-API-Key` validated by `ApiKeyAuthenticationFilter`.

Outbound events (Kafka):
- Player, payment, game, and sports events are formatted for Smartico and published to Kafka topics.
- Field mapping via `SmarticoStatusMapper`.

Code:
- `casino-b/src/main/kotlin/com/casino/core/security/ApiKeyAuthenticationFilter.kt`
- `casino-b/src/main/kotlin/com/casino/core/kafka/service/*EventService.kt`
- `casino-b/src/main/kotlin/com/casino/core/kafka/util/SmarticoStatusMapper.kt`

## Cellxpert Affiliate Integration

Endpoints:
- `/api/v1/cellxpert/players`
- `/api/v1/cellxpert/transactions`
- `/api/v1/cellxpert/activities`

Behavior:
- Supports independent registration and last-modified filters.
- Transactions include deposits, withdrawals, chargebacks.
- Activities use daily aggregated GGR view `cellxpert_player_daily_activity`.

Auth:
- `X-Cellxpert-API-Key` hashed with SHA-256 and compared to stored hash.

Code:
- `casino-b/src/main/kotlin/com/casino/core/controller/CellxpertController.kt`
- `casino-b/src/main/kotlin/com/casino/core/service/CellxpertService.kt`

## Campaigns and Free Spins CRM

Admin campaigns:
- CRUD through `/api/v1/admin/campaigns` and related endpoints.
- Uses external Campaigns API for vendor free spin campaigns.
- Local sync maintains player free spins awards.

Code:
- `casino-b/src/main/kotlin/com/casino/core/campaigns/controller/CampaignAdminController.kt`
- `casino-b/src/main/kotlin/com/casino/core/campaigns/service/CampaignService.kt`

## Promotions, Banners, and CMS

Marketing content is managed via:
- `PromotionController`
- `BannerController` / `AdminBannerController`
- CMS page, menu, widget configuration controllers

Code:
- `casino-b/src/main/kotlin/com/casino/core/controller/PromotionController.kt`
- `casino-b/src/main/kotlin/com/casino/core/controller/cms/*`

## Customer Portal Self-Service

Endpoints in `CustomerPortalController` support:
- Profile view and update.
- Wallet summary and transactions.
- Responsible gambling limits and status.
- GDPR data export requests.

Code:
- `casino-b/src/main/kotlin/com/casino/core/controller/CustomerPortalController.kt`
