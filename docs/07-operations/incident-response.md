# Incident Response

## Severity levels

- SEV1: full outage or financial integrity risk
- SEV2: partial outage or severe performance degradation
- SEV3: localized defects or degraded UX

## Triage checklist

1. Check health endpoint: /actuator/health
2. Review recent deploys and config changes
3. Inspect application logs and Nginx logs
4. Verify database and Redis connectivity
5. Check Kafka publish/consume health (if relevant)

## Communication

- Create incident channel
- Notify on-call and product owner
- Record timeline and actions

## Post-incident

- Create RCA and mitigation tasks
- Update runbooks
