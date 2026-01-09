# CLAUDE.md - Online Casino Platform

An enterprise-grade online casino platform with player management, wallet systems, bonus mechanics, game integration, and sports betting. Built with Kotlin/Spring Boot backend and Angular 17 frontends.

## Quick Reference

| Component | Technology | Location | Port |
|-----------|------------|----------|------|
| Backend | Kotlin 2.3 / Spring Boot 3.2.5 / Java 21 | `casino-b/` | 8080 |
| Admin Frontend | Angular 17 / TypeScript 5.2 | `casino-f/` | 4200 |
| Customer Frontend | Angular 17 (standalone) / TypeScript 5.4 | `casino-customer-f/` | 4201 |
| Database | PostgreSQL 14+ | DigitalOcean managed | 25060 |
| Cache | Redis + Caffeine (multi-level) | - | 6379 |
| Message Broker | Apache Kafka (Confluent Cloud) | - | 9092 |
| API Docs | Swagger/OpenAPI 3.0 | `/swagger-ui.html` | - |

## Critical Rules

1. **NEVER** add features not in the current task
2. **ALWAYS** verify builds before submitting: `./gradlew clean build` and `ng build`
3. **ALWAYS** use `BIGSERIAL` for database IDs, never `SERIAL`
4. **NEVER** store passwords unhashed (use BCrypt/Argon2)
5. **ALWAYS** use `BigDecimal` from String: `BigDecimal("123.45")` (never from double)
6. **ALWAYS** use `TIMESTAMP WITH TIME ZONE` for dates in PostgreSQL
7. **ALWAYS** document API changes in `casino-b/docs/api/`
8. **ALWAYS** use parameterized queries via JPA (never string concatenation)

## Monorepo Setup

This project uses **Git submodules** to manage three independent repositories as a unified monorepo:

| Repo | Remote | Purpose |
|------|--------|---------|
| `casino-b/` | `git@github.com:psh-inc/core.git` | Backend (Kotlin/Spring Boot) |
| `casino-f/` | `git@github.com:psh-inc/cadmin.git` | Admin Frontend (Angular) |
| `casino-customer-f/` | `git@github.com:psh-inc/casino-customer-f.git` | Customer Frontend (Angular) |

Each repo maintains its own git history, branch, and remote. The root monorepo tracks them at specific commit points.

### Cloning the Monorepo

```bash
# Clone with all submodules (recursive)
git clone --recurse-submodules <root-repo-url>

# Or if already cloned without submodules
git submodule update --init --recursive
```

### Working with Submodules

```bash
# View submodule status
git submodule status

# Pull latest from all submodule remotes
git submodule update --remote

# Work in a specific submodule
cd casino-b
git add .
git commit -m "feat: new feature"
git push origin master

# Update root repo to track new submodule commits
cd ..
git add casino-b
git commit -m "chore: update casino-b submodule"
git push
```

### Important Submodule Rules

- **Each repo is independent**: Push changes directly to the submodule's remote
- **Root tracks commits**: The root monorepo records which commit of each submodule is "current"
- **Always push twice**:
  1. Push changes within the submodule to its remote
  2. Push the root repo to record the new commit reference
- **Keep submodules in sync**: Run `git submodule update --remote` before major operations

## Quick Start

```bash
# Prerequisites: Java 21+, Node.js 18+, PostgreSQL 14+, Redis 6+

# Backend
cd casino-b
cp ../.env.example .env  # Configure database credentials
./gradlew clean build
./gradlew bootRun        # Runs on http://localhost:8080

# Admin Frontend
cd casino-f
npm install
ng serve                 # Runs on http://localhost:4200

# Customer Frontend
cd casino-customer-f
npm install
ng serve                 # Runs on http://localhost:4201
```

## Project Structure

