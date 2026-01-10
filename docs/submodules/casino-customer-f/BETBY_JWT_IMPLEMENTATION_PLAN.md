# BetBy JWT Token Implementation Plan

## Overview
BetBy requires a custom JWT token with ES256 algorithm (ECDSA with P-256 curve and SHA-256) for user authorization. This is different from the standard JWT tokens used for general authentication in the casino platform.

## Requirements Analysis

### Token Structure
1. **Algorithm**: ES256 (ECDSA using P-256 curve and SHA-256)
2. **Header**:
   - `alg`: "ES256"
   - `typ`: "JWT"

3. **Payload**:
   - `iss`: Brand ID (e.g., "2566675164829982720")
   - `sub`: Player's unique ID from our system
   - `name`: Player's username
   - `iat`: Token creation timestamp
   - `exp`: Token expiration timestamp
   - `jti`: Unique token ID for session tracking
   - `lang`: User's language preference
   - `currency`: User's currency (e.g., "USD")
   - `odds_format`: Optional, defaults to "decimal"
   - `ff`: Feature flags object
     - `is_cashout_available`: Boolean
     - `is_match_tracker_available`: Boolean

## Implementation Plan for casino-b Backend

### 1. Key Management Setup

#### Files to Create:
```
casino-b/
  src/main/kotlin/com/casino/
    sports/
      config/
        BetByKeyConfig.kt         # Key configuration
      service/
        BetByJwtService.kt        # JWT generation service
      controller/
        SportsAuthController.kt   # API endpoint
      dto/
        BetByTokenRequest.kt      # Request DTO
        BetByTokenResponse.kt     # Response DTO
  src/main/resources/
    keys/
      betby-private.pem          # Private key (gitignored)
      betby-public.pem           # Public key (to share with BetBy)
```

### 2. Dependencies to Add

```kotlin
// build.gradle.kts
dependencies {
    // For ES256 JWT support
    implementation("io.jsonwebtoken:jjwt-api:0.11.5")
    implementation("io.jsonwebtoken:jjwt-impl:0.11.5")
    implementation("io.jsonwebtoken:jjwt-jackson:0.11.5")
    
    // For ECDSA key handling
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")
    implementation("org.bouncycastle:bcpkix-jdk15on:1.70")
}
```

### 3. Key Generation Script

```kotlin
// BetByKeyGenerator.kt - Utility to generate keys (run once)
package com.casino.sports.util

import org.bouncycastle.jce.ECNamedCurveTable
import org.bouncycastle.jce.provider.BouncyCastleProvider
import org.bouncycastle.openssl.jcajce.JcaPEMWriter
import org.bouncycastle.util.io.pem.PemObject
import java.io.File
import java.io.FileWriter
import java.security.KeyPairGenerator
import java.security.Security

object BetByKeyGenerator {
    @JvmStatic
    fun main(args: Array<String>) {
        Security.addProvider(BouncyCastleProvider())
        
        val keyPairGenerator = KeyPairGenerator.getInstance("EC", "BC")
        val parameterSpec = ECNamedCurveTable.getParameterSpec("secp256r1")
        keyPairGenerator.initialize(parameterSpec)
        val keyPair = keyPairGenerator.generateKeyPair()
        
        // Save private key
        File("src/main/resources/keys/betby-private.pem").apply {
            parentFile.mkdirs()
            FileWriter(this).use { writer ->
                JcaPEMWriter(writer).use { pemWriter ->
                    pemWriter.writeObject(PemObject("EC PRIVATE KEY", keyPair.private.encoded))
                }
            }
        }
        
        // Save public key
        File("src/main/resources/keys/betby-public.pem").apply {
            FileWriter(this).use { writer ->
                JcaPEMWriter(writer).use { pemWriter ->
                    pemWriter.writeObject(keyPair.public)
                }
            }
        }
        
        println("Keys generated successfully!")
        println("Share betby-public.pem with BetBy Integration Manager")
    }
}
```

### 4. Service Implementation

