# Redis Caching Workflows

## Cache Warming on Startup

Pre-populate caches with frequently accessed data:

```kotlin
@Service
class PlayerCacheService(...) {
    fun warmActivePlayersCache() {
        val since = LocalDateTime.now().minusHours(1)
        val activePlayers = playerRepository.findActivePlayersSince(since)
        
        logger.info("Warming player cache with ${activePlayers.size} active players")
        
        activePlayers.forEach { player ->
            val cachedPlayer = CachedPlayer.from(player)
            populateCaches(player.id!!, cachedPlayer)
        }
        
        meterRegistry.gauge("player.cache.warmed", activePlayers.size)
    }
}
```

## Bulk Cache Warming

```kotlin
fun warmCache(wallets: List<WalletBalance>) {
    if (wallets.isEmpty()) return
    
    // Batch set for efficiency
    val operations = wallets.associate { wallet ->
        val key = "$WALLET_KEY_PREFIX${wallet.playerId}"
        key to objectMapper.writeValueAsString(wallet)
    }
    redisTemplate.opsForValue().multiSet(operations)
    
    // Set TTL for each key
    wallets.forEach { wallet ->
        val key = "$WALLET_KEY_PREFIX${wallet.playerId}"
        redisTemplate.expire(key, Duration.ofSeconds(activeTtlSeconds))
    }
}
```

## WARNING: Cache Warming Without TTL

**The Problem:**

```kotlin
// BAD - multiSet without TTL
redisTemplate.opsForValue().multiSet(operations)
// Keys live forever, memory grows unbounded
```

**Why This Breaks:**
1. Redis memory grows until OOM kills it
2. Stale data persists indefinitely
3. No automatic cleanup of inactive player data

**The Fix:**

```kotlin
// GOOD - Set TTL after multiSet
redisTemplate.opsForValue().multiSet(operations)
wallets.forEach { wallet ->
    redisTemplate.expire("$WALLET_KEY_PREFIX${wallet.playerId}", ttl)
}
```

## Cache Invalidation Strategies

### Single Key Invalidation

```kotlin
@CacheEvict(value = ["gameDetails"], key = "#gameId")
fun updateGame(gameId: String, request: GameUpdateRequest): GameDetailsResponse
```

### Bulk Invalidation

```kotlin
@CacheEvict(
    value = ["games", "gameDetails", "gameCountryConfigs", "featuredGames", "popularGames"],
    allEntries = true
)
fun bulkUpdateGameTypesFromCsv(file: MultipartFile): BulkUpdateGameTypesResponse
```

### Pattern-Based Invalidation

```kotlin
fun invalidatePlayerCache(playerId: Long) {
    val pattern = "player:*:$playerId:*"
    val keys = redisTemplate.keys(pattern)
    if (keys.isNotEmpty()) {
        redisTemplate.delete(keys)
        logger.debug("Deleted ${keys.size} Redis cache entries for player: $playerId")
    }
}
```

## WARNING: Using KEYS in Production

**The Problem:**

```kotlin
// BAD - KEYS blocks Redis
val keys = redisTemplate.keys("player:*")  // Scans ALL keys
redisTemplate.delete(keys)
```

**Why This Breaks:**
1. `KEYS *` is O(N) and blocks Redis during execution
2. With millions of keys, this can freeze Redis for seconds
3. All other operations queue behind it

**The Fix:**

```kotlin
// GOOD - Use SCAN for large keyspaces (in batch cleanup)
// Or better: use specific cache names and allEntries = true
@CacheEvict(value = ["playerCache"], allEntries = true)
fun clearPlayerCaches() { }

// For programmatic cleanup, limit scope:
val keys = redisTemplate.keys("player:stats:$playerId:*")  // Narrow pattern
```

**When You Might Be Tempted:**
When you need to clear "all player caches" but the pattern is too broad.

## Cache Health Monitoring

