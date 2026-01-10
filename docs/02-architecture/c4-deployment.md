# C4 Deployment - Casino Platform

Based on infra/ production configs (see infra/docker-compose.production.yml and infra/nginx-api.betportal.com.conf).

```mermaid
flowchart LR
  Client[Browser] --> Cloudflare[Cloudflare/WAF]
  Cloudflare --> Nginx[Nginx - api.betportal.com]
  Nginx --> App[casino-core container :8080]
  App --> Postgres[(PostgreSQL host)]
  App --> Redis[(Redis host)]
  App --> Kafka[(Kafka - Confluent Cloud)]
```

Notes:
- Backend is published on loopback and proxied via Nginx.
- Redis and PostgreSQL are local to the host.
- Kafka uses Confluent Cloud in application.yml.
