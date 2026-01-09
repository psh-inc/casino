---
name: spring-boot
description: |
  Spring Boot 3.2.5 REST controllers, services, and configuration for the casino platform.
  Use when: Building REST APIs, configuring security, setting up caching, implementing service layer logic, or managing database transactions.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Spring Boot 3.2.5 Skill

This codebase uses Spring Boot 3.2.5 with Kotlin 2.3.0 and Java 21. Key patterns include OAuth2/JWT security, multi-level caching (Caffeine L1 + Redis L2), Kafka event publishing with circuit breakers, and Jakarta Bean Validation. All services use constructor injection, `@Transactional` management, and fire-and-forget event publishing.

## Quick Start

### Controller Pattern

```kotlin
@RestController
@RequestMapping("/api/v1/players")
@Tag(name = "Players", description = "Player management API")
class PlayerController(
    private val playerService: PlayerService
) {
    @GetMapping("/{id}")
    @Operation(summary = "Get player by ID")
    @PreAuthorize("hasAnyAuthority('ADMIN') or #id == authentication.principal.username")
    fun getPlayer(@PathVariable id: Long): ResponseEntity<PlayerDto> {
        return ResponseEntity.ok(playerService.findById(id))
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun create(@Valid @RequestBody request: CreatePlayerRequest): PlayerDto {
        return playerService.create(request)
    }
}
```

### Service Pattern

```kotlin
@Service
class PlayerService(
    private val repository: PlayerRepository,
    private val eventService: PlayerEventService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Transactional(readOnly = true)
    @Cacheable(cacheNames = ["players"], key = "'player:' + #id")
    fun findById(id: Long): PlayerDto {
        val player = repository.findById(id)
            .orElseThrow { ResourceNotFoundException("Player not found: $id") }
        return PlayerDto.from(player)
    }

    @Transactional
    @CacheEvict(cacheNames = ["players"], key = "'player:' + #result.id")
    fun create(request: CreatePlayerRequest): PlayerDto {
        val player = repository.save(Player(username = request.username))
        // Fire-and-forget event publishing
        try {
            eventService.publishPlayerCreated(player)
        } catch (e: Exception) {
            logger.error("Failed to publish event", e)
        }
        return PlayerDto.from(player)
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Constructor DI | All dependencies via constructor | `class Service(private val repo: Repository)` |
| Read Transactions | Use for queries | `@Transactional(readOnly = true)` |
| Cache Keys | String interpolation | `key = "'player:' + #id"` |
| Fire-and-Forget | Event publishing | Try-catch without rethrowing |
| Validation | Jakarta annotations | `@Valid @RequestBody` |

## Common Patterns

### Exception Handling

**When:** Returning structured error responses

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleNotFound(ex: ResourceNotFoundException, request: WebRequest): ResponseEntity<ErrorResponse> {
        return ResponseEntity(
            ErrorResponse(
                status = 404,
                error = "Not Found",
                message = ex.message ?: "Resource not found",
                path = request.getDescription(false).substringAfter("uri=")
            ),
            HttpStatus.NOT_FOUND
        )
    }
}
```

### Multi-Level Caching

**When:** High-frequency reads with distributed cache needs

```kotlin
@Bean
fun walletCache(): Cache<Long, WalletBalance> {
    return Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(Duration.ofSeconds(5))
        .recordStats()
        .build()
}
```

### Async Configuration

**When:** Background processing without blocking HTTP threads

```kotlin
@Bean("walletAsyncExecutor")
fun walletAsyncExecutor(): Executor {
    val executor = ThreadPoolTaskExecutor()
    executor.corePoolSize = 32
    executor.maxPoolSize = 128
    executor.setThreadNamePrefix("wallet-async-")
    executor.setRejectedExecutionHandler(ThreadPoolExecutor.CallerRunsPolicy())
    executor.initialize()
    return executor
}
```

## See Also

- [patterns](references/patterns.md) - Controller, service, and configuration patterns
- [workflows](references/workflows.md) - Development workflows and testing

## Related Skills

- See the **kotlin** skill for Kotlin-specific patterns
- See the **jpa** skill for entity and repository patterns
- See the **postgresql** skill for database migrations
- See the **kafka** skill for event publishing patterns
- See the **redis** skill for distributed caching