```kotlin
// BetByJwtService.kt
package com.casino.sports.service

import io.jsonwebtoken.Jwts
import io.jsonwebtoken.SignatureAlgorithm
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import java.security.KeyFactory
import java.security.PrivateKey
import java.security.spec.PKCS8EncodedKeySpec
import java.time.Instant
import java.util.*
import javax.annotation.PostConstruct

@Service
class BetByJwtService(
    private val userService: UserService,
    private val profileService: ProfileService
) {
    @Value("\${betby.brand-id}")
    private lateinit var brandId: String
    
    @Value("\${betby.private-key-path}")
    private lateinit var privateKeyPath: String
    
    @Value("\${betby.token-expiry-seconds:3600}")
    private var tokenExpirySeconds: Long = 3600
    
    private lateinit var privateKey: PrivateKey
    
    @PostConstruct
    fun init() {
        // Load private key
        val keyBytes = this::class.java.getResourceAsStream(privateKeyPath)
            ?.readBytes() ?: throw IllegalStateException("Private key not found")
        
        // Parse PEM and extract key
        val keyString = String(keyBytes)
            .replace("-----BEGIN EC PRIVATE KEY-----", "")
            .replace("-----END EC PRIVATE KEY-----", "")
            .replace("\\s".toRegex(), "")
        
        val decoded = Base64.getDecoder().decode(keyString)
        val keySpec = PKCS8EncodedKeySpec(decoded)
        val keyFactory = KeyFactory.getInstance("EC")
        privateKey = keyFactory.generatePrivate(keySpec)
    }
    
    fun generateBetByToken(userId: Long): String {
        val user = userService.findById(userId) 
            ?: throw IllegalArgumentException("User not found")
        
        val profile = profileService.getProfile(userId)
        
        val now = Instant.now()
        val expiry = now.plusSeconds(tokenExpirySeconds)
        
        // Build feature flags
        val featureFlags = mapOf(
            "is_cashout_available" to true,
            "is_match_tracker_available" to true
        )
        
        return Jwts.builder()
            .setHeaderParam("typ", "JWT")
            .setIssuer(brandId)
            .setSubject(userId.toString())
            .claim("name", user.username)
            .setIssuedAt(Date.from(now))
            .setExpiration(Date.from(expiry))
            .setId(UUID.randomUUID().toString()) // jti
            .claim("lang", profile.language ?: "en")
            .claim("currency", profile.currency ?: "USD")
            .claim("odds_format", "decimal")
            .claim("ff", featureFlags)
            .signWith(privateKey, SignatureAlgorithm.ES256)
            .compact()
    }
}
```

### 5. Controller Implementation

```kotlin
// SportsAuthController.kt
package com.casino.sports.controller

import com.casino.sports.dto.BetByTokenResponse
import com.casino.sports.service.BetByJwtService
import org.springframework.http.ResponseEntity
import org.springframework.security.access.prepost.PreAuthorize
import org.springframework.security.core.annotation.AuthenticationPrincipal
import org.springframework.security.core.userdetails.UserDetails
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/v1/sports")
class SportsAuthController(
    private val betByJwtService: BetByJwtService,
    private val userService: UserService
) {
    
    @GetMapping("/token")
    @PreAuthorize("isAuthenticated()")
    fun getBetByToken(
        @AuthenticationPrincipal userDetails: UserDetails
    ): ResponseEntity<BetByTokenResponse> {
        val user = userService.findByUsername(userDetails.username)
            ?: return ResponseEntity.notFound().build()
        
        val token = betByJwtService.generateBetByToken(user.id!!)
        
        return ResponseEntity.ok(
            BetByTokenResponse(
                token = token,
                expiresIn = 3600,
                brandId = brandId
            )
        )
    }
    
    @PostMapping("/refresh-token")
    @PreAuthorize("isAuthenticated()")
    fun refreshBetByToken(
        @AuthenticationPrincipal userDetails: UserDetails
    ): ResponseEntity<BetByTokenResponse> {
        // Same as getBetByToken but could have different logic if needed
        return getBetByToken(userDetails)
    }
}
```

### 6. DTOs

```kotlin
// BetByTokenResponse.kt
package com.casino.sports.dto

data class BetByTokenResponse(
    val token: String,
    val expiresIn: Long,
    val brandId: String
)
```

