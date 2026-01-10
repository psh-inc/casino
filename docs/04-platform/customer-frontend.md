# Customer Frontend Features and Implementation (Code-Derived)

Customer UI code lives in `casino-customer-f/src/app`.

## Route Map

Primary routes from `app.routes.ts`:
- `/` and `/**` - CMS-driven pages
- `/kyc` - KYC dashboard (auth required)
- `/promotions`
- `/ai-game-finder`
- `/sports` and `/esports`
- `/casino`, `/live-casino`, `/mini-games`
- `/games` - games module
- `/game/:id` - game page
- `/game-preview/:gameId` - mobile preview
- `/account/*` - account routes
- `/login`, `/register`, `/forgot-password`
- `/verify-email`, `/reset-password`
- `/affiliate`, `/contact`

Code:
- `casino-customer-f/src/app/app.routes.ts`
- `casino-customer-f/src/app/features/account/account.routes.ts`

## Game Launch Logic

`GameLauncherService` handles game launch across desktop and mobile:
- Demo mode bypasses auth.
- Real money checks authentication and session time limit status.
- Mobile always routes to preview first.
- Launch uses query params: `demo`, `autoLaunch`, `entryPoint`, `isMobile`.

Code:
- `casino-customer-f/src/app/core/services/game-launcher.service.ts`

## Wallet, Deposits, and Withdrawals

Wallet behavior:
- `WalletService` auto-refreshes summary every 15 seconds when authenticated.
- WebSocket updates update cached summary (real + bonus).
- Deposit and withdrawal calls update summary and handle KYC errors.

Payment session:
- `PaymentService` calls `/api/customer/payment/initiate-session`.
- KYC errors are surfaced via snackbar and redirected to `/account/kyc`.

Code:
- `casino-customer-f/src/app/core/services/wallet.service.ts`
- `casino-customer-f/src/app/core/services/payment.service.ts`

## Bonuses

`CustomerBonusService`:
- Caches available bonuses and bonus balance.
- Auto-refresh every 60 seconds when authenticated.
- Claims bonuses via `/api/customer/bonuses` endpoints.

Code:
- `casino-customer-f/src/app/core/services/customer-bonus.service.ts`

## Responsible Gambling

`ResponsibleGamblingService`:
- Manage limits and self-exclusion.
- Session time limit status is used by `GameLauncherService`.

Code:
- `casino-customer-f/src/app/core/services/responsible-gambling.service.ts`

## Real-Time Updates

`WebSocketService` provides:
- Balance updates
- Bonus balance updates
- Combined balance updates
- Wagering progress and milestone notifications
- Account status notifications

Code:
- `casino-customer-f/src/app/core/services/websocket.service.ts`

## Smartico Gamification (Client SDK)

`SmarticoService`:
- Uses `_smartico.api` to load current level and levels list.
- Maps Smartico snake_case fields to camelCase interfaces.

Code:
- `casino-customer-f/src/app/core/services/smartico.service.ts`

## CMS and Content

- `CmsPageComponent` renders dynamic CMS pages (catch-all route).
- CMS data loaded via `CmsService` and related helpers.

Code:
- `casino-customer-f/src/app/features/cms-page/cms-page.component.ts`
- `casino-customer-f/src/app/core/services/cms.service.ts`

## Account Area

Features under `/account`:
- Profile, wallet, bonuses, game history, responsible gambling.

Code:
- `casino-customer-f/src/app/features/account/*`

## Service Inventory (All Service Files)

```text
casino-customer-f/src/app/core/services/active-players.service.ts
casino-customer-f/src/app/core/services/angular-i18n.service.ts
casino-customer-f/src/app/core/services/auth-modal.service.ts
casino-customer-f/src/app/core/services/auth.service.ts
casino-customer-f/src/app/core/services/banner.service.ts
casino-customer-f/src/app/core/services/category.service.ts
casino-customer-f/src/app/core/services/cms.service.ts
casino-customer-f/src/app/core/services/config.service.ts
casino-customer-f/src/app/core/services/customer-bonus.service.ts
casino-customer-f/src/app/core/services/favorites.service.ts
casino-customer-f/src/app/core/services/filter-state.service.ts
casino-customer-f/src/app/core/services/fingerprint.service.ts
casino-customer-f/src/app/core/services/game-filter-config.service.ts
casino-customer-f/src/app/core/services/game-launcher.service.ts
casino-customer-f/src/app/core/services/game.service.ts
casino-customer-f/src/app/core/services/global-game-search.service.ts
casino-customer-f/src/app/core/services/global-game-stats.service.ts
casino-customer-f/src/app/core/services/inactivity-logout.service.ts
casino-customer-f/src/app/core/services/kyc.service.ts
casino-customer-f/src/app/core/services/language.service.ts
casino-customer-f/src/app/core/services/loading.service.ts
casino-customer-f/src/app/core/services/locale-redirect.service.ts
casino-customer-f/src/app/core/services/logger.service.ts
casino-customer-f/src/app/core/services/mobile-preview.service.ts
casino-customer-f/src/app/core/services/payment.service.ts
casino-customer-f/src/app/core/services/phone-verification.service.ts
casino-customer-f/src/app/core/services/preloader.service.ts
casino-customer-f/src/app/core/services/profile-picture.service.ts
casino-customer-f/src/app/core/services/profile.service.ts
casino-customer-f/src/app/core/services/promotion-modal.service.ts
casino-customer-f/src/app/core/services/promotion.service.ts
casino-customer-f/src/app/core/services/registration-field.service.ts
casino-customer-f/src/app/core/services/responsible-gambling.service.ts
casino-customer-f/src/app/core/services/route-preloader.service.ts
casino-customer-f/src/app/core/services/script-loader.service.ts
casino-customer-f/src/app/core/services/simple-kyc.service.ts
casino-customer-f/src/app/core/services/smartico.service.ts
casino-customer-f/src/app/core/services/token-refresh.service.ts
casino-customer-f/src/app/core/services/top-winners.service.ts
casino-customer-f/src/app/core/services/translation.service.ts
casino-customer-f/src/app/core/services/two-factor.service.ts
casino-customer-f/src/app/core/services/user-activity.service.ts
casino-customer-f/src/app/core/services/user-context.service.ts
casino-customer-f/src/app/core/services/vendor.service.ts
casino-customer-f/src/app/core/services/verification-progress.service.ts
casino-customer-f/src/app/core/services/wagering-progress.service.ts
casino-customer-f/src/app/core/services/wallet-v2.service.ts
casino-customer-f/src/app/core/services/wallet.service.ts
casino-customer-f/src/app/core/services/websocket.service.ts
casino-customer-f/src/app/core/services/widget-loading.service.ts
casino-customer-f/src/app/core/services/widget-registry.service.ts
casino-customer-f/src/app/features/promotions/services/countdown.service.ts
casino-customer-f/src/app/features/promotions/services/promotion.service.ts
casino-customer-f/src/app/services/affiliate-tracking.service.ts
casino-customer-f/src/app/services/bonus-balance-websocket.service.ts
casino-customer-f/src/app/shared/services/bonus.service.ts
casino-customer-f/src/app/shared/services/promotion.service.ts
```
