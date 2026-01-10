# Platform Deep Dive (Code-Derived)

This section documents the casino platform based only on the current codebase in:
- `casino-b` (backend services, integrations, business logic)
- `casino-f` (admin frontend)
- `casino-customer-f` (customer frontend)
- `config` and runtime configuration in `casino-b/src/main/resources`

No legacy documentation was used as a source. Each section references the specific code paths it is derived from.

## Index

- `information-movement.md` - end-to-end data movement schemes and sequence diagrams
- `external-protocols.md` - external provider communication protocols and auth
- `gaming-logic.md` - game session, provider wallet, round tracking logic
- `wallet-logic.md` - wallet, transactions, payments, wagering locks
- `bonus-logic.md` - bonus lifecycle, eligibility, wagering, free spins
- `crm-operations.md` - CRM, affiliate, segmentation, player ops flows
- `admin-frontend.md` - admin panel features and implementation flow
- `customer-frontend.md` - customer frontend features and implementation flow
- `game-provider-integration.md` - provider wallet callbacks and game sync
- `betby-integration.md` - BetBy sportsbook integration (inbound + external API)
- `smartico-integration.md` - Smartico HTTP integration overview
- `smartico-kafka-events.md` - Smartico Kafka topics and payload schemas
- `cellxpert-integration.md` - Cellxpert affiliate integration
- `reporting-analytics.md` - reporting, analytics, and statistics modules
- `contracts-map.md` - OpenAPI endpoint map by tag and controller
- `other-modules.md` - additional modules and endpoints inventory
- `module-inventory.md` - full component inventory by module and package

## Coverage Map (All Modules/Controllers)

Use these references for complete coverage:
- `contracts-map.md` - every HTTP endpoint grouped by controller and tag.
- `module-inventory.md` - exhaustive list of backend packages and controllers.
- `../specs/openapi/*` - request/response schemas for REST APIs.
- `../specs/asyncapi/*` - event schemas for Kafka and async flows.

## Submodule Deep Dives (Mirrored)

These references point to deep dives that originally lived inside submodules and
are now mirrored in `docs/submodules/`.

- `../submodules/README.md` - submodule documentation index
- `../submodules/casino-b/api/WALLET_API.md` - wallet API details
- `../submodules/casino-b/api/admin-bonus-award-wagering-transactions.md` - admin bonus award wagering transactions
- `../submodules/casino-b/api/betby-sports-bonus-integration.md` - BetBy sports bonus integration
- `../submodules/casino-b/reporting-analytics.md` - reporting and analytics deep dive
- `../submodules/casino-f/platform-admin-panel.md` - admin panel deep dive
- `../submodules/casino-customer-f/platform-customer-frontend.md` - customer frontend deep dive

## Source of Truth (Code)

- Backend core: `casino-b/src/main/kotlin/com/casino/core`
- Sports integration: `casino-b/src/main/kotlin/com/casino/core/sports`
- Backend config: `casino-b/src/main/resources/application.yml`
- Admin UI: `casino-f/src/app`
- Customer UI: `casino-customer-f/src/app`
- API contracts:
  - `specs/openapi/casino-core.json`
  - `specs/openapi/provider-integration.yaml`
  - `specs/openapi/betby.yaml`
  - `specs/openapi/smartico.yaml`
  - `specs/openapi/cellxpert.yaml`
  - `specs/openapi/reporting-analytics.yaml`
- Event contracts:
  - `specs/asyncapi/smartico-events.yaml`
  - `specs/asyncapi/casino-core.json`
