```markdown
---
name: kotlin
description: |
  Kotlin language patterns, coroutines, and Spring Boot integration.
  Use when: Writing/modifying Kotlin backend code in casino-b/, implementing
  services, controllers, DTOs, or entities, working with BigDecimal/financial data.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Kotlin Skill

This codebase uses Kotlin 2.3 with Spring Boot 3.2.5 on Java 21. The backend follows idiomatic Kotlin patterns with strong emphasis on null safety, immutable data classes, and functional collection operations. Financial calculations MUST use BigDecimal created from String (NEVER from Double).

## Quick Start

### Service Pattern

```kotlin
@Service
@Transactional
class PlayerService(
    private val playerRepository: PlayerRepository,
    private val walletService: WalletService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Cacheable(value = ["players"], key = "#id")
    fun findById(id: Long): PlayerDto {
        val player = playerRepository.findById(id)
            .orElseThrow { NotFoundException("Player not found: $id") }
        return PlayerDto.from(player)
    }
}
```

### Data Class Pattern

```kotlin
data class ProfileUpdateRequest(
    val playerId: Long,
    val updateFirstName: Boolean = false,
    val updateLastName: Boolean = false,
    val adminUserId: Long,
    val reason: String
)
```

### BigDecimal Pattern (Critical)

```kotlin
// CORRECT - Always from String
val amount = BigDecimal("123.45")
val calculated = depositAmount
    .multiply(percentageValue)
    .divide(BigDecimal("100"), 2, RoundingMode.DOWN)

// WRONG - NEVER do this (precision loss)
val amount = BigDecimal(123.45)  // DON'T
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Elvis operator | Null fallback | `value ?: defaultValue` |
| Safe call | Null-safe access | `player?.wallet?.balance` |
| let scope | Transform nullable | `value?.let { process(it) }` |
| when expression | Pattern matching | `when (type) { is A -> ... }` |
| require/check | Validation | `require(x > 0) { "msg" }` |

## Common Patterns

### Collection Operations

**When:** Transforming lists, filtering, aggregating

```kotlin
val lockedDeposits = activeRequirements.map { req ->
    LockedDepositInfo(
        requirementId = req.id!!,
        lockedAmount = req.calculateLockedAmount(),
        progressPercentage = req.getProgress()
    )
}
val totalLocked = lockedDeposits.sumOf { it.lockedAmount }
```

### Extension Functions

**When:** Adding behavior to existing classes

```kotlin
fun ComplianceSettingsService.getAISettings(): AIComplianceSettings {
    return AIComplianceSettings(
        aiEnabled = getBooleanSetting(AI_ENABLED, false),
        aiAutoApproveThreshold = getDoubleSetting(AI_THRESHOLD, 0.95)
    )
}
```

### When Expression with Smart Cast

**When:** Type-safe branching

```kotlin
val amount = responseBody["amount"]?.let {
    when (it) {
        is Number -> BigDecimal(it.toString())
        is String -> BigDecimal(it)
        else -> BigDecimal.ONE
    }
} ?: BigDecimal.ONE
```

## See Also

- [patterns](references/patterns.md) - Idiomatic patterns, null safety, scope functions
- [types](references/types.md) - Data classes, enums, sealed classes
- [modules](references/modules.md) - Package structure, dependency injection
- [errors](references/errors.md) - Exception handling, validation

## Related Skills

- See the **spring-boot** skill for Spring framework integration
- See the **jpa** skill for entity and repository patterns
- See the **postgresql** skill for database type mappings
- See the **kafka** skill for event publishing patterns
```