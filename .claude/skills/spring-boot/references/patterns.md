# Spring Boot Patterns Reference

## Controller Patterns

### Standard REST Controller

Controllers follow a consistent pattern with OpenAPI documentation and method-level security.

```kotlin
@RestController
@RequestMapping("/api/v1/wallets")
@Tag(name = "Wallets", description = "Wallet and transaction management API")
class WalletController(
    private val walletService: WalletService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @GetMapping("/{playerId}/balance")
    @Operation(summary = "Get player wallet balance")
    @PreAuthorize("hasAnyAuthority('PLAYER') and #playerId == authentication.principal.username or hasAnyAuthority('ADMIN')")
    fun getBalance(@PathVariable playerId: Long): ResponseEntity<WalletSummaryResponse> {
        return ResponseEntity.ok(walletService.getWalletSummary(playerId))
    }
}
```

### WARNING: Business Logic in Controllers

**The Problem:**

```kotlin
// BAD - Controller doing too much
@PostMapping
fun createDeposit(@RequestBody request: DepositRequest): ResponseEntity<*> {
    val player = playerRepository.findById(request.playerId).orElseThrow()
    if (player.status != PlayerStatus.ACTIVE) {
        return ResponseEntity.badRequest().body("Player not active")
    }
    val wallet = walletRepository.findByPlayerId(request.playerId)
    wallet.balance = wallet.balance.add(request.amount)
    walletRepository.save(wallet)
    return ResponseEntity.ok(wallet)
}
```

**Why This Breaks:**
1. Untestable without full Spring context
2. Transaction boundaries unclear
3. No separation of concerns - impossible to reuse logic

**The Fix:**

```kotlin
// GOOD - Controller delegates to service
@PostMapping
fun createDeposit(@Valid @RequestBody request: DepositRequest): ResponseEntity<DepositResponse> {
    return ResponseEntity.status(HttpStatus.CREATED)
        .body(walletService.processDeposit(request))
}
```

**When You Might Be Tempted:** Quick prototypes, "simple" endpoints that grow complex over time.

---

## Service Layer Patterns

### Transactional Service with Caching

```kotlin
@Service
class PlayerService(
    private val repository: PlayerRepository,
    private val eventService: PlayerEventService
) {
    @Transactional(readOnly = true)
    @Cacheable(cacheNames = ["playerDetails"], key = "'player:id:' + #id")
    fun getPlayerById(id: Long): PlayerDetailsResponse {
        val player = repository.findByIdWithDetails(id)
            .orElseThrow { ResourceNotFoundException("Player not found: $id") }
        return mapToPlayerDetailsResponse(player)
    }

    @Transactional
    @Caching(
        evict = [
            CacheEvict(cacheNames = ["playerDetails"], key = "'player:id:' + #id"),
            CacheEvict(cacheNames = ["playerEntity"], allEntries = true)
        ]
    )
    fun updatePlayerStatus(id: Long, status: PlayerStatus): PlayerDetailsResponse {
        val player = repository.findById(id)
            .orElseThrow { ResourceNotFoundException("Player not found: $id") }
        val updated = player.copy(status = status, updatedAt = LocalDateTime.now())
        return mapToPlayerDetailsResponse(repository.save(updated))
    }
}
```

### WARNING: Throwing Exceptions in Event Publishers

**The Problem:**

```kotlin
// BAD - Event failure breaks main flow
@Transactional
fun registerPlayer(request: PlayerRegistrationRequest): PlayerResponse {
    val player = repository.save(Player(username = request.username))
    eventService.publishPlayerRegistered(player) // If this throws, registration fails!
    return PlayerResponse.from(player)
}
```

**Why This Breaks:**
1. Kafka unavailability breaks user registration
2. Event publishing is secondary to core business logic
3. User sees error even though registration succeeded

**The Fix:**

```kotlin
// GOOD - Fire-and-forget pattern
@Transactional
fun registerPlayer(request: PlayerRegistrationRequest): PlayerResponse {
    val player = repository.save(Player(username = request.username))
    try {
        eventService.publishPlayerRegistered(player)
    } catch (e: Exception) {
        logger.error("Failed to publish player registered event: ${player.id}", e)
        // Don't throw - event publishing should not break main flow
    }
    return PlayerResponse.from(player)
}
```

