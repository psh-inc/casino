# Customer Frontend Deep Dive (Code-Derived)

This document describes the customer-facing web app behavior and integration points, derived from code in `casino-customer-f/`.

## Source Files

Routing and layout:
- `casino-customer-f/src/app/app.routes.ts`
- `casino-customer-f/src/app/features/account/account.routes.ts`
- `casino-customer-f/src/app/core/components/main-layout/main-layout.component.ts`
- `casino-customer-f/src/app/core/components/header-new/header-new.component.ts`
- `casino-customer-f/src/app/core/components/footer-new/footer-new.component.ts`

Authentication and session:
- `casino-customer-f/src/app/core/services/auth.service.ts`
- `casino-customer-f/src/app/core/services/auth-modal.service.ts`
- `casino-customer-f/src/app/core/services/token-refresh.service.ts`
- `casino-customer-f/src/app/core/services/user-activity.service.ts`
- `casino-customer-f/src/app/core/services/inactivity-logout.service.ts`

Games and launch:
- `casino-customer-f/src/app/core/services/game.service.ts`
- `casino-customer-f/src/app/core/services/game-launcher.service.ts`
- `casino-customer-f/src/app/features/games/components/casino-page/casino-page.component.ts`
- `casino-customer-f/src/app/modules/game-page/game-page.component.ts`

Sports (BetBy):
- `casino-customer-f/src/app/features/sports/sports.component.ts`
- `casino-customer-f/src/app/core/services/script-loader.service.ts`

Wallet, payments, and wagering:
- `casino-customer-f/src/app/core/services/wallet.service.ts`
- `casino-customer-f/src/app/core/services/wallet-v2.service.ts`
- `casino-customer-f/src/app/core/services/payment.service.ts`
- `casino-customer-f/src/app/core/services/wagering-progress.service.ts`

Bonuses and promotions:
- `casino-customer-f/src/app/core/services/customer-bonus.service.ts`
- `casino-customer-f/src/app/core/services/promotion.service.ts`
- `casino-customer-f/src/app/core/services/promotion-modal.service.ts`
- `casino-customer-f/src/app/core/services/banner.service.ts`

Compliance and responsible gaming:
- `casino-customer-f/src/app/core/services/kyc.service.ts`
- `casino-customer-f/src/app/core/services/simple-kyc.service.ts`
- `casino-customer-f/src/app/core/services/responsible-gambling.service.ts`
- `casino-customer-f/src/app/core/services/verification-progress.service.ts`
- `casino-customer-f/src/app/core/services/two-factor.service.ts`

Realtime:
- `casino-customer-f/src/app/core/services/websocket.service.ts`

## App Routing and Page Model

Top-level routes (`casino-customer-f/src/app/app.routes.ts`):
- `/` and catch-all (`**`) render CMS pages via `CmsPageComponent`.
- `/casino`, `/live-casino`, `/mini-games` render casino lists (with `gameType` route data).
- `/game/:id` renders the game session page.
- `/game-preview/:gameId` renders the mobile preview flow.
- `/sports` and `/esports` render BetBy sports with esports mode data.
- `/promotions`, `/ai-game-finder`, `/affiliate`, `/contact` are public pages.
- `/kyc` and `/account/*` are guarded by `authGuard`.
- Auth screens are exposed both as routes and named outlet `auth` (login/register/forgot-password).

Account routes (`casino-customer-f/src/app/features/account/account.routes.ts`):
- `/account/profile`
- `/account/wallet`
- `/account/bonuses`
- `/account/history`
- `/account/responsible-gaming`

## Authentication and Session Flow

`AuthService`:
- Uses `/api/v1/public/registration` for signup config, validation, and registration.
- Uses `/api/v1/auth` for login and token refresh.
- JWT is decoded to extract expiry and claims; refresh token is stored and periodically validated.
- Fingerprint is generated during registration (via `FingerprintService`).
- Token refresh logic runs proactively (interval-based) and before logout on expiration.

