# Vision and Roadmap - Casino Platform

## Current state (from repo)

- Phase 1-4: Core backend, frontends, integrations, and initial documentation are marked complete in README.md.
- Phase 5: Deployment preparation is in progress.
- Phase 6: Final validation and cleanup is in progress.

## Near-term roadmap (next 1-2 phases)

1) Security remediation (highest priority)
- Rotate and remove committed secrets
- Enforce provider and WebSocket authentication
- Redact sensitive logs and secure KYC file storage

2) Contract maturity
- Publish OpenAPI specs under specs/openapi
- Publish AsyncAPI specs for Kafka topics
- Align API docs under casino-b/docs/api

3) Production readiness
- Finalize infra hardening and monitoring
- Complete DR testing and runbooks
- Stabilize migration issues and failing tests

## Mid-term roadmap

- Expand reporting/analytics exports and schedules
- Improve CMS and localization flows
- Enhance AI-based recommendations and personalization

## Open questions (TODO)

- Target jurisdictions and compliance frameworks
- Target availability/latency SLOs and RTO/RPO
- Release cadence and migration windows
