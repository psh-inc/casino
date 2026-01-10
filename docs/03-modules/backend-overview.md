# Backend Overview (casino-b)

## Purpose

Casino Core is the primary backend service providing REST APIs, WebSocket updates, and Kafka events for all casino domains.

## Package layout

- controller/: REST endpoints (admin, customer, public, integration)
- service/: business logic
- repository/: JPA repositories
- domain/: JPA entities
- kafka/: event publishers, consumers, and topics
- security/: JWT and security filters
- sports/: BetBy integration module
- campaigns/: external campaign integration

## Runtime

- Kotlin 2.3.x + Spring Boot 3.2.x
- Java 21
- PostgreSQL, Redis, Kafka

## Key interfaces

- REST: /api/v1/*
- WebSocket: /ws (STOMP)
- Kafka topics: casino.*.v1
