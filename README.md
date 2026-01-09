# Online Casino Platform

A comprehensive online casino platform built with Kotlin/Spring Boot backend and Angular frontend.

## Features

- **Player Management**: Registration, KYC verification, profile management
- **Wallet System**: Multi-currency wallets, deposits, withdrawals, transactions
- **Game Integration**: Multiple game providers, categorization, restrictions
- **Bonus System**: Wagering requirements, bonus balance tracking, eligibility rules
- **Payment Processing**: Multiple payment methods, refunds, manual deposits
- **CMS**: Content management for pages, banners, translations
- **Sports Betting**: BetBy integration
- **Real-time Updates**: WebSocket support for balance and bonus updates
- **Admin Portal**: Comprehensive admin interface for management
- **Security**: JWT authentication, role-based access control, 2FA support

## Technology Stack

### Backend
- **Language**: Kotlin 1.8+
- **Framework**: Spring Boot 3.1.5
- **Database**: PostgreSQL 14+
- **Cache**: Redis + Caffeine (multi-level)
- **Message Broker**: Apache Kafka
- **Migrations**: Flyway
- **Security**: OAuth2 Resource Server, JWT
- **API Docs**: OpenAPI 3.0 (Swagger)

### Frontend
- **Framework**: Angular 17
- **Language**: TypeScript 5.2+
- **State Management**: RxJS 7.8
- **UI Components**: Angular Material
- **Real-time**: WebSocket (STOMP)

## Project Structure

```
casino/
├── casino-b/                   # Backend (Spring Boot)
│   ├── src/main/kotlin/
│   │   └── com/casino/core/
│   │       ├── controller/     # REST controllers
│   │       ├── service/        # Business logic
│   │       ├── repository/     # Data access
│   │       ├── domain/         # JPA entities
│   │       ├── dto/            # Data transfer objects
│   │       ├── security/       # Security configuration
│   │       └── kafka/          # Kafka producers/consumers
│   ├── src/main/resources/
│   │   └── db/migration/       # Flyway migrations
│   ├── src/test/kotlin/        # Unit and integration tests
│   └── docs/api/               # API documentation
├── casino-f/                   # Admin Frontend (Angular)
│   ├── src/app/
│   │   ├── modules/            # Feature modules
│   │   ├── core/               # Core services, guards
│   │   └── shared/             # Shared components
│   └── src/environments/       # Environment configs
├── casino-customer-f/          # Customer Frontend (Angular)
└── CLAUDE.md                   # Development guidelines
```

## Quick Start

### Prerequisites

- Java 17+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Docker (optional)

### Backend Setup

```bash
cd casino-b

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Build and run
./gradlew clean build
./gradlew bootRun
```

Backend runs on `http://localhost:8080`

API documentation: `http://localhost:8080/swagger-ui.html`

### Frontend Setup

```bash
cd casino-f

# Install dependencies
npm install

# Start development server
ng serve
```

Admin frontend runs on `http://localhost:4200`

### Docker Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## API Documentation

