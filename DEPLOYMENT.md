# Deployment Guide - Casino Platform

This guide summarizes deployment based on infra/ configuration.

## Production topology

- Cloudflare/WAF -> Nginx (api.betportal.com) -> casino-core container
- PostgreSQL and Redis on host (loopback-only)
- Kafka on Confluent Cloud

## Backend deployment (Docker Compose)

1. Copy infra/docker-compose.production.yml to the server as docker-compose.yml
2. Create /root/.env.casino with secrets (chmod 600)
3. Start services:
   - docker compose up -d
4. Verify health:
   - curl http://127.0.0.1:8080/actuator/health

## Nginx configuration

- Use infra/nginx-api.betportal.com.conf
- Enable HTTPS via certbot
- Ensure CORS origins are whitelisted

## Environment variables

Required (examples):
- SPRING_DATASOURCE_URL
- SPRING_DATASOURCE_USERNAME
- SPRING_DATASOURCE_PASSWORD
- JWT_SECRET
- REDIS_HOST / REDIS_PASSWORD
- KAFKA_BOOTSTRAP_SERVERS
- SENDGRID_API_KEY
- TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN

See .env.example and infra/docker-compose.production.yml for full list.

## Troubleshooting

- If API is unreachable, confirm Nginx proxy_pass and backend health endpoint.
- If database errors occur, verify DB connectivity and credentials.
- If Redis errors occur, verify Redis host/port and password.
- If Kafka errors occur, verify bootstrap servers and credentials.

## References

- infra/PRODUCTION_AUDIT_2025-12-14.md
- infra/docker-compose.production.yml
- infra/nginx-api.betportal.com.conf