`AuthModalService`:
- Controls modal state for login/register via the named `auth` outlet.
- Supports contextual flows (favorite, deposit, play, generic) and post-login callbacks.

`UserActivityService` + `InactivityLogoutService`:
- Tracks user interactions (mouse, keyboard, touch, focus) and stores last activity time.
- Logs out users after configured inactivity (from `ConfigService`), defaulting to 30 minutes.

## Game Discovery and Launch

`GameService`:
- Uses public endpoints under `/api/v3/public/games` for cached lists and ranked search.
- Adds filter parameters for type, vendor/provider/category, RTP, volatility, and availability.
- Uses in-memory cache with a 5-minute TTL for list endpoints.

`GameLauncherService`:
- Orchestrates demo vs real launch, desktop vs mobile behavior.
- Mobile always routes to preview (`/game-preview/:gameId`), then to `/game/:id`.
- Real-money launches require auth and pass session limit checks from `ResponsibleGamblingService`.
- Launch routing includes query params (demo, autoLaunch, from, entryPoint, isMobile).

## Sports (BetBy) Integration

`SportsComponent`:
- Loads BetBy client script from `https://ui.invisiblesport.com/bt-renderer.min.js`.
- Retrieves JWT via `/api/v1/sports/token` (authenticated) or `/api/v1/sports/guest-token` (guest).
- Initializes `BTRenderer` with brand ID, language, theme, and callbacks.
- Handles token expiry by refreshing auth token and updating/reinitializing renderer.
- Supports esports mode with `sportType`, `defaultView`, and filters.

## Wallet, Payments, and Wagering

`WalletService`:
- Uses `/api/customer` endpoints for wallet summary, transactions, deposits, and withdrawals.
- Caches wallet summary and refreshes every 15 seconds while authenticated.
- Subscribes to balance, bonus, and combined balance websocket events to update cached state.
- Shows KYC-required prompts and routes to `/account/kyc` on withdrawal gating.

`WalletV2Service`:
- Uses Phase 3 unified balance endpoints defined in `balance.models` and `api.constants`.
- Auto-refreshes balance every 30 seconds and reacts to websocket balance updates.
- Provides deposit/withdraw flows with local notifications and routing.

`PaymentService`:
- Initiates cashier sessions via `/api/customer/payment/initiate-session`.
- Handles KYC-required errors by prompting user and routing to `/account/kyc`.

`WebSocketService`:
- Connects to `{apiUrl}/ws` via SockJS + STOMP with Bearer token headers.
- Emits balance updates, bonus balance updates, combined balances, wagering status/progress,
  account status notifications, and session/bet limit warnings.

## Bonuses and Promotions

`CustomerBonusService`:
- Fetches available bonuses from `/api/customer/bonuses/available`.
- Fetches bonus balance from `/api/customer/bonuses/balance`.
- Supports claim-by-id and claim-by-code; refreshes wallet summary post-claim.
- Supports forfeit and refreshes wallet and bonus data.

`PromotionService`:
- Uses `/api/v1/promotions` public endpoints with paging and language filtering.

`BannerService`:
- Uses `/api/v1/public/banners/active` and normalizes banner content for display.
- Supports admin banner upload and creation via CMS endpoints.

## Responsible Gaming and KYC

`ResponsibleGamblingService`:
- Manages limits and self-exclusion via `/api/customer/responsible-gambling/*` endpoints.
- Provides session status used by `GameLauncherService` to prevent play during break periods.

`KycService` and `SimpleKycService`:
- Fetch KYC status, upload requirements, and verification data for account flows.

`TwoFactorService`:
- Integrates `/api/v1/two-factor` for activation/deactivation and login verification.

## Information Movement Patterns

- REST APIs are called via `HttpClient` with `environment.apiUrl`.
- Authenticated flows attach JWT via interceptors in `core/interceptors`.
- WebSocket events provide near real-time updates for wallet and wagering states.
- Game discovery uses cached public endpoints and ranked search for relevance.
- Sports uses an embedded external renderer initialized with backend-issued JWT tokens.
