# Redis Caching Patterns

## Multi-Level Cache Configuration

The project uses `CompositeCacheManager` to chain Caffeine and Redis:

```kotlin
@Bean
@Primary
fun compositeCacheManager(
    caffeineCacheManager: CacheManager,
    redisCacheManager: CacheManager
): CacheManager {
    val compositeCacheManager = CompositeCacheManager()
    compositeCacheManager.setCacheManagers(listOf(caffeineCacheManager, redisCacheManager))
    compositeCacheManager.setFallbackToNoOpCache(false)
    return compositeCacheManager
}
```

**Cache lookup order:** Caffeine → Redis → Database

## Cache Configuration by Domain

```kotlin
val cacheConfigurations = mapOf(
    "walletBalance" to config.entryTtl(Duration.ofSeconds(30)),      // Hot data
    "playerProfile" to config.entryTtl(Duration.ofMinutes(5)),       // Warm data
    "gameDetails" to config.entryTtl(Duration.ofMinutes(15)),        // Stable data
    "verificationLevels" to config.entryTtl(Duration.ofHours(2))     // Cold data
)
```

## WARNING: Silent Cache Failures

**The Problem:**

```kotlin
// BAD - Swallowing exceptions silently
fun getBalance(playerId: Long): WalletBalance? {
    return try {
        redisTemplate.opsForValue().get(key)
    } catch (e: Exception) {
        null  // Silent failure - no logging, no metrics
    }
}
```

**Why This Breaks:**
1. You lose visibility into Redis connectivity issues
2. Cache misses spike without alerting
3. Database gets hammered as fallback with no warning

**The Fix:**

```kotlin
// GOOD - Log and track metrics on failure
fun getBalance(playerId: Long): WalletBalance? {
    return try {
        redisTemplate.opsForValue().get(key)
    } catch (e: Exception) {
        logger.error("Error getting cached balance for player $playerId", e)
        meterRegistry.counter("cache.error", "operation", "get").increment()
        null
    }
}
```

**When You Might Be Tempted:**
When you want to "gracefully degrade" but forget that silent failures hide production issues.

## WARNING: N+1 Cache Operations

**The Problem:**

```kotlin
// BAD - One Redis call per player
fun getBalances(playerIds: List<Long>): Map<Long, WalletBalance> {
    return playerIds.associate { id ->
        id to redisTemplate.opsForValue().get("$WALLET_KEY_PREFIX$id")
    }
}
```

**Why This Breaks:**
1. 1000 players = 1000 network round-trips to Redis
2. Latency scales linearly with list size
3. Redis connection pool exhaustion under load

**The Fix:**

```kotlin
// GOOD - Batch with multiGet
fun getBalances(playerIds: List<Long>): Map<Long, WalletBalance> {
    if (playerIds.isEmpty()) return emptyMap()
    
    val keys = playerIds.map { "$WALLET_KEY_PREFIX$it" }
    val values = redisTemplate.opsForValue().multiGet(keys)
    
    return values?.mapIndexedNotNull { index, json ->
        json?.let { playerIds[index] to parseBalance(it) }
    }?.toMap() ?: emptyMap()
}
```

**When You Might Be Tempted:**
When iterating over a list and caching seems "simple enough" for each item.

## Dynamic TTL Based on Activity

Active players need fresher data; inactive players can tolerate staleness:

```kotlin
@Service
class DistributedWalletCache(
    @Value("\${wallet.cache.distributed.active-ttl-seconds:30}") 
    private val activeTtlSeconds: Long,
    @Value("\${wallet.cache.distributed.inactive-ttl-seconds:300}") 
    private val inactiveTtlSeconds: Long
) {
    fun setBalance(playerId: Long, balance: WalletBalance, isActive: Boolean) {
        val ttl = if (isActive) activeTtlSeconds else inactiveTtlSeconds
        redisTemplate.opsForValue().set(key, json, Duration.ofSeconds(ttl))
    }
}
```

## Cache Key Generation

Use consistent key patterns with a utility class:

```kotlin
@Component("cacheKeys")
class CacheKeys {
    fun playerStats(playerId: Long, currency: String): String = 
        "player:stats:$playerId:$currency"
    
    fun verificationLevel(levelId: Long): String = 
        "verification:level:$levelId"
    
    // Pattern for bulk invalidation
    fun playerPattern(playerId: Long): String = 
        "player:*:$playerId:*"
}
```

## WARNING: Inconsistent Key Formats

**The Problem:**

```kotlin
// BAD - Different formats across services
class ServiceA { val key = "player_${id}_balance" }
class ServiceB { val key = "player:$id:balance" }
class ServiceC { val key = "balance-player-$id" }
```

**Why This Breaks:**
1. Pattern-based invalidation fails (`player:*` misses `player_*`)
2. Debugging becomes nightmare - which format is which service?
3. Key collisions when formats accidentally overlap

**The Fix:**

```kotlin
// GOOD - Centralized key generation
companion object {
    private const val WALLET_KEY_PREFIX = "wallet:balance:"
    private const val WALLET_LOCK_PREFIX = "wallet:lock:"
}

private fun walletKey(playerId: Long) = "$WALLET_KEY_PREFIX$playerId"
```

## Distributed Locking for Concurrent Writes

```kotlin
fun tryAcquireLock(playerId: Long, lockId: String): Boolean {
    val key = "$WALLET_LOCK_PREFIX$playerId"
    return redisTemplate.opsForValue()
        .setIfAbsent(key, lockId, Duration.ofSeconds(LOCK_TIMEOUT_SECONDS)) ?: false
}

fun releaseLock(playerId: Long, lockId: String) {
    val key = "$WALLET_LOCK_PREFIX$playerId"
    val currentLockId = redisTemplate.opsForValue().get(key)
    if (currentLockId == lockId) {
        redisTemplate.delete(key)
    }
}
```

## Caffeine Local Cache with Metrics

```kotlin
@Bean
fun walletBalanceCache(): Cache<Long, WalletBalance> {
    val cache = Caffeine.newBuilder()
        .maximumSize(localCacheMaxSize)
        .expireAfterWrite(Duration.ofSeconds(localCacheTtlSeconds))
        .recordStats()
        .build<Long, WalletBalance>()
    
    CaffeineCacheMetrics.monitor(meterRegistry, cache, "wallet.balance.cache")
    return cache
}
```