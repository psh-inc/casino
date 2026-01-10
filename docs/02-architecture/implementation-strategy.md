# Implementation Strategy

## Backend patterns

- Controller -> Service -> Repository layering.
- JPA/Hibernate persistence with PostgreSQL.
- Multi-level caching: Caffeine (L1) + Redis (L2).
- Event publishing via Kafka with retry and DLQ.
- Resilience with circuit breakers for external APIs.

## Data rules (from CLAUDE.md)

- Use BIGSERIAL for IDs.
- Use TIMESTAMP WITH TIME ZONE for date/time.
- Use BigDecimal created from String for monetary values.

## Frontend patterns

- Admin SPA: Angular modules for feature domains.
- Customer SPA: Angular standalone components and feature folders.
- State management: RxJS and NGRX (admin).

## Security rules

- JWT for API auth; RBAC for admin endpoints.
- Never store passwords unhashed (BCrypt/Argon2).
- Parameterized queries only.

## Testing strategy

- Backend: JUnit5 + MockK + Testcontainers.
- Frontend: Jasmine/Karma + Playwright (customer E2E).
