# Information Movement Schemes (Code-Derived)

This document maps how data moves through the platform and across integrations. Each flow is derived from backend services and frontend routing and services.

## System Actors

- Customer UI: `casino-customer-f/src/app`
- Admin UI: `casino-f/src/app`
- Backend API: `casino-b/src/main/kotlin/com/casino/core`
- Sports API: `casino-b/src/main/kotlin/com/casino/core/sports`
- Data stores: Postgres via JPA repositories
- Messaging: Kafka topics in `com.casino.core.kafka.constants.KafkaTopics`
- Realtime: STOMP/WebSocket controllers in `com.casino.core.controller.*WebSocketController`
- External providers: Payment, game providers, BetBy, Smartico, Cellxpert, Campaigns API

## Flow 1 - Registration, Email Verification, Login, 2FA

```mermaid
sequenceDiagram
    participant C as Customer UI
    participant B as Backend API
    participant DB as Database
    participant SG as SendGrid
    participant SMS as SMS Provider
    participant K as Kafka

    C->>B: GET /api/v1/public/registration/signup-config
    B->>B: SignupConfigCacheService
    B-->>C: PublicSignupConfigurationDto

    C->>B: POST /api/v1/public/registration/signup
    B->>B: PublicRegistrationService -> PlayerService.registerPlayer
    B->>DB: Create Player + Address + Wallet
    B->>K: publish PlayerRegisteredEvent
    B->>SG: EmailService.sendVerificationEmail
    B-->>C: RegistrationResponse

    C->>B: POST /api/v1/auth/login
    B->>B: PublicAuthController -> AuthenticationManager
    B->>B: LoginAttemptService + LoginHistoryService
    alt 2FA enabled
        B->>SMS: TwoFactorAuthService.sendLoginVerificationCode
        B-->>C: twoFactorRequired=true + sessionToken
        C->>B: POST /api/v1/auth/verify-2fa
    end
    B-->>C: JWT access/refresh tokens

    C->>B: GET /api/v1/email-verification/status
    B-->>C: VerificationStatusResponse
    C->>B: GET /api/v1/email-verification/verify/{token}
    B-->>C: VerificationResponse
```

Key logic:
- Registration uses dynamic signup config and creates wallet in `PlayerService`.
- Login tracks failed attempts and can block accounts in `LoginAttemptService`.
- 2FA flow uses `TwoFactorAuthService` and SMS provider.
- Email verification gates gameplay and deposits via `ComplianceSettingsService` and `GameLaunchService`/`PaymentService`.

## Flow 2 - Game Launch and Provider Wallet Callbacks

```mermaid
sequenceDiagram
    participant C as Customer UI
    participant B as Backend API
    participant DB as Database
    participant GEO as GeoLocation
    participant GP as Game Provider
    participant W as Wallet Cache
    participant WS as WebSocket
    participant K as Kafka

    C->>B: POST /api/games/{id}/launch
    B->>B: GameLaunchService.validatePlayerStatusForGameplay
    B->>GEO: GeoLocationService.detectCountryFromIp
    B->>B: GameAvailabilityService.getGameAvailabilityStatus
    B->>DB: GameLaunchTransaction + GameSession
    B-->>C: launchUrl + token + sessionId

    C->>GP: Open launchUrl (token as session key)
    GP->>B: POST /api/v1/provider/{provider}/authenticate
    B->>W: HighPerformanceWalletService.getBalance + bonus
    B-->>GP: balance + user profile

    GP->>B: POST /api/v1/provider/{provider}/changebalance
    B->>B: ProviderIntegrationService
    B->>W: updateBalance + bonus wagering + deposit wagering
    B->>DB: ProviderTransaction + GameRound updates
    B->>WS: Balance and wagering notifications
    B->>K: game/bet/win events
    B-->>GP: updated balance
```

Key logic:
- Launch URL includes operator_id, token, device, language, and optional RTP/bet limits.
- Provider callbacks use request hashing and operator headers in `ProviderSecurityService`.
- Change balance is idempotent by provider transaction ID and request hash.

## Flow 3 - Generic Game Provider Callbacks

```mermaid
sequenceDiagram
    participant GP as Game Provider
    participant B as Backend API
    participant DB as Database
    participant W as Wallet/Bonus
    participant K as Kafka

    GP->>B: POST /api/callbacks/game-round
    B->>B: GameCallbackService.processGameRound
    B->>DB: Find GameSession + GameLaunchTransaction
    B->>W: calculateAndDeductBet + applyBetDeduction
    B->>DB: GameRound created/updated
    B->>B: WinDistributionService (proportional win)
    B->>W: credit wins and update bonus
    B->>K: publish game events
    B-->>GP: GameResultResponse
```

