---
name: redis
description: |
  Redis caching with Spring Cache abstraction and Caffeine L1 cache
  Use when: implementing caching strategies, cache invalidation, distributed caching, multi-level caching
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Redis Skill

This project implements a sophisticated multi-level caching strategy with Caffeine as L1 (in-memory, sub-millisecond) and Redis as L2 (distributed, cross-instance). Spring Cache abstraction is used for declarative caching with `@Cacheable`, `@CacheEvict`, and `@CachePut` annotations. The architecture prioritizes consistency for financial data (wallet balances) and performance for read-heavy data (games, player profiles).

## Quick Start

### Spring Cache Annotations

```kotlin
// Read-through caching with @Cacheable
@Cacheable(value = ["gameDetails"], key = "#gameId")
fun getGameDetails(gameId: String): GameDetailsResponse {
    return gameRepository.findById(gameId).orElseThrow()
}

// Evict on write operations
@CacheEvict(value = ["gameDetails"], key = "#gameId")
fun updateGame(gameId: String, request: GameUpdateRequest): GameDetailsResponse {
    // Update logic - cache automatically invalidated
}
```

### Direct Redis Template Operations

```kotlin
// For fine-grained control over TTL and serialization
fun setBalance(playerId: Long, balance: WalletBalance, isActive: Boolean) {
    val key = "$WALLET_KEY_PREFIX$playerId"
    val ttl = if (isActive) activeTtlSeconds else inactiveTtlSeconds
    val json = objectMapper.writeValueAsString(balance)
    redisTemplate.opsForValue().set(key, json, Duration.ofSeconds(ttl))
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Multi-level cache | Caffeine (L1) → Redis (L2) → DB | `CompositeCacheManager` |
| Dynamic TTL | Active players: 30s, Inactive: 300s | `DistributedWalletCache` |
| Key patterns | `domain:type:id` format | `player:cache:123` |
| Bulk operations | `multiGet`/`multiSet` for batching | `getBalances(playerIds)` |
| Distributed locks | `setIfAbsent` for mutex | `tryAcquireLock(playerId)` |

## Common Patterns

### Cache-Aside with Fallback

**When:** Reading data that may not be in cache

```kotlin
fun getPlayer(playerId: Long): CachedPlayer? {
    // L1: Local cache
    localCache.getIfPresent(playerId)?.let { return it }
    
    // L2: Redis cache
    redisTemplate.opsForValue().get(redisKey)?.let { 
        localCache.put(playerId, it)  // Populate L1
        return it 
    }
    
    // L3: Database
    return playerRepository.findById(playerId).orElse(null)?.let { player ->
        populateCaches(playerId, CachedPlayer.from(player))
    }
}
```

### Bulk Eviction on Write

**When:** Write affects multiple cache entries

```kotlin
@CacheEvict(
    value = ["games", "gameDetails", "featuredGames", "popularGames"],
    allEntries = true
)
fun bulkUpdateGames(): BulkUpdateResponse { ... }
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

For Kotlin patterns, see the **kotlin** skill. For Spring Boot configuration, see the **spring-boot** skill. For JPA repository patterns, see the **jpa** skill.