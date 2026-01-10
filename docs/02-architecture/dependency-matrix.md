# Dependency Matrix

| Component | Depends On | Notes |
| --- | --- | --- |
| casino-f (Admin SPA) | casino-b API | Uses /api endpoints; environment.apiUrl in casino-f/src/environments |
| casino-customer-f (Customer SPA) | casino-b API, WebSocket | Uses /api and /ws; locales in Angular i18n |
| casino-b (Backend API) | PostgreSQL | Core persistence |
| casino-b (Backend API) | Redis + Caffeine | Multi-level cache |
| casino-b (Backend API) | Kafka | Domain events |
| casino-b (Backend API) | Object Storage | Media/KYC assets |
| casino-b (Backend API) | External Providers | BetBy, game provider, payment, Smartico, Cellxpert, SendGrid, Twilio |
| casino-b (Backend API) | OpenSearch | Logs explorer integration |
| casino-shared | Used by frontends | Shared models/utils |
| Infra (Nginx) | Backend API | Reverse proxy + CORS |
