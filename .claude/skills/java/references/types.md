```markdown
# Java Type Mappings

Type interop between Java 21, Kotlin, JPA, and PostgreSQL in this project.

## Core Type Mappings

| Java Type | Kotlin Type | JPA/Hibernate | PostgreSQL |
|-----------|-------------|---------------|------------|
| `Long` | `Long` | `@Id` | `BIGSERIAL` |
| `BigDecimal` | `BigDecimal` | `precision=19, scale=2` | `DECIMAL(19,2)` |
| `LocalDateTime` | `LocalDateTime` | `@Column` | `TIMESTAMP WITH TIME ZONE` |
| `LocalDate` | `LocalDate` | `@Column` | `DATE` |
| `String` | `String` | `@Column` | `VARCHAR(n)` / `TEXT` |
| `Boolean` | `Boolean` | `@Column` | `BOOLEAN` |

## WARNING: BigDecimal from Double

**The Problem:**

```kotlin
// BAD - Precision loss from floating point
val amount = BigDecimal(123.45)  // Actually 123.4499999999999...
val price = BigDecimal(0.1 + 0.2) // Not 0.3!
```

**Why This Breaks:**
1. Financial calculations become incorrect
2. Balance mismatches accumulate over time
3. Audit failures and compliance issues

**The Fix:**

```kotlin
// GOOD - Always from String
val amount = BigDecimal("123.45")
val zero = BigDecimal.ZERO
val percentage = BigDecimal("0.05")

// Arithmetic
val total = amount.multiply(BigDecimal("1.10"))
```

**When You Might Be Tempted:**
Receiving a `Double` from an external API. Always convert to String first.

## WARNING: BigDecimal Equality Comparison

**The Problem:**

```kotlin
// BAD - Scale affects equality
val a = BigDecimal("10.0")
val b = BigDecimal("10.00")
println(a == b)  // false!
```

**Why This Breaks:**
1. Conditionals fail unexpectedly
2. Tests become flaky
3. Balance checks give wrong results

**The Fix:**

```kotlin
// GOOD - Use compareTo for value equality
if (amount.compareTo(BigDecimal.ZERO) > 0) {
    // Positive balance
}

if (a.compareTo(b) == 0) {
    // Values are equal regardless of scale
}
```

## Date/Time Handling

### Jackson Configuration

```kotlin
// JacksonConfig.kt
companion object {
    val DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd")
    val DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss'Z'")
}

@Bean
fun jsonCustomizer(): Jackson2ObjectMapperBuilderCustomizer {
    return Jackson2ObjectMapperBuilderCustomizer { builder ->
        val javaTimeModule = JavaTimeModule()
        javaTimeModule.addSerializer(LocalDateTime::class.java,
            LocalDateTimeSerializer(DATE_TIME_FORMATTER))
        javaTimeModule.addDeserializer(LocalDateTime::class.java,
            FlexibleLocalDateTimeDeserializer())
        builder.modules(KotlinModule.Builder().build(), javaTimeModule)
        builder.featuresToDisable(WRITE_DATES_AS_TIMESTAMPS)
    }
}
```

### WARNING: Timestamp Without Timezone

**The Problem:**

```sql
-- BAD - No timezone info
CREATE TABLE events (
    created_at TIMESTAMP
);
```

**Why This Breaks:**
1. Server timezone changes corrupt data
2. Multi-region deployments show wrong times
3. DST transitions cause duplicate/missing records

**The Fix:**

```sql
-- GOOD - Always store with timezone
CREATE TABLE events (
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Nullable Types

Kotlin's null-safety maps to Java's nullable annotations.

```kotlin
// Kotlin nullable → Java @Nullable
data class PlayerRequest(
    val username: String,           // Required (non-null)
    val phoneNumber: String? = null // Optional (nullable)
)

// JPA entity with nullable fields
@Entity
data class Player(
    @Id @GeneratedValue(strategy = IDENTITY)
    val id: Long? = null,  // Null before persistence
    
    @Column(nullable = false)
    val email: String,     // Always required
    
    @Column(nullable = true)
    val phoneNumber: String? = null
)
```

## Enum Handling

```kotlin
// Kotlin enum
enum class PlayerStatus {
    PENDING, ACTIVE, FROZEN, BLOCKED, SUSPENDED
}

// JPA mapping - defaults to ordinal (avoid!)
@Enumerated(EnumType.STRING)  // Store as string
@Column(name = "status")
val status: PlayerStatus = PlayerStatus.PENDING
```

**ALWAYS** use `EnumType.STRING` to avoid ordinal position bugs.

## Collection Type Mappings

| Java | Kotlin | JPA Annotation |
|------|--------|----------------|
| `List<E>` | `List<E>` | `@OneToMany` |
| `Set<E>` | `Set<E>` | `@ManyToMany` |
| `Map<K,V>` | `Map<K,V>` | `@ElementCollection` |

See the **jpa** skill for entity relationship patterns.
```