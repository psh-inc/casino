# Spring Boot Patterns

## Controller Patterns

### Standard REST Controller

```kotlin
@RestController
@RequestMapping("/api/v1/bonuses")
@Tag(name = "Bonuses", description = "Bonus management API")
class BonusController(
    private val bonusService: BonusService
) {
    @GetMapping
    @Operation(summary = "List bonuses with pagination")
    fun list(@PageableDefault(size = 20) pageable: Pageable): Page<BonusDto> {
        return bonusService.findAll(pageable)
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun create(@Valid @RequestBody request: CreateBonusRequest): BonusDto {
        return bonusService.create(request)
    }

    @PatchMapping("/{id}/activate")
    fun activate(@PathVariable id: Long): BonusDto {
        return bonusService.activate(id)
    }
}
```

### WARNING: Business Logic in Controllers

**The Problem:**

```kotlin
// BAD - Controller doing service work
@PostMapping
fun create(@RequestBody request: CreatePlayerRequest): ResponseEntity<Player> {
    if (playerRepository.existsByEmail(request.email)) {
        throw ResourceAlreadyExistsException("Email exists")
    }
    val player = Player(email = request.email)
    val saved = playerRepository.save(player)
    walletRepository.save(Wallet(player = saved))
    return ResponseEntity.status(201).body(saved)
}
```

**Why This Breaks:**
1. Untestable without full Spring context
2. Transaction boundaries are wrong - wallet creation not atomic
3. No caching, no events, violates SRP

**The Fix:**

```kotlin
// GOOD - Controller delegates to service
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
fun create(@Valid @RequestBody request: CreatePlayerRequest): PlayerDto {
    return playerService.registerPlayer(request)
}
```

**When You Might Be Tempted:** Simple CRUD operations where "it's just one line."

---

## Service Patterns

### Transactional Service

```kotlin
@Service
class WalletService(
    private val walletRepository: WalletRepository,
    private val transactionRepository: TransactionRepository
) {
    @Transactional(readOnly = true)
    fun getBalance(playerId: Long): WalletDto {
        return walletRepository.findByPlayerId(playerId)
            .map { WalletDto.from(it) }
            .orElseThrow { ResourceNotFoundException("Wallet not found") }
    }

    @Transactional
    fun debit(playerId: Long, amount: BigDecimal): WalletDto {
        val wallet = walletRepository.findByPlayerIdForUpdate(playerId)
            .orElseThrow { ResourceNotFoundException("Wallet not found") }
        
        if (wallet.balance < amount) {
            throw InsufficientFundsException("Insufficient balance")
        }
        
        wallet.balance = wallet.balance.subtract(amount)
        transactionRepository.save(Transaction(wallet = wallet, amount = amount.negate()))
        return WalletDto.from(walletRepository.save(wallet))
    }
}
```

### WARNING: Missing @Transactional on Write Operations

**The Problem:**

```kotlin
// BAD - No transaction boundary
fun transferFunds(from: Long, to: Long, amount: BigDecimal) {
    val sourceWallet = walletRepository.findById(from).get()
    sourceWallet.balance = sourceWallet.balance.subtract(amount)
    walletRepository.save(sourceWallet)
    
    val destWallet = walletRepository.findById(to).get() // Fails here?
    destWallet.balance = destWallet.balance.add(amount)
    walletRepository.save(destWallet)
}
```

**Why This Breaks:**
1. If second save fails, money disappears
2. Race conditions with concurrent requests
3. No rollback capability

**The Fix:**

```kotlin
// GOOD - Atomic transaction
@Transactional
fun transferFunds(from: Long, to: Long, amount: BigDecimal) {
    val sourceWallet = walletRepository.findByIdForUpdate(from).get()
    val destWallet = walletRepository.findByIdForUpdate(to).get()
    // Both succeed or both rollback
    sourceWallet.balance = sourceWallet.balance.subtract(amount)
    destWallet.balance = destWallet.balance.add(amount)
}
```

---

## Caching Patterns

### Multi-Level Cache Usage

```kotlin
@Service
class GameService(
    private val gameRepository: GameRepository
) {
    // L1 (Caffeine) → L2 (Redis) → Database
    @Cacheable(value = ["games"], key = "#id")
    fun findById(id: Long): GameDto {
        return gameRepository.findById(id)
            .map { GameDto.from(it) }
            .orElseThrow { ResourceNotFoundException("Game not found") }
    }

    @CacheEvict(value = ["games"], key = "#result.id")
    @Transactional
    fun update(id: Long, request: UpdateGameRequest): GameDto {
        val game = gameRepository.findById(id).orElseThrow { ... }
        game.apply { name = request.name }
        return GameDto.from(gameRepository.save(game))
    }
}
```

### WARNING: Caching Mutable Objects

**The Problem:**

```kotlin
// BAD - Returns mutable entity, cache gets corrupted
@Cacheable(value = ["players"], key = "#id")
fun findById(id: Long): Player {
    return playerRepository.findById(id).get()
}

// Caller modifies cached object
val player = playerService.findById(1)
player.status = PlayerStatus.BLOCKED // Corrupts cache!
```

**The Fix:**

```kotlin
// GOOD - Return immutable DTO
@Cacheable(value = ["players"], key = "#id")
fun findById(id: Long): PlayerDto {
    return playerRepository.findById(id)
        .map { PlayerDto.from(it) }
        .orElseThrow { ResourceNotFoundException("Player not found") }
}
```

---

## Exception Pattern

### Custom Exception Hierarchy

```kotlin
// Base exceptions with proper HTTP status
@ResponseStatus(HttpStatus.NOT_FOUND)
class ResourceNotFoundException(message: String) : RuntimeException(message)

@ResponseStatus(HttpStatus.CONFLICT)
class ResourceAlreadyExistsException(message: String) : RuntimeException(message)

@ResponseStatus(HttpStatus.PAYMENT_REQUIRED)
class InsufficientFundsException(message: String) : RuntimeException(message)

@ResponseStatus(HttpStatus.PRECONDITION_FAILED)
class BusinessRuleViolationException(message: String) : RuntimeException(message)
```

### WARNING: Swallowing Exceptions Silently

**The Problem:**

```kotlin
// BAD - Silent failure
fun processPayment(amount: BigDecimal) {
    try {
        paymentGateway.charge(amount)
    } catch (e: Exception) {
        // Nothing happens - payment fails silently
    }
}
```

**The Fix:**

```kotlin
// GOOD - Log and handle appropriately
fun processPayment(amount: BigDecimal) {
    try {
        paymentGateway.charge(amount)
    } catch (e: PaymentGatewayException) {
        logger.error("Payment failed: ${e.message}", e)
        throw ExternalServiceException("Payment processing failed")
    }
}
```

---

## Security Patterns

### Method-Level Security

```kotlin
@RestController
@RequestMapping("/api/v1/admin/players")
class AdminPlayerController(private val playerService: PlayerService) {

    @GetMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    fun listAll(pageable: Pageable): Page<PlayerDto> {
        return playerService.findAll(pageable)
    }

    @PatchMapping("/{id}/block")
    @PreAuthorize("hasAuthority('ADMIN') and !#id.equals(authentication.principal.id)")
    fun blockPlayer(@PathVariable id: Long): PlayerDto {
        return playerService.updateStatus(id, PlayerStatus.BLOCKED)
    }
}
```

See the **jpa** skill for entity mapping and query patterns.
See the **kafka** skill for event publishing details.