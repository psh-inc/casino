# GEMINI.md - Agent Context & Instructions

## Project Overview
**Casino Platform** is a full-stack online casino application.
- **Backend**: Kotlin / Spring Boot (in `casino-b/`)
- **Admin Frontend**: Angular / TypeScript (in `casino-f/`)
- **Customer Frontend**: Angular / TypeScript (in `casino-customer-f/`)
- **Infrastructure**: Docker, PostgreSQL, Redis, Kafka.

## Quick Reference: Commands

### Backend (`casino-b`)
*   **Build**: `./gradlew clean build`
*   **Run**: `./gradlew bootRun` (Runs on `localhost:8080`)
*   **Test**: `./gradlew test`
*   **Docs**: `http://localhost:8080/swagger-ui.html`

### Admin Frontend (`casino-f`)
*   **Install**: `npm install`
*   **Run**: `ng serve` (Runs on `localhost:4200`)
*   **Test**: `ng test`

### Customer Frontend (`casino-customer-f`)
*   **Install**: `npm install`
*   **Run**: `npm start` (Runs on `localhost:4200` - check port if running both)
*   **Test**: `npm test`
*   **E2E**: `npm run e2e` (Playwright)

### Infrastructure
*   **Start All**: `docker-compose up -d`
*   **Logs**: `docker-compose logs -f`

## Critical Development Rules
1.  **IDs**: ALWAYS use `BIGSERIAL` in SQL and `Long` in Kotlin. Never `SERIAL`.
2.  **Money**: ALWAYS use `BigDecimal` initialized from **String** (e.g., `BigDecimal("10.00")`). Never from double.
3.  **Dates**: ALWAYS use `TIMESTAMP WITH TIME ZONE` in SQL.
4.  **Security**: NEVER store plain-text passwords. Use BCrypt.
5.  **Verification**: ALWAYS run `./gradlew clean build` before considering a backend task complete.

## Code Patterns

### Backend (Kotlin/Spring)
*   **Controller**: `@RestController`, `@RequestMapping("/api/v1/...")`, returns DTOs.
*   **Service**: `@Service`, `@Transactional`, handles business logic.
*   **Repository**: Spring Data JPA interfaces.
*   **Entity**: JPA `@Entity` with immutable properties (`val`) where possible.
*   **DTOs**: Data classes for API requests/responses.

### Frontend (Angular)
*   **Architecture**: Feature modules (Admin) or Standalone components (Customer).
*   **State**: RxJS (`BehaviorSubject`, `Observable`).
*   **HTTP**: Typed `HttpClient` calls in services.

## Database & Migrations
*   **Tool**: Flyway.
*   **Location**: `casino-b/src/main/resources/db/migration/`
*   **Naming**: `V{timestamp}__{description}.sql` (e.g., `V20251118120000__add_table.sql`)
*   **Timestamp**: `yyyyMMddHHmmss`

## Git Conventions
*   **Format**: `[Component] Brief description`
*   **Examples**:
    *   `[Wallet] Fix transaction calculation`
    *   `[Auth] Add login endpoint`
    *   `[UI] Update dashboard layout`

## Documentation
*   **API**: `docs/submodules/casino-b/api/`
*   **Deployment**: `DEPLOYMENT.md`
*   **Guidelines**: `CLAUDE.md` (Detailed reference)
