# Service Catalog

## Core services

| Service | Location | Purpose | Interfaces |
| --- | --- | --- | --- |
| Casino Core API | casino-b/ | Backend API, business logic, integrations | REST, WebSocket, Kafka |
| Admin SPA | casino-f/ | Admin portal for operations | Browser SPA -> REST |
| Customer SPA | casino-customer-f/ | Player-facing web app | Browser SPA -> REST/WS |
| Shared Library | casino-shared/ | Shared TypeScript models/utils | NPM package |

## Data and infrastructure

| Component | Purpose | Notes |
| --- | --- | --- |
| PostgreSQL | Primary datastore | DigitalOcean managed in config; 14+ / 17 in prod audit |
| Redis | Cache + session support | L2 cache; Caffeine L1 in app |
| Kafka | Event streaming | Confluent Cloud in config |
| Nginx | Reverse proxy + CORS | infra/nginx-api.betportal.com.conf |
| Docker Compose | Production runtime | infra/docker-compose.production.yml |

## External integrations

- BetBy sportsbook
- Game provider APIs
- Payment provider
- SendGrid (email)
- Twilio (SMS)
- Smartico (CRM)
- Cellxpert (affiliate tracking)
- OpenSearch (logs)
- Claude AI and Google Vertex AI
- Frankfurter FX
