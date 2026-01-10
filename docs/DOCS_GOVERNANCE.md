# Documentation Governance - Casino Platform

Owner: Platform Engineering + Product
Status: Draft (initial docs generated from current codebase)

## Scope and sources of truth

The codebase is the source of truth. Contracts and specs are managed as code.

Primary sources:
- Backend: casino-b/src/main, casino-b/src/main/resources
- Admin frontend: casino-f/src/app
- Customer frontend: casino-customer-f/src/app
- Infrastructure: infra/, config/, scripts/
- Operational guidance: QA_TESTING_GUIDE.md, CODE_REVIEW_SECURITY_ASSESSMENT_2025-12-14.md
- Compliance sources: docs/06-compliance/regulatory-sources.md

## Document ownership

- Architecture + Infrastructure: Platform Engineering
- Backend module specs: Backend Team
- Admin frontend module specs: Admin UI Team
- Customer frontend module specs: Customer UI Team
- Security + Compliance: Security lead + Platform Engineering
- Operations + Runbooks: Platform Engineering + SRE

## Review cadence

- Architecture and security docs: every 90 days or on significant change.
- Module specs: every 90 days or on feature change.
- Specs/Contracts: on any API/event change.
- Operations/runbooks: after incidents and every 180 days.

## Status labels

- Draft: initial or partially validated content
- In Review: under team review
- Approved: validated against code and runtime behavior
- Deprecated: no longer relevant but kept for audit

## Approval gates

- Security architecture and compliance docs require Security sign-off.
- Contract changes require API owner + consumer review.
- Production runbooks require Platform Engineering approval.

## Change management

- Update docs in the same change set as code.
- If a submodule changes, update docs inside the submodule first, then update root docs and submodule references.
- Include references to code paths and specs.

## Known gaps (must be closed)

- Formal non-functional targets (SLO/SLI, RTO/RPO) are not defined in code; documented as explicit gaps.
- Compliance obligations are sourced and documented, but evidence collection is not yet assessed.
