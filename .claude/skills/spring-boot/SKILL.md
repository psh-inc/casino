---
name: spring-boot
description: |
  Spring Boot 3.2.5 REST controllers, services, and configuration for the casino backend.
  Use when: Building REST APIs, configuring security, setting up caching, implementing service layer logic, or managing database transactions.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Spring Boot Skill

Enterprise Spring Boot 3.2.5 backend using Kotlin 2.3, Java 21, JWT authentication, multi-level caching (Caffeine + Redis), and Kafka event publishing. Controllers use OpenAPI annotations, services are transactional, and exceptions are mapped globally.

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
    @PreAuthorize("hasAuthority('ADMIN') or #id == authentication.principal.username")
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
    private val eventPublisher: EventPublisher
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Cacheable(value = ["players"], key = "#id")
    @Transactional(readOnly = true)
    fun findById(id: Long): PlayerDto {
        return repository.findById(id)
            .map { PlayerDto.from(it) }
            .orElseThrow { ResourceNotFoundException("Player not found: $id") }
    }

    @CacheEvict(value = ["players"], allEntries = true)
    @Transactional
    fun create(request: CreatePlayerRequest): PlayerDto {
        val player = repository.save(Player(username = request.username))
        publishEvent(player) // Fire-and-forget
        return PlayerDto.from(player)
    }

    private fun publishEvent(player: Player) {
        try {
            eventPublisher.publish(KafkaTopics.PLAYER_REGISTERED, player.id.toString(), event)
        } catch (e: Exception) {
            logger.error("Failed to publish event", e) // Log, don't throw
        }
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `@Transactional` | Wrap DB operations | `@Transactional(readOnly = true)` for queries |
| `@Cacheable` | Cache method results | `@Cacheable(value = ["players"], key = "#id")` |
| `@Valid` | Trigger validation | `fun create(@Valid @RequestBody req: Dto)` |
| `@PreAuthorize` | Method security | `@PreAuthorize("hasAuthority('ADMIN')")` |
| `ResponseEntity` | Control HTTP response | `ResponseEntity.status(HttpStatus.CREATED).body(dto)` |

## Common Patterns

### Exception Handling

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleNotFound(ex: ResourceNotFoundException): ResponseEntity<ErrorResponse> {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(message = ex.message))
    }
}
```

### Repository with Custom Queries

```kotlin
@Repository
interface PlayerRepository : JpaRepository<Player, Long> {
    @Query("SELECT p FROM Player p LEFT JOIN FETCH p.wallet WHERE p.id = :id")
    fun findByIdWithWallet(@Param("id") id: Long): Optional<Player>

    @Modifying
    @Query("UPDATE Player p SET p.status = :status WHERE p.id = :id")
    fun updateStatus(@Param("id") id: Long, @Param("status") status: PlayerStatus)
}
```

## See Also

- [patterns](references/patterns.md) - Controller/Service/Repository patterns
- [workflows](references/workflows.md) - Development workflows and testing

## Related Skills

- **kotlin** skill for Kotlin-specific patterns and idioms
- **jpa** skill for entity mapping and query optimization
- **kafka** skill for event publishing configuration
- **redis** skill for distributed caching setup
- **postgresql** skill for database migrations and schema design