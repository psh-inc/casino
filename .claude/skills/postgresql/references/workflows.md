# PostgreSQL Workflows Reference

## Migration Workflow

### Creating Migrations

**Naming Convention:** `V{yyyyMMddHHmmss}__{description}.sql`

```bash
# Generate timestamp in UTC
date -u +"%Y%m%d%H%M%S"
# Output: 20260110143022

# Create migration file
touch casino-b/src/main/resources/db/migration/V20260110143022__add_player_loyalty_tier.sql
```

### Migration Best Practices

```sql
-- V20260110143022__add_player_loyalty_tier.sql

-- 1. Always use IF NOT EXISTS for safety
CREATE TABLE IF NOT EXISTS player_loyalty_tiers (
    id BIGSERIAL PRIMARY KEY,
    player_id BIGINT NOT NULL REFERENCES players(id),
    tier VARCHAR(20) NOT NULL DEFAULT 'BRONZE',
    points NUMERIC(15,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 2. Create indices with IF NOT EXISTS
CREATE INDEX IF NOT EXISTS idx_loyalty_player_id 
ON player_loyalty_tiers(player_id);

-- 3. Use separate statements for ALTER operations
ALTER TABLE player_loyalty_tiers 
ADD CONSTRAINT chk_tier_values 
CHECK (tier IN ('BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND'));
```

### WARNING: Destructive Migrations Without Backup Plan

**The Problem:**

```sql
-- BAD - irreversible data loss
ALTER TABLE players DROP COLUMN legacy_field;
DROP TABLE old_transactions;
```

**Why This Breaks:**
1. No rollback if deployment fails
2. Lost data cannot be recovered
3. Compliance violations for financial data

**The Fix:**

```sql
-- GOOD - rename first, drop in later migration
ALTER TABLE players RENAME COLUMN legacy_field TO _legacy_field_deprecated;
-- Then in V202601151200__cleanup_deprecated.sql (after verification):
-- ALTER TABLE players DROP COLUMN _legacy_field_deprecated;
```

### Running Migrations

```bash
# Via Gradle
cd casino-b
./gradlew flywayMigrate

# Via application startup (automatic)
./gradlew bootRun

# Check migration status
./gradlew flywayInfo
```

## Entity Mapping Workflow

### 1. Design Table First

```sql
CREATE TABLE bonus_claims (
    id BIGSERIAL PRIMARY KEY,
    player_id BIGINT NOT NULL REFERENCES players(id),
    bonus_id BIGINT NOT NULL REFERENCES bonuses(id),
    amount_credited NUMERIC(19,4) NOT NULL,
    wagering_required NUMERIC(19,4) NOT NULL,
    wagering_completed NUMERIC(19,4) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    claimed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    forfeited_at TIMESTAMP WITH TIME ZONE
);
```

### 2. Create Entity

```kotlin
@Entity
@Table(name = "bonus_claims")
data class BonusClaim(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false)
    val player: Player,
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "bonus_id", nullable = false)
    val bonus: Bonus,
    
    @Column(name = "amount_credited", nullable = false, precision = 19, scale = 4)
    val amountCredited: BigDecimal,
    
    @Column(name = "wagering_required", nullable = false, precision = 19, scale = 4)
    val wageringRequired: BigDecimal,
    
    @Column(name = "wagering_completed", nullable = false, precision = 19, scale = 4)
    var wageringCompleted: BigDecimal = BigDecimal.ZERO,
    
    @Column(nullable = false, length = 20)
    @Enumerated(EnumType.STRING)
    var status: BonusClaimStatus = BonusClaimStatus.ACTIVE,
    
    @Column(name = "claimed_at", nullable = false)
    val claimedAt: LocalDateTime = LocalDateTime.now(),
    
    @Column(name = "completed_at")
    var completedAt: LocalDateTime? = null
) {
    // Required for JPA proxies
    override fun hashCode(): Int = id?.hashCode() ?: 0
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is BonusClaim) return false
        return id != null && id == other.id
    }
}
```

### 3. Create Repository

```kotlin
@Repository
interface BonusClaimRepository : JpaRepository<BonusClaim, Long> {
    
    fun findByPlayerIdAndStatus(
        playerId: Long, 
        status: BonusClaimStatus
    ): List<BonusClaim>
    
    @Query("""
        SELECT bc FROM BonusClaim bc
        LEFT JOIN FETCH bc.bonus
        WHERE bc.player.id = :playerId
        ORDER BY bc.claimedAt DESC
    """)
    fun findByPlayerIdWithBonus(
        @Param("playerId") playerId: Long,
        pageable: Pageable
    ): Page<BonusClaim>
}
```

## Testing Database Queries

### Unit Testing Repositories

```kotlin
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class BonusClaimRepositoryTest {
    
    companion object {
        @Container
        val postgres = PostgreSQLContainer<Nothing>("postgres:14").apply {
            withDatabaseName("testdb")
        }
        
        @JvmStatic
        @DynamicPropertySource
        fun properties(registry: DynamicPropertyRegistry) {
            registry.add("spring.datasource.url", postgres::getJdbcUrl)
            registry.add("spring.datasource.username", postgres::getUsername)
            registry.add("spring.datasource.password", postgres::getPassword)
        }
    }
    
    @Autowired
    lateinit var repository: BonusClaimRepository
    
    @Test
    fun `should find active claims by player`() {
        // Arrange - use TestEntityManager or fixtures
        
        // Act
        val claims = repository.findByPlayerIdAndStatus(playerId, ACTIVE)
        
        // Assert
        assertThat(claims).hasSize(2)
    }
}
```

### Verifying Query Performance

```kotlin
// Add to test to catch N+1 issues
@Test
fun `should load claims with single query`() {
    // Enable query counting in test properties
    val queryCount = DataSourceUtils.getQueryCount()
    
    val claims = repository.findByPlayerIdWithBonus(playerId, Pageable.unpaged())
    claims.content.forEach { it.bonus.name }  // Access lazy field
    
    // Should be exactly 1 query due to JOIN FETCH
    assertThat(DataSourceUtils.getQueryCount() - queryCount).isEqualTo(1)
}
```

## Performance Troubleshooting

### Analyze Slow Queries

```sql
-- Enable query logging temporarily
SET log_statement = 'all';
SET log_duration = on;

-- Analyze specific query
EXPLAIN ANALYZE 
SELECT * FROM transactions 
WHERE wallet_id = 123 
AND created_at > NOW() - INTERVAL '30 days';
```

### Common Performance Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Slow joins | Missing FK index | Add index on FK column |
| Sequential scans | Missing composite index | Create covering index |
| Lock waits | Long transactions | Reduce transaction scope |
| Memory issues | Large result sets | Add pagination, use streaming |

### Connection Pool Monitoring

```yaml
# application.yml - HikariCP settings
spring:
  datasource:
    hikari:
      maximum-pool-size: 50
      minimum-idle: 10
      connection-timeout: 20000
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 60000  # Warn if connection held > 1 min
```

## Related Skills

- See the **jpa** skill for advanced entity relationships
- See the **spring-boot** skill for `@Transactional` configuration