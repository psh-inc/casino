```markdown
# Java Modules & Dependencies

Module configuration, dependency management, and build setup for Java 21.

## Build Configuration

### Gradle Plugins

```kotlin
// build.gradle.kts
plugins {
    id("org.springframework.boot") version "3.2.5"
    id("io.spring.dependency-management") version "1.1.3"
    id("java")
    jacoco
    kotlin("jvm") version "2.3.0"
    kotlin("plugin.spring") version "2.3.0"
    kotlin("plugin.jpa") version "2.3.0"
    kotlin("plugin.noarg") version "2.3.0"
    kotlin("kapt") version "2.3.0"
}
```

| Plugin | Purpose |
|--------|---------|
| `spring-boot` | Spring Boot packaging & run |
| `dependency-management` | BOM version alignment |
| `kotlin-jpa` | JPA entity no-arg constructors |
| `kotlin-spring` | Open classes for Spring proxies |
| `kapt` | Kotlin annotation processing |

### Java Toolchain

```kotlin
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}
```

Enables automatic JDK 21 download via Gradle.

## Kotlin Annotation Processing (kapt)

```kotlin
dependencies {
    // JPA metamodel generation for type-safe queries
    kapt("org.hibernate.orm:hibernate-jpamodelgen")
}
```

Generates `Player_` metamodel classes for Criteria API.

## NoArg Plugin Configuration

```kotlin
noArg {
    annotation("jakarta.persistence.Entity")
    annotation("jakarta.persistence.Embeddable")
    annotation("jakarta.persistence.MappedSuperclass")
    annotation("com.fasterxml.jackson.annotation.JsonIgnoreProperties")
    annotation("com.casino.core.annotation.NoArg")
    invokeInitializers = true
}
```

**Purpose:** JPA and Jackson require no-arg constructors. This plugin generates them for annotated classes without polluting Kotlin data classes.

## WARNING: Missing Module Opens for Testing

**The Problem:**

```
java.lang.reflect.InaccessibleObjectException:
Unable to make field private final java.math.BigInteger java.math.BigDecimal.intVal accessible
```

**Why This Breaks:**
1. MockK uses reflection to mock JDK classes
2. Java 21's module system blocks reflective access by default
3. Tests fail with cryptic `InaccessibleObjectException`

**The Fix:**

```kotlin
// build.gradle.kts
tasks.withType<Test> {
    useJUnitPlatform()
    jvmArgs(
        "--add-opens", "java.base/java.math=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED"
    )
}
```

## Dependency Exclusions

```kotlin
configurations.all {
    exclude(group = "commons-logging", module = "commons-logging")
}
```

Spring uses SLF4J; exclude commons-logging to avoid duplicate logging implementations.

## Key Dependencies

### Core Framework

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-cache")
}
```

### Kotlin Support

```kotlin
dependencies {
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
}
```

### Caching Stack

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-data-redis")
    implementation("com.github.ben-manes.caffeine:caffeine:3.1.8")
    implementation("javax.cache:cache-api")
}
```

See the **redis** skill for caching patterns.

### Testing Stack

```kotlin
dependencies {
    testImplementation("io.mockk:mockk:1.13.5")
    testImplementation("io.kotest:kotest-assertions-core:5.8.0")
    testImplementation("org.testcontainers:postgresql:1.19.3")
    testImplementation("org.testcontainers:kafka:1.19.3")
}
```

**Note:** MockK (not Mockito) for Kotlin-friendly mocking.

## Gradle Performance Settings

```properties
# gradle.properties
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.configureondemand=true
org.gradle.daemon=true
kotlin.incremental=true
kotlin.caching.enabled=true
buildCache.local.enabled=true
```

These settings significantly reduce incremental build times.

## Custom Tasks

```kotlin
// Generate BetBy ECDSA keys
tasks.register<JavaExec>("generateBetByKeys") {
    group = "application"
    description = "Generate ECDSA keys for BetBy integration"
    mainClass.set("com.casino.core.sports.util.BetByKeyGenerator")
    classpath = sourceSets["main"].runtimeClasspath
}
```

Run with: `./gradlew generateBetByKeys`
```