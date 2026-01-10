# DR Test Runbook

Status: TODO (define RTO/RPO and DR environment)

Suggested steps:
1. Restore PostgreSQL from latest backup into DR environment.
2. Restore Redis if needed (or warm caches).
3. Start backend container with production env file.
4. Validate /actuator/health and key workflows (login, wallet, game launch).
5. Record recovery time and data loss window.
