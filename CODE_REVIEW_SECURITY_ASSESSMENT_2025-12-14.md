# Casino Platform Code Review & Security Assessment

**Date:** 2025-12-14  
**Scope:** `casino-b/` (Kotlin/Spring Boot), `casino-f/` (Angular admin), `casino-customer-f/` (Angular customer), plus relevant `infra/` docs.  
**Reviewed revisions:**
- Backend (`casino-b`): `e5a349f59a8744d2cc2a903dea3f53d6f8698da9`
- Admin SPA (`casino-f`): `61aa0d1041591930e4689c7c5afb857aa4b3f52c`
- Customer SPA (`casino-customer-f`): `87ade3c39db7fe1e18861715e1364f73b8ff9e9c`

**Method:** static review (targeted reading + ripgrep), plus `cd casino-b && ./gradlew test` (passed).

---

## Overall Assessment (1–10)

- **Code quality & maintainability:** **5/10**
- **Production readiness:** **3/10**
- **Security & compliance posture:** **1/10**

Rationale: the codebase contains many core casino components and tests, but multiple “ship-stopper” security issues (including committed secrets/keys and disabled authentication checks) make it unsafe for production in its current state.

---

## Strengths

- **Broad domain coverage**: registration/auth, wallet/transactions, payment session + webhooks, bonuses + wagering, CMS, responsible gambling, reporting/analytics, sports integration.
- **Monetary handling mostly uses `BigDecimal`** with explicit precision/scale in schema (`NUMERIC(19,4)` etc).
- **Concurrency awareness in wallet**:
  - pessimistic lock path (`WalletRepository.findByPlayerIdWithLock`)
  - atomic update path (`WalletRepository.updateBalanceAtomic`)
  - idempotency table for provider callbacks (`ProviderTransaction` unique constraint).
- **Responsible gambling hooks exist in core bet flow** (`ProviderIntegrationService.processBetTransactionCached` validates bet/session limits and records bets).
- **Backend test suite exists and currently passes** (`casino-b ./gradlew test`).

---

## Critical Issues (Security / Compliance / Integrity)

### CRITICAL-01 — Secrets and private keys are committed to the repository

**Evidence (examples, non-exhaustive):**
- Hard-coded credentials in `casino-b/src/main/resources/application.yml` (Kafka SASL creds, DB password, SendGrid key, Twilio token, etc).
- AI provider keys in `casino-b/src/main/resources/application-ai.yml` (Claude/Gemini keys as defaults).
- EC private key committed: `casino-b/src/main/resources/keys/betby-private.pem`.
- Backup config with credentials: `casino-b/src/main/resources/config-backup-20251116_231622/application_n.yml`.

**Impact:** immediate compromise risk (payments, messaging, DB access, third-party billing abuse), plus regulatory exposure (PII, KYC documents).

**Fix (high priority):**
1) Rotate/revoke all exposed keys and passwords immediately.  
2) Purge secrets from git history (BFG / filter-repo) and enforce secret scanning in CI.  
3) Remove private keys from the repo; load via secret manager/KMS or runtime secret injection.

---

### CRITICAL-02 — Provider authentication is effectively disabled (balance-changing endpoints can be abused)

**Evidence:**
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderSecurityService.kt`:
  - `validateAuthorizationHeader(...)` computes `isValid` but returns `true // TODO FIX REAL AUTH`
  - `validateRequestHash(...)` computes `isValid` but returns `true // TODO REAL AUTH`
- Provider endpoints are public (`SecurityConfig` permits `/api/v1/provider/**`) via `casino-b/src/main/kotlin/com/casino/core/security/SecurityConfig.kt`.

**Impact:** anyone who can reach `/api/v1/provider/*` can potentially call `changebalance` and manipulate player balances and wagering state.

**Fix (high priority):**
- Implement real authentication (HMAC with shared secret, timestamp + nonce, strict replay window, constant-time compare).
- Remove permissive defaults (`provider.secret-key`, `provider.operator-id`) and require env-provided secrets.
- Add allowlist by source IP (provider ranges) at edge/firewall in addition to app-level auth.

---

### CRITICAL-03 — WebSocket layer is unauthenticated; balance data is exposed by client-supplied `playerId`

