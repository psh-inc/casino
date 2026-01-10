# Documentation Index - Casino Platform

This documentation set describes the casino platform across the backend (casino-b), admin frontend (casino-f), customer frontend (casino-customer-f), shared library (casino-shared), and infrastructure (infra/).

Sources used for this docs set:
- Backend: `casino-b/src/main/kotlin`, `casino-b/src/main/resources` (code + runtime config)
- Admin frontend: `casino-f/src/app`
- Customer frontend: `casino-customer-f/src/app`
- Shared library: `casino-shared`
- Infra/config: `infra/*`, `config/*`
- Compliance: Anjouan OFA and Gaming Board sources listed in `docs/06-compliance/regulatory-sources.md`

Start here (recommended order):
1. DOCS_GOVERNANCE.md - ownership, review cadence, approval gates
2. STYLE_GUIDE.md - writing standards and quality bar
3. 00-project-charter.md - objectives, scope, constraints, risks
4. 00-vision-roadmap.md - current phase and next milestones
5. 02-architecture/README.md - system map, diagrams, integrations
6. 03-modules/README.md - module/service specs and responsibilities
7. 04-infrastructure/environments.md - environments and deployment
8. 07-operations/README.md - runbooks and operational readiness

Supporting docs:
- 00-ai-agent-implementation-plan.md - AI agent execution plan
- 01-discovery/* - journeys, UX stories, screen inventory
- 06-compliance/* - compliance scaffolding and traceability
- ../specs/README.md - contracts index (OpenAPI/AsyncAPI/files)
- ../epics/README.md - delivery backlog and sprint planning
- ../AGENT.md - AI agent operational guide

Submodule docs (mirrored into root docs):
- submodules/casino-b/api/WALLET_API.md - Wallet API documentation
- submodules/casino-b/api/admin-bonus-award-wagering-transactions.md - Admin bonus award wagering transactions
- submodules/casino-b/api/betby-sports-bonus-integration.md - BetBy sports bonus integration
- submodules/casino-b/reporting-analytics.md - Reporting and analytics deep dive
- submodules/casino-f/platform-admin-panel.md - Admin panel deep dive
- submodules/casino-customer-f/platform-customer-frontend.md - Customer frontend deep dive

Principles:
- Prefer links to authoritative sources and code locations over duplication.
- Avoid secrets and environment values in docs; use variable names only.
- Keep docs diff-friendly (Markdown + Mermaid).