```
casino/
├── casino-b/                        # Backend (Kotlin/Spring Boot)
│   ├── src/main/kotlin/com/casino/core/
│   │   ├── controller/              # REST controllers (101 files)
│   │   ├── service/                 # Business logic (140 files)
│   │   ├── repository/              # JPA repositories (112 files)
│   │   ├── domain/                  # JPA entities (107 files)
│   │   ├── dto/                     # Data transfer objects (104 files)
│   │   ├── kafka/                   # Kafka producers/consumers/config
│   │   ├── security/                # JWT, OAuth2, guards
│   │   ├── config/                  # Spring configuration (29 files)
│   │   ├── event/                   # Domain events
│   │   ├── scheduler/               # Scheduled tasks
│   │   └── sports/                  # BetBy sports integration
│   ├── src/main/resources/
│   │   ├── db/migration/            # Flyway migrations (V{timestamp}__{name}.sql)
│   │   └── application.yml          # Main configuration
│   ├── src/test/kotlin/             # Unit & integration tests
│   └── docs/api/                    # API documentation
│
├── casino-f/                        # Admin Frontend (Angular)
│   └── src/app/
│       ├── modules/                 # Feature modules (17 modules)
│       │   ├── player-management/   # Player CRUD, KYC, wallet, bets
│       │   ├── game-management/     # Games, providers, restrictions
│       │   ├── campaigns/           # Marketing campaigns
│       │   ├── cms/                 # Content management
│       │   ├── reporting/           # Analytics & reports
│       │   ├── payments/            # Payment processing
│       │   └── ...
│       ├── core/                    # Guards, interceptors, services
│       ├── shared/                  # Shared UI components (ui-*)
│       └── services/                # Global services
│
├── casino-customer-f/               # Customer Frontend (Angular standalone)
│   └── src/app/
│       ├── features/                # Feature modules (14 features)
│       │   ├── games/               # Casino games, search, filters
│       │   ├── wallet/              # Deposits, withdrawals
│       │   ├── promotions/          # Bonus claiming
│       │   ├── sports/              # BetBy sports betting
│       │   ├── account/             # Profile, settings
│       │   ├── kyc/                 # Document verification
│       │   └── ...
│       ├── core/                    # Guards, interceptors, models
│       └── shared/                  # Shared components
│
├── infra/                           # Production deployment configs
├── scripts/                         # Build/deployment scripts
└── .claude/                         # Claude Code configuration
    ├── agents/                      # Custom agent definitions
    └── skills/                      # Custom skills (metabase-api)
```

## Architecture Overview

### Multi-Level Caching Strategy
```
Request → Caffeine (L1, in-memory) → Redis (L2, distributed) → Database
```
- **L1 Cache**: Caffeine with 10K max entries, 5s TTL for hot data
- **L2 Cache**: Redis with 30s active TTL, 300s inactive TTL
- Cache keys use `CacheKeyGenerator` for consistency

### Event-Driven Architecture (Kafka)
```
Service → AsyncKafkaPublisher → Circuit Breaker → Kafka (Confluent Cloud)
                ↓ (on failure)
         FailedKafkaEvent table → Retry Job → Dead Letter Queue
```

#### Kafka Topics (defined in `KafkaTopics.kt`)
| Domain | Topics |
|--------|--------|
| Player | `casino.player.registered.v1`, `casino.player.profile-updated.v1`, `casino.player.status-changed.v1`, `casino.player.session-started.v1` |
| Payment | `casino.payment.deposit-created.v1`, `casino.payment.deposit-completed.v1`, `casino.payment.withdrawal-created.v1`, `casino.payment.withdrawal-completed.v1` |
| Game | `casino.game.session-started.v1`, `casino.game.bet-placed.v1`, `casino.game.win-awarded.v1`, `casino.game.round-completed.v1` |
| Bonus | `casino.bonus.offered.v1`, `casino.bonus.activated.v1`, `casino.bonus.wagering-updated.v1`, `casino.bonus.converted.v1`, `casino.bonus.forfeited.v1` |
| Compliance | `casino.compliance.kyc-submitted.v1`, `casino.compliance.kyc-approved.v1`, `casino.compliance.level-upgraded.v1`, `casino.compliance.self-excluded.v1` |
| Sports | `casino.sports.bet-placed.v1`, `casino.sports.bet-settled.v1` |
| System | `casino.dlq.all.v1` (Dead Letter Queue) |

### WebSocket Real-Time Updates
- Endpoint: `/ws` (STOMP over WebSocket)
- Topics: `/topic/balance/{playerId}`, `/topic/bonus/{playerId}`, `/topic/wagering/{playerId}`

## Code Patterns