```kotlin
fun getCacheHealthStatus(): CacheHealthStatus {
    val caffeineAvailable = cacheManager.cacheNames.isNotEmpty()
    val redisAvailable = try {
        redisTemplate.connectionFactory?.connection?.ping() != null
    } catch (e: Exception) { false }
    
    val cacheStats = cacheManager.cacheNames.mapNotNull { cacheName ->
        val cache = cacheManager.getCache(cacheName) as? CaffeineCache
        cache?.let {
            val stats = it.nativeCache.stats()
            CacheStatistics(
                cacheName = cacheName,
                size = it.nativeCache.estimatedSize(),
                hitRate = stats.hitRate(),
                evictionCount = stats.evictionCount()
            )
        }
    }
    
    return CacheHealthStatus(
        healthy = caffeineAvailable && redisAvailable,
        cacheStatistics = cacheStats
    )
}
```

## Cache Statistics Tracking

```kotlin
fun getPlayer(playerId: Long): CachedPlayer? {
    // L1: Local cache
    localCache.getIfPresent(playerId)?.let {
        meterRegistry.counter("player.cache.hit", "layer", "local").increment()
        return it
    }
    
    // L2: Redis cache
    redisTemplate.opsForValue().get(redisKey)?.let {
        meterRegistry.counter("player.cache.hit", "layer", "redis").increment()
        localCache.put(playerId, it)
        return it
    }
    
    // L3: Database miss
    meterRegistry.counter("player.cache.miss").increment()
    return loadFromDatabase(playerId)
}
```

## WARNING: Caching Null Values

**The Problem:**

```kotlin
// BAD - Caching null allows cache penetration attacks
@Cacheable(value = ["players"], key = "#id")
fun findPlayer(id: Long): Player? {
    return playerRepository.findById(id).orElse(null)
}
// Repeated requests for non-existent ID bypass cache
```

**Why This Breaks:**
1. Every request for non-existent ID hits database
2. Attackers can DoS your database with invalid IDs
3. Redis config `disableCachingNullValues()` silently skips nulls

**The Fix:**

```kotlin
// GOOD - Cache a sentinel value or use unless condition
@Cacheable(value = ["players"], key = "#id", unless = "#result == null")
fun findPlayer(id: Long): Player? {
    return playerRepository.findById(id).orElse(null)
}

// Or use a wrapper that caches the absence
data class CacheablePlayer(val player: Player?, val exists: Boolean)
```

## Scheduled Cache Cleanup

```kotlin
@Scheduled(fixedRate = 3600000)  // Every hour
fun scheduledCacheCleanup() {
    logger.debug("Running scheduled cache cleanup")
    
    // Clean up expired Redis entries
    val expiredPattern = "*:expired:*"
    val expiredKeys = redisTemplate.keys(expiredPattern)
    if (expiredKeys.isNotEmpty()) {
        redisTemplate.delete(expiredKeys)
    }
    
    // Remove old entries from active players sorted set
    val activePlayersKey = "active:players:sorted"
    val cutoffTime = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(1)
    redisTemplate.opsForZSet().removeRangeByScore(activePlayersKey, 0.0, cutoffTime.toDouble())
}
```

## Redis Serialization Configuration

```kotlin
@Bean
fun redisTemplate(redisObjectMapper: ObjectMapper): RedisTemplate<String, Any> {
    val template = RedisTemplate<String, Any>()
    template.connectionFactory = redisConnectionFactory()
    template.keySerializer = StringRedisSerializer()
    template.valueSerializer = GenericJackson2JsonRedisSerializer(redisObjectMapper)
    template.hashKeySerializer = StringRedisSerializer()
    template.hashValueSerializer = GenericJackson2JsonRedisSerializer(redisObjectMapper)
    return template
}
```

## Related Skills

For Spring Boot configuration details, see the **spring-boot** skill. For Kotlin-specific patterns in services, see the **kotlin** skill. For JPA repository caching integration, see the **jpa** skill.