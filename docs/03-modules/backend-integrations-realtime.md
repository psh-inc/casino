# Backend - Integrations and Realtime

## Responsibilities

- Kafka event publishing and retry/DLQ
- WebSocket real-time updates
- External integrations: game providers, BetBy, Smartico, Cellxpert, campaigns, payments

## Key controllers

- BalanceWebSocketController, WageringWebSocketController
- DepositWageringWebSocketController
- SmarticoController, SmarticoIntegrationController
- CellxpertController, CellxpertAdminController
- GameCallbackController, ProviderCallbackController
- BetByController, BetByWalletController

## Key modules

- kafka/ (events, publishers, retry)
- sports/ (BetBy integration)
- campaigns/ (external campaign integration)
- controller/integration/ (Smartico endpoints)

## Dependencies

- Kafka topics and events in `casino-b/src/main/kotlin/com/casino/core/kafka`
- External APIs documented in `docs/04-platform/*.md`
- Contracts in `specs/openapi/*.yaml` and `specs/asyncapi/smartico-events.yaml`
