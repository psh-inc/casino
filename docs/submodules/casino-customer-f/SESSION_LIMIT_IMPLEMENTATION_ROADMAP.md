# Session Time Limit - Customer Frontend Implementation Roadmap

**Document Version**: 1.0
**Created**: 2025-10-16
**Based on**: Actual customer frontend codebase analysis
**Backend Status**: ✅ COMPLETE
**Frontend Status**: ❌ NOT STARTED

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Codebase Analysis](#codebase-analysis)
3. [Where Session Limits Apply](#where-session-limits-apply)
4. [Implementation Phases](#implementation-phases)
5. [Detailed Task Breakdown](#detailed-task-breakdown)
6. [Integration Points](#integration-points)
7. [Testing Strategy](#testing-strategy)

---

## Executive Summary

### What We Discovered

After analyzing the customer frontend codebase, we found:

#### ✅ **Strong Foundation**
- **WebSocket Service**: Fully operational (`websocket.service.ts` - 430 lines)
- **Responsible Gambling Module**: Complete feature module exists
- **Game Launcher Service**: Centralized game launching (`game-launcher.service.ts` - 233 lines)
- **Main Layout**: Clean structure ready for global components

#### 🎯 **Game Launch Points Identified**
- **44 files** contain game launching logic across the app
- **7 major components** where users can launch games:
  1. Home page game sections
  2. Casino/Games page
  3. Mobile game preview page
  4. Game cards (reusable component)
  5. Game grid component
  6. Direct game page (`/game/:id`)
  7. Search results

#### 📍 **Key Architectural Decision**
The codebase uses a **centralized GameLauncherService** - this is PERFECT for session limit integration. We only need to add session limit checks in ONE place, and it will apply across the entire application.

---

## Codebase Analysis

### Architecture Overview

```
casino-customer-f/
├── src/app/
│   ├── core/
│   │   ├── services/
│   │   │   ├── game-launcher.service.ts      ← ⭐ MAIN INTEGRATION POINT
│   │   │   ├── websocket.service.ts          ← Add session subscription
│   │   │   ├── responsible-gambling.service.ts ← Add REST endpoint
│   │   │   └── auth.service.ts               ← Already handles auth
│   │   ├── components/
│   │   │   └── main-layout/                  ← Add warning banner & modal
│   │   └── models/
│   │       └── responsible-gambling.models.ts ← Add WebSocket interfaces
│   ├── features/
│   │   ├── home/                             ← Launches games (home.component.ts)
│   │   ├── games/                            ← Launches games (multiple components)
│   │   └── responsible-gambling/             ← Existing feature module
│   └── modules/
│       └── game-page/                        ← Direct game page
```

### Centralized Game Launch Flow

**Current Flow** (works perfectly for our needs):
```
User Click (any component)
    ↓
GameLauncherService.launchGame()
    ↓
Check authentication
    ↓
Navigate to /game/:id
    ↓
GamePageComponent loads iframe
```

**Enhanced Flow** (what we'll implement):
```
User Click (any component)
    ↓
GameLauncherService.launchGame()
    ↓
⭐ NEW: Check session time limit ⭐
    ↓
Check authentication
    ↓
Navigate to /game/:id
    ↓
GamePageComponent loads iframe
    ↓
⭐ NEW: WebSocket monitors session ⭐
    ↓
⭐ NEW: Show warnings (80%, 90%, 95%) ⭐
    ↓
⭐ NEW: Force end at 100% ⭐
```

---

## Where Session Limits Apply

### 1. Game Launch Points (7 Locations)

#### A. Home Page (`/`)
**File**: `src/app/features/home/home.component.ts`

**Methods**:
- `onGamePlay()` - Play real money (line 234)
- `onGameDemo()` - Play demo (line 260)
- `onGameTap()` - Mobile tap handling (line 210)

**Integration**: ✅ Already uses `GameLauncherService` - no changes needed here

---

#### B. Casino/Games Page (`/games`)
**File**: `src/app/features/games/components/casino-page/casino-page.component.ts`

**Integration**: ✅ Uses `GameLauncherService` - no changes needed

---

#### C. Games List Page (`/games`)
**File**: `src/app/features/games/components/games-page/games-page.component.ts`

**Integration**: ✅ Uses `GameLauncherService` - no changes needed

---

#### D. Game Grid Component (Reusable)
**File**: `src/app/features/games/components/game-grid/game-grid.component.ts`

**Integration**: ✅ Uses `GameLauncherService` - no changes needed

---

#### E. Game Card Component (Reusable)
**File**: `src/app/features/games/components/game-card/game-card.component.ts`

**Methods**:
- `playReal()` - Emits event to parent (line 28)
- `playDemo()` - Emits event to parent (line 34)

**Integration**: ✅ Parents use `GameLauncherService` - no changes needed

---

#### F. Mobile Game Preview Page
**File**: `src/app/features/games/components/mobile-game-preview-page/mobile-game-preview-page.component.ts`

**Integration**: ✅ Uses `GameLauncherService` - no changes needed

---

#### G. Direct Game Page (`/game/:id`)
**File**: `src/app/modules/game-page/game-page.component.ts`

**Note**: This is where the actual iframe launches. Game launch request happens here.

**Integration**: ⚠️ Need to handle backend API errors for break period

---

### 2. WebSocket Notification Display Points

#### A. Warning Banner
**Display**: Fixed position below header (all pages)
**Trigger**: 80%, 90%, 95% thresholds
**Behavior**: Non-blocking, can be dismissed (except critical)

#### B. Session Expired Modal
**Display**: Full-screen blocking modal (all pages)
**Trigger**: 100% threshold reached
**Behavior**: Blocks all interaction, forces navigation to lobby

#### C. Grace Period Banner
**Display**: Fixed position (all pages)
**Trigger**: 100% reached with pending bet
**Behavior**: Shows countdown, blocks new bets

---

## Implementation Phases

### Phase 1: Foundation (1 hour)
**Goal**: Set up TypeScript models and extend existing services

**Deliverables**:
- [ ] Add WebSocket event interfaces to `responsible-gambling.models.ts`
- [ ] Add session limit subscription to `websocket.service.ts`
- [ ] Add `getCurrentSessionStatus()` to `responsible-gambling.service.ts`
- [ ] Add helper functions for formatting time

**Files Modified**: 3 files
**Lines Added**: ~150 lines

---

### Phase 2: UI Components (2 hours)
**Goal**: Create the three visual components for session limit notifications

**Deliverables**:
- [ ] Create `session-warning-banner` component
- [ ] Create `session-expired-modal` component
- [ ] Create `break-period-error-dialog` component
- [ ] Add components to CoreModule
- [ ] Style components to match design system

**Files Created**: 9 files (3 components × 3 files each)
**Lines Added**: ~600 lines

---

### Phase 3: Integration (1 hour)
**Goal**: Connect components to main layout and game launcher

**Deliverables**:
- [ ] Add components to `main-layout.component.html`
- [ ] Add session limit check to `GameLauncherService`
- [ ] Add error handling to `GamePageComponent`
- [ ] Test WebSocket connection flow

**Files Modified**: 3 files
**Lines Added**: ~100 lines

---

### Phase 4: Testing & Polish (1 hour)
**Goal**: Comprehensive testing and edge case handling

**Deliverables**:
- [ ] Test warning progression (80%, 90%, 95%)
- [ ] Test session expiry with/without pending bets
- [ ] Test break period enforcement
- [ ] Test WebSocket reconnection
- [ ] Test mobile responsive
- [ ] Fix any bugs found

---

## Detailed Task Breakdown

### PHASE 1: Foundation

#### Task 1.1: Update Responsible Gambling Models
**File**: `src/app/core/models/responsible-gambling.models.ts`
**Current Size**: 237 lines
**Additions**: ~80 lines

**What to Add**:
```typescript
// Add after existing enums (line ~50)

/**
 * Warning level for session time limit proximity
 */
export enum WarningLevel {
  APPROACHING = 'APPROACHING',  // 80%
  NEAR = 'NEAR',                // 90%
  CRITICAL = 'CRITICAL'         // 95%
}

/**
 * WebSocket event: Session limit warning
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
  timestamp: string;
}

/**
 * WebSocket event: Session expired
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
  canPlayAgainAt: string | null;
  hasPendingRound: boolean;
  gracePeriodMinutes: number | null;
  message: string;
  timestamp: string;
}

/**
 * REST response: Current session status
 */
export interface CurrentSessionStatusResponse {
  hasActiveSession: boolean;
  sessionId: string | null;
  gameId: string | null;
  gameName: string | null;
  startedAt: string | null;
  elapsedMinutes: number | null;
  limitMinutes: number | null;
  remainingMinutes: number | null;
  percentageUsed: number | null;
  willExpireSoon: boolean;
  warningsSent: number;
}

/**
 * Helper: Get CSS class for warning level
 */
export function getWarningLevelColor(level: WarningLevel): string {
  switch (level) {
    case WarningLevel.APPROACHING: return 'warning-orange';
    case WarningLevel.NEAR: return 'warning-yellow';
    case WarningLevel.CRITICAL: return 'warning-red';
  }
}

/**
 * Helper: Get icon for warning level
 */
export function getWarningLevelIcon(level: WarningLevel): string {
  switch (level) {
    case WarningLevel.APPROACHING: return '⚠️';
    case WarningLevel.NEAR: return '⏰';
    case WarningLevel.CRITICAL: return '🚨';
  }
}

/**
 * Helper: Format minutes to readable time
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
- [ ] Interfaces match backend DTOs exactly
- [ ] TypeScript compiles without errors
- [ ] Helper functions tested with various inputs

---

#### Task 1.2: Extend WebSocket Service
**File**: `src/app/core/services/websocket.service.ts`
**Current Size**: 430 lines
**Additions**: ~60 lines

**Changes Required**:

**Step 1**: Add subjects (after line ~50)
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
 * Subscribe to session limit notifications
 */
private subscribeToSessionLimits(playerId: number): void {
  const destination = `/user/${playerId}/queue/session-limits`;

  this.client.subscribe(destination, (message: IMessage) => {
    try {
      const event = JSON.parse(message.body);

      if (event.type === 'SESSION_WARNING') {
        this.sessionWarning$.next(event as SessionLimitWarning);
        console.log(`[WebSocket] Session warning: ${event.warningLevel}`);
      } else if (event.type === 'SESSION_EXPIRED') {
        this.sessionExpired$.next(event as SessionExpiredNotification);
        console.log(`[WebSocket] Session expired: ${event.reason}`);
      }
    } catch (error) {
      console.error('[WebSocket] Error parsing session limit message:', error);
    }
  });

  console.log(`[WebSocket] Subscribed to: ${destination}`);
}
```

**Step 3**: Call in connection setup (find existing `setupSubscriptions()` method)
```typescript
// Add to existing subscription setup
this.subscribeToSessionLimits(playerId);
```

**Step 4**: Clear on disconnect
```typescript
// Add to disconnect method
this.sessionWarning$.next(null);
this.sessionExpired$.next(null);
```

**Acceptance Criteria**:
- [ ] Subscription created on WebSocket connect
- [ ] Events parsed and emitted correctly
- [ ] Console logs confirm subscription
- [ ] State cleared on disconnect

---

#### Task 1.3: Extend Responsible Gambling Service
**File**: `src/app/core/services/responsible-gambling.service.ts`
**Current Size**: 163 lines
**Additions**: ~40 lines

**What to Add** (at end of class, before closing brace):
```typescript
/**
 * Get current session status
 */
getCurrentSessionStatus(): Observable<CurrentSessionStatusResponse> {
  return this.http.get<CurrentSessionStatusResponse>(
    `${this.apiUrl}/session/current`
  );
}

/**
 * Check if player is in break period
 */
isInBreakPeriod(status: CurrentSessionStatusResponse): boolean {
  return !status.hasActiveSession &&
         status.canPlayAgainAt != null &&
         new Date(status.canPlayAgainAt) > new Date();
}

/**
 * Calculate remaining break minutes
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
- [ ] Helper methods calculate correctly
- [ ] Error handling for API failures

---

### PHASE 2: UI Components

#### Task 2.1: Create Session Warning Banner

**Generate Component**:
```bash
cd casino-customer-f
ng generate component core/components/session-warning-banner --skip-tests
```

**Files Created**:
- `session-warning-banner.component.ts`
- `session-warning-banner.component.html`
- `session-warning-banner.component.scss`

**Implementation**: See `SESSION_LIMIT_FRONTEND_IMPLEMENTATION.md` Task 3.1 for complete code

**Key Features**:
- Fixed position below header
- Color-coded by severity (orange/yellow/red)
- Progress bar showing percentage used
- Dismissible (except critical warnings)
- Responsive mobile design

**Acceptance Criteria**:
- [ ] Displays at correct position
- [ ] Colors change based on warning level
- [ ] Progress bar animates smoothly
- [ ] Dismiss works correctly
- [ ] Mobile responsive

---

#### Task 2.2: Create Session Expired Modal

**Generate Component**:
```bash
ng generate component core/components/session-expired-modal --skip-tests
```

**Files Created**:
- `session-expired-modal.component.ts`
- `session-expired-modal.component.html`
- `session-expired-modal.component.scss`

**Implementation**: See `SESSION_LIMIT_FRONTEND_IMPLEMENTATION.md` Task 3.2 for complete code

**Key Features**:
- Full-screen blocking modal
- Shows two states: grace period OR expired
- Countdown timer for break period
- Cannot be closed (forces lobby navigation)
- Responsive mobile design

**Acceptance Criteria**:
- [ ] Modal blocks all interaction
- [ ] Grace period content shows correctly
- [ ] Countdown updates every second
- [ ] Button navigates to lobby
- [ ] Mobile responsive

---

#### Task 2.3: Create Break Period Error Dialog

**Generate Component**:
```bash
ng generate component core/components/break-period-error-dialog --skip-tests
```

**Files Created**:
- `break-period-error-dialog.component.ts`
- `break-period-error-dialog.component.html`
- `break-period-error-dialog.component.scss`

**Implementation**: See `SESSION_LIMIT_FRONTEND_IMPLEMENTATION.md` Task 4.2 for complete code

**Key Features**:
- Angular Material dialog
- Shows remaining break time
- Cannot be dismissed via backdrop
- Clean, simple design

**Acceptance Criteria**:
- [ ] Dialog shows correct time
- [ ] Cannot close via backdrop
- [ ] Button closes dialog
- [ ] Matches app theme

---

#### Task 2.4: Register Components in Module

**File**: `src/app/core/core.module.ts` (if using modules)

OR if using standalone components (recommended for Angular 17):

**File**: `src/app/core/components/index.ts`

**Add exports**:
```typescript
export { SessionWarningBannerComponent } from './session-warning-banner/session-warning-banner.component';
export { SessionExpiredModalComponent } from './session-expired-modal/session-expired-modal.component';
export { BreakPeriodErrorDialogComponent } from './break-period-error-dialog/break-period-error-dialog.component';
```

**Acceptance Criteria**:
- [ ] Components compile without errors
- [ ] Can be imported in other components

---

### PHASE 3: Integration

#### Task 3.1: Add Components to Main Layout

**File**: `src/app/core/components/main-layout/main-layout.component.html`
**Current Size**: 50 lines

**Change** (after line 7, after header):
```html
<app-header-new
  [config]="layoutConfig?.headerConfig"
  [navigationMenu]="layoutConfig?.sidebarMenu"
  (authModalOpening)="closeDrawer()">
</app-header-new>

<!-- NEW: Session limit components -->
<app-session-warning-banner></app-session-warning-banner>
<app-session-expired-modal></app-session-expired-modal>

<!-- Main Content -->
<main class="main-content">
  <router-outlet></router-outlet>
</main>
```

**File**: `src/app/core/components/main-layout/main-layout.component.ts`
**Add imports**:
```typescript
import { SessionWarningBannerComponent } from '../session-warning-banner/session-warning-banner.component';
import { SessionExpiredModalComponent } from '../session-expired-modal/session-expired-modal.component';

@Component({
  // ...
  imports: [
    // ... existing imports
    SessionWarningBannerComponent,
    SessionExpiredModalComponent
  ]
})
```

**Acceptance Criteria**:
- [ ] Components appear in layout
- [ ] No console errors
- [ ] Components hidden until events received

---

#### Task 3.2: Add Session Limit Check to Game Launcher

**File**: `src/app/core/services/game-launcher.service.ts`
**Current Size**: 233 lines

**Step 1**: Import service (line ~6)
```typescript
import { ResponsibleGamblingService } from './responsible-gambling.service';
```

**Step 2**: Inject in constructor (line ~19)
```typescript
constructor(
  private router: Router,
  private authService: AuthService,
  private responsibleGamblingService: ResponsibleGamblingService  // NEW
) {}
```

**Step 3**: Add check method (before `handleDesktopLaunch`, line ~54)
```typescript
/**
 * Check if player can launch game (session time limit enforcement)
 */
private async checkSessionTimeLimit(): Promise<{ allowed: boolean; reason?: string; remainingMinutes?: number }> {
  try {
    const status = await firstValueFrom(
      this.responsibleGamblingService.getCurrentSessionStatus()
    );

    // Check if in break period
    if (this.responsibleGamblingService.isInBreakPeriod(status)) {
      const remainingMinutes = this.responsibleGamblingService
        .getRemainingBreakMinutes(status.canPlayAgainAt);

      return {
        allowed: false,
        reason: `You need to take a break. You can play again in ${remainingMinutes} minutes.`,
        remainingMinutes
      };
    }

    return { allowed: true };
  } catch (error) {
    console.error('Error checking session time limit:', error);
    // On error, allow game launch (fail open for better UX)
    return { allowed: true };
  }
}
```

**Step 4**: Call check in launch methods (line ~56 and ~86)

**In `handleDesktopLaunch`**:
```typescript
private async handleDesktopLaunch(options: GameLaunchOptions): Promise<void> {
  const { game, mode, from } = options;

  // For demo mode, always launch directly
  if (mode === 'demo') {
    this.navigateToGameScreen(game, from, true, 'desktop');
    return;
  }

  // NEW: Check session time limit
  const limitCheck = await this.checkSessionTimeLimit();
  if (!limitCheck.allowed) {
    this.showBreakPeriodError(limitCheck.remainingMinutes || 15);
    return;
  }

  // For real money mode, check authentication
  const isAuthenticated = await this.checkAuthentication();
  // ... rest of method
}
```

**In `handleMobilePreviewAction`**:
```typescript
async handleMobilePreviewAction(game: Game, mode: 'demo' | 'real', from: GameLaunchOptions['from'] = 'casino'): Promise<void> {
  if (mode === 'demo') {
    this.navigateToGameScreen(game, from, true, 'mobile');
    return;
  }

  // NEW: Check session time limit
  const limitCheck = await this.checkSessionTimeLimit();
  if (!limitCheck.allowed) {
    this.showBreakPeriodError(limitCheck.remainingMinutes || 15);
    return;
  }

  // Real money mode - check authentication
  const isAuthenticated = await this.checkAuthentication();
  // ... rest of method
}
```

**Step 5**: Add error dialog method (at end of class)
```typescript
/**
 * Show break period error dialog
 */
private showBreakPeriodError(remainingMinutes: number): void {
  // Use Angular Material dialog or custom modal
  alert(`Break Required\n\nYou need to take a break after reaching your session limit.\nYou can play again in ${remainingMinutes} minutes.`);

  // TODO: Replace with proper dialog component
  // const dialogRef = this.dialog.open(BreakPeriodErrorDialogComponent, {
  //   data: { remainingMinutes },
  //   disableClose: true
  // });
}
```

**Acceptance Criteria**:
- [ ] Session limit checked before game launch
- [ ] Break period blocks game launch
- [ ] Error message shows remaining time
- [ ] Demo mode bypasses check

---

#### Task 3.3: Add Error Handling to Game Page

**File**: `src/app/modules/game-page/game-page.component.ts`

**Find**: The method that calls backend API to launch game (around line 100+)

**Add**: Error handling for `BusinessRuleViolationException`

```typescript
// In the catch block of game launch
.catch(error => {
  if (error.status === 400 && error.error?.message?.includes('take a break')) {
    // Extract remaining minutes from error message
    const match = error.error.message.match(/(\d+) minutes/);
    const remainingMinutes = match ? parseInt(match[1]) : 15;

    this.showBreakPeriodError(remainingMinutes);
  } else {
    // Handle other errors normally
    this.handleLaunchError(error);
  }
})
```

**Acceptance Criteria**:
- [ ] Backend break period errors caught
- [ ] User-friendly message displayed
- [ ] Shows remaining break time

---

### PHASE 4: Testing & Polish

#### Test Scenario 1: Complete Warning Flow
**Steps**:
1. Set 2-hour session limit in responsible gambling settings
2. Launch a game
3. Monitor warnings at 96min, 108min, 114min
4. Verify colors, messages, progress bar

**Expected**:
- [ ] Orange banner at 80% (96 min)
- [ ] Yellow banner at 90% (108 min)
- [ ] Red banner at 95% (114 min)
- [ ] All dismissible except critical

---

#### Test Scenario 2: Session Expiry Without Bet
**Steps**:
1. Continue from Scenario 1
2. Wait until 120 minutes
3. Do not place any bet

**Expected**:
- [ ] Modal appears at 120 minutes
- [ ] Game window closes
- [ ] Shows 15-minute break
- [ ] Cannot launch new games

---

#### Test Scenario 3: Grace Period With Pending Bet
**Steps**:
1. Set 30-minute limit (faster testing)
2. At 29:30, place a bet
3. Let time reach 30:00

**Expected**:
- [ ] Grace period notification appears
- [ ] Shows 5-minute countdown
- [ ] Bet completes normally
- [ ] Session ends after bet completion

---

#### Test Scenario 4: Break Period Enforcement
**Steps**:
1. Complete Scenario 2
2. Try to launch game immediately
3. Wait 5 minutes, try again
4. Wait 15 minutes, try again

**Expected**:
- [ ] First attempt: Error with countdown
- [ ] Second attempt: Still blocked (~10 min)
- [ ] Third attempt: Launches successfully

---

#### Test Scenario 5: Mobile Responsive
**Steps**:
1. Open on mobile device
2. Set short limit (30 min)
3. Launch game
4. Test all warnings and modals

**Expected**:
- [ ] Banner fits screen
- [ ] Modal fits screen
- [ ] Text readable
- [ ] Touch works

---

## Integration Points Summary

### Critical Files to Modify

| File | Purpose | Lines | Priority |
|------|---------|-------|----------|
| `responsible-gambling.models.ts` | Add WebSocket interfaces | +80 | 🔴 HIGH |
| `websocket.service.ts` | Add session subscription | +60 | 🔴 HIGH |
| `responsible-gambling.service.ts` | Add REST endpoint | +40 | 🔴 HIGH |
| `game-launcher.service.ts` | Add session check | +50 | 🔴 HIGH |
| `main-layout.component.html` | Add components | +3 | 🟡 MEDIUM |
| `game-page.component.ts` | Add error handling | +20 | 🟡 MEDIUM |

### New Components to Create

| Component | Files | Lines | Priority |
|-----------|-------|-------|----------|
| `session-warning-banner` | 3 | ~150 | 🔴 HIGH |
| `session-expired-modal` | 3 | ~180 | 🔴 HIGH |
| `break-period-error-dialog` | 3 | ~80 | 🟡 MEDIUM |

**Total**: 9 new files, ~850 lines of code

---

## Timeline Estimate

### Optimistic (Experienced Angular Developer)
- Phase 1: 1 hour
- Phase 2: 2 hours
- Phase 3: 1 hour
- Phase 4: 1 hour
**Total: 5 hours**

### Realistic (Mid-level Developer)
- Phase 1: 1.5 hours
- Phase 2: 3 hours
- Phase 3: 1.5 hours
- Phase 4: 2 hours
**Total: 8 hours (1 day)**

### Conservative (Junior Developer + Learning)
- Phase 1: 2 hours
- Phase 2: 4 hours
- Phase 3: 2 hours
- Phase 4: 3 hours
**Total: 11 hours (1.5 days)**

---

## Success Metrics

### Functional
- [ ] Warnings display at correct thresholds
- [ ] Grace period handles pending bets
- [ ] Break period blocks game launches
- [ ] WebSocket reconnection works
- [ ] All 5 test scenarios pass

### Technical
- [ ] No console errors
- [ ] No memory leaks
- [ ] Proper error handling
- [ ] Clean, maintainable code
- [ ] TypeScript strict mode passes

### UX
- [ ] Clear, non-intrusive warnings
- [ ] Fair handling of active bets
- [ ] Responsive on all devices
- [ ] Accessible (WCAG 2.1 AA)

---

## Risk Mitigation

### Risk 1: WebSocket Connection Failure
**Mitigation**: Implement REST polling fallback (every 30 seconds)

### Risk 2: Multiple Tabs
**Mitigation**: WebSocket subscriptions in each tab work independently

### Risk 3: Clock Skew
**Mitigation**: Always use server-calculated times, never client time

### Risk 4: Existing Code Conflicts
**Mitigation**: Use centralized GameLauncherService - single integration point

---

## Next Steps

1. **Review this roadmap** with team for feedback
2. **Set up development branch**: `feature/session-time-limits-frontend`
3. **Start Phase 1**: Foundation (models & services)
4. **Daily standups**: Track progress, blockers
5. **Code reviews**: After each phase
6. **Final QA**: All 5 test scenarios before merge

---

**Document Maintained By**: Development Team
**Last Updated**: 2025-10-16
**Next Review**: After Phase 1 completion

---

## Appendix: Quick Reference

### Backend Endpoints
- **WebSocket**: `ws://localhost:8080/ws`
- **Destination**: `/user/{playerId}/queue/session-limits`
- **REST**: `GET /api/customer/responsible-gambling/session/current`

### Key Services
- **GameLauncherService**: Centralized game launching
- **WebsocketService**: Real-time notifications
- **ResponsibleGamblingService**: Session status API

### Component Hierarchy
```
MainLayoutComponent
├── SessionWarningBannerComponent    (fixed position)
├── SessionExpiredModalComponent     (overlay)
└── [Router Outlet Content]
    └── GamePageComponent
        └── [Game Iframe]
```

**End of Roadmap**