# Documentation Index - Casino Platform

This documentation set describes the casino platform across the backend (casino-b), admin frontend (casino-f), customer frontend (casino-customer-f), shared library (casino-shared), and infrastructure (infra/).

Sources used for this docs set:
- Root: README.md, CLAUDE.md, GEMINI.md, QA_TESTING_GUIDE.md, CODE_REVIEW_SECURITY_ASSESSMENT_2025-12-14.md
- Backend: casino-b/README.md, casino-b/docs/api/*, casino-b/specs/*, KafkaTopics.kt
- Admin frontend: casino-f/docs/*, casino-f/src/app/modules
- Customer frontend: casino-customer-f/docs/*, casino-customer-f/src/app/features
- Infra: infra/*, config/postgres/*, .env.example, .env.production.example

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

Principles:
- Prefer links to authoritative sources and code locations over duplication.
- Avoid secrets and environment values in docs; use variable names only.
- Keep docs diff-friendly (Markdown + Mermaid).
