# Epic: Phase 05 - Production Readiness

## Objective

Prepare the platform for production deployment with hardened infrastructure and validated operational procedures.

## Stories

- STORY-PR-001: Harden Docker Compose deployment
  - Use loopback-only exposure and non-root container
  - Verify env file and secret injection

- STORY-PR-002: Nginx reverse proxy and CORS
  - Enforce HTTPS, HSTS, and rate limiting
  - Restrict Swagger access

- STORY-PR-003: Monitoring baseline
  - Confirm /actuator/prometheus
  - Deploy Prometheus + Alertmanager on localhost

## Acceptance criteria

- Backend reachable only through Nginx
- Health checks pass with /actuator/health
- Monitoring endpoints available and documented