**When You Might Be Tempted:** When you want "guaranteed" event delivery (use outbox pattern instead).

---

## Configuration Patterns

### Externalized Configuration with Defaults

```kotlin
@Configuration
class AsyncConfig {
    @Value("\${async.wallet.core-size:32}")
    private var walletCoreSize: Int = 32

    @Value("\${async.wallet.max-size:128}")
    private var walletMaxSize: Int = 128

    @Bean("walletAsyncExecutor")
    fun walletAsyncExecutor(): Executor {
        val executor = ThreadPoolTaskExecutor()
        executor.corePoolSize = walletCoreSize
        executor.maxPoolSize = walletMaxSize
        executor.setThreadNamePrefix("wallet-async-")
        executor.setRejectedExecutionHandler(ThreadPoolExecutor.CallerRunsPolicy())
        executor.setWaitForTasksToCompleteOnShutdown(true)
        executor.setAwaitTerminationSeconds(60)
        executor.initialize()
        return executor
    }
}
```

### WARNING: Hardcoded Configuration Values

**The Problem:**

```kotlin
// BAD - Hardcoded values
@Bean
fun restTemplate(): RestTemplate {
    return RestTemplateBuilder()
        .setConnectTimeout(Duration.ofSeconds(10))
        .setReadTimeout(Duration.ofSeconds(30))
        .build()
}
```

**Why This Breaks:**
1. Can't tune for different environments
2. Requires code change and redeploy to adjust
3. No visibility into what values are configured

**The Fix:**

```kotlin
// GOOD - Externalized with sensible defaults
@Value("\${http.client.connect-timeout-seconds:10}")
private var connectTimeout: Long = 10

@Value("\${http.client.read-timeout-seconds:30}")
private var readTimeout: Long = 30

@Bean
fun restTemplate(): RestTemplate {
    return RestTemplateBuilder()
        .setConnectTimeout(Duration.ofSeconds(connectTimeout))
        .setReadTimeout(Duration.ofSeconds(readTimeout))
        .build()
}
```

---

## Security Patterns

### JWT + OAuth2 Resource Server

```kotlin
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig(
    private val jwtAuthenticationFilter: JwtAuthenticationFilter
) {
    @Bean
    fun securityFilterChain(http: HttpSecurity): SecurityFilterChain {
        return http
            .csrf { it.disable() }
            .sessionManagement { it.sessionCreationPolicy(SessionCreationPolicy.STATELESS) }
            .authorizeHttpRequests { authorize ->
                authorize
                    .requestMatchers("/api/auth/**").permitAll()
                    .requestMatchers("/actuator/**").permitAll()
                    .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                    .anyRequest().authenticated()
            }
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter::class.java)
            .build()
    }

    @Bean
    fun passwordEncoder(): PasswordEncoder {
        return Argon2PasswordEncoder(16, 32, 1, 65536, 4)
    }
}
```

---

## Exception Handling Patterns

### Global Exception Handler with Logging

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler(
    private val exceptionLoggingService: Optional<ExceptionLoggingService>
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleNotFound(ex: ResourceNotFoundException, request: WebRequest): ResponseEntity<ErrorResponse> {
        return ResponseEntity(
            ErrorResponse(
                timestamp = LocalDateTime.now(),
                status = HttpStatus.NOT_FOUND.value(),
                error = "Not Found",
                message = ex.message ?: "Resource not found",
                path = request.getDescription(false).substringAfter("uri=")
            ),
            HttpStatus.NOT_FOUND
        )
    }

    @ExceptionHandler(Exception::class)
    fun handleGlobalException(ex: Exception, request: WebRequest): ResponseEntity<ErrorResponse> {
        logger.error("Unhandled exception", ex)
        // Log 5xx to OpenSearch
        exceptionLoggingService.ifPresent { it.logException(request, ex) }
        return ResponseEntity(
            ErrorResponse(status = 500, error = "Internal Server Error", message = ex.message ?: ""),
            HttpStatus.INTERNAL_SERVER_ERROR
        )
    }
}
```

See the **jpa** skill for repository patterns and the **kafka** skill for event publishing.