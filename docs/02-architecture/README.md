# Architecture Overview - Casino Platform

This section documents the system architecture for the casino platform.

Key patterns (from codebase):
- Layered backend: controller -> service -> repository
- Multi-level caching: Caffeine (L1) + Redis (L2)
- Event-driven integrations: Kafka topics for domain events
- Real-time updates: STOMP over WebSocket
- External integrations: BetBy, game providers, payment providers, Smartico, Cellxpert, SendGrid, Twilio, OpenSearch

## Contents

- c4-context.md - system context
- c4-container.md - container view
- c4-deployment.md - deployment topology
- service-catalog.md - services and responsibilities
- integration-architecture.md - APIs, events, external integrations
- security-architecture.md - auth, authorization, and risks
- observability-architecture.md - logs, metrics, monitoring
- dependency-matrix.md - component dependencies
- implementation-strategy.md - design patterns and coding standards
- adr/README.md - architecture decision records