Key logic:
- Bet deduction uses real money first, then bonus balances ordered by age.
- Mixed-bet win distribution uses `WinDistributionService`.

## Flow 4 - Deposits, Cashier Session, Webhooks

```mermaid
sequenceDiagram
    participant C as Customer UI
    participant B as Backend API
    participant PP as Payment Provider
    participant DB as Database
    participant W as Wallet
    participant K as Kafka

    C->>B: POST /api/customer/payment/initiate-session
    B->>PP: POST /api/v1/auth/client/login (client id/secret)
    PP-->>B: access_token
    B->>PP: POST /api/v1/cashier/initiate-session
    PP-->>B: cashierUrl + sessionId
    B-->>C: PaymentSessionResponse

    PP->>B: POST /api/payment/cashier/hook (webhook)
    B->>B: WebhookSignatureService.validateSignature
    B->>DB: PaymentTransaction create/update
    B->>W: WalletService.credit (deposit)
    B->>B: DepositWageringService.createDepositWagering
    B->>B: BonusEligibilityService + BonusService
    B->>K: Payment and bonus events
    B-->>PP: 200 OK
```

Key logic:
- Cashier webhooks drive transaction state transitions in `PaymentWebhookService`.
- Email verification requirements can block deposits.

## Flow 5 - Bonus Awarding and Wagering Progress

```mermaid
sequenceDiagram
    participant B as Backend API
    participant DB as Database
    participant W as Wallet Cache
    participant WS as WebSocket
    participant K as Kafka

    B->>B: DepositCompletedEvent
    B->>B: BonusEligibilityService.findEligible...()
    B->>B: BonusService.activate/award
    B->>DB: PlayerBonusAward + PlayerBonusBalance
    B->>B: BonusBalanceService.createBonusBalance
    B->>W: HighPerformanceWalletService.updateBonusBalance
    B->>WS: WageringNotificationService
    B->>K: BONUS_* events
```

Key logic:
- DEPOSIT_PLUS_BONUS bonuses cancel active deposit wagering and lock deposit.
- Wagering contribution uses game contribution factors and wagering mode.

## Flow 6 - Sports Betting (BetBy)

```mermaid
sequenceDiagram
    participant BetBy as BetBy API
    participant B as Backend API
    participant DB as Database
    participant W as Wallet
    participant K as Kafka

    BetBy->>B: POST /api/v1/sport/betby/bet/make (JWT payload)
    B->>B: BetByJwtService.decryptPayload
    B->>B: BetByApiService.processBetMake
    B->>W: BetByWalletService.deductBetAmount
    B->>DB: SportsBet + SportsTransaction
    B->>K: SPORTS_BET_PLACED (Smartico)
    B-->>BetBy: BetMakeResponse

    BetBy->>B: /bet/win or /bet/settlement
    B->>W: Credit winnings/refunds
    B->>DB: Update bet status
    B->>K: SPORTS_BET_SETTLED
```

## Flow 7 - Realtime Balance, Wagering, and Account Status

```mermaid
sequenceDiagram
    participant B as Backend API
    participant WS as WebSocket/STOMP
    participant A as Admin UI
    participant C as Customer UI

    B->>WS: BalanceUpdateEvent / BonusBalanceUpdateEvent
    WS-->>A: /topic/bonus-balance/{playerId}
    WS-->>C: /topic/balance/{playerId}
    WS-->>C: /topic/combined-balance/{playerId}
    B->>WS: Wagering progress and milestone notifications
```

## Flow 8 - Kafka Event Publishing (CRM/Analytics)

```mermaid
flowchart LR
    Backend[casino-b services] --> Kafka[Kafka topics]
    Kafka --> CRM[Smartico CRM consumer]
    Kafka --> Analytics[Reporting/BI consumers]

    subgraph Events
      P[Player events]
      Pay[Payment events]
      G[Game events]
      S[Sports events]
      B[Bonus events]
      C[Compliance events]
    end

    Backend --> P
    Backend --> Pay
    Backend --> G
    Backend --> S
    Backend --> B
    Backend --> C
    P --> Kafka
    Pay --> Kafka
    G --> Kafka
    S --> Kafka
    B --> Kafka
    C --> Kafka
```

## Data Movement Summary

- HTTP requests are handled by controller classes in `com.casino.core.controller`.
- Business logic is executed in service classes in `com.casino.core.service` and `com.casino.core.sports.service`.
- Persistent state is stored via JPA repositories in `com.casino.core.repository` and `com.casino.core.sports.repository`.
- High-frequency balance operations use `HighPerformanceWalletService` with local + Redis caches.
- Real-time updates are emitted via WebSocket controllers and event services.
- Cross-system integration relies on explicit protocols documented in `external-protocols.md`.