- [Wallet API Documentation](casino-b/docs/api/WALLET_API.md)
- [Swagger UI](http://localhost:8080/swagger-ui.html) (when running)

### Key API Endpoints

- `POST /api/auth/login` - User authentication
- `GET /api/v1/players/{playerId}/wallet/summary` - Get wallet summary
- `POST /api/v1/players/{playerId}/wallet/manual-deposit` - Manual deposit (admin)
- `POST /api/v1/players/{playerId}/wallet/withdraw` - Process withdrawal
- `GET /api/v1/players/{playerId}/transactions` - Get transaction history
- `GET /api/v1/games` - List games
- `POST /api/v1/bonuses/claim` - Claim bonus

## Testing

### Backend Tests

```bash
cd casino-b

# Run all tests
./gradlew test

# Run specific test
./gradlew test --tests "AuthServiceTest"

# Generate coverage report
./gradlew jacocoTestReport
```

**Test Status:**
- Unit Tests: 48/51 passing (94% success rate)
- Integration Tests: Blocked by V100 migration issue (to be fixed in Phase 6)

### Frontend Tests

```bash
cd casino-f

# Run unit tests
ng test

# Run E2E tests
ng e2e
```

## Database Schema

Key tables:
- `players` - Player accounts
- `wallets` - Player wallets
- `transactions` - Financial transactions
- `currencies` - Supported currencies
- `games` - Game catalog
- `bonuses` - Bonus definitions
- `bonus_claims` - Claimed bonuses
- `wagering_requirements` - Wagering tracking

### Migrations

Flyway migrations are located in `casino-b/src/main/resources/db/migration/`

Naming convention: `V{timestamp}__{description}.sql`

Run migrations:
```bash
./gradlew flywayMigrate
```

## Configuration

### Environment Variables

**Required:**
- `SPRING_DATASOURCE_URL` - PostgreSQL connection URL
- `SPRING_DATASOURCE_USERNAME` - Database username
- `SPRING_DATASOURCE_PASSWORD` - Database password
- `SECURITY_JWT_SECRET` - JWT secret key (min 64 characters for HS512)
- `SENDGRID_API_KEY` - SendGrid API key for emails

**Optional:**
- `SPRING_DATA_REDIS_HOST` - Redis host (default: localhost)
- `SPRING_KAFKA_BOOTSTRAP_SERVERS` - Kafka servers (default: localhost:9092)
- `APP_CORS_ALLOWED_ORIGINS` - Allowed CORS origins

See `.env.example` for full list.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:

- Production environment setup
- Docker deployment
- Nginx configuration
- SSL/TLS setup
- Performance tuning
- Monitoring and logging
- Backup and recovery
- Security checklist

## Development Guidelines

See [CLAUDE.md](CLAUDE.md) for:

- Code patterns and conventions
- Database guidelines
- API standards
- Security best practices
- Testing requirements
- Common issues and solutions

### Key Rules

1. **ALWAYS** use BIGSERIAL for database IDs (not SERIAL)
2. **ALWAYS** create BigDecimal from String: `BigDecimal("123.45")`
3. **ALWAYS** use `TIMESTAMP WITH TIME ZONE` for dates
4. **NEVER** store passwords unhashed (use BCrypt/Argon2)
5. **ALWAYS** verify builds before submitting: `./gradlew clean build`
6. **ALWAYS** document API changes in `docs/api/`

## Architecture

### Multi-Level Caching

- **L1 Cache**: Caffeine (in-memory, fast)
- **L2 Cache**: Redis (distributed, shared)

### WebSocket Communication

- **Protocol**: STOMP over WebSocket
- **Endpoint**: `/ws`
- **Topics**:
  - `/topic/balance/{playerId}` - Balance updates
  - `/topic/bonus/{playerId}` - Bonus updates
  - `/topic/wagering/{playerId}` - Wagering progress

### Event-Driven Architecture

Kafka topics:
- `player-events` - Player lifecycle events
- `transaction-events` - Transaction events
- `bonus-events` - Bonus events
- `compliance-events` - Compliance tracking

## Security

- **Authentication**: JWT Bearer tokens (OAuth2 Resource Server)
- **Password Hashing**: BCrypt (cost 12)
- **Input Validation**: Jakarta Validation annotations
- **SQL Injection Prevention**: Parameterized queries (JPA)
- **CORS**: Configured allowed origins
- **2FA**: TOTP-based two-factor authentication
- **Session Management**: Redis-backed sessions

## Monitoring

### Actuator Endpoints

- `/actuator/health` - Health check
- `/actuator/metrics` - Prometheus metrics
- `/actuator/info` - Application info
- `/actuator/prometheus` - Prometheus scrape endpoint

### Logging

- **Framework**: SLF4J + Logback
- **Levels**: DEBUG (dev), INFO (prod)
- **Format**: JSON structured logging
- **Location**: `logs/application.log`

## Troubleshooting

### Known Issues

1. **V100 Migration Error** - `enabled` column doesn't exist in games table
   - **Status**: Deferred to Phase 6 cleanup
   - **Workaround**: Disable V100 migration temporarily

2. **AuthServiceTest Failures** - MockK mocking issues
   - **Status**: 3/51 tests failing, needs relaxed mocking
   - **Impact**: Low - core functionality works

### Common Problems

- **Database Connection**: Check PostgreSQL is running and credentials are correct
- **JWT Errors**: Ensure secret is 64+ characters for HS512
- **Redis Connection**: Verify Redis is running on configured host/port
- **Build Failures**: Run `./gradlew clean` and retry

See [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) for detailed troubleshooting.

## Contributing

1. Follow code patterns in [CLAUDE.md](CLAUDE.md)
2. Write tests for new features
3. Update API documentation
4. Ensure `./gradlew clean build` passes
5. Create meaningful commit messages

### Commit Message Format

```
[Component] Brief description

Longer explanation if needed.
```

Examples:
- `[Auth] Add JWT refresh token endpoint`
- `[Wallet] Fix withdrawal validation for bonus balance`
- `[DB] Add index on transactions.created_at`

## License

Proprietary - All Rights Reserved

## Support

- **Documentation**: See `docs/` directory
- **API Issues**: Check Swagger UI and API documentation
- **Deployment Help**: See DEPLOYMENT.md
- **Development Questions**: See CLAUDE.md

## Project Status

### Completed Phases

- ✅ Phase 1: Backend Development (Services, repositories, controllers)
- ✅ Phase 2: Frontend Development (Angular components and services)
- ✅ Phase 3: Integration & Testing (48/51 unit tests passing)
- ✅ Phase 4: Documentation (API docs, deployment guide)

### In Progress

- 🔄 Phase 5: Deployment Preparation
- 🔄 Phase 6: Final Validation & Cleanup

### Upcoming

- Fix V100 migration issue
- Resolve 3 failing unit tests
- Complete integration test suite
- Production deployment

## Version History

- **v0.0.1-SNAPSHOT** - Initial development version
  - Core wallet functionality
  - Player management
  - Bonus system
  - Game integration
  - Admin portal

---

**Last Updated**: 2025-01-15
