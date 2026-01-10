# Backend - Integrations and Realtime

## Responsibilities

- Kafka event publishing and retry/DLQ
- WebSocket real-time updates
- External integrations: BetBy, Smartico, Cellxpert, campaigns

## Key controllers

- BalanceWebSocketController, WageringWebSocketController
- DepositWageringWebSocketController
- SmarticoController, SmarticoIntegrationController
- CellxpertController, CellxpertAdminController
- GameCallbackController, ProviderCallbackController

## Key modules

- kafka/ (events, publishers, retry)
- sports/ (BetBy integration)
- campaigns/ (external campaign integration)

## Dependencies

- Kafka topics in KafkaTopics.kt
- External APIs (BetBy, Smartico, Cellxpert)