**Evidence:**
- `casino-b/src/main/kotlin/com/casino/core/config/WebSocketSecurityConfig.kt`: explicitly allows all STOMP connects; does not validate JWT.
- `casino-b/src/main/kotlin/com/casino/core/config/WebSocketConfig.kt`: `setAllowedOriginPatterns("*")` and token is accepted via query param but never validated.
- `casino-b/src/main/kotlin/com/casino/core/controller/BalanceWebSocketController.kt`: uses `request.playerId` (“TODO: In production, get playerId from authenticated principal”).
- `casino-b/src/main/kotlin/com/casino/core/controller/DepositWageringWebSocketController.kt`: uses `request.playerId` and even `playerId = 1L` for `/deposit-wagering/status`.

**Impact:** unauthorized users can subscribe to other players’ balances/bonus/wagering status; potentially supports targeted fraud and privacy violations.

**Fix (high priority):**
- Enforce JWT authentication on websocket connect and bind `Principal` to player identity.
- Remove/ignore any client-provided `playerId` in websocket subscription payloads.
- Restrict websocket CORS/origins and disable token-in-query-parameter patterns.

---

### CRITICAL-04 — Sensitive request/response logging will leak credentials/tokens/PII

**Evidence:**
- `casino-b/src/main/kotlin/com/casino/core/filter/RequestResponseLoggingFilter.kt` logs full request and response bodies (not just metadata). It does not redact passwords, refresh tokens, KYC data, etc.
- `casino-b/src/main/kotlin/com/casino/core/security/JwtAuthenticationFilter.kt` dumps all headers and logs the `Authorization` header value.
- `casino-b/src/main/resources/logback-spring.xml` routes `RequestResponseLoggingFilter` logs to `requests.log` at INFO regardless of profile.

**Impact:** credential leakage to log files; token replay; major compliance issues (GDPR/PCI/AML audit integrity).

**Fix (high priority):**
- Remove body logging in production; keep only structured metadata with strict redaction.
- Never log auth headers or tokens (even at DEBUG).
- Add correlation IDs and centralize security audit logs separately from app logs.

---

### CRITICAL-05 — KYC document uploads appear publicly accessible (severe privacy/regulatory breach)

**Evidence:**
- `casino-b/src/main/kotlin/com/casino/core/service/MediaAssetService.kt` uploads all files with `CannedAccessControlList.PublicRead` and sets `cacheControl = "public, max-age=31536000"`.
- `casino-b/src/main/kotlin/com/casino/core/service/simple/SimpleKycService.kt` uploads identity/address docs via `mediaAssetService.uploadFile(...)`.

**Impact:** KYC documents (passport/bills) may be publicly readable if URL is known or indexed; catastrophic regulatory failure.

**Fix (high priority):**
- Store KYC files in a private bucket/prefix; never `PublicRead`.
- Serve access via short-lived signed URLs with strict authorization checks.
- Add content-type sniffing + AV scanning + size limits + retention policies.

---

### CRITICAL-06 — Bonus/real-money integrity flaw: cancellations/refunds do not restore bonus portion (enables bonus→cash conversion)

**Evidence:**
- `casino-b/src/main/kotlin/com/casino/core/service/ProviderIntegrationService.kt`:
  - `processBetTransactionCached` can split bets between wallet and bonus.
  - `cancelTransaction` reverses BET by crediting the full amount back to the real wallet only (no bonus restoration).
  - `processRefundTransactionCached` credits refunds to real wallet only.

**Impact:** players can potentially shift value from bonus balance into withdrawable real balance through cancel/refund paths, breaking bonus terms and financial integrity.

**Fix (high priority):**
- Persist funding split per bet (real/bonus) and apply the same split in refund/cancel/reversal.
- Enforce immutable transaction linkage (bet↔refund) with strict invariants and reconciliation tooling.

---

### CRITICAL-07 — Payment/security integrations are not strict enough for production

