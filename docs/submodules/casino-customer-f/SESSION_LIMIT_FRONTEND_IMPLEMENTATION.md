# Session Time Limit - Frontend Implementation Plan

**Document Version**: 1.0
**Created**: 2025-10-16
**Backend Implementation**: ✅ COMPLETE
**Frontend Implementation**: ❌ PENDING

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Backend Analysis](#backend-analysis)
3. [Frontend Current State](#frontend-current-state)
4. [Technical Requirements](#technical-requirements)
5. [Step-by-Step Implementation Plan](#step-by-step-implementation-plan)
6. [Testing Strategy](#testing-strategy)
7. [Edge Cases & Error Handling](#edge-cases--error-handling)
8. [Appendix: Code References](#appendix-code-references)

---

## Executive Summary

### What We're Building
A comprehensive frontend system to handle session time limits for responsible gambling compliance. When a player sets a session time limit (e.g., 2 hours), the system will:

1. **Warn progressively** as time runs out (80%, 90%, 95%)
2. **Handle active bets gracefully** with 5-minute grace period
3. **Enforce mandatory breaks** (15 minutes) after limit reached
4. **Block game launches** during break periods

### Backend Status: ✅ COMPLETE
- Scheduled monitoring service (runs every 60 seconds)
- WebSocket notifications to `/user/{playerId}/queue/session-limits`
- Grace period mechanism for pending bets (5 minutes)
- Break period enforcement (15 minutes)
- REST endpoint for current session status

### Frontend Status: ❌ NOT STARTED
- WebSocket infrastructure exists but not connected
- No UI components for warnings/notifications
- No session limit models/interfaces
- No integration with game launcher

### Estimated Implementation Time
**Total: 3-4 hours** (for experienced Angular developer)
- Models & Services: 45 minutes
- UI Components: 2 hours
- Integration & Testing: 1-1.5 hours

---

## Backend Analysis

### 1. WebSocket Architecture

**Endpoint**: `ws://localhost:8080/ws`
**Protocol**: STOMP over SockJS
**Destination**: `/user/{playerId}/queue/session-limits`

```kotlin
// WebSocketConfig.kt - Lines 19-29
config.enableSimpleBroker("/topic", "/queue")
config.setApplicationDestinationPrefixes("/app")
config.setUserDestinationPrefix("/user")
```

**Key Points**:
- User-specific queues: Each player gets their own queue
- Simple in-memory broker (no external message queue needed)
- SockJS fallback for browsers without WebSocket support
- Supports token-based authentication via query parameter

---

### 2. Scheduled Monitoring Service

**Service**: `SessionTimeLimitMonitorService`
**Location**: `casino-b/src/main/kotlin/com/casino/core/service/responsible/SessionTimeLimitMonitorService.kt`

**How It Works**:
```kotlin
@Scheduled(fixedDelay = 60000)  // Runs every 60 seconds
@Transactional
fun monitorActiveSessions() {
    val activeSessions = gameSessionRepository.findByStatus(GameSessionStatus.ACTIVE)

    activeSessions.forEach { session ->
        val sessionTimeLimit = playerLimitRepository
            .findAllActiveByPlayerIdAndType(session.player.id!!, LimitType.SESSION_TIME_LIMIT)
            .firstOrNull()

        if (sessionTimeLimit != null) {
            checkSessionTimeLimit(session.id!!, session.player.id!!, limitValue)
        }
    }
}
```

**Key Thresholds**:
- **80% used** (APPROACHING): First warning - orange banner
- **90% used** (NEAR): Second warning - yellow banner
- **95% used** (CRITICAL): Final warning - red banner
- **100% used**: Session termination (with grace period if bet active)

**Warning Deduplication**:
```kotlin
private val warningsSent = ConcurrentHashMap<Long, MutableSet<WarningLevel>>()
```
- Tracks which warnings have been sent per session
- Prevents duplicate warnings
- Cleared when session ends

---

### 3. Grace Period Mechanism

**Purpose**: Prevent unfair mid-bet termination

**How It Works** (Lines 194-258):
```kotlin
// Check for pending rounds
val pendingRounds = gameRoundRepository.findByPlayerIdAndStatus(playerId, GameRoundStatus.PENDING)
val hasPendingRound = pendingRounds.isNotEmpty()

if (hasPendingRound) {
    val gracePeriodStart = sessionsInGracePeriod.getOrPut(sessionId) { LocalDateTime.now() }
    val gracePeriodElapsed = Duration.between(gracePeriodStart, LocalDateTime.now()).toMinutes()

    if (gracePeriodElapsed < GRACE_PERIOD_MINUTES) {
        // Send grace period notification, DO NOT end session
        return
    }
}

// Safe to end session (no pending rounds OR grace period expired)
```

**Grace Period**: 5 minutes
**Tracking**: `ConcurrentHashMap<Long, LocalDateTime>` (sessionId → startTime)

**States**:
1. **No Pending Rounds**: Instant session termination
2. **Has Pending Rounds**: Enter grace period
3. **Grace Period Active**: Send notifications, allow bet completion
4. **Grace Period Expired**: Force-end session even if rounds still pending

---

### 4. Break Period Enforcement

**Location**: `GameLaunchService.kt` - Lines 686-745

**Duration**: 15 minutes mandatory break

**How It Works**:
```kotlin
private fun checkSessionTimeLimit(playerId: Long) {
    val recentSessions = gameSessionRepository
        .findByPlayerIdAndStatus(playerId, GameSessionStatus.COMPLETED)
        .sortedByDescending { it.endedAt }
        .take(1)

    if (recentSessions.isNotEmpty()) {
        val lastSession = recentSessions.first()
        val sessionDuration = Duration.between(lastSession.startedAt, lastSession.endedAt).toMinutes()
        val limitMinutes = sessionTimeLimit.limitValue.toInt() * 60

        // If session was close to or exceeded limit
        if (sessionDuration >= limitMinutes - 5) {
            val minutesSinceEnd = Duration.between(lastSession.endedAt, LocalDateTime.now()).toMinutes()

            if (minutesSinceEnd < 15) {
                throw BusinessRuleViolationException(
                    "You need to take a break. You can play again in ${15 - minutesSinceEnd.toInt()} minutes..."
                )
            }
        }
    }
}
```

**Trigger**: Called in `launchGame()` before creating GameSession (Line 106)

**Error Handling**: Throws `BusinessRuleViolationException` → Frontend must catch and display

---

### 5. WebSocket Message Formats

**File**: `SessionLimitWebSocketDto.kt` (121 lines)

#### A. Session Limit Warning

```kotlin
data class SessionLimitWarning(
    val type: String = "SESSION_WARNING",
    val sessionId: String,              // UUID format
    val gameId: String,                 // Game identifier
    val gameName: String,               // Display name
    val limitMinutes: Int,              // Total limit (e.g., 120)
    val elapsedMinutes: Int,            // Time used (e.g., 96)
    val remainingMinutes: Int,          // Time left (e.g., 24)
    val percentageUsed: Int,            // 0-100 (e.g., 80)
    val warningLevel: WarningLevel,     // APPROACHING | NEAR | CRITICAL
    val message: String,                // Human-readable message
    val timestamp: LocalDateTime
)

enum class WarningLevel {
    APPROACHING,  // 80% - Orange banner
    NEAR,         // 90% - Yellow banner
    CRITICAL      // 95% - Red banner
}
```

**Example Payload** (80% threshold):
```json
{
  "type": "SESSION_WARNING",
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "gameId": "book-of-ra",
  "gameName": "Book of Ra Deluxe",
  "limitMinutes": 120,
  "elapsedMinutes": 96,
  "remainingMinutes": 24,
  "percentageUsed": 80,
  "warningLevel": "APPROACHING",
  "message": "Your session time limit is approaching. 24 minutes remaining.",
  "timestamp": "2024-10-16T14:36:00"
}
```

#### B. Session Expired Notification

```kotlin
data class SessionExpiredNotification(
    val type: String = "SESSION_EXPIRED",
    val sessionId: String,
    val gameId: String,
    val gameName: String,
    val reason: String,                 // Why session ended
    val totalDurationMinutes: Int,      // How long played
    val limitExceeded: Boolean,         // Always true
    val breakRequiredMinutes: Int?,     // 15 or null
    val canPlayAgainAt: LocalDateTime?, // When break ends
    val hasPendingRound: Boolean,       // Grace period active?
    val gracePeriodMinutes: Int?,       // Remaining grace time
    val message: String,
    val timestamp: LocalDateTime
)
```

**Example Payload** (No pending bet):
```json
{
  "type": "SESSION_EXPIRED",
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "gameId": "book-of-ra",
  "gameName": "Book of Ra Deluxe",
  "reason": "Session time limit exceeded",
  "totalDurationMinutes": 120,
  "limitExceeded": true,
  "breakRequiredMinutes": 15,
  "canPlayAgainAt": "2024-10-16T15:15:00",
  "hasPendingRound": false,
  "gracePeriodMinutes": null,
  "message": "Your session has been ended as you have reached your 120-minute session time limit. Please take a 15-minute break before starting a new session.",
  "timestamp": "2024-10-16T15:00:00"
}
```

**Example Payload** (With pending bet - grace period):
```json
{
  "type": "SESSION_EXPIRED",
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "gameId": "book-of-ra",
  "gameName": "Book of Ra Deluxe",
  "reason": "Session time limit exceeded - finish current round",
  "totalDurationMinutes": 120,
  "limitExceeded": true,
  "breakRequiredMinutes": 15,
  "canPlayAgainAt": "2024-10-16T15:15:00",
  "hasPendingRound": true,
  "gracePeriodMinutes": 5,
  "message": "Your session time limit has been reached. Please finish your current round. You have 5 minutes to complete pending bets.",
  "timestamp": "2024-10-16T15:00:00"
}
```

#### C. Current Session Status Response

**REST Endpoint**: `GET /api/customer/responsible-gambling/session/current`

```kotlin
data class CurrentSessionStatusResponse(
    val hasActiveSession: Boolean,
    val sessionId: String?,
    val gameId: String?,
    val gameName: String?,
    val startedAt: LocalDateTime?,
    val elapsedMinutes: Int?,
    val limitMinutes: Int?,
    val remainingMinutes: Int?,
    val percentageUsed: Int?,
    val willExpireSoon: Boolean,        // true if >= 80%
    val warningsSent: Int               // 0-3
)
```

**Example Response**:
```json
{
  "hasActiveSession": true,
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "gameId": "book-of-ra",
  "gameName": "Book of Ra Deluxe",
  "startedAt": "2024-10-16T13:00:00",
  "elapsedMinutes": 96,
  "limitMinutes": 120,
  "remainingMinutes": 24,
  "percentageUsed": 80,
  "willExpireSoon": true,
  "warningsSent": 1
}
```

---

### 6. Database Schema

**Relevant Tables**:

#### game_sessions
```sql
CREATE TABLE game_sessions (
    id BIGSERIAL PRIMARY KEY,
    session_uuid UUID NOT NULL UNIQUE,
    player_id BIGINT NOT NULL,
    game_id VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL,          -- ACTIVE, COMPLETED, etc.
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    -- ... other fields
);
```

**Key Fields**:
- `started_at`: Used to calculate elapsed time
- `ended_at`: Used to calculate break period
- `status`: Must be ACTIVE for monitoring

#### game_rounds
```sql
CREATE TABLE game_rounds (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL,
    player_id BIGINT NOT NULL,
    round_status VARCHAR(20) NOT NULL,    -- PENDING, COMPLETED, etc.
    round_start_time TIMESTAMP NOT NULL,
    round_end_time TIMESTAMP,
    -- ... other fields
);
```

**Key Fields**:
- `round_status`: PENDING = bet active, must grant grace period

---

## Frontend Current State

### Existing Infrastructure

#### 1. WebSocket Service
**File**: `src/app/core/services/websocket.service.ts` (430 lines)

**Status**: ✅ Infrastructure exists, ❌ Session limits not integrated

**Current Capabilities**:
```typescript
export class WebsocketService {
  private client!: Client;
  private isConnected$ = new BehaviorSubject<boolean>(false);

  // Already subscribes to balance updates
  private subscribeToBalanceUpdates(playerId: number): void {
    const balanceDestination = `/user/${playerId}/queue/balance`;
    this.client.subscribe(balanceDestination, (message: IMessage) => {
      const balance = JSON.parse(message.body) as BalanceUpdateEvent;
      this.balanceUpdate$.next(balance);
    });
  }
}
```

**Connection Configuration**:
```typescript
const socketUrl = `${environment.apiUrl}/ws`;
this.client = new Client({
  brokerURL: socketUrl.replace(/^http/, 'ws'),
  reconnectDelay: 5000,
  heartbeatIncoming: 4000,
  heartbeatOutgoing: 4000
});
```

**What We Need to Add**:
- `subscribeToSessionLimits(playerId: number)` method
- `sessionWarning$` BehaviorSubject
- `sessionExpired$` BehaviorSubject

---

#### 2. Responsible Gambling Service
**File**: `src/app/core/services/responsible-gambling.service.ts` (163 lines)

**Status**: ⚠️ Exists but incomplete

**Current Capabilities**:
```typescript
@Injectable({ providedIn: 'root' })
export class ResponsibleGamblingService {
  private apiUrl = `${environment.apiUrl}/api/customer/responsible-gambling`;

  getPlayerLimits(): Observable<PlayerLimitListResponse> { }
  setLimit(request: SetPlayerLimitRequest): Observable<PlayerLimitResponse> { }
  updateLimit(limitId: number, request: UpdatePlayerLimitRequest): Observable<PlayerLimitResponse> { }
  removeLimit(limitId: number): Observable<MessageResponse> { }

  // Helper methods
  hasActiveLimit(limits: PlayerLimit[], type: LimitType): boolean { }
  getActiveLimit(limits: PlayerLimit[], type: LimitType): PlayerLimit | undefined { }
}
```

**What We Need to Add**:
- `getCurrentSessionStatus(): Observable<CurrentSessionStatusResponse>` method

---

#### 3. Responsible Gambling Models
**File**: `src/app/core/models/responsible-gambling.models.ts` (237 lines)

**Status**: ⚠️ Basic models exist, missing WebSocket event types

**Current Models**:
```typescript
export enum LimitType {
  DEPOSIT_LIMIT = 'DEPOSIT_LIMIT',
  WAGER_LIMIT = 'WAGER_LIMIT',
  LOSS_LIMIT = 'LOSS_LIMIT',
  SESSION_TIME_LIMIT = 'SESSION_TIME_LIMIT',  // ✅ Exists
  SESSION_COUNT_LIMIT = 'SESSION_COUNT_LIMIT'
}

export const SESSION_TIME_OPTIONS = [
  { value: 30, label: '30 minutes' },
  { value: 60, label: '1 hour' },
  { value: 120, label: '2 hours' },
  { value: 180, label: '3 hours' },
  { value: 240, label: '4 hours' }
];
```

**What We Need to Add**:
```typescript
// Missing interfaces
export interface SessionLimitWarning { }
export interface SessionExpiredNotification { }
export interface CurrentSessionStatusResponse { }
export enum WarningLevel { }
```

---

#### 4. Game Launcher Service
**File**: `src/app/core/services/game-launcher.service.ts`

**Status**: ⚠️ Exists but needs error handling enhancement

**Current Functionality**:
- Launches games (desktop/mobile)
- Handles authentication
- Opens game windows/iframes

**What We Need to Add**:
- Error interceptor for `BusinessRuleViolationException`
- Display user-friendly modal when break period active
- Show countdown timer for remaining break time

---

### Missing Components

❌ **SessionWarningBanner** - Progressive warning display
❌ **SessionExpiredModal** - Blocking modal for session end
❌ **GracePeriodBanner** - Special notification for pending bets

---

## Technical Requirements

### 1. Dependencies

**Already Installed** (no new dependencies needed):
- `@stomp/stompjs` ^7.2.0
- `sockjs-client` ^1.6.1
- `rxjs` ^7.8.0
- `@angular/core` ^17.3.0

---

### 2. Browser Compatibility

**WebSocket Support**:
- Chrome 16+
- Firefox 11+
- Safari 7+
- Edge (all versions)
- Mobile browsers (iOS Safari 7.1+, Android Chrome 4.4+)

**SockJS Fallback**: Automatic for older browsers

---

### 3. Performance Considerations

**Memory Usage**:
- RxJS subscriptions: ~2-5 KB per subscription
- Component state: ~1-2 KB per warning banner
- No significant performance impact

**Network Traffic**:
- Heartbeat: ~50 bytes every 4 seconds
- Session warning: ~500 bytes (3 times max per session)
- Session expired: ~600 bytes (1 time per session)
- Total per 2-hour session: ~30 KB (negligible)

---

## Step-by-Step Implementation Plan

### Phase 1: TypeScript Models & Interfaces (30 minutes)

#### Task 1.1: Add WebSocket Event Interfaces
**File**: `src/app/core/models/responsible-gambling.models.ts`

**What to Add**:
```typescript
// Add to existing file after line 237

/**
 * Warning level indicating proximity to session time limit
 */
export enum WarningLevel {
  APPROACHING = 'APPROACHING',  // 80% used
  NEAR = 'NEAR',                // 90% used
  CRITICAL = 'CRITICAL'         // 95% used
}

/**
 * WebSocket event: Session time limit warning
 * Sent at 80%, 90%, 95% thresholds
 */
export interface SessionLimitWarning {
  type: 'SESSION_WARNING';
  sessionId: string;
  gameId: string;
  gameName: string;
  limitMinutes: number;
  elapsedMinutes: number;
  remainingMinutes: number;
  percentageUsed: number;
  warningLevel: WarningLevel;
  message: string;
  timestamp: string;  // ISO-8601 format
}

/**
 * WebSocket event: Session expired notification
 * Sent when session time limit reached
 */
export interface SessionExpiredNotification {
  type: 'SESSION_EXPIRED';
  sessionId: string;
  gameId: string;
  gameName: string;
  reason: string;
  totalDurationMinutes: number;
  limitExceeded: boolean;
  breakRequiredMinutes: number | null;
  canPlayAgainAt: string | null;  // ISO-8601 format
  hasPendingRound: boolean;
  gracePeriodMinutes: number | null;
  message: string;
  timestamp: string;
}

/**
 * REST API response: Current session status
 */
export interface CurrentSessionStatusResponse {
  hasActiveSession: boolean;
  sessionId: string | null;
  gameId: string | null;
  gameName: string | null;
  startedAt: string | null;  // ISO-8601 format
  elapsedMinutes: number | null;
  limitMinutes: number | null;
  remainingMinutes: number | null;
  percentageUsed: number | null;
  willExpireSoon: boolean;
  warningsSent: number;
}
```

**Acceptance Criteria**:
- [ ] All interfaces match backend DTOs exactly
- [ ] TypeScript compiles without errors
- [ ] Enums use same values as backend

---

#### Task 1.2: Add Helper Functions
**File**: `src/app/core/models/responsible-gambling.models.ts`

**What to Add**:
```typescript
/**
 * Get color class for warning level
 */
export function getWarningLevelColor(level: WarningLevel): string {
  switch (level) {
    case WarningLevel.APPROACHING: return 'warning-orange';
    case WarningLevel.NEAR: return 'warning-yellow';
    case WarningLevel.CRITICAL: return 'warning-red';
  }
}

/**
 * Get icon for warning level
 */
export function getWarningLevelIcon(level: WarningLevel): string {
  switch (level) {
    case WarningLevel.APPROACHING: return '⚠️';
    case WarningLevel.NEAR: return '⏰';
    case WarningLevel.CRITICAL: return '🚨';
  }
}

/**
 * Format minutes to human-readable time
 * Examples: 5 → "5 minutes", 90 → "1 hour 30 minutes"
 */
export function formatMinutesToReadable(minutes: number): string {
  if (minutes < 1) return 'less than a minute';
  if (minutes === 1) return '1 minute';
  if (minutes < 60) return `${minutes} minutes`;

  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  if (remainingMinutes === 0) {
    return hours === 1 ? '1 hour' : `${hours} hours`;
  }

  return `${hours} hour${hours > 1 ? 's' : ''} ${remainingMinutes} minute${remainingMinutes > 1 ? 's' : ''}`;
}
```

**Acceptance Criteria**:
- [ ] Helper functions tested with various inputs
- [ ] Color classes match CSS design system
- [ ] Time formatting handles edge cases (0, 1, 60, etc.)

---

### Phase 2: Service Layer Enhancement (45 minutes)

#### Task 2.1: Extend WebSocket Service
**File**: `src/app/core/services/websocket.service.ts`

**What to Add**:

**Step 1**: Add new BehaviorSubjects (after line ~50)
```typescript
// Session limit observables
private sessionWarning$ = new BehaviorSubject<SessionLimitWarning | null>(null);
private sessionExpired$ = new BehaviorSubject<SessionExpiredNotification | null>(null);

// Public observables
public readonly sessionWarning = this.sessionWarning$.asObservable();
public readonly sessionExpired = this.sessionExpired$.asObservable();
```

**Step 2**: Add subscription method (after existing subscription methods)
```typescript
/**
 * Subscribe to session limit notifications for a player
 * Receives warnings at 80%, 90%, 95% and expiry notification
 */
private subscribeToSessionLimits(playerId: number): void {
  const destination = `/user/${playerId}/queue/session-limits`;

  this.client.subscribe(destination, (message: IMessage) => {
    try {
      const event = JSON.parse(message.body);

      // Determine event type and emit to appropriate subject
      if (event.type === 'SESSION_WARNING') {
        const warning = event as SessionLimitWarning;
        this.sessionWarning$.next(warning);
        console.log(`[WebSocket] Session warning received: ${warning.warningLevel}, ${warning.remainingMinutes} minutes left`);
      } else if (event.type === 'SESSION_EXPIRED') {
        const expiry = event as SessionExpiredNotification;
        this.sessionExpired$.next(expiry);
        console.log(`[WebSocket] Session expired: ${expiry.reason}`);
      }
    } catch (error) {
      console.error('[WebSocket] Error parsing session limit message:', error);
    }
  });

  console.log(`[WebSocket] Subscribed to session limits: ${destination}`);
}
```

**Step 3**: Call subscription in connect method (find existing subscriptions block)
```typescript
private setupSubscriptions(): void {
  const playerId = this.authService.getPlayerId();
  if (!playerId) return;

  // Existing subscriptions
  this.subscribeToBalanceUpdates(playerId);
  this.subscribeToWageringUpdates(playerId);

  // NEW: Add session limit subscription
  this.subscribeToSessionLimits(playerId);
}
```

**Step 4**: Clear subjects on disconnect
```typescript
public disconnect(): void {
  if (this.client && this.client.active) {
    this.client.deactivate();
  }
  this.isConnected$.next(false);

  // Clear session limit state
  this.sessionWarning$.next(null);
  this.sessionExpired$.next(null);
}
```

**Acceptance Criteria**:
- [ ] Subscription created when WebSocket connects
- [ ] Events parsed correctly and emitted to observables
- [ ] Errors logged but don't crash connection
- [ ] State cleared on disconnect
- [ ] Console logs confirm subscription success

---

#### Task 2.2: Extend Responsible Gambling Service
**File**: `src/app/core/services/responsible-gambling.service.ts`

**What to Add**:
```typescript
/**
 * Get current session status (REST API call)
 * Use this for initial state or when WebSocket not connected
 */
getCurrentSessionStatus(): Observable<CurrentSessionStatusResponse> {
  return this.http.get<CurrentSessionStatusResponse>(
    `${this.apiUrl}/session/current`
  );
}

/**
 * Check if player is currently in a break period
 * Helper method for UI state management
 */
isInBreakPeriod(status: CurrentSessionStatusResponse): boolean {
  return !status.hasActiveSession &&
         status.canPlayAgainAt != null &&
         new Date(status.canPlayAgainAt) > new Date();
}

/**
 * Calculate remaining break time in minutes
 */
getRemainingBreakMinutes(canPlayAgainAt: string | null): number {
  if (!canPlayAgainAt) return 0;

  const now = new Date().getTime();
  const canPlay = new Date(canPlayAgainAt).getTime();
  const diffMs = canPlay - now;

  return Math.max(0, Math.ceil(diffMs / 1000 / 60));
}
```

**Acceptance Criteria**:
- [ ] REST endpoint returns correct status
- [ ] Helper methods calculate values correctly
- [ ] Error handling for API failures
- [ ] Works when WebSocket disconnected

---

### Phase 3: UI Components (2 hours)

#### Task 3.1: Create Session Warning Banner Component

**Component**: `session-warning-banner`
**Location**: `src/app/core/components/session-warning-banner/`

**Generate Command**:
```bash
ng generate component core/components/session-warning-banner --skip-tests
```

**TypeScript** (`session-warning-banner.component.ts`):
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { WebsocketService } from '../../services/websocket.service';
import {
  SessionLimitWarning,
  WarningLevel,
  getWarningLevelColor,
  getWarningLevelIcon,
  formatMinutesToReadable
} from '../../models/responsible-gambling.models';

@Component({
  selector: 'app-session-warning-banner',
  templateUrl: './session-warning-banner.component.html',
  styleUrls: ['./session-warning-banner.component.scss']
})
export class SessionWarningBannerComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  warning: SessionLimitWarning | null = null;
  isVisible = false;
  isDismissed = false;

  // Expose enums to template
  WarningLevel = WarningLevel;

  constructor(private websocketService: WebsocketService) {}

  ngOnInit(): void {
    // Subscribe to session warnings from WebSocket
    this.websocketService.sessionWarning
      .pipe(takeUntil(this.destroy$))
      .subscribe(warning => {
        if (warning) {
          this.warning = warning;
          this.isVisible = true;
          this.isDismissed = false;

          // Auto-show critical warnings even if previously dismissed
          if (warning.warningLevel === WarningLevel.CRITICAL) {
            this.isDismissed = false;
          }
        } else {
          this.isVisible = false;
          this.warning = null;
        }
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Get CSS class for current warning level
   */
  getColorClass(): string {
    return this.warning ? getWarningLevelColor(this.warning.warningLevel) : '';
  }

  /**
   * Get icon for current warning level
   */
  getIcon(): string {
    return this.warning ? getWarningLevelIcon(this.warning.warningLevel) : '';
  }

  /**
   * Get formatted time remaining
   */
  getFormattedTime(): string {
    return this.warning ? formatMinutesToReadable(this.warning.remainingMinutes) : '';
  }

  /**
   * Dismiss banner (can be reshown for critical warnings)
   */
  dismiss(): void {
    this.isDismissed = true;
  }

  /**
   * Determine if banner should be shown
   */
  shouldShow(): boolean {
    return this.isVisible && !this.isDismissed && this.warning !== null;
  }
}
```

**HTML** (`session-warning-banner.component.html`):
```html
<div
  *ngIf="shouldShow()"
  class="session-warning-banner"
  [ngClass]="getColorClass()"
  role="alert"
  aria-live="polite">

  <div class="banner-content">
    <div class="banner-icon">
      {{ getIcon() }}
    </div>

    <div class="banner-text">
      <div class="banner-title">
        <ng-container [ngSwitch]="warning?.warningLevel">
          <span *ngSwitchCase="WarningLevel.APPROACHING">Session Time Alert</span>
          <span *ngSwitchCase="WarningLevel.NEAR">Warning: Session Ending Soon</span>
          <span *ngSwitchCase="WarningLevel.CRITICAL">CRITICAL: Session Expiring</span>
        </ng-container>
      </div>

      <div class="banner-message">
        {{ warning?.message }}
      </div>

      <div class="banner-details">
        <strong>{{ getFormattedTime() }}</strong> remaining
        ({{ warning?.percentageUsed }}% of {{ warning?.limitMinutes }} minute limit used)
      </div>
    </div>

    <button
      class="banner-dismiss"
      (click)="dismiss()"
      [disabled]="warning?.warningLevel === WarningLevel.CRITICAL"
      aria-label="Dismiss warning">
      <ng-container *ngIf="warning?.warningLevel === WarningLevel.CRITICAL">
        <!-- No dismiss for critical warnings -->
      </ng-container>
      <ng-container *ngIf="warning?.warningLevel !== WarningLevel.CRITICAL">
        ✕
      </ng-container>
    </button>
  </div>

  <div class="banner-progress">
    <div
      class="progress-bar"
      [style.width.%]="warning?.percentageUsed">
    </div>
  </div>
</div>
```

**SCSS** (`session-warning-banner.component.scss`):
```scss
.session-warning-banner {
  position: fixed;
  top: 60px; // Below header
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  animation: slideDown 0.3s ease-out;

  &.warning-orange {
    background-color: #fff3cd;
    border-bottom: 3px solid #ffc107;
    color: #856404;
  }

  &.warning-yellow {
    background-color: #fff8e1;
    border-bottom: 3px solid #ff9800;
    color: #663c00;
  }

  &.warning-red {
    background-color: #ffebee;
    border-bottom: 3px solid #f44336;
    color: #c62828;
  }
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.banner-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.banner-text {
  flex: 1;
}

.banner-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.banner-message {
  font-size: 14px;
  margin-bottom: 4px;
}

.banner-details {
  font-size: 12px;
  opacity: 0.9;

  strong {
    font-weight: 700;
  }
}

.banner-dismiss {
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 8px;
  opacity: 0.7;
  transition: opacity 0.2s;

  &:hover:not(:disabled) {
    opacity: 1;
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.3;
  }
}

.banner-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background-color: rgba(0, 0, 0, 0.1);

  .progress-bar {
    height: 100%;
    background-color: currentColor;
    transition: width 0.5s ease;
  }
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .session-warning-banner {
    top: 50px;
    padding: 12px 16px;
  }

  .banner-icon {
    font-size: 24px;
  }

  .banner-title {
    font-size: 16px;
  }

  .banner-message {
    font-size: 13px;
  }
}
```

**Acceptance Criteria**:
- [ ] Banner displays at correct position (below header)
- [ ] Colors match warning levels (orange/yellow/red)
- [ ] Progress bar animates smoothly
- [ ] Dismiss button works (except for critical)
- [ ] Critical warnings cannot be dismissed
- [ ] Responsive on mobile devices
- [ ] Accessible (ARIA labels, keyboard navigation)

---

#### Task 3.2: Create Session Expired Modal Component

**Component**: `session-expired-modal`
**Location**: `src/app/core/components/session-expired-modal/`

**Generate Command**:
```bash
ng generate component core/components/session-expired-modal --skip-tests
```

**TypeScript** (`session-expired-modal.component.ts`):
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subject, takeUntil, interval } from 'rxjs';
import { WebsocketService } from '../../services/websocket.service';
import { ResponsibleGamblingService } from '../../services/responsible-gambling.service';
import {
  SessionExpiredNotification,
  formatMinutesToReadable
} from '../../models/responsible-gambling.models';

@Component({
  selector: 'app-session-expired-modal',
  templateUrl: './session-expired-modal.component.html',
  styleUrls: ['./session-expired-modal.component.scss']
})
export class SessionExpiredModalComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  notification: SessionExpiredNotification | null = null;
  isVisible = false;
  remainingBreakMinutes = 0;

  constructor(
    private websocketService: WebsocketService,
    private responsibleGamblingService: ResponsibleGamblingService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Subscribe to session expired events
    this.websocketService.sessionExpired
      .pipe(takeUntil(this.destroy$))
      .subscribe(notification => {
        if (notification) {
          this.notification = notification;
          this.isVisible = true;
          this.startBreakCountdown();
        }
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Start countdown timer for break period
   */
  private startBreakCountdown(): void {
    if (!this.notification?.canPlayAgainAt) return;

    // Update remaining time every second
    interval(1000)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.remainingBreakMinutes = this.responsibleGamblingService
          .getRemainingBreakMinutes(this.notification?.canPlayAgainAt || null);
      });

    // Initial calculation
    this.remainingBreakMinutes = this.responsibleGamblingService
      .getRemainingBreakMinutes(this.notification.canPlayAgainAt);
  }

  /**
   * Get formatted break time remaining
   */
  getFormattedBreakTime(): string {
    return formatMinutesToReadable(this.remainingBreakMinutes);
  }

  /**
   * Get formatted time when can play again
   */
  getCanPlayAgainTime(): string {
    if (!this.notification?.canPlayAgainAt) return '';
    return new Date(this.notification.canPlayAgainAt).toLocaleTimeString();
  }

  /**
   * Check if grace period is active
   */
  isGracePeriodActive(): boolean {
    return this.notification?.hasPendingRound === true &&
           (this.notification?.gracePeriodMinutes || 0) > 0;
  }

  /**
   * Close modal and return to lobby
   */
  goToLobby(): void {
    this.isVisible = false;
    this.router.navigate(['/lobby']);
  }

  /**
   * Prevent closing modal by clicking backdrop
   */
  preventClose(event: MouseEvent): void {
    event.stopPropagation();
  }
}
```

**HTML** (`session-expired-modal.component.html`):
```html
<div
  *ngIf="isVisible"
  class="modal-backdrop"
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title">

  <div class="modal-container" (click)="preventClose($event)">

    <!-- Grace Period Content -->
    <div *ngIf="isGracePeriodActive()" class="modal-content grace-period">
      <div class="modal-icon grace-icon">⏳</div>

      <h2 id="modal-title" class="modal-title">
        Grace Period: Complete Your Bet
      </h2>

      <p class="modal-message">
        {{ notification?.message }}
      </p>

      <div class="grace-period-info">
        <div class="info-card">
          <div class="info-label">Grace Period Remaining</div>
          <div class="info-value">
            {{ notification?.gracePeriodMinutes }} minutes
          </div>
        </div>

        <div class="info-card">
          <div class="info-label">Current Bet Status</div>
          <div class="info-value">Pending Settlement</div>
        </div>
      </div>

      <p class="modal-note">
        <strong>Note:</strong> New bets are blocked. Please complete your current round.
      </p>
    </div>

    <!-- Session Expired Content -->
    <div *ngIf="!isGracePeriodActive()" class="modal-content expired">
      <div class="modal-icon expired-icon">⏱️</div>

      <h2 id="modal-title" class="modal-title">
        Session Time Limit Reached
      </h2>

      <p class="modal-message">
        {{ notification?.message }}
      </p>

      <div class="session-stats">
        <div class="stat-card">
          <div class="stat-label">Session Duration</div>
          <div class="stat-value">
            {{ notification?.totalDurationMinutes }} minutes
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-label">Game Played</div>
          <div class="stat-value">{{ notification?.gameName }}</div>
        </div>
      </div>

      <div class="break-info">
        <div class="break-icon">🛑</div>
        <div class="break-text">
          <div class="break-title">Mandatory Break Period</div>
          <div class="break-time">
            <strong>{{ getFormattedBreakTime() }}</strong> remaining
          </div>
          <div class="break-can-play">
            You can play again at <strong>{{ getCanPlayAgainTime() }}</strong>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button
          class="btn-primary"
          (click)="goToLobby()">
          OK - Back to Lobby
        </button>
      </div>

      <p class="modal-footer">
        This limit was set for responsible gambling.
        Take this time to rest and reflect on your gaming.
      </p>
    </div>
  </div>
</div>
```

**SCSS** (`session-expired-modal.component.scss`):
```scss
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease-out;
}

.modal-container {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

.modal-content {
  padding: 40px;
  text-align: center;
}

.modal-icon {
  font-size: 64px;
  margin-bottom: 20px;

  &.grace-icon {
    color: #ff9800;
  }

  &.expired-icon {
    color: #f44336;
  }
}

.modal-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #333;
}

.modal-message {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 24px;
}

.grace-period-info,
.session-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.info-card,
.stat-card {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
}

.info-label,
.stat-label {
  font-size: 12px;
  text-transform: uppercase;
  color: #999;
  margin-bottom: 8px;
  font-weight: 600;
}

.info-value,
.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.modal-note {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 12px 16px;
  border-radius: 4px;
  font-size: 14px;
  text-align: left;
  color: #856404;
}

.break-info {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #ffebee;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  text-align: left;
}

.break-icon {
  font-size: 48px;
  flex-shrink: 0;
}

.break-text {
  flex: 1;
}

.break-title {
  font-size: 18px;
  font-weight: 700;
  color: #c62828;
  margin-bottom: 8px;
}

.break-time {
  font-size: 24px;
  color: #333;
  margin-bottom: 4px;

  strong {
    color: #f44336;
  }
}

.break-can-play {
  font-size: 14px;
  color: #666;

  strong {
    color: #333;
  }
}

.modal-actions {
  margin-bottom: 16px;
}

.btn-primary {
  background: #2196f3;
  color: white;
  border: none;
  padding: 14px 32px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  width: 100%;

  &:hover {
    background: #1976d2;
  }

  &:active {
    transform: scale(0.98);
  }
}

.modal-footer {
  font-size: 12px;
  color: #999;
  font-style: italic;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .modal-container {
    width: 95%;
  }

  .modal-content {
    padding: 24px;
  }

  .modal-icon {
    font-size: 48px;
  }

  .modal-title {
    font-size: 22px;
  }

  .grace-period-info,
  .session-stats {
    grid-template-columns: 1fr;
  }

  .break-info {
    flex-direction: column;
    text-align: center;
  }
}
```

**Acceptance Criteria**:
- [ ] Modal blocks all interaction (cannot close)
- [ ] Grace period content shows when bet pending
- [ ] Expired content shows after session end
- [ ] Countdown timer updates every second
- [ ] Button navigates to lobby
- [ ] Responsive on mobile
- [ ] Accessible (ARIA labels, keyboard focus)

---

#### Task 3.3: Integrate Components into Main Layout

**File**: `src/app/core/components/main-layout/main-layout.component.html`

**What to Add** (after header, before content):
```html
<app-header></app-header>

<!-- NEW: Session limit components -->
<app-session-warning-banner></app-session-warning-banner>
<app-session-expired-modal></app-session-expired-modal>

<div class="main-content">
  <router-outlet></router-outlet>
</div>

<app-footer></app-footer>
```

**Module Registration** (`src/app/core/core.module.ts`):
```typescript
import { SessionWarningBannerComponent } from './components/session-warning-banner/session-warning-banner.component';
import { SessionExpiredModalComponent } from './components/session-expired-modal/session-expired-modal.component';

@NgModule({
  declarations: [
    // ... existing components
    SessionWarningBannerComponent,
    SessionExpiredModalComponent
  ],
  exports: [
    // ... existing exports
    SessionWarningBannerComponent,
    SessionExpiredModalComponent
  ]
})
export class CoreModule { }
```

**Acceptance Criteria**:
- [ ] Components declared in module
- [ ] Components appear in layout
- [ ] No console errors
- [ ] Components don't show until events received

---

### Phase 4: Game Launcher Enhancement (30 minutes)

#### Task 4.1: Add Break Period Error Handling

**File**: `src/app/core/services/game-launcher.service.ts`

**Find** the `launchGame()` method error handling block:
```typescript
// Existing error handling
catchError(error => {
  this.handleLaunchError(error);
  return throwError(() => error);
})
```

**Add** new error handler method:
```typescript
/**
 * Handle game launch errors
 * Displays user-friendly messages for different error types
 */
private handleLaunchError(error: any): void {
  // Check if error is due to break period
  if (error.status === 400 && error.error?.message?.includes('take a break')) {
    // Extract remaining break time from error message
    const match = error.error.message.match(/(\d+) minutes/);
    const remainingMinutes = match ? parseInt(match[1]) : 15;

    this.showBreakPeriodError(remainingMinutes);
  } else if (error.status === 403) {
    this.showError('You are not authorized to play this game.');
  } else if (error.status === 404) {
    this.showError('Game not found or unavailable.');
  } else {
    this.showError('Failed to launch game. Please try again.');
  }
}

/**
 * Show modal for break period violation
 */
private showBreakPeriodError(remainingMinutes: number): void {
  // Use Angular Material Dialog or custom modal service
  const dialogRef = this.dialog.open(BreakPeriodErrorDialogComponent, {
    data: { remainingMinutes },
    disableClose: true,
    width: '400px'
  });
}
```

**Acceptance Criteria**:
- [ ] Break period errors caught and handled
- [ ] User-friendly modal displayed
- [ ] Shows remaining break time
- [ ] Cannot bypass modal
- [ ] Other errors still handled correctly

---

#### Task 4.2: Create Break Period Error Dialog

**Component**: `break-period-error-dialog`
**Location**: `src/app/core/components/break-period-error-dialog/`

**TypeScript**:
```typescript
import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { formatMinutesToReadable } from '../../models/responsible-gambling.models';

@Component({
  selector: 'app-break-period-error-dialog',
  templateUrl: './break-period-error-dialog.component.html',
  styleUrls: ['./break-period-error-dialog.component.scss']
})
export class BreakPeriodErrorDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<BreakPeriodErrorDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { remainingMinutes: number }
  ) {}

  getFormattedTime(): string {
    return formatMinutesToReadable(this.data.remainingMinutes);
  }

  close(): void {
    this.dialogRef.close();
  }
}
```

**HTML**:
```html
<div class="dialog-content">
  <div class="dialog-icon">🛑</div>
  <h2 class="dialog-title">Break Required</h2>

  <p class="dialog-message">
    You need to take a break after reaching your session limit.
  </p>

  <div class="time-display">
    <div class="time-label">You can play again in</div>
    <div class="time-value">{{ getFormattedTime() }}</div>
  </div>

  <button class="btn-primary" (click)="close()">
    OK
  </button>
</div>
```

**Acceptance Criteria**:
- [ ] Dialog shows correct remaining time
- [ ] Cannot close by clicking backdrop
- [ ] Button closes dialog
- [ ] Styling matches app theme

---

### Phase 5: Testing & Validation (1 hour)

#### Test Scenario 1: Warning Flow
**Steps**:
1. Set 2-hour session limit in responsible gambling settings
2. Launch a game
3. Use browser dev tools to simulate time passing (or wait)
4. Verify warnings appear at 80%, 90%, 95%
5. Verify correct colors, icons, messages

**Expected Results**:
- [ ] Orange banner at 96 minutes (80%)
- [ ] Yellow banner at 108 minutes (90%)
- [ ] Red banner at 114 minutes (95%)
- [ ] Progress bar reflects percentage
- [ ] Dismiss works (except critical)

---

#### Test Scenario 2: Normal Session Expiry
**Steps**:
1. Continue from Scenario 1
2. Wait until 120 minutes elapsed
3. Do NOT place any bet
4. Verify session ends immediately

**Expected Results**:
- [ ] Modal appears instantly at 120 minutes
- [ ] Shows "Session Time Limit Reached"
- [ ] Shows 15-minute break required
- [ ] Game window closes/freezes
- [ ] Cannot launch new games

---

#### Test Scenario 3: Grace Period Flow
**Steps**:
1. Set 30-minute session limit for faster testing
2. Launch a slot game
3. At 29:30, place a bet
4. Let session time reach 30:00 while bet is pending

**Expected Results**:
- [ ] Grace period notification appears
- [ ] Shows "Complete Your Bet"
- [ ] Shows 5-minute grace period countdown
- [ ] Bet completes normally
- [ ] After bet completion, session ends
- [ ] 15-minute break enforced

---

#### Test Scenario 4: Break Period Enforcement
**Steps**:
1. Complete Scenario 2 or 3 (session ended)
2. Try to launch any game immediately
3. Wait 5 minutes, try again
4. Wait full 15 minutes, try again

**Expected Results**:
- [ ] First attempt: Error modal shows remaining break time
- [ ] Second attempt (5 min): Still blocked, shows ~10 min remaining
- [ ] Third attempt (15 min): Game launches successfully
- [ ] New session starts with fresh timer

---

#### Test Scenario 5: WebSocket Reconnection
**Steps**:
1. Start a session with active time limit
2. Disconnect internet for 30 seconds
3. Reconnect internet
4. Verify warnings still received

**Expected Results**:
- [ ] WebSocket reconnects automatically
- [ ] Subscription re-established
- [ ] Warnings continue after reconnection
- [ ] No duplicate warnings
- [ ] No missed warnings

---

#### Test Scenario 6: Multiple Tabs
**Steps**:
1. Open casino in Tab A
2. Start game session
3. Open casino in Tab B
4. Verify warnings appear in both tabs

**Expected Results**:
- [ ] Both tabs receive warnings
- [ ] Both tabs show expiry modal
- [ ] Break period enforced in both tabs

---

#### Test Scenario 7: Mobile Responsive
**Steps**:
1. Open casino on mobile device
2. Set short time limit (30 min)
3. Launch game
4. Verify all warning and modal displays

**Expected Results**:
- [ ] Banner fits mobile screen
- [ ] Modal fits mobile screen
- [ ] Text readable on small screens
- [ ] Touch interactions work
- [ ] No horizontal scrolling

---

## Edge Cases & Error Handling

### Edge Case 1: WebSocket Connection Failure
**Problem**: What if WebSocket never connects?

**Solution**: Fallback to polling
```typescript
// In a component that needs session status
ngOnInit(): void {
  // Subscribe to WebSocket
  this.websocketService.sessionWarning.subscribe(/* ... */);

  // Fallback: Poll every 30 seconds if WebSocket disconnected
  interval(30000)
    .pipe(
      takeUntil(this.destroy$),
      filter(() => !this.websocketService.isConnected)
    )
    .subscribe(() => {
      this.responsibleGamblingService.getCurrentSessionStatus()
        .subscribe(status => {
          if (status.willExpireSoon) {
            // Show warning manually
          }
        });
    });
}
```

---

### Edge Case 2: Clock Skew (Client/Server Time Difference)
**Problem**: Client clock is wrong, countdown inaccurate

**Solution**: Always use server-provided times
```typescript
// Don't calculate based on client time
// BAD: const remaining = limit - (Date.now() - startTime);

// Good: Use server-calculated remaining time
const remaining = status.remainingMinutes; // Server calculates this
```

---

### Edge Case 3: User Changes Limit During Session
**Problem**: User increases limit while session active

**Solution**: Backend handles this
- New limit doesn't affect current session
- Current session uses original limit
- Next session uses new limit
- Frontend just displays what backend sends

---

### Edge Case 4: Grace Period Expires but Bet Still Pending
**Problem**: Bet takes > 5 minutes to settle

**Solution**: Backend force-ends anyway (documented behavior)
- Session marked COMPLETED
- GameRound remains PENDING
- Provider's backend eventually settles bet
- Balance updated when provider callback arrives
- Frontend shows modal: "Grace period expired"

---

### Edge Case 5: User Refreshes Page During Grace Period
**Problem**: Lose grace period notification state

**Solution**: Query session status on page load
```typescript
ngOnInit(): void {
  // Check current session status on app init
  this.authService.user$.pipe(
    filter(user => !!user),
    switchMap(() => this.responsibleGamblingService.getCurrentSessionStatus())
  ).subscribe(status => {
    if (status.hasActiveSession && status.percentageUsed >= 100) {
      // Session should have ended, check for pending rounds
      // Show appropriate UI based on backend state
    }
  });
}
```

---

### Edge Case 6: Network Latency Delays Warning
**Problem**: Warning arrives 30 seconds late

**Solution**: Accept it (not critical)
- Warnings are informational, not enforcement
- Backend still enforces at 100%
- Late warning better than no warning
- 30-second delay is acceptable UX

---

### Edge Case 7: User Has No Time Limit Set
**Problem**: What to display?

**Solution**: Show nothing
- Backend won't send warnings
- Components remain hidden
- REST endpoint returns `hasActiveSession: false`
- Game launches normally without checks

---

## Appendix: Code References

### Backend Files
| File | Lines | Purpose |
|------|-------|---------|
| `SessionTimeLimitMonitorService.kt` | 399 | Core monitoring logic |
| `SessionLimitWebSocketDto.kt` | 121 | Message formats |
| `SessionLimitWebSocketController.kt` | 52 | WebSocket subscription handling |
| `GameLaunchService.kt` | 686-745 | Break period enforcement |
| `CustomerResponsibleGamblingController.kt` | 298-310 | REST endpoint |
| `WebSocketConfig.kt` | 63 | WebSocket configuration |

### Frontend Files (To Be Created/Modified)
| File | Estimated Lines | Purpose |
|------|-----------------|---------|
| `responsible-gambling.models.ts` | +80 | WebSocket event interfaces |
| `websocket.service.ts` | +60 | Session limit subscription |
| `responsible-gambling.service.ts` | +40 | Session status API call |
| `session-warning-banner.component.ts` | 150 | Warning banner |
| `session-expired-modal.component.ts` | 180 | Expiry modal |
| `break-period-error-dialog.component.ts` | 80 | Break error dialog |
| `game-launcher.service.ts` | +50 | Error handling |
| `main-layout.component.html` | +3 | Component integration |

**Total New/Modified Code**: ~650 lines

---

## Implementation Checklist

### Phase 1: Models & Services
- [ ] Add WebSocket event interfaces to models
- [ ] Add helper functions for formatting
- [ ] Add session limit subscription to WebSocket service
- [ ] Add getCurrentSessionStatus to Responsible Gambling service
- [ ] Test services with mock data

### Phase 2: UI Components
- [ ] Create SessionWarningBannerComponent
- [ ] Create SessionExpiredModalComponent
- [ ] Create BreakPeriodErrorDialogComponent
- [ ] Style components to match design system
- [ ] Add to main layout
- [ ] Register in module

### Phase 3: Integration
- [ ] Connect WebSocket observables to components
- [ ] Add error handling to game launcher
- [ ] Test end-to-end flow
- [ ] Test WebSocket reconnection
- [ ] Test mobile responsive

### Phase 4: Edge Cases
- [ ] Implement polling fallback
- [ ] Handle page refresh scenarios
- [ ] Test multiple tabs
- [ ] Test with no time limit set
- [ ] Test network failure scenarios

### Phase 5: QA & Polish
- [ ] All 7 test scenarios pass
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Performance check (no memory leaks)
- [ ] Cross-browser testing
- [ ] Mobile device testing
- [ ] Final code review

---

## Success Criteria

✅ **Functional Requirements Met**:
- Progressive warnings display correctly
- Grace period handles pending bets
- Break period enforced strictly
- WebSocket communication reliable
- REST fallback works

✅ **User Experience**:
- Clear, non-intrusive warnings
- Fair handling of active bets
- Understandable error messages
- Responsive on all devices
- Accessible to all users

✅ **Technical Quality**:
- No console errors
- No memory leaks
- Proper error handling
- Clean, maintainable code
- Well-documented

✅ **Compliance**:
- Regulatory requirements met
- Audit trail complete (backend)
- Tamper-proof enforcement
- User cannot bypass limits

---

**End of Document**

**Next Steps**: Review this document with team, then proceed with Phase 1 implementation.