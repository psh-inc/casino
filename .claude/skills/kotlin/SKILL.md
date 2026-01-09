---
name: kotlin
description: |
  Kotlin 2.3.0 language patterns, coroutines, and Spring integration
  Use when: Writing backend services, JPA entities, DTOs, controllers, or any Kotlin code in casino-b
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Kotlin Skill

Kotlin 2.3.0 with Spring Boot 3.2.5 and Java 21 for the casino backend. This codebase uses data classes extensively for entities and DTOs, relies on constructor injection, and follows strict BigDecimal handling for financial operations. Null safety is critical—leverage Kotlin's type system to prevent runtime errors.

## Quick Start

### Data Class for DTOs

```kotlin
data class CreateBonusRequest(
    @field:NotBlank(message = "Name is required")
    val name: String,

    @field:NotNull(message = "Amount is required")
    val amount: BigDecimal,

    val category: BonusCategory? = null
)
```

### Service with Constructor Injection

```kotlin
@Service
@Transactional
class BonusService(
    private val bonusRepository: BonusRepository,
    private val playerRepository: PlayerRepository,
    private val eventPublisher: EventPublisher
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    fun create(request: CreateBonusRequest): BonusDto {
        logger.info("Creating bonus: ${request.name}")
        val bonus = Bonus(name = request.name, amount = request.amount)
        return BonusDto.from(bonusRepository.save(bonus))
    }
}
```

### Entity with JPA Annotations

```kotlin
@Entity
@Table(name = "bonuses")
data class Bonus(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,

    @Column(nullable = false)
    val name: String,

    @Column(precision = 19, scale = 2)
    val amount: BigDecimal = BigDecimal.ZERO,

    @Enumerated(EnumType.STRING)
    val category: BonusCategory? = null
)
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Null safety | Use `?` for nullable, `!!` sparingly | `player?.wallet?.balance` |
| BigDecimal | Always from String | `BigDecimal("123.45")` |
| Data classes | DTOs and entities | `data class PlayerDto(...)` |
| Extension functions | Utility methods | `fun String.toSlug()` |
| Scope functions | Object configuration | `apply`, `let`, `also`, `run` |

## Common Patterns

### Repository Lookup with Null Handling

**When:** Finding entities that may not exist

```kotlin
fun findById(id: Long): PlayerDto {
    val player = playerRepository.findById(id)
        .orElseThrow { PlayerNotFoundException("Player not found: $id") }
    return PlayerDto.from(player)
}
```

### Safe BigDecimal Comparison

**When:** Comparing monetary values

```kotlin
// CORRECT - use compareTo
if (balance.compareTo(BigDecimal.ZERO) > 0) {
    processWithdrawal()
}

// WRONG - equals checks scale too
if (balance == BigDecimal.ZERO) { } // May fail unexpectedly
```

## See Also

- [patterns](references/patterns.md)
- [types](references/types.md)
- [modules](references/modules.md)
- [errors](references/errors.md)

## Related Skills

- See the **spring-boot** skill for REST controllers and service configuration
- See the **jpa** skill for entity mapping and repository patterns
- See the **kafka** skill for event publishing patterns
- See the **postgresql** skill for database migrations and queries