**Evidence:**
- `casino-b/src/main/kotlin/com/casino/core/controller/CashierWebhookController.kt`: signature failures are logged but webhook is still processed.
- `casino-b/src/main/kotlin/com/casino/core/service/WebhookSignatureService.kt`: default secret is empty; signature comparison is not constant-time; logs expected signature.
- Public balance/config endpoints lack authentication:
  - `casino-b/src/main/kotlin/com/casino/core/controller/PublicCashierController.kt` (`/api/player/public/balance`) trusts `x-customer-id`, ignores `merchantId`.
  - `casino-b/src/main/kotlin/com/casino/core/service/CashierConfigService.kt` ignores `merchantId` entirely and looks up player by username.

**Impact:** forged webhooks can credit wallets; attackers can enumerate users and query balances/withdrawability; direct financial risk.

**Fix (high priority):**
- Reject invalid webhook signatures in prod (fail closed).
- Require merchant authentication (HMAC signature + allowlisted IPs + request-id replay protection).
- Do not use username as “customer id” for provider integrations; use opaque IDs.

---

### CRITICAL-08 — Numerous test/demo endpoints are deployed and reachable

**Evidence:**
- `casino-b/src/main/kotlin/com/casino/core/security/SecurityConfig.kt` permits `/api/test/**` and `/api/demo/**` and `/api/v1/admin/smartico-test/**` as `permitAll()`.
- Examples of dangerous endpoints:
  - `casino-b/src/main/kotlin/com/casino/core/controller/TestController.kt` populates payment data.
  - `casino-b/src/main/kotlin/com/casino/core/controller/BonusLifecycleTestController.kt` can create players, simulate deposits/wagering, cleanup, etc.
  - `casino-b/src/main/kotlin/com/casino/core/controller/admin/SmarticoTestDataController.kt` publishes Kafka events and is `permitAll`.

**Impact:** attackers can mutate data, generate transactions/events, poison analytics, and potentially trigger balance changes.

**Fix (high priority):**
- Remove these from production builds or gate them behind a non-prod Spring profile + admin auth + network allowlist.

---

## Important Gaps (Missing/Incomplete)

- **Withdrawal flow appears incomplete** (customer-facing initiation/approval/payout orchestration is not clearly implemented end-to-end; some endpoints are stubs such as `WalletService.processWithdrawal` returning “PENDING” without processor integration).
- **Token/session hardening gaps**:
  - refresh tokens are not differentiated from access tokens and appear non-revocable (`AuthController.refreshToken`, `PublicAuthController.refreshToken`).
  - no server-side refresh token rotation / reuse detection.
- **Geolocation/geoblocking is bypassable**:
  - `GameLaunchService` uses `request.ipAddress` from client payload (`GameLaunchController` passes it through), enabling spoofing.
  - `GeoLocationService` calls public third-party IP services directly without clear timeouts/consent story.
- **Regulatory/financial-crime controls appear incomplete**:
  - limited fraud signals exist (e.g., “suspicious login activity”), but no backend AML transaction-monitoring, sanctions/PEP screening, source-of-funds/source-of-wealth workflow, or regulatory reporting pipeline is evident.
- **Age verification is largely self-declared**: minimum-age validation exists on date-of-birth fields, but regulatory-grade identity/age verification depends on KYC enforcement and should be treated as a hard gate for deposit/withdraw/play where required by jurisdiction.
- **Admin/security auditability**:
  - no clear, tamper-evident audit log for privileged actions (manual balance adjustments, config edits, KYC decisions, etc).
- **Front-end XSS hardening is insufficient for a CMS-driven product** (see next section).

---

## Frontend Security Findings (Admin + Customer)

### High-risk XSS surfaces (stored XSS likely)

**Customer portal:**
- `casino-customer-f/src/app/shared/widgets/tab-content/tab-content.component.ts` uses `bypassSecurityTrustHtml` without sanitizing.
- `casino-customer-f/src/app/shared/modules/translation/translate.directive.ts` can set `innerHTML` from translations without sanitization.
- `casino-customer-f/src/app/shared/widgets/custom-html/custom-html.component.ts` supports disabling sanitization (`sanitize === false`) and injects scoped `<style>` via trusted HTML.

**Admin portal:**
- `casino-f/src/app/shared/pipes/safe-html.pipe.ts` blindly trusts HTML via `bypassSecurityTrustHtml`.
- CMS editors validate JS with `new Function(...)` (`casino-f/src/app/modules/cms-admin/pages/page-form/page-form.component.ts`, `casino-f/src/app/modules/cms-admin/widgets/widget-edit/configs/custom-html-config/custom-html-config.component.ts`), increasing the blast radius of XSS if the admin UI is compromised.

