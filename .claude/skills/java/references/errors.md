```markdown
# Java Runtime Errors

Common JVM errors, causes, and solutions for this casino platform.

## InaccessibleObjectException

**Error:**
```
java.lang.reflect.InaccessibleObjectException:
Unable to make field private final java.math.BigInteger java.math.BigDecimal.intVal accessible:
module java.base does not "opens java.math" to unnamed module
```

**Cause:** Java 21's strong encapsulation blocks reflection on JDK internals.

**Solution:**
```kotlin
// build.gradle.kts
tasks.withType<Test> {
    jvmArgs(
        "--add-opens", "java.base/java.math=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
        "--add-opens", "java.base/java.util=ALL-UNNAMED",
        "--add-opens", "java.base/java.time=ALL-UNNAMED"
    )
}
```

## OutOfMemoryError: Java Heap Space

**Error:**
```
java.lang.OutOfMemoryError: Java heap space
```

**Cause:** Heap exhausted during builds or batch processing.

**Solution:**
```properties
# gradle.properties
org.gradle.jvmargs=-Xmx4096m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=./heapdumps/
```

**Debug:** Analyze heap dump with `jmap` or VisualVM.

## OutOfMemoryError: Metaspace

**Error:**
```
java.lang.OutOfMemoryError: Metaspace
```

**Cause:** Too many classes loaded (common with Spring Boot dev reload).

**Solution:**
```properties
# gradle.properties
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1024m
```

## WARNING: Silent Thread Pool Exhaustion

**The Problem:**

```kotlin
// BAD - No logging when pool is saturated
executor.setRejectedExecutionHandler(DiscardPolicy())
```

**Why This Breaks:**
1. Tasks silently disappear
2. No metrics on rejection rate
3. Production issues go unnoticed until user complaints

**The Fix:**

```kotlin
// GOOD - Log rejections for monitoring
executor.setRejectedExecutionHandler { r, executor ->
    logger.warn("Task rejected - pool saturated: ${executor.threadNamePrefix}")
    // Optionally: metrics.increment("thread_pool.rejected")
    CallerRunsPolicy().rejectedExecution(r, executor)
}
```

## Jackson Deserialization Failures

**Error:**
```
com.fasterxml.jackson.databind.exc.InvalidDefinitionException:
Cannot construct instance of `Player` (no Creators, like default constructor, exist)
```

**Cause:** Kotlin data class without no-arg constructor.

**Solution:**
```kotlin
// build.gradle.kts - noArg plugin
noArg {
    annotation("jakarta.persistence.Entity")
    annotation("com.fasterxml.jackson.annotation.JsonIgnoreProperties")
    invokeInitializers = true
}
```

## HikariPool Connection Timeout

**Error:**
```
HikariPool-1 - Connection is not available, request timed out after 30000ms
```

**Cause:** Pool exhausted due to connection leaks or too many concurrent queries.

**Solution:**
```yaml
# application.yml
spring:
  datasource:
    hikari:
      maximum-pool-size: 50
      minimum-idle: 10
      connection-timeout: 20000
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 60000  # Detect leaks!
```

**Debug:** Enable leak detection to find unclosed connections.

## CircuitBreakerOpenException

**Error:**
```
io.github.resilience4j.circuitbreaker.CallNotPermittedException:
CircuitBreaker 'kafka-publisher' is OPEN
```

**Cause:** Downstream service (Kafka/BetBy) failures triggered circuit breaker.

**Solution:** Wait for cooldown period or check downstream service health.

```yaml
# application.yml
resilience4j:
  circuitbreaker:
    instances:
      kafka-publisher:
        failureRateThreshold: 50
        waitDurationInOpenState: 30s
        slidingWindowSize: 10
```

## DateTimeParseException

**Error:**
```
java.time.format.DateTimeParseException:
Text '2025-01-15T10:30:00.000Z' could not be parsed
```

**Cause:** Timezone suffix 'Z' not handled by default formatter.

**Solution:**
```kotlin
// JacksonConfig.kt - Flexible deserializer
class FlexibleLocalDateTimeDeserializer : JsonDeserializer<LocalDateTime>() {
    override fun deserialize(p: JsonParser, ctxt: DeserializationContext): LocalDateTime {
        val text = p.text
        return try {
            LocalDateTime.parse(text, DateTimeFormatter.ISO_DATE_TIME)
        } catch (e: Exception) {
            // Handle 'Z' suffix
            LocalDateTime.parse(text.removeSuffix("Z"),
                DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS"))
        }
    }
}
```

## ClassNotFoundException: Kotlin Reflect

**Error:**
```
java.lang.ClassNotFoundException: kotlin.reflect.full.KClasses
```

**Cause:** Missing kotlin-reflect dependency.

**Solution:**
```kotlin
// build.gradle.kts
dependencies {
    implementation("org.jetbrains.kotlin:kotlin-reflect")
}
```

## NoSuchMethodError with Spring Boot

**Error:**
```
java.lang.NoSuchMethodError: 'void org.springframework...'
```

**Cause:** Version mismatch between Spring Boot and a dependency.

**Solution:**
```kotlin
// Use Spring's dependency management
plugins {
    id("io.spring.dependency-management") version "1.1.3"
}

// Don't override Spring-managed versions unless necessary
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    // NO explicit version - managed by BOM
}
```

## Test Parallelism Failures

**Error:**
```
org.postgresql.util.PSQLException: FATAL: too many connections
```

**Cause:** Parallel tests each create connections, exhausting pool.

**Solution:**
```properties
# gradle.properties - limit parallel test forks
maxParallelForks=4
```

Or use Testcontainers with shared container:
```kotlin
@Testcontainers
class IntegrationTest {
    companion object {
        @Container
        @JvmStatic
        val postgres = PostgreSQLContainer<Nothing>("postgres:14")
    }
}
```

See the **postgresql** skill for Testcontainers patterns.
```