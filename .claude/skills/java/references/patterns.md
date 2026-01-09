```markdown
# Java 21 Patterns

JVM tuning, concurrency, and runtime patterns for the casino platform.

## Thread Pool Sizing Strategy

This platform is optimized for AMD Ryzen 9 9950X (16 physical / 32 logical cores).

### Decision Tree: Choosing Pool Size

```
Is the task CPU-bound or I/O-bound?
├── CPU-bound → core = logical cores (32)
│   └── Example: wallet balance calculations
└── I/O-bound → core = physical cores (16)
    └── Example: database queries, HTTP calls
```

### WARNING: Under-Sized Thread Pools

**The Problem:**

```kotlin
// BAD - Too few threads for high-concurrency system
val executor = ThreadPoolTaskExecutor()
executor.corePoolSize = 4
executor.maxPoolSize = 8
executor.queueCapacity = 100
```

**Why This Breaks:**
1. Queue fills instantly during burst traffic (1000+ concurrent bets)
2. CallerRunsPolicy blocks HTTP threads, causing cascading timeouts
3. WebSocket notifications pile up, causing stale balance displays

**The Fix:**

```kotlin
// GOOD - Sized for production load
val executor = ThreadPoolTaskExecutor()
executor.corePoolSize = 32        // Match logical cores
executor.maxPoolSize = 128        // 4x for burst handling
executor.queueCapacity = 2000     // Buffer for 2000 pending ops
executor.setRejectedExecutionHandler(CallerRunsPolicy())
```

**When You Might Be Tempted:**
Local development works fine with small pools. Only production load reveals the problem.

## Rejection Policies by Use Case

| Policy | Use Case | Example |
|--------|----------|---------|
| `CallerRunsPolicy` | Critical ops (never lose) | Wallet transactions |
| `DiscardOldestPolicy` | Real-time (stale = useless) | WebSocket notifications |
| `AbortPolicy` | Fail-fast requirements | Payment callbacks |

```kotlin
// WebSocket: drop stale notifications, never block HTTP threads
executor.setRejectedExecutionHandler(DiscardOldestPolicy())

// Wallet: slow down but never lose a transaction
executor.setRejectedExecutionHandler(CallerRunsPolicy())
```

## Graceful Shutdown Configuration

**The Problem:**

```kotlin
// BAD - No shutdown handling
executor.initialize()
// Application kills in-flight tasks on shutdown
```

**The Fix:**

```kotlin
// GOOD - Wait for in-flight tasks
executor.setWaitForTasksToCompleteOnShutdown(true)
executor.setAwaitTerminationSeconds(60)  // Standard ops
// OR
executor.setAwaitTerminationSeconds(300) // Long-running syncs
```

## JVM Memory Configuration

### Gradle Build Settings

```properties
# gradle.properties
org.gradle.jvmargs=-Xmx4096m -XX:MaxMetaspaceSize=1024m -XX:+HeapDumpOnOutOfMemoryError -XX:+UseParallelGC
```

| Setting | Purpose |
|---------|---------|
| `-Xmx4096m` | Max heap for builds |
| `-XX:MaxMetaspaceSize=1024m` | Class metadata space |
| `-XX:+HeapDumpOnOutOfMemoryError` | Debug OOM crashes |
| `-XX:+UseParallelGC` | Throughput-optimized GC |

### WARNING: Missing Heap Dump Configuration

**The Problem:**

```properties
# BAD - No diagnostic info on OOM
org.gradle.jvmargs=-Xmx2g
```

**Why This Breaks:**
1. OOM crashes leave no trace
2. Can't diagnose memory leaks post-mortem
3. Production issues become impossible to debug

**The Fix:**

```properties
# GOOD - Always enable heap dumps
org.gradle.jvmargs=-Xmx4g -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/casino/
```

## Module System Reflection Access

Java 21 enforces strong encapsulation. Testing frameworks need explicit module opens.

```kotlin
// build.gradle.kts
tasks.withType<Test> {
    jvmArgs(
        "--add-opens", "java.base/java.math=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
        "--add-opens", "java.base/java.util=ALL-UNNAMED",
        "--add-opens", "java.base/java.time=ALL-UNNAMED",
        "--add-opens", "java.base/java.text=ALL-UNNAMED"
    )
}
```

**Required for:** MockK, Kotest, and other frameworks that use reflection on JDK classes.

## Parallel Test Execution

```properties
# gradle.properties
maxParallelForks=4
```

**Rule of thumb:** `maxParallelForks = physicalCores / 4` for memory-intensive tests.

## Missing Java 21 Features (Opportunities)

This project doesn't yet use these Java 21 features:

| Feature | Benefit | Status |
|---------|---------|--------|
| Virtual Threads | 1M+ concurrent WebSocket connections | Not used |
| Sealed Classes | Better domain modeling | Use Kotlin sealed instead |
| Pattern Matching | Cleaner switch expressions | Use Kotlin when |
| Records | Immutable DTOs | Use Kotlin data class |

See the **kotlin** skill for idiomatic alternatives.
```