**Token storage amplifies XSS impact:**
- Both SPAs store bearer tokens in `localStorage` (`casino-f/src/app/core/services/auth.service.ts`, `casino-customer-f/src/app/core/services/auth.service.ts`).

**Recommendation:** treat CMS HTML as untrusted input. Enforce sanitization server-side and client-side; remove “disable sanitization” switches for production; move tokens to HttpOnly cookies if feasible; deploy strict CSP.

---

## Feature Completeness Snapshot (Casino Essentials)

- **Registration & login:** Present (public registration + login + optional SMS 2FA). Needs rate limiting + refresh token hardening.
- **KYC:** Present (simple KYC statuses + document uploads + admin review). Storage/access control is currently not acceptable for production.
- **Wallet & ledger:** Present (wallet, transactions, provider transaction idempotency). Refund/cancel correctness for mixed funds must be fixed.
- **Deposits:** Present via cashier session + webhook processing. Signature verification must be strict; public “balance/config” endpoints must be authenticated.
- **Withdrawals:** Partially present (entities/statuses exist; end-to-end orchestration unclear and some code paths look stubbed).
- **Game catalog & provider integration:** Present (public games endpoints + provider callbacks + caching). Provider authentication must be fixed.
- **Bonus/promotion engine:** Present (eligibility, wagering modes, deposit wagering). Needs stronger invariants and reconciliation on reversals.
- **Responsible gambling:** Present (limits, self-exclusion, bet/session limit validation). Enforcement must be server-trustworthy (no client IP spoofing; websocket auth).
- **Fraud/AML:** Partial (login “suspicious activity” signals exist). No clear transaction-monitoring/sanctions screening/source-of-funds automation found in code.
- **Audit logs:** Partial (compliance events, KYC audit log, login history). Needs admin action audit trail and secure log handling.
- **Admin controls:** Present (CMS, players, payments, bonuses). Needs hard security boundaries and removal of test endpoints.

---

## Recommendations (Prioritized)

### High (ship-stoppers)
1) **Rotate/revoke all committed secrets/keys immediately**; remove from repo history; add secret scanning.  
2) **Fix provider authentication** (`ProviderSecurityService`) and add replay protection + IP allowlisting.  
3) **Lock down WebSockets**: authenticate, bind player identity to `Principal`, remove client-supplied `playerId`, restrict origins.  
4) **Remove/disable test/demo endpoints in production**; delete `permitAll()` matchers for them.  
5) **Stop logging sensitive data**: remove request/response body logging and header dumps; implement structured redaction.  
6) **Fix KYC storage**: private buckets, signed URLs, encryption, scanning, retention; never `PublicRead`.  
7) **Fix mixed-fund reversal correctness** (refund/cancel) to prevent bonus→cash conversion.  
8) **Enforce webhook signature validation** (fail closed in prod) and secure public provider-facing endpoints.

### Medium
- Add refresh token rotation + revocation + “token type” claims and tighten refresh logic.
- Harden error handling: stop returning internal exception messages in prod (`GlobalExceptionHandler`).
- Server-trust geolocation: extract IP from request context, not from client payload; define geoblocking source of truth.
- Replace ad-hoc third-party IP lookups with a controlled provider and explicit timeouts/consent story.
- Encrypt or hash sensitive DB fields (2FA secrets/backup codes) and add operational rotation.
- Normalize RBAC conventions (`ROLE_` vs non-prefixed authorities) and audit admin actions.

### Low
- Remove dead/duplicate controllers and config drift (multiple auth controllers, inconsistent expiry constants, duplicate Gradle deps).
- Align README/actual versions (Java/Spring Boot versions, logging format claims).
- Replace `println` with structured logging and add metrics where TODOs exist.

---

## Related Infrastructure Notes

There is a separate host-level hardening document at `infra/PRODUCTION_AUDIT_2025-12-14.md`. It addresses edge/origin exposure, firewalling, Nginx, Docker isolation, and secrets injection at runtime. Those improvements are valuable but **do not mitigate the code-level ship-stoppers above** (provider auth bypass, websocket exposure, public KYC files, etc.).