### Backend Controller Pattern
```kotlin
@RestController
@RequestMapping("/api/v1/resources")
@Tag(name = "Resources", description = "Resource management API")
class ResourceController(
    private val resourceService: ResourceService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @GetMapping
    @Operation(summary = "List resources with pagination")
    fun list(@PageableDefault(size = 20) pageable: Pageable): Page<ResourceDto> {
        return resourceService.findAll(pageable)
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun create(@Valid @RequestBody request: CreateResourceRequest): ResourceDto {
        return resourceService.create(request)
    }
}
```

### Backend Service Pattern
```kotlin
@Service
@Transactional
class ResourceService(
    private val repository: ResourceRepository,
    private val cacheManager: CacheManager
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Cacheable(value = ["resources"], key = "#id")
    fun findById(id: Long): ResourceDto {
        val resource = repository.findById(id)
            .orElseThrow { ResourceNotFoundException("Resource not found: $id") }
        return ResourceDto.from(resource)
    }

    @CacheEvict(value = ["resources"], key = "#result.id")
    fun create(request: CreateResourceRequest): ResourceDto {
        logger.info("Creating resource: ${request.name}")
        val resource = Resource(name = request.name)
        return ResourceDto.from(repository.save(resource))
    }
}
```

### Backend Entity Pattern
```kotlin
@Entity
@Table(name = "players")
data class Player(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,

    @Column(nullable = false, unique = true)
    val username: String,

    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now(ZoneOffset.UTC),

    @Column(name = "balance", precision = 19, scale = 2)
    val balance: BigDecimal = BigDecimal.ZERO
)
```

### Kafka Event Pattern
```kotlin
@Service
class PlayerEventService(
    private val eventPublisher: EventPublisher,
    private val metadataBuilder: EventMetadataBuilder
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    fun publishPlayerRegistered(player: Player) {
        try {
            val event = PlayerRegisteredEvent(
                eventId = EventBuilder.generateEventId(),
                eventTimestamp = EventBuilder.getCurrentTimestamp(),
                userId = player.id.toString(),
                payload = PlayerRegisteredPayload(
                    username = player.username,
                    email = player.email
                )
            )
            eventPublisher.publish(
                topic = KafkaTopics.PLAYER_REGISTERED,
                key = player.id.toString(),
                event = event
            )
            logger.info("Published player registered event: ${player.id}")
        } catch (e: Exception) {
            logger.error("Failed to publish event: ${player.id}", e)
            // Don't throw - event publishing should not break main flow
        }
    }
}
```

### Frontend Service Pattern (Angular)
```typescript
@Injectable({ providedIn: 'root' })
export class ResourceService {
  private apiUrl = `${environment.apiUrl}/resources`;

  constructor(private http: HttpClient) {}

  list(page = 0, size = 20): Observable<Page<Resource>> {
    const params = new HttpParams()
      .set('page', page)
      .set('size', size);
    return this.http.get<Page<Resource>>(this.apiUrl, { params });
  }

  create(request: CreateResourceRequest): Observable<Resource> {
    return this.http.post<Resource>(this.apiUrl, request).pipe(
      catchError(error => {
        console.error('Failed to create resource', error);
        return throwError(() => error);
      })
    );
  }
}
```

### Frontend Component Pattern (Standalone)
```typescript
@Component({
  selector: 'app-resource-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './resource-list.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ResourceListComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  resources$ = new BehaviorSubject<Resource[]>([]);

  constructor(private resourceService: ResourceService) {}

  ngOnInit() {
    this.resourceService.list().pipe(
      takeUntil(this.destroy$),
      map(page => page.content)
    ).subscribe(resources => this.resources$.next(resources));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Database Guidelines

### Flyway Migration Naming
- Format: `V{timestamp}__{description}.sql` (e.g., `V20250115120000__add_user_table.sql`)
- Timestamp: `yyyyMMddHHmmss` in UTC
- Configuration: `out-of-order: true` enabled for development flexibility

### Data Type Mapping
| SQL Type | Kotlin Type | Notes |
|----------|-------------|-------|
| `BIGSERIAL` | `Long` | Always use BIGSERIAL, never SERIAL |
| `DECIMAL(19,2)` | `BigDecimal` | Create from String only |
| `TIMESTAMP WITH TIME ZONE` | `LocalDateTime` | Always UTC |
| `JSONB` | Custom/String | Use for structured data |
| `TEXT` | `String` | For long content |
| `VARCHAR(n)` | `String` | For limited content |

### BigDecimal Usage
```kotlin
// CORRECT - from String
val amount = BigDecimal("123.45")
val zero = BigDecimal.ZERO

