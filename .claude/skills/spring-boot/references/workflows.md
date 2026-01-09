# Spring Boot Workflows

## Development Workflow

### Starting the Backend

```bash
cd casino-b
cp ../.env.example .env  # Configure credentials
./gradlew clean build    # Compile and test
./gradlew bootRun        # Start on port 8080
```

### Running Tests

```bash
# All tests
./gradlew test

# Specific test class
./gradlew test --tests "PlayerServiceTest"

# With coverage report
./gradlew jacocoTestReport
```

---

## Creating a New Endpoint

### 1. Define the DTO

```kotlin
// src/main/kotlin/com/casino/core/dto/CreateBonusRequest.kt
data class CreateBonusRequest(
    @field:NotBlank(message = "Name is required")
    val name: String,

    @field:NotNull(message = "Amount is required")
    @field:DecimalMin(value = "0.01", message = "Amount must be positive")
    val amount: BigDecimal,

    @field:NotNull
    val type: BonusType
)
```

### 2. Create the Service Method

```kotlin
@Service
class BonusService(
    private val bonusRepository: BonusRepository,
    private val eventPublisher: EventPublisher
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Transactional
    fun create(request: CreateBonusRequest): BonusDto {
        val bonus = Bonus(
            name = request.name,
            amount = request.amount,
            type = request.type
        )
        val saved = bonusRepository.save(bonus)
        
        // Fire-and-forget event
        try {
            eventPublisher.publish(KafkaTopics.BONUS_CREATED, saved.id.toString(), event)
        } catch (e: Exception) {
            logger.error("Event publish failed", e)
        }
        
        return BonusDto.from(saved)
    }
}
```

### 3. Add Controller Endpoint

```kotlin
@RestController
@RequestMapping("/api/v1/admin/bonuses")
@Tag(name = "Bonus Admin", description = "Bonus administration API")
class BonusAdminController(private val bonusService: BonusService) {

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Create a new bonus")
    @PreAuthorize("hasAuthority('ADMIN')")
    fun create(@Valid @RequestBody request: CreateBonusRequest): BonusDto {
        return bonusService.create(request)
    }
}
```

---

## Testing Patterns

### Unit Testing Services with MockK

```kotlin
@ExtendWith(MockKExtension::class)
class BonusServiceTest {

    @MockK
    private lateinit var bonusRepository: BonusRepository

    @MockK
    private lateinit var eventPublisher: EventPublisher

    @InjectMockKs
    private lateinit var bonusService: BonusService

    @Test
    fun `create should save bonus and return DTO`() {
        // Given
        val request = CreateBonusRequest(
            name = "Welcome Bonus",
            amount = BigDecimal("100.00"),
            type = BonusType.DEPOSIT
        )
        val savedBonus = Bonus(id = 1L, name = "Welcome Bonus", ...)
        
        every { bonusRepository.save(any()) } returns savedBonus
        every { eventPublisher.publish(any(), any(), any<Any>()) } just Runs

        // When
        val result = bonusService.create(request)

        // Then
        assertThat(result.name).isEqualTo("Welcome Bonus")
        verify { bonusRepository.save(any()) }
    }
}
```

### Integration Testing with @SpringBootTest

```kotlin
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class BonusControllerIntegrationTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @Autowired
    private lateinit var objectMapper: ObjectMapper

    @Test
    @WithMockUser(authorities = ["ADMIN"])
    fun `POST should create bonus and return 201`() {
        val request = CreateBonusRequest(
            name = "Test Bonus",
            amount = BigDecimal("50.00"),
            type = BonusType.DEPOSIT
        )

        mockMvc.perform(
            post("/api/v1/admin/bonuses")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request))
        )
            .andExpect(status().isCreated)
            .andExpect(jsonPath("$.name").value("Test Bonus"))
    }
}
```

---

## Database Migrations

### Creating a New Migration

```sql
-- src/main/resources/db/migration/V20250106120000__add_bonus_table.sql
CREATE TABLE bonuses (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(19, 2) NOT NULL,
    type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_bonuses_type ON bonuses(type);
```

### WARNING: Using SERIAL Instead of BIGSERIAL

**The Problem:**

```sql
-- BAD - Will overflow at 2.1 billion records
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    ...
);
```

**Why This Breaks:**
1. SERIAL is 4 bytes (max 2,147,483,647)
2. High-volume tables hit this in production
3. Migration to BIGSERIAL requires downtime

**The Fix:**

```sql
-- GOOD - 8 bytes, practically unlimited
CREATE TABLE players (
    id BIGSERIAL PRIMARY KEY,
    ...
);
```

---

## Configuration Best Practices

### Environment-Specific Configuration

```yaml
# application.yml - defaults
spring:
  datasource:
    url: ${SPRING_DATASOURCE_URL}
    username: ${SPRING_DATASOURCE_USERNAME}
    password: ${SPRING_DATASOURCE_PASSWORD}
  
cache:
  multilevel:
    enabled: true

---
# application-dev.yml - development overrides
spring:
  config:
    activate:
      on-profile: dev
      
logging:
  level:
    com.casino: DEBUG
```

### WARNING: Hardcoded Secrets

**The Problem:**

```kotlin
// BAD - Secrets in code
@Configuration
class PaymentConfig {
    val apiKey = "sk_live_abc123xyz"  // Committed to git!
}
```

**The Fix:**

```kotlin
// GOOD - Environment variables
@Configuration
class PaymentConfig(
    @Value("\${payment.api-key}") 
    private val apiKey: String
)
```

---

## Debugging Common Issues

### 401 Unauthorized

1. Check JWT token format: `Authorization: Bearer <token>`
2. Verify JWT secret is 64+ characters for HS512
3. Check token expiration

### N+1 Query Problems

```kotlin
// BAD - N+1 queries
@Transactional(readOnly = true)
fun getPlayersWithWallets(): List<PlayerDto> {
    return playerRepository.findAll() // 1 query
        .map { 
            val wallet = it.wallet // N queries!
            PlayerDto(it, wallet)
        }
}

// GOOD - Single query with JOIN FETCH
@Query("SELECT p FROM Player p LEFT JOIN FETCH p.wallet")
fun findAllWithWallets(): List<Player>
```

### Cache Not Working

1. Ensure `@EnableCaching` is present
2. Check cache name matches configuration
3. Verify cache key is correct type (Long vs String)

See the **postgresql** skill for migration patterns.
See the **redis** skill for cache configuration.