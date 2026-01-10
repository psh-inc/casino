# Observability Architecture

## Application telemetry

- Spring Actuator endpoints enabled: /actuator/health, /actuator/info, /actuator/prometheus
- Logging: SLF4J + Logback with structured logs
- Logs explorer: OpenSearch integration for admin logs explorer

## Infrastructure monitoring (from infra/PRODUCTION_AUDIT_2025-12-14.md)

- Prometheus + exporters bound to localhost
- Alertmanager for alert routing
- Nginx access/error logs on host

## Recommended dashboards (TODO)

- API latency, error rate, and throughput
- Wallet transaction volume and failure rate
- Bonus conversion and wagering completion
- WebSocket connection count and message rate
- Kafka publish and DLQ rates
