# Redis Caching Workflows

## Cache Configuration Setup

### Multi-Level Cache Manager

```kotlin
// casino-b/src/main/kotlin/com/casino/core/config/MultiLevelCacheConfig.kt
@Configuration
class MultiLevelCacheConfig {
    
    @Bean
    @Primary
    fun compositeCacheManager(
        @Qualifier("caffeineCacheManager") caffeineCacheManager: CacheManager,
        @Qualifier("redisCacheManager") redisCacheManager: CacheManager
    ): CacheManager {
        return CompositeCacheManager().apply {
            setCacheManagers(listOf(caffeineCacheManager, redisCacheManager))
            setFallbackToNoOpCache(false)
        }
    }
}
```

### Caffeine L1 Cache Configuration

```kotlin
// casino-b/src/main/kotlin/com/casino/core/config/CaffeineConfig.kt
@Configuration
@EnableCaching
class CaffeineConfig {
    
    @Bean("caffeineCacheManager")
    fun caffeineCacheManager(): CacheManager {
        val caffeineCacheManager = CaffeineCacheManager()
        caffeineCacheManager.setCaffeine(
            Caffeine.newBuilder()
                .maximumSize(10_000)
                .expireAfterWrite(Duration.ofMinutes(5))
                .recordStats()
        )
        return caffeineCacheManager
    }
    
    @Bean("playerLocalCache")
    fun playerLocalCache(): Cache<Long, CachedPlayer> {
        return Caffeine.newBuilder()
            .maximumSize(10_000)
            .expireAfterWrite(Duration.ofMinutes(5))
            .expireAfterAccess(Duration.ofMinutes(2))
            .recordStats()
            .build()
    }
}
```

### Redis L2 Cache Configuration

```kotlin
// casino-b/src/main/kotlin/com/casino/core/config/RedisConfig.kt
@Configuration
class RedisConfig {
    
    @Bean("redisCacheManager")
    fun redisCacheManager(connectionFactory: RedisConnectionFactory): RedisCacheManager {
        val defaultConfig = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(1))
            .serializeKeysWith(RedisSerializationContext.SerializationPair
                .fromSerializer(StringRedisSerializer()))
            .serializeValuesWith(RedisSerializationContext.SerializationPair
                .fromSerializer(GenericJackson2JsonRedisSerializer()))
        
        // Per-cache TTL overrides
        val cacheConfigs = mapOf(
            "walletBalance" to defaultConfig.entryTtl(Duration.ofSeconds(30)),
            "playerProfile" to defaultConfig.entryTtl(Duration.ofMinutes(5)),
            "games" to defaultConfig.entryTtl(Duration.ofMinutes(15)),
            "verificationLevels" to defaultConfig.entryTtl(Duration.ofHours(2))
        )
        
        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(defaultConfig)
            .withInitialCacheConfigurations(cacheConfigs)
            .transactionAware()
            .build()
    }
}
```

---

## Cache Warming Workflow

**When:** Application startup or after cache flush

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/cache/CacheManagementService.kt
@Service
class CacheManagementService(
    private val playerRepository: PlayerRepository,
    private val gameRepository: GameRepository,
    private val distributedWalletCache: DistributedWalletCache
) {
    private val logger = LoggerFactory.getLogger(javaClass)
    
    @EventListener(ApplicationReadyEvent::class)
    fun warmCacheOnStartup() {
        logger.info("Warming cache on startup...")
        
        // Warm active player wallets (last 24h activity)
        val activePlayerIds = playerRepository.findActivePlayerIds(
            since = LocalDateTime.now().minusHours(24)
        )
        warmPlayerWallets(activePlayerIds)
        
        // Warm game catalog
        warmGameCache()
        
        logger.info("Cache warming complete: ${activePlayerIds.size} wallets warmed")
    }
    
    fun warmPlayerWallets(playerIds: List<Long>) {
        playerIds.chunked(100).forEach { batch ->
            val wallets = walletRepository.findByPlayerIds(batch)
            distributedWalletCache.warmCache(wallets)
        }
    }
}
```

---

## WARNING: No Cache Warming Strategy

**The Problem:**

```kotlin
// BAD - Cold cache after deployment causes thundering herd
@PostConstruct
fun init() {
    // No cache warming - first requests hit database
}

