```markdown
---
name: java
description: |
  Java 21 runtime, JVM patterns, and Spring Boot configuration for the casino platform.
  Use when: Configuring JVM settings, thread pools, memory tuning, toolchains, or debugging JVM-specific issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Java 21 Skill

This casino platform runs on **Java 21** with **Kotlin 2.3.0** targeting the JVM. While business logic is written in Kotlin, understanding Java 21 features, JVM tuning, and runtime configuration is essential for performance optimization and debugging.

## Quick Start

### Java Toolchain Configuration

```kotlin
// build.gradle.kts
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

tasks.withType<KotlinCompile>().configureEach {
    compilerOptions {
        freeCompilerArgs.add("-Xjsr305=strict")
        jvmTarget.set(JvmTarget.JVM_21)
    }
}
```

### JVM Arguments for Tests

```kotlin
// build.gradle.kts - required for MockK reflective access
tasks.withType<Test> {
    useJUnitPlatform()
    jvmArgs(
        "--add-opens", "java.base/java.math=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
        "--add-opens", "java.base/java.util=ALL-UNNAMED",
        "--add-opens", "java.base/java.time=ALL-UNNAMED"
    )
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Toolchain | Auto-download JDK 21 | `languageVersion.of(21)` |
| Target | Bytecode version | `jvmTarget.set(JVM_21)` |
| Module opens | Reflection access | `--add-opens java.base/...` |
| GC selection | Throughput vs latency | `-XX:+UseG1GC` |
| Heap sizing | Memory allocation | `-Xmx4096m` |

## Common Patterns

### Thread Pool Configuration

**When:** High-concurrency operations (wallet, WebSocket, batch jobs)

```kotlin
@Bean("walletAsyncExecutor")
fun walletAsyncExecutor(): Executor {
    val executor = ThreadPoolTaskExecutor()
    executor.corePoolSize = 32        // Match logical cores
    executor.maxPoolSize = 128        // 4x core for bursts
    executor.queueCapacity = 2000
    executor.setThreadNamePrefix("wallet-async-")
    executor.setRejectedExecutionHandler(CallerRunsPolicy())
    executor.setWaitForTasksToCompleteOnShutdown(true)
    executor.initialize()
    return executor
}
```

### Caffeine Cache with Metrics

**When:** Sub-millisecond local caching

```kotlin
@Bean
fun walletBalanceCache(): Cache<Long, WalletBalance> {
    val cache = Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(Duration.ofSeconds(5))
        .recordStats()
        .build<Long, WalletBalance>()

    CaffeineCacheMetrics.monitor(meterRegistry, cache, "wallet.balance")
    return cache
}
```

## See Also

- [patterns](references/patterns.md) - JVM tuning and concurrency patterns
- [types](references/types.md) - Type mappings between Java and Kotlin
- [modules](references/modules.md) - Module system and dependency management
- [errors](references/errors.md) - Common JVM errors and solutions

## Related Skills

- See the **kotlin** skill for Kotlin language patterns on the JVM
- See the **spring-boot** skill for Spring Boot configuration
- See the **jpa** skill for Hibernate/JPA entity patterns
- See the **redis** skill for distributed caching with Redis

## Build Commands

```bash
# Build with tests
./gradlew clean build

# Run application
./gradlew bootRun

# Run specific test class
./gradlew test --tests "*ServiceTest"

# Generate coverage report
./gradlew jacocoTestReport
```

## JVM Version Check

```bash
# Verify Java version
java -version
# Expected: openjdk version "21.x.x"

# Check Gradle's JVM
./gradlew -version
```
```