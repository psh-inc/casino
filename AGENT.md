# AI Code Agent Guide - Casino Platform

Last Updated: 2026-01-10
Owner: Platform Engineering + Product
Status: Draft

## Purpose

Defines how an AI agent should work in this repo and submodules.

## Entry points

- docs/00-ai-agent-implementation-plan.md
- docs/03-modules/README.md
- specs/README.md
- AGENTS.md (submodule workflow)
- CLAUDE.md (coding standards)

## Tech stack

- Backend: Kotlin 2.3.x, Spring Boot 3.2.x, Java 21
- Database: PostgreSQL 14+ (17 in production audit)
- Cache: Redis + Caffeine
- Eventing: Kafka (Confluent Cloud)
- Admin frontend: Angular 17, TypeScript 5.2, NGRX
- Customer frontend: Angular 17, TypeScript 5.4, i18n XLF
- Shared library: TypeScript

## Operating rules

- Work inside submodules for code changes (casino-b, casino-f, casino-customer-f, casino-shared).
- Push submodule changes first, then update the root submodule reference.
- Never force-push to master unless explicitly approved.
- Update docs/specs for behavior changes.
- Avoid introducing new features outside task scope.

## Testing

- Backend: ./gradlew clean build
- Admin frontend: npm install && ng build
- Customer frontend: npm install && ng build

## Security reminders

- Do not commit secrets or keys.
- Redact sensitive data in logs.
- Enforce JWT auth for APIs and WebSocket.