// Result: 1000 concurrent requests all hit DB simultaneously
```

**Why This Breaks:**
1. First requests after deployment/restart hit database
2. Thundering herd effect under load spikes
3. Database connection pool exhaustion

**The Fix:**

```kotlin
// GOOD - Pre-warm hot data on startup
@EventListener(ApplicationReadyEvent::class)
fun warmCacheOnStartup() {
    val activePlayerIds = playerRepository.findActivePlayerIds(
        since = LocalDateTime.now().minusHours(24)
    )
    distributedWalletCache.warmCache(walletRepository.findByPlayerIds(activePlayerIds))
}
```

---

## Cache Invalidation Patterns

### Single Entity Eviction

```kotlin
@CacheEvict(value = ["playerDetails"], key = "'player:id:' + #id")
fun updatePlayer(id: Long, request: UpdatePlayerRequest): PlayerDto
```

### Multi-Cache Eviction

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/CurrencyService.kt
@CacheEvict(value = ["currencies", "active-currencies", "currency-options"], allEntries = true)
fun createCurrency(request: CreateCurrencyRequest): CurrencyDto
```

### Pattern-Based Eviction

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/cache/PlayerStatisticsCacheService.kt
fun evictPlayerStatisticsCache(playerId: Long) {
    // L1: Clear Caffeine
    localCache.invalidate(playerId)
    
    // L2: Pattern-based Redis eviction
    val pattern = cacheKeys.playerPattern(playerId)  // "player:*:123:*"
    val keys = redisTemplate.keys(pattern)
    if (keys.isNotEmpty()) {
        redisTemplate.delete(keys)
        logger.debug("Evicted ${keys.size} cache entries for player $playerId")
    }
}
```

---

## WARNING: Forgetting L1 Invalidation

**The Problem:**

```kotlin
// BAD - Only evicts Redis, L1 Caffeine still has stale data
@CacheEvict(value = ["players"], key = "#playerId")
fun updatePlayer(playerId: Long, request: UpdateRequest): Player {
    // Spring Cache only targets redisCacheManager
    // Caffeine localCache still has old data!
}
```

**Why This Breaks:**
1. L1 cache serves stale data for its remaining TTL (up to 5 minutes)
2. Users see inconsistent data depending on which server handles request
3. Debug nightmare - "works on my machine" but fails in production

**The Fix:**

```kotlin
// GOOD - Invalidate both layers explicitly
fun updatePlayer(playerId: Long, request: UpdateRequest): Player {
    val player = playerRepository.save(...)
    
    // Evict L1 (Caffeine)
    localCache.invalidate(playerId)
    
    // Evict L2 (Redis) 
    redisTemplate.delete("player:$playerId")
    
    return player
}
```

---

## Cache Health Monitoring

```kotlin
// casino-b/src/main/kotlin/com/casino/core/service/cache/CacheManagementService.kt
fun getCacheHealthStatus(): CacheHealthStatus {
    val caffeineStats = caffeineCache.stats()
    
    val warnings = mutableListOf<String>()
    
    // Check hit rate
    if (caffeineStats.hitRate() < 0.5) {
        warnings.add("Low cache hit rate: ${caffeineStats.hitRate()}")
    }
    
    // Check Redis connectivity
    val redisHealthy = try {
        redisTemplate.connectionFactory?.connection?.ping() == "PONG"
    } catch (e: Exception) {
        warnings.add("Redis connection failed: ${e.message}")
        false
    }
    
    return CacheHealthStatus(
        caffeineHitRate = caffeineStats.hitRate(),
        caffeineSize = caffeineStats.estimatedSize(),
        redisHealthy = redisHealthy,
        warnings = warnings
    )
}
```

---

## application.yml Configuration

```yaml
# casino-b/src/main/resources/application.yml
spring:
  cache:
    type: redis
    redis:
      time-to-live: 3600000  # 1 hour default
      cache-null-values: false
      use-key-prefix: true
      key-prefix: "casino:"
  
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD:}
      timeout: 2000ms
      lettuce:
        pool:
          max-active: 32
          max-idle: 16
          min-idle: 4

# Custom cache config
wallet:
  cache:
    local:
      max-size: 10000
      ttl-seconds: 5
    distributed:
      active-ttl-seconds: 30
      inactive-ttl-seconds: 300
```

---

## Related Skills

- See the **spring-boot** skill for `@Cacheable` annotation configuration
- See the **kotlin** skill for data class serialization with Jackson
- See the **jpa** skill for repository patterns used in cache fallback