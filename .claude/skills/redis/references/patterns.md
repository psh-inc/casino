# Redis Caching Patterns

## Multi-Level Caching Architecture

```
Request → Caffeine (L1) → Redis (L2) → Database (L3)
           │                │            │
           └─ 5s TTL        └─ 30-300s   └─ Source of truth
```

### Implementing L1 → L2 → L3 Fallback

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/cache/PlayerCacheService.kt
@Service
class PlayerCacheService(
    @Qualifier("playerLocalCache") private val localCache: Cache<Long, CachedPlayer>,
    private val redisTemplate: RedisTemplate<String, CachedPlayer>,
    private val playerRepository: PlayerRepository,
    private val meterRegistry: MeterRegistry
) {
    fun getPlayer(playerId: Long): CachedPlayer? {
        // L1: Local Caffeine (sub-millisecond)
        localCache.getIfPresent(playerId)?.let {
            meterRegistry.counter("player.cache.hit", "layer", "local").increment()
            return it
        }
        
        // L2: Redis distributed (1-5ms)
        redisTemplate.opsForValue().get("player:$playerId")?.let { cached ->
            meterRegistry.counter("player.cache.hit", "layer", "redis").increment()
            localCache.put(playerId, cached)  // Promote to L1
            return cached
        }
        
        // L3: Database fallback
        meterRegistry.counter("player.cache.miss").increment()
        return playerRepository.findById(playerId).orElse(null)?.let { player ->
            val cached = CachedPlayer.from(player)
            setPlayer(playerId, cached)  // Populate both caches
            cached
        }
    }
}
```

---

## WARNING: Direct Redis Operations Without L1

**The Problem:**

```kotlin
// BAD - Bypasses L1 cache, causes inconsistency between layers
@Cacheable(cacheNames = ["players"], key = "#playerId")
fun getPlayer(playerId: Long): Player {
    // This only uses Redis (L2), not the local Caffeine cache
    return playerRepository.findById(playerId).orElseThrow()
}

// Another service reads from L1 directly
localCache.getIfPresent(playerId)  // Returns stale data or null!
```

**Why This Breaks:**
1. L1 and L2 caches become unsynchronized - L1 may have stale data
2. Cache promotion never happens - L1 stays cold, adding latency
3. Micrometer metrics report incorrect hit rates per layer

**The Fix:**

```kotlin
// GOOD - Explicit multi-level lookup with promotion
fun getPlayer(playerId: Long): CachedPlayer? {
    return localCache.getIfPresent(playerId)
        ?: redisTemplate.opsForValue().get("player:$playerId")?.also {
            localCache.put(playerId, it)  // Promote to L1
        }
        ?: loadFromDatabase(playerId)?.also {
            setPlayer(playerId, it)  // Populate both layers
        }
}
```

**When You Might Be Tempted:**
When using Spring's `@Cacheable` which only targets one cache manager - it doesn't understand multi-level semantics.

---

## WARNING: Hardcoded Cache Keys

**The Problem:**

```kotlin
// BAD - Magic strings scattered across services
@Cacheable(cacheNames = ["stats"], key = "'player_' + #id + '_' + #currency")
fun getStats(id: Long, currency: String): PlayerStats

// In another file, different format
redisTemplate.delete("player-$playerId-stats")  // Won't match!
```

**Why This Breaks:**
1. Key format drift causes phantom cache entries
2. Pattern-based eviction misses orphaned keys (`KEYS player*` vs `KEYS player_*`)
3. Debugging cache issues requires grep across entire codebase

**The Fix:**

```kotlin
// GOOD - Centralized key generation
// casino-b/src/main/kotlin/com/casino/core/cache/CacheKeyGenerator.kt
@Component("cacheKeys")
class CacheKeys {
    fun playerStats(playerId: Long, currency: String) = "player:stats:$playerId:$currency"
    fun playerPattern(playerId: Long) = "player:*:$playerId:*"
}

// Usage with SpEL
@Cacheable(
    cacheNames = ["playerStatistics"],
    key = "@cacheKeys.playerStats(#playerId, #currency)"
)
fun getStats(playerId: Long, currency: String): PlayerStats

// Eviction uses same patterns
redisTemplate.delete(redisTemplate.keys(cacheKeys.playerPattern(playerId)))
```

---

## Distributed Locking Pattern

**When:** Serializing wallet operations to prevent race conditions

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/cache/DistributedWalletCache.kt
fun tryAcquireLock(playerId: Long, lockId: String): Boolean {
    return redisTemplate.opsForValue()
        .setIfAbsent("wallet:lock:$playerId", lockId, Duration.ofSeconds(5))
        ?: false
}

fun releaseLock(playerId: Long, lockId: String) {
    val currentLockId = redisTemplate.opsForValue().get("wallet:lock:$playerId")
    if (currentLockId == lockId) {
        redisTemplate.delete("wallet:lock:$playerId")
    }
}

// Usage pattern
val lockId = UUID.randomUUID().toString()
if (distributedWalletCache.tryAcquireLock(playerId, lockId)) {
    try {
        // Critical section: update wallet balance
        processTransaction(playerId, amount)
    } finally {
        distributedWalletCache.releaseLock(playerId, lockId)
    }
} else {
    throw ConcurrentModificationException("Wallet locked")
}
```

---

## WARNING: N+1 Cache Lookups

**The Problem:**

```kotlin
// BAD - One Redis call per player
fun getPlayerBalances(playerIds: List<Long>): Map<Long, WalletBalance> {
    return playerIds.associateWith { playerId ->
        redisTemplate.opsForValue().get("wallet:balance:$playerId")
    }
}
```

**Why This Breaks:**
1. 1000 players = 1000 Redis round-trips = 1-5 seconds latency
2. Redis connection pool exhaustion under load
3. Network overhead dominates response time

**The Fix:**

```kotlin
// GOOD - Batch operation with mGet
// casino-b/src/main/kotlin/com/casino/core/service/cache/DistributedWalletCache.kt
fun getBalances(playerIds: List<Long>): Map<Long, WalletBalance> {
    if (playerIds.isEmpty()) return emptyMap()
    
    val keys = playerIds.map { "wallet:balance:$it" }
    val values = redisTemplate.opsForValue().multiGet(keys) ?: return emptyMap()
    
    return playerIds.zip(values)
        .filter { it.second != null }
        .associate { it.first to it.second!! }
}
```

---

## Serialization Configuration

```kotlin
// casino-b/src/main/kotlin/com/casino/core/config/RedisConfig.kt
@Bean
fun redisTemplate(connectionFactory: RedisConnectionFactory): RedisTemplate<String, Any> {
    val template = RedisTemplate<String, Any>()
    template.connectionFactory = connectionFactory
    
    // Keys always as strings for readability
    template.keySerializer = StringRedisSerializer()
    template.hashKeySerializer = StringRedisSerializer()
    
    // Values as JSON with Kotlin/Java8 support
    val mapper = ObjectMapper().apply {
        registerModule(KotlinModule.Builder().build())
        registerModule(JavaTimeModule())
        disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
        configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
    }
    template.valueSerializer = GenericJackson2JsonRedisSerializer(mapper)
    
    return template
}
```