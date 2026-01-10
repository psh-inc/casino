# Observability Architecture

## Application telemetry

- Spring Actuator endpoints enabled: /actuator/health, /actuator/info, /actuator/prometheus
- Logging: SLF4J + Logback with structured logs
- Logs explorer: OpenSearch integration for admin logs explorer

## Infrastructure monitoring (from infra/PRODUCTION_AUDIT_2025-12-14.md)

- Prometheus + exporters bound to localhost
- Alertmanager for alert routing
- Nginx access/error logs on host

## Recommended dashboards

- API latency, error rate, throughput (Actuator + gateway logs)
- Wallet metrics: transaction volume, balance updates, failure rate (`WalletMetricsController`)
- Bonus lifecycle: awards, wagering progress, forfeits (`BonusAnalyticsController`)
- WebSocket activity: session count, message rate (STOMP topics + logs)
- Kafka publish rates, retries, DLQ volume (`KafkaAdminController`)
- Reporting pipeline health (`AggregationMonitoringController`)
