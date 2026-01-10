# Project Charter - Casino Platform

## Mission

Deliver an end-to-end online casino platform that supports player lifecycle management, wallets and payments, games and bonuses, sports betting, CMS-driven content, and administrative operations with real-time updates and event-driven integrations.

## Scope

In scope (based on codebase):
- Backend services (Kotlin/Spring Boot) for player, wallet, games, bonuses, CMS, sports, reporting, integrations
- Admin frontend (Angular) for operations, CMS, payments, reporting, and configuration
- Customer frontend (Angular) for player experience, wallet, games, promotions, sports, KYC, responsible gambling
- Shared library for frontend models and utilities
- Infrastructure configs (Docker, Nginx, PostgreSQL, Redis, Kafka)

Out of scope (not present in repo):
- Native mobile apps
- Third-party cashier UI
- External BI dashboards (beyond exports and reporting APIs)

## Critical workflows

- Player onboarding: registration -> email/phone verification -> KYC -> activation
- Authentication: login -> JWT -> role-based access
- Wallet lifecycle: deposit -> wagering -> withdrawal -> transaction history
- Bonus lifecycle: offer -> claim/activate -> wagering -> convert/forfeit
- Game lifecycle: discovery -> launch -> session -> bet/win callbacks
- Sports betting: BetBy integration and bonus usage
- CMS content: pages, banners, widgets, translations
- Responsible gambling: limits, cooling-off, self-exclusion
- Admin operations: player management, reporting, payments, compliance

## Success criteria

- All platform modules and integrations are documented with code references.
- API and event contracts are published in `specs/` and indexed in `specs/README.md`.
- Documentation link hygiene passes (see `scripts/check_md_links.py`).
- Non-functional targets (SLOs, RTO/RPO) are acknowledged as gaps when not defined in code.

## Constraints

- Backend: Kotlin 2.3.x, Spring Boot 3.2.x, Java 21
- Frontend: Angular 17, TypeScript 5.2/5.4
- Data: PostgreSQL, Redis, Kafka
- Security: JWT auth, BCrypt/Argon2 passwords, TIMESTAMP WITH TIME ZONE

## Known risks (from codebase)

- Security assessment identifies critical issues (secrets in repo, weak provider auth, unauthenticated WebSocket). See CODE_REVIEW_SECURITY_ASSESSMENT_2025-12-14.md.
- Production hardening and firewall posture are tracked in infra/PRODUCTION_AUDIT_2025-12-14.md.

## Stakeholders

- Product: player growth, promotions, game catalog
- Compliance: KYC, responsible gambling, audit readiness
- Finance: wallet integrity, refunds, settlements
- Operations: uptime, incident response, release management
- Marketing: campaigns, CRM, affiliate tracking
