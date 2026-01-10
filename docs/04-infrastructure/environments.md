# Environments and Deployment

## Environments

### Local development

- Backend: run casino-b with .env (see .env.example)
- Admin SPA: casino-f (ng serve)
- Customer SPA: casino-customer-f (ng serve)
- Dependencies: local PostgreSQL, Redis, Kafka (optional)

### Staging (TODO)

No staging environment definition is present in repo. Define:
- Hostnames
- Data isolation and anonymization
- Monitoring and alerting

### Production

Infra docs describe production hardening and reverse proxy:
- Docker Compose: infra/docker-compose.production.yml
- Nginx: infra/nginx-api.betportal.com.conf
- Audit: infra/PRODUCTION_AUDIT_2025-12-14.md

## Key configuration variables

Backend (see .env.example and application.yml):
- SPRING_DATASOURCE_URL, SPRING_DATASOURCE_USERNAME, SPRING_DATASOURCE_PASSWORD
- JWT_SECRET, SECURITY_JWT_EXPIRATION
- SPRING_DATA_REDIS_HOST, SPRING_DATA_REDIS_PORT, SPRING_DATA_REDIS_PASSWORD
- SPRING_KAFKA_BOOTSTRAP_SERVERS
- SENDGRID_API_KEY, EMAIL_FROM
- TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
- DO_SPACES_ACCESS_KEY, DO_SPACES_SECRET_KEY, DO_SPACES_ENDPOINT
- BETBY_BRAND_ID, BETBY_PRIVATE_KEY_PATH

Frontend:
- casino-f: environment.apiUrl
- casino-customer-f: environment.apiUrl, environment.cmsApiUrl

## Deployment topology (prod)

- Client -> Cloudflare/WAF -> Nginx -> casino-core container
- PostgreSQL and Redis hosted on the same server (loopback-only)
- Kafka on Confluent Cloud

## Secrets management

- Secrets must be injected via env files or secret managers.
- Remove hard-coded secrets from repo (see security assessment).