### 7. Configuration Properties

```yaml
# application.yml
betby:
  brand-id: "2566675164829982720"
  private-key-path: "/keys/betby-private.pem"
  token-expiry-seconds: 3600
```

### 8. Frontend Integration Update

Update the sports component to fetch BetBy token:

```typescript
// sports.component.ts - Update the initializeBetBy method
private async initializeBetBy(): Promise<void> {
  try {
    // First, get BetBy-specific token if user is authenticated
    let betByToken = '';
    
    if (this.authService.getAccessToken()) {
      try {
        const response = await this.http.get<{ token: string }>(
          `${environment.apiUrl}/api/v1/sports/token`
        ).toPromise();
        
        betByToken = response?.token || '';
      } catch (error) {
        console.warn('Failed to get BetBy token, continuing as guest', error);
      }
    }
    
    // Initialize with BetBy token
    const config: BTRendererConfig = {
      brand_id: this.BRAND_ID,
      token: betByToken, // Use BetBy-specific token
      // ... rest of config
    };
    
    this.btRenderer = new window.BTRenderer();
    this.btRenderer.initialize(config);
    
  } catch (error) {
    console.error('Error initializing BetBy:', error);
  }
}

// Update token refresh handler
private async handleTokenExpired(): Promise<void> {
  try {
    const response = await this.http.post<{ token: string }>(
      `${environment.apiUrl}/api/v1/sports/refresh-token`,
      {}
    ).toPromise();
    
    if (response?.token && this.btRenderer) {
      this.btRenderer.updateToken(response.token);
    }
  } catch (error) {
    console.error('Failed to refresh BetBy token:', error);
  }
}
```

## Implementation Steps

1. **Generate Keys** (One-time setup)
   - Run the BetByKeyGenerator utility
   - Store private key securely
   - Share public key with BetBy Integration Manager

2. **Backend Implementation**
   - Add dependencies to build.gradle.kts
   - Create BetByJwtService
   - Create SportsAuthController
   - Add configuration properties
   - Test token generation

3. **Frontend Updates**
   - Update sports component to fetch BetBy token
   - Implement token refresh logic
   - Handle authentication state changes

4. **Security Considerations**
   - Never expose private key in version control
   - Use environment variables for production
   - Implement rate limiting on token endpoint
   - Log token generation for audit purposes

5. **Testing**
   - Unit tests for JWT service
   - Integration tests for controller
   - End-to-end test with BetBy widget

## Environment Variables for Production

```bash
# Production environment variables
BETBY_BRAND_ID=2566675164829982720
BETBY_PRIVATE_KEY_PATH=/secure/keys/betby-private.pem
BETBY_TOKEN_EXPIRY_SECONDS=3600
```

## API Documentation

### Endpoint: GET /api/v1/sports/token

**Description**: Generate BetBy-specific JWT token for authenticated user

**Authentication**: Required (Bearer token)

**Response**:
```json
{
  "token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 3600,
  "brandId": "2566675164829982720"
}
```

**Error Responses**:
- 401: Unauthorized (not authenticated)
- 404: User not found
- 500: Internal server error

### Endpoint: POST /api/v1/sports/refresh-token

**Description**: Refresh BetBy JWT token for authenticated user

**Authentication**: Required (Bearer token)

**Response**: Same as GET /api/v1/sports/token

## Migration Script (Flyway)

```sql
-- V{timestamp}__add_sports_betting_preferences.sql
ALTER TABLE user_profiles
ADD COLUMN IF NOT EXISTS cashout_enabled BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS match_tracker_enabled BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS odds_format VARCHAR(20) DEFAULT 'decimal';
```

## Monitoring & Logging

- Log all token generation requests
- Monitor token expiration patterns
- Track feature flag usage
- Alert on key rotation requirements

## Notes

1. The ES256 algorithm requires ECDSA keys with P-256 curve
2. BetBy token is separate from main platform JWT
3. Token should be refreshed before expiration
4. Feature flags can be configured per user basis
5. Currency and language should match user profile settings