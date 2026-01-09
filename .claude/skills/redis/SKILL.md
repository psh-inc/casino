---
name: redis
description: |
  Redis caching with Spring Cache abstraction and Caffeine L1 cache
  Use when: implementing caching strategies, cache invalidation, distributed caching, multi-level caching
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Redis Skill

This casino platform implements a **three-layer caching strategy**: L1 (Caffeine in-memory) → L2 (Redis distributed) → L3 (Database). Uses Spring Cache abstraction with custom key generators, adaptive TTLs based on player activity, and distributed locking for wallet operations.

## Quick Start

### Read-Through Caching with @Cacheable

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/PlayerService.kt
@Cacheable(
    cacheNames = ["playerDetails"],
    key = "'player:id:' + #id"
)
fun getPlayerById(id: Long): PlayerDetailsResponse {
    return playerRepository.findById(id)
        .map(PlayerDetailsResponse::from)
        .orElseThrow { NotFoundException("Player not found: $id") }
}
```

### Cache Invalidation with @CacheEvict

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/CurrencyService.kt
@CacheEvict(value = ["currencies", "active-currencies"], allEntries = true)
fun createCurrency(request: CreateCurrencyRequest): CurrencyDto {
    val currency = Currency(code = request.code, name = request.name)
    return CurrencyDto.from(currencyRepository.save(currency))
}
```

### Multi-Level Cache Lookup

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/cache/PlayerCacheService.kt
fun getPlayer(playerId: Long): CachedPlayer? {
    // L1: Caffeine local cache
    localCache.getIfPresent(playerId)?.let { return it }
    
    // L2: Redis distributed cache
    redisTemplate.opsForValue().get("player:$playerId")?.let { 
        localCache.put(playerId, it)  // Promote to L1
        return it
    }
    
    // L3: Database fallback
    return playerRepository.findById(playerId).orElse(null)
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| L1 Cache | In-memory Caffeine, 5s-30min TTL | `localCache.getIfPresent(key)` |
| L2 Cache | Redis distributed, 30s-2h TTL | `redisTemplate.opsForValue().get()` |
| Key Generation | SpEL with @cacheKeys bean | `key = "@cacheKeys.playerStats(#id)"` |
| Adaptive TTL | Active players: 30s, Inactive: 300s | Wallet balance caching |
| Distributed Lock | Redis SETNX for wallet ops | `setIfAbsent(key, value, duration)` |

## Common Patterns

### SpEL Key Generation with Custom Bean

**When:** Complex key patterns needed across multiple services

```kotlin
// casino-b/src/main/kotlin/com/casino/core/cache/CacheKeyGenerator.kt
@Component("cacheKeys")
class CacheKeys {
    fun playerStats(playerId: Long, currency: String) = "player:stats:$playerId:$currency"
    fun playerPattern(playerId: Long) = "player:*:$playerId:*"
}

// Usage in service
@Cacheable(
    cacheNames = ["playerStatistics"],
    key = "@cacheKeys.playerStatsPeriod(#playerId, #currency, #periodType.name())"
)
fun getPlayerStatistics(playerId: Long, currency: String, periodType: StatisticsPeriodType)
```

### Adaptive TTL Based on Activity

**When:** Hot data needs shorter TTL for freshness

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/cache/DistributedWalletCache.kt
fun setBalance(playerId: Long, balance: WalletBalance, isActive: Boolean) {
    val ttl = if (isActive) activeTtl else inactiveTtl  // 30s vs 300s
    redisTemplate.opsForValue().set(
        "wallet:balance:$playerId",
        balance,
        ttl
    )
}
```

## TTL Reference

| Cache | L1 TTL | L2 TTL | Use Case |
|-------|--------|--------|----------|
| walletBalance | 5s | 30s/300s | Real-time balance |
| playerProfile | - | 5 min | Player details |
| games | - | 15 min | Game catalog |
| verificationLevels | 30 min | 2 hours | KYC config |

## See Also

- [patterns](references/patterns.md) - Caching patterns and anti-patterns
- [workflows](references/workflows.md) - Cache warming, invalidation, monitoring

## Related Skills

- See the **spring-boot** skill for service configuration
- See the **kotlin** skill for Kotlin-specific patterns
- See the **jpa** skill for database fallback patterns