// WRONG - from double (precision loss!)
val amount = BigDecimal(123.45) // DON'T DO THIS

// Comparisons
if (amount.compareTo(BigDecimal.ZERO) > 0) { ... }
```

## API Standards

### REST Endpoints
| Method | Path | Action | Status |
|--------|------|--------|--------|
| GET | `/api/v1/resources` | List (paginated) | 200 |
| GET | `/api/v1/resources/{id}` | Get single | 200/404 |
| POST | `/api/v1/resources` | Create | 201 |
| PUT | `/api/v1/resources/{id}` | Full update | 200 |
| PATCH | `/api/v1/resources/{id}` | Partial update | 200 |
| DELETE | `/api/v1/resources/{id}` | Delete | 204 |

### Pagination Response
```json
{
  "content": [...],
  "totalElements": 100,
  "totalPages": 5,
  "size": 20,
  "number": 0,
  "first": true,
  "last": false
}
```

### Error Response
```json
{
  "status": "ERROR",
  "code": "VALIDATION_FAILED",
  "message": "Validation failed",
  "timestamp": "2024-01-15T10:30:00Z",
  "details": {
    "fields": {
      "email": "Invalid email format"
    }
  }
}
```

### HTTP Status Codes
- `200` - Success (GET, PUT, PATCH)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Validation Error
- `500` - Internal Server Error

## Naming Conventions

### Backend (Kotlin) - File & Code
| Type | Convention | Example |
|------|------------|---------|
| Files | PascalCase.kt | `PlayerService.kt`, `AuthController.kt` |
| Classes | PascalCase | `PlayerService`, `AuthController` |
| Functions | camelCase | `findUserById`, `createGame` |
| Properties | camelCase | `firstName`, `createdAt` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Packages | lowercase | `com.casino.core.service` |

### Frontend (TypeScript) - File & Code
| Type | Convention | Example |
|------|------------|---------|
| Component Files | kebab-case | `player-list.component.ts` |
| Service Files | kebab-case | `players.service.ts` |
| Model Files | kebab-case | `player.model.ts` |
| Component Classes | PascalCase | `PlayerListComponent` |
| Service Classes | PascalCase | `PlayersService` |
| Interfaces | PascalCase | `Player` (not `IPlayer`) |
| Variables | camelCase | `isLoading`, `playerData` |
| Constants | UPPER_SNAKE_CASE | `API_URL` |

### Database
| Type | Convention | Example |
|------|------------|---------|
| Tables | snake_case, plural | `players`, `game_sessions` |
| Columns | snake_case | `created_at`, `user_id` |
| Indexes | `idx_table_column` | `idx_players_email` |
| Foreign Keys | `fk_table_reference` | `fk_wallets_player` |

### TypeScript Path Aliases (Admin Frontend)
```typescript
// tsconfig.json paths:
@core/*     → src/app/core/*
@shared/*   → src/app/shared/*
@auth/*     → src/app/auth/*
@modules/*  → src/app/modules/*
@environments/* → src/environments/*
```

## Security

### Authentication Flow
1. POST `/api/auth/login` with username/password (supports email login)
2. Receive JWT access token (2-hour expiry)
3. Include `Authorization: Bearer {token}` in subsequent requests
4. Token validated by OAuth2 Resource Server

### Security Rules
- Passwords: BCrypt (cost 12+) or Argon2
- JWT: Minimum 64 characters for HS512
- Input: Jakarta validation on all DTOs
- SQL: JPA parameterized queries only
- CORS: Configured in `WebMvcConfig`
- Frontend tokens: SessionStorage (cleared on tab close)

### Validation Example
```kotlin
data class CreateUserRequest(
    @field:NotBlank(message = "Email is required")
    @field:Email(message = "Invalid email format")
    val email: String,

    @field:NotBlank(message = "Password is required")
    @field:Size(min = 8, max = 100)
    val password: String
)
```

## Testing

### Backend Testing Stack
- **Framework**: JUnit 5, MockK (not Mockito)
- **Integration**: `@SpringBootTest`, Testcontainers
- **Repository**: `@DataJpaTest`
- **Location**: `casino-b/src/test/kotlin/com/casino/core/`
- **Coverage Target**: 80% for services

```bash
./gradlew test                          # Run all tests
./gradlew test --tests "*ServiceTest"   # Run service tests
./gradlew jacocoTestReport              # Generate coverage report
```

### Frontend Testing Stack
- **Unit Tests**: Jasmine/Karma
- **E2E Tests**: Playwright
- **Coverage Target**: 70% for services

```bash
# Admin frontend
cd casino-f
ng test

# Customer frontend
cd casino-customer-f
ng test
playwright test            # E2E tests
playwright test --ui       # Interactive mode
```

## Available Commands

### Backend
| Command | Description |
|---------|-------------|
| `./gradlew clean build` | Build and run all tests |
| `./gradlew bootRun` | Start development server |
| `./gradlew test` | Run tests |
| `./gradlew flywayMigrate` | Run database migrations |
| `./gradlew jacocoTestReport` | Generate test coverage |

### Admin Frontend (`casino-f/`)
| Command | Description |
|---------|-------------|
| `ng serve` | Start dev server (4200) |
| `ng build` | Production build |
| `ng test` | Run unit tests |
| `ng lint` | Run ESLint |
| `npm run storybook` | Start Storybook |

### Customer Frontend (`casino-customer-f/`)
| Command | Description |
|---------|-------------|
| `ng serve` | Start dev server (4201) |
| `ng serve --configuration de` | Start with German locale |
| `ng build --configuration production` | Production build |
| `ng extract-i18n` | Extract translation strings |
| `playwright test` | Run E2E tests |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SPRING_DATASOURCE_URL` | Yes | PostgreSQL connection URL |
| `SPRING_DATASOURCE_USERNAME` | Yes | Database username |
| `SPRING_DATASOURCE_PASSWORD` | Yes | Database password |
| `JWT_SECRET` | Yes | JWT signing key (64+ chars for HS512) |
| `REDIS_HOST` | No | Redis host (default: localhost) |
| `KAFKA_BOOTSTRAP_SERVERS` | No | Kafka servers |
| `SENDGRID_API_KEY` | Yes | Email service API key |
| `TWILIO_ACCOUNT_SID` | Yes | SMS service account |
| `TWILIO_AUTH_TOKEN` | Yes | SMS service token |
| `DO_SPACES_ACCESS_KEY` | Yes | DigitalOcean Spaces (S3) |
| `DO_SPACES_SECRET_KEY` | Yes | DigitalOcean Spaces secret |
| `CLAUDE_API_KEY` | No | Claude AI for KYC analysis |

See `.env.example` for full list.

## Key Integrations

| Integration | Purpose | Configuration Key |
|-------------|---------|-------------------|
| BetBy | Sports betting | `betby.*` |
| SendGrid | Email delivery | `sendgrid.api-key` |
| Twilio | SMS verification | `twilio.*` |
| DigitalOcean Spaces | File storage (S3-compatible) | `digitalocean.spaces.*` |
| Confluent Cloud | Kafka messaging | `spring.kafka.*` |
| OpenSearch | Exception logging | `opensearch.*` |
| Claude AI | KYC document analysis | `claude.api.*` |
| Smartico | Gamification | `smartico.*` |
| Cellxpert | Affiliate tracking | via `CellxpertService` |

## Internationalization (i18n)

### Customer Frontend
- Uses Angular i18n with `.xlf` files
- Locale routing: `/en/`, `/de/`, `/fr/`, `/es/`
- Start with locale: `ng serve --configuration de`
- Extract strings: `ng extract-i18n`

### Backend
- Locale stored in `Player.locale`
- Content localization via `ContentLocalization` entity
- Translation keys in `Translation` and `TranslationKey` tables

## Common Issues

### CORS Error
Check `WebMvcConfig` CORS configuration, ensure origin matches frontend URL.

### 401 Unauthorized
Verify JWT token in request headers, check JWT secret length (64+ chars).

### Database Connection
Verify `SPRING_DATASOURCE_*` environment variables are set correctly.

### Build Failures
```bash
./gradlew clean                # Clear Gradle cache
rm -rf node_modules && npm i   # Clear npm cache
```

### Type Mismatch in JPA
Ensure `BIGSERIAL` → `Long`, `DECIMAL` → `BigDecimal`, `TIMESTAMP WITH TIME ZONE` → `LocalDateTime`.

## Git Commit Conventions

```
[Component] Brief description

Longer explanation if needed.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Component Prefixes
`[Auth]` `[Player]` `[Game]` `[Bonus]` `[Wallet]` `[DB]` `[UI]` `[API]` `[Fix]` `[Perf]` `[Refactor]` `[Kafka]` `[Sports]` `[KYC]` `[CMS]`

## Pre-Submit Checklist

- [ ] `./gradlew clean build` passes
- [ ] `ng build` passes (both frontends)
- [ ] No hardcoded values (use config/constants)
- [ ] Proper error handling
- [ ] API documented if new endpoint
- [ ] Database migrations use BIGSERIAL and TIMESTAMP WITH TIME ZONE
- [ ] BigDecimal created from String
- [ ] Observable subscriptions cleaned up with `takeUntil`
- [ ] Follows project naming conventions
- [ ] No sensitive data in logs

### Common Mistakes to Avoid
- Using SERIAL instead of BIGSERIAL
- Storing passwords unhashed
- Creating BigDecimal from double
- Forgetting CORS configuration
- Not validating user input
- Memory leaks (not unsubscribing from Observables)
- Exposing sensitive data in logs
- Adding features not in requirements
- Throwing exceptions in Kafka event publishers (use fire-and-forget pattern)
- Using `==` or `!=` for BigDecimal comparison (use `compareTo()`)

## Key Domain Entities

### Player Entity (excerpt)
The `Player` entity is central to the platform. Key fields include:
- **Status**: `PENDING`, `ACTIVE`, `FROZEN`, `BLOCKED`, `SUSPENDED`, `SELF_EXCLUDED`, `COOLING_OFF`
- **KYC Status**: Simple KYC system (`SimpleKycStatus`) with `NONE`, `PARTIAL`, `PENDING_REVIEW`, `VERIFIED`, `REJECTED`
- **Activation Steps**: `EMAIL_PENDING` → `EMAIL_VERIFIED` → `PROFILE_COMPLETED` → `PHONE_VERIFIED` → `KYC_VERIFIED` → `FULLY_ACTIVATED`
- **Restrictions**: `depositsRestricted`, `withdrawalsRestricted`, `allBonusesRestricted`, `bonusGameRestricted`
- **Security**: `failedLoginAttempts`, `blockedUntil`, `twoFactorEnabled`

### Wallet System
- **Multi-currency**: Each player has wallets per currency
- **Balance Types**: `realBalance`, `bonusBalance`, `lockedBalance`
- **Transaction Types**: Deposits, withdrawals, bets, wins, bonuses, refunds

### Bonus System
- **Types**: `DEPOSIT`, `NTH_DEPOSIT`, `ANY_DEPOSIT`, `RELOAD`, `NO_DEPOSIT`
- **Activation**: `AUTOMATIC`, `MANUAL_CLAIM`, `DEPOSIT_SELECTION`
- **Rewards**: Money bonuses, free spins, sports bonuses
- **Wagering**: Configurable multipliers, mode (bonus only vs deposit+bonus)

---

**Project Status**: Active development
**Last Updated**: 2025-01-05


## Skill Usage Guide

When working on tasks involving these technologies, invoke the corresponding skill:

| Skill | Invoke When |
|-------|-------------|
| kafka | Apache Kafka event publishing, topics, and async message handling |
| redis | Redis caching with Spring Cache abstraction and Caffeine L1 cache |
| jpa | JPA entities, repositories, and Hibernate ORM patterns |
| postgresql | PostgreSQL database design, Flyway migrations, and JPA queries |
| jasmine | Jasmine/Karma unit testing for Angular components and services |
| typescript | TypeScript type patterns and strict mode |
| spring-boot | Spring Boot 3.2.5 REST controllers, services, and configuration |
| playwright | Playwright E2E testing for customer frontend |
| angular | Angular 17 components, services, routing, and reactive patterns |
| kotlin | Kotlin language patterns, coroutines, and Spring Boot integration |
| frontend-design | Angular UI components with CSS styling and responsive design |
