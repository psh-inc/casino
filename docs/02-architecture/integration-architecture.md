# Integration Architecture

## API surfaces

- REST API: /api with versioned paths (Swagger at /swagger-ui.html when running backend)
- WebSocket: /ws (STOMP), topics include /topic/balance/{playerId}, /topic/bonus/{playerId}, /topic/wagering/{playerId}
- Kafka: domain events listed in KafkaTopics.kt and `specs/asyncapi/smartico-events.yaml`
- Exports: CSV, Excel, PDF (Apache POI + iText + Jackson CSV)

## External integrations (from code)

- Game providers: launch, wallet callbacks, sync (`docs/04-platform/game-provider-integration.md`)
- BetBy sportsbook: sports betting and wallet integration (`docs/04-platform/betby-integration.md`)
- Payment provider: cashier session + webhooks (`docs/04-platform/external-protocols.md`)
- Smartico CRM: HTTP integration + Kafka events (`docs/04-platform/smartico-integration.md`, `docs/04-platform/smartico-kafka-events.md`)
- Cellxpert affiliate: player/transaction/activity feeds (`docs/04-platform/cellxpert-integration.md`)
- SendGrid: email delivery
- Twilio: SMS verification
- DigitalOcean Spaces: media storage
- OpenSearch: logs explorer
- Claude AI + Google Vertex AI: KYC and recommendation services
- Frankfurter: currency exchange

## Event topics (Kafka)

See `casino-b/src/main/kotlin/com/casino/core/kafka/constants/KafkaTopics.kt` for the authoritative list. Topics include:
- Player: casino.player.registered.v1, casino.player.profile-updated.v1, casino.player.authenticated.v1
- Payment: casino.payment.deposit-created.v1, casino.payment.withdrawal-completed.v1
- Game: casino.game.session-started.v1, casino.game.bet-placed.v1
- Bonus: casino.bonus.offered.v1, casino.bonus.wagering-updated.v1
- Compliance: casino.compliance.kyc-approved.v1, casino.compliance.self-excluded.v1
- Sports: casino.sports.bet-placed.v1
- Engagement: casino.engagement.*, plus login/logout topics published by `EngagementEventService`
- System: casino.dlq.all.v1

## Integration risks (from assessments)

- Provider authentication is not enforced in some endpoints (see CODE_REVIEW_SECURITY_ASSESSMENT_2025-12-14.md).
- WebSocket auth is permissive; requires remediation before production.
