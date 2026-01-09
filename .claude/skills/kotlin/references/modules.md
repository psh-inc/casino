```markdown
# Kotlin Modules Reference

Package structure, dependency injection, and module organization in casino-b/.

## Package Structure

```
com.casino.core/
├── controller/      # REST API endpoints (@RestController)
├── service/         # Business logic (@Service, @Transactional)
├── repository/      # Data access (@Repository, JpaRepository)
├── domain/          # JPA entities (@Entity)
├── dto/             # Data transfer objects (data class)
├── config/          # Spring configuration (@Configuration)
├── security/        # Authentication/authorization
├── kafka/           # Event producers/consumers
├── event/           # Domain events
├── scheduler/       # Scheduled tasks (@Scheduled)
└── exception/       # Custom exceptions
```

## Dependency Injection

### Constructor Injection Pattern

```kotlin
@Service
class PaymentService(
    private val paymentRepository: PaymentRepository,
    private val playerRepository: PlayerRepository,
    private val walletService: WalletService,
    private val eventPublisher: ApplicationEventPublisher,
    private val notificationService: NotificationService
) {
    private val logger = LoggerFactory.getLogger(PaymentService::class.java)
    
    // Service methods...
}
```

### Configuration Properties

```kotlin
@ConfigurationProperties(prefix = "app.payment")
data class PaymentProperties(
    val maxRetries: Int = 3,
    val timeoutMs: Long = 30000,
    val currencies: List<String> = listOf("EUR", "USD")
)
```

## WARNING: Field Injection with @Autowired

**The Problem:**

```kotlin
// BAD - Field injection
@Service
class PlayerService {
    @Autowired
    private lateinit var playerRepository: PlayerRepository
    
    @Autowired  
    private lateinit var walletService: WalletService
}
```

**Why This Breaks:**
1. Cannot create instance without Spring context (testing nightmare)
2. Hidden dependencies - not visible in constructor
3. lateinit can cause UninitializedPropertyAccessException
4. Circular dependencies hidden until runtime

**The Fix:**

```kotlin
// GOOD - Constructor injection
@Service
class PlayerService(
    private val playerRepository: PlayerRepository,
    private val walletService: WalletService
) {
    // Dependencies are explicit and required
}
```

**When You Might Be Tempted:**
When you have many dependencies and the constructor looks long. That's a sign to split the service.

## Extension Functions as Modules

### Pattern: Group Extensions by Domain

```kotlin
// ComplianceSettingsServiceExtensions.kt
fun ComplianceSettingsService.getAISettings(): AIComplianceSettings {
    return AIComplianceSettings(
        aiEnabled = getBooleanSetting(ComplianceSettingKeys.AI_ENABLED, false),
        aiAutoApproveThreshold = getDoubleSetting(AI_AUTO_APPROVE_THRESHOLD, 0.95)
    )
}

fun ComplianceSettingsService.setAIEnabled(enabled: Boolean, updatedBy: String) {
    updateSettingByKey(ComplianceSettingKeys.AI_ENABLED, enabled.toString(), updatedBy)
}

fun ComplianceSettingsService.updateAIThresholds(
    autoApproveThreshold: Double? = null,
    manualReviewThreshold: Double? = null,
    updatedBy: String
) {
    autoApproveThreshold?.let {
        require(it in 0.0..1.0) { "Threshold must be between 0 and 1" }
        updateSettingByKey(AI_AUTO_APPROVE_THRESHOLD, it.toString(), updatedBy)
    }
}
```

## Service Layer Patterns

### Transaction Boundaries

```kotlin
@Service
class WalletService(
    private val walletRepository: WalletRepository,
    private val transactionRepository: TransactionRepository
) {
    @Transactional
    fun transfer(from: Long, to: Long, amount: BigDecimal): Transaction {
        val sourceWallet = walletRepository.findByIdForUpdate(from)
            ?: throw NotFoundException("Source wallet not found")
        val targetWallet = walletRepository.findByIdForUpdate(to)
            ?: throw NotFoundException("Target wallet not found")
            
        require(sourceWallet.balance >= amount) { "Insufficient funds" }
        
        sourceWallet.balance = sourceWallet.balance - amount
        targetWallet.balance = targetWallet.balance + amount
        
        return transactionRepository.save(Transaction(...))
    }
    
    @Transactional(readOnly = true)
    fun getBalance(walletId: Long): BigDecimal {
        return walletRepository.findById(walletId)?.balance ?: BigDecimal.ZERO
    }
}
```

## WARNING: Business Logic in Controllers

**The Problem:**

```kotlin
// BAD - Logic in controller
@RestController
class PaymentController(
    private val paymentRepository: PaymentRepository,
    private val walletRepository: WalletRepository
) {
    @PostMapping("/payments")
    fun createPayment(@RequestBody request: PaymentRequest): Payment {
        val wallet = walletRepository.findByPlayerId(request.playerId)!!
        if (wallet.balance < request.amount) {
            throw BadRequestException("Insufficient funds")
        }
        wallet.balance = wallet.balance - request.amount
        walletRepository.save(wallet)
        return paymentRepository.save(Payment(...))
    }
}
```

**Why This Breaks:**
1. Untestable without HTTP context
2. Transaction boundaries unclear
3. Logic duplicated across endpoints
4. Violates Single Responsibility Principle

**The Fix:**

```kotlin
// GOOD - Controller delegates to service
@RestController
class PaymentController(private val paymentService: PaymentService) {
    @PostMapping("/payments")
    @ResponseStatus(HttpStatus.CREATED)
    fun createPayment(@Valid @RequestBody request: PaymentRequest): PaymentDto {
        return paymentService.createPayment(request)
    }
}

@Service
@Transactional
class PaymentService(
    private val paymentRepository: PaymentRepository,
    private val walletService: WalletService
) {
    fun createPayment(request: PaymentRequest): PaymentDto {
        walletService.debit(request.playerId, request.amount)
        val payment = paymentRepository.save(Payment(...))
        return PaymentDto.from(payment)
    }
}
```

## Companion Objects

### Factory Methods

```kotlin
data class PlayerDto(
    val id: Long,
    val username: String,
    val status: PlayerStatus
) {
    companion object {
        fun from(player: Player) = PlayerDto(
            id = player.id!!,
            username = player.username,
            status = player.status
        )
        
        fun fromList(players: List<Player>) = players.map { from(it) }
    }
}
```

### Constants

```kotlin
object KafkaTopics {
    const val PLAYER_REGISTERED = "casino.player.registered.v1"
    const val DEPOSIT_COMPLETED = "casino.payment.deposit-completed.v1"
    const val GAME_BET_PLACED = "casino.game.bet-placed.v1"
}
```

## Related Skills

- See the **spring-boot** skill for @Configuration beans
- See the **kafka** skill for event producer modules
- See the **jpa** skill for repository patterns
```