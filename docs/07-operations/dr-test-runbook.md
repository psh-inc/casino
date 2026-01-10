# DR Test Runbook

Status: Not defined in repo (RTO/RPO and DR environment are not specified in code)

Suggested steps:
1. Restore PostgreSQL from latest backup into DR environment.
2. Restore Redis if needed (or warm caches).
3. Start backend container with production env file.
4. Validate /actuator/health and key workflows (login, wallet, game launch).
5. Record recovery time and data loss window.
