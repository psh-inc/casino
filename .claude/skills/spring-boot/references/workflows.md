# Spring Boot Workflows Reference

## Development Workflow

### Creating a New REST Endpoint

1. **Define the DTO** with Jakarta validation:

```kotlin
data class CreatePlayerRequest(
    @field:NotBlank(message = "Username is required")
    @field:Size(min = 3, max = 50, message = "Username must be 3-50 characters")
    val username: String,

    @field:NotBlank(message = "Email is required")
    @field:Email(message = "Invalid email format")
    val email: String,

    @field:NotBlank(message = "Password is required")
    @field:Size(min = 8, max = 100, message = "Password must be 8-100 characters")
    val password: String
)
```

2. **Create the service method** with proper transactions:

```kotlin
@Service
class PlayerService(private val repository: PlayerRepository) {
    @Transactional
    fun create(request: CreatePlayerRequest): PlayerDto {
        if (repository.existsByUsername(request.username)) {
            throw ResourceAlreadyExistsException("Username already exists")
        }
        val player = repository.save(Player(
            username = request.username,
            email = request.email
        ))
        return PlayerDto.from(player)
    }
}
```

3. **Add the controller endpoint**:

```kotlin
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
@Operation(summary = "Create a new player")
fun create(@Valid @RequestBody request: CreatePlayerRequest): PlayerDto {
    return playerService.create(request)
}
```

4. **Document in `docs/api/`** if it's a new API.

---

## Testing Workflow

### Service Layer Testing with MockK

```kotlin
@ExtendWith(MockKExtension::class)
class PlayerServiceTest {
    @MockK
    private lateinit var repository: PlayerRepository

    @MockK
    private lateinit var eventService: PlayerEventService

    @InjectMockKs
    private lateinit var service: PlayerService

    @Test
    fun `should create player successfully`() {
        // Given
        val request = CreatePlayerRequest(username = "testuser", email = "test@example.com")
        val savedPlayer = Player(id = 1L, username = "testuser", email = "test@example.com")

        every { repository.existsByUsername("testuser") } returns false
        every { repository.save(any()) } returns savedPlayer
        every { eventService.publishPlayerRegistered(any()) } just runs

        // When
        val result = service.create(request)

        // Then
        assertThat(result.id).isEqualTo(1L)
        assertThat(result.username).isEqualTo("testuser")
        verify { repository.save(any()) }
    }
}
```

### WARNING: Not Using `readOnly = true` for Queries

**The Problem:**

```kotlin
// BAD - Missing readOnly flag
@Transactional
fun findAll(pageable: Pageable): Page<PlayerDto> {
    return repository.findAll(pageable).map { PlayerDto.from(it) }
}
```

**Why This Breaks:**
1. Database connection held in write mode unnecessarily
2. Hibernate dirty checking runs for all entities
3. Potential for accidental writes
4. Worse performance under load

**The Fix:**

```kotlin
// GOOD - Explicit read-only transaction
@Transactional(readOnly = true)
fun findAll(pageable: Pageable): Page<PlayerDto> {
    return repository.findAll(pageable).map { PlayerDto.from(it) }
}
```

---

## Caching Workflow

### Adding Cache to a Service Method

1. **Define cache in configuration**:

```kotlin
@Bean
fun playerCache(): Cache<Long, PlayerDto> {
    return Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(Duration.ofMinutes(5))
        .recordStats()
        .build()
}
```

2. **Add `@Cacheable` to read methods**:

```kotlin
@Cacheable(cacheNames = ["players"], key = "'player:' + #id")
@Transactional(readOnly = true)
fun findById(id: Long): PlayerDto { ... }
```

3. **Add `@CacheEvict` to write methods**:

```kotlin
@CacheEvict(cacheNames = ["players"], key = "'player:' + #id")
@Transactional
fun update(id: Long, request: UpdatePlayerRequest): PlayerDto { ... }
```

4. **For complex invalidation, use `@Caching`**:

```kotlin
@Caching(
    evict = [
        CacheEvict(cacheNames = ["players"], key = "'player:' + #id"),
        CacheEvict(cacheNames = ["playerList"], allEntries = true)
    ]
)
fun delete(id: Long) { ... }
```

---

## Build & Verification Workflow

### Pre-Commit Checklist

```bash
# 1. Run full build with tests
cd casino-b
./gradlew clean build

# 2. Check for compilation errors
./gradlew compileKotlin

# 3. Run specific tests
./gradlew test --tests "*PlayerServiceTest"

# 4. Generate test coverage report
./gradlew jacocoTestReport
```

### WARNING: Skipping Build Verification

**The Problem:**

Pushing code without running `./gradlew clean build`.

**Why This Breaks:**
1. CI/CD pipeline fails
2. Integration tests may catch issues too late
3. Other developers pull broken code

**The Fix:**

ALWAYS run before committing:
```bash
./gradlew clean build && echo "Build passed!"
```

---

## Database Migration Workflow

See the **postgresql** skill for Flyway migration patterns.

### Quick Migration Steps

1. Create migration file: `V{yyyyMMddHHmmss}__{description}.sql`
2. Place in `src/main/resources/db/migration/`
3. Run: `./gradlew flywayMigrate`

**Critical Rules:**
- ALWAYS use `BIGSERIAL` for IDs
- ALWAYS use `TIMESTAMP WITH TIME ZONE` for dates
- NEVER use `SERIAL` (32-bit overflow risk)

---

## Async Processing Workflow

### Background Task with Named Executor

```kotlin
@Service
class NotificationService(
    @Qualifier("websocketNotificationExecutor")
    private val executor: Executor
) {
    fun sendNotificationAsync(playerId: Long, message: String) {
        CompletableFuture.runAsync({
            // Send notification
        }, executor)
    }
}
```

### Executor Selection Guide

| Executor | Use Case | Rejection Policy |
|----------|----------|------------------|
| `walletAsyncExecutor` | Financial operations | CallerRunsPolicy (never drop) |
| `websocketNotificationExecutor` | Real-time UI updates | DiscardOldestPolicy (drop stale) |
| `taskExecutor` | General background work | CallerRunsPolicy |

---

## Related Skills

- See the **jpa** skill for entity and repository patterns
- See the **kafka** skill for async event publishing
- See the **redis** skill for distributed caching configuration