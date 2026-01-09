# Angular State Management Patterns

## BehaviorSubject Pattern

This codebase uses `BehaviorSubject` for service-level state management. No external state library (NgRx, Akita) is used.

### Basic State Service

```typescript
@Injectable({ providedIn: 'root' })
export class AuthService implements OnDestroy {
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  private destroy$ = new Subject<void>();

  // Expose as Observable (read-only)
  public currentUser$ = this.currentUserSubject.asObservable();
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  // Synchronous access when needed
  get currentUser(): User | null {
    return this.currentUserSubject.value;
  }

  get isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  login(request: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.authUrl}/login`, request).pipe(
      tap(response => {
        if (response.token) {
          this.storeTokens(response.token, response.refreshToken);
          this.currentUserSubject.next(response.user);
          this.isAuthenticatedSubject.next(true);
        }
      })
    );
  }

  logout(): void {
    this.clearTokens();
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Multi-State Service (WalletService)

```typescript
@Injectable({ providedIn: 'root' })
export class WalletV2Service implements OnDestroy {
  private currentPlayerId$ = new BehaviorSubject<number | null>(null);
  private playerBalance$ = new BehaviorSubject<PlayerBalanceDto | null>(null);
  private wageringStatus$ = new BehaviorSubject<WageringStatus | null>(null);
  private destroy$ = new Subject<void>();

  getCurrentPlayerId(): Observable<number | null> {
    return this.currentPlayerId$.asObservable();
  }

  getPlayerBalance(): Observable<PlayerBalanceDto | null> {
    return this.playerBalance$.asObservable();
  }

  getWageringStatus(): Observable<WageringStatus | null> {
    return this.wageringStatus$.asObservable();
  }

  setCurrentPlayer(playerId: number): void {
    this.currentPlayerId$.next(playerId);
    this.startBalanceRefresh(playerId);
  }

  clearState(): void {
    this.currentPlayerId$.next(null);
    this.playerBalance$.next(null);
    this.wageringStatus$.next(null);
  }
}
```

---

## WARNING: Exposing BehaviorSubject Directly

**The Problem:**

```typescript
// BAD - Exposes mutable subject
@Injectable({ providedIn: 'root' })
export class UserService {
  public user$ = new BehaviorSubject<User | null>(null);  // Anyone can call .next()!
}

// In some component:
this.userService.user$.next(fakeUser);  // Bypasses service logic
```

**Why This Breaks:**
1. Any component can mutate state directly
2. Validation logic in service is bypassed
3. State changes become unpredictable
4. Debugging becomes nearly impossible

**The Fix:**

```typescript
// GOOD - Private subject, public Observable
@Injectable({ providedIn: 'root' })
export class UserService {
  private userSubject = new BehaviorSubject<User | null>(null);
  public user$ = this.userSubject.asObservable();  // Read-only

  updateUser(user: User): void {
    // Validation, logging, side effects happen here
    this.userSubject.next(user);
  }
}
```

---

## WARNING: Not Using distinctUntilChanged

**The Problem:**

```typescript
// BAD - Triggers on every emission, even if value unchanged
this.playerId$.subscribe(id => {
  this.loadPlayerData(id);  // Called even when id didn't change
});
```

**Why This Breaks:**
1. Unnecessary API calls
2. UI flickers from redundant updates
3. Performance degradation

**The Fix:**

```typescript
// GOOD - Only triggers on actual changes
this.playerId$.pipe(
  distinctUntilChanged(),
  switchMap(id => this.playerService.getById(id)),
  takeUntil(this.destroy$)
).subscribe(player => this.player = player);
```

---

## Filter State Persistence

```typescript
@Injectable({ providedIn: 'root' })
export class FilterStateService {
  private static readonly STORAGE_KEY = 'casino_filter_state';

  saveFilterState(state: CasinoFilterState): void {
    try {
      const cleanState: CasinoFilterState = {};
      Object.keys(state).forEach(key => {
        const value = (state as any)[key];
        if (value !== undefined && value !== null && value !== '') {
          (cleanState as any)[key] = value;
        }
      });
      sessionStorage.setItem(FilterStateService.STORAGE_KEY, JSON.stringify(cleanState));
    } catch (error) {
      console.warn('Failed to save filter state:', error);
    }
  }

  loadFilterState(): CasinoFilterState | null {
    try {
      const saved = sessionStorage.getItem(FilterStateService.STORAGE_KEY);
      return saved ? JSON.parse(saved) : null;
    } catch (error) {
      console.warn('Failed to load filter state:', error);
      return null;
    }
  }

  clearFilterState(): void {
    sessionStorage.removeItem(FilterStateService.STORAGE_KEY);
  }
}
```

---

## Combining Multiple States

```typescript
// In component
ngOnInit(): void {
  combineLatest([
    this.authService.currentUser$,
    this.walletService.getPlayerBalance(),
    this.configService.getSettings()
  ]).pipe(
    takeUntil(this.destroy$)
  ).subscribe(([user, balance, settings]) => {
    this.user = user;
    this.balance = balance;
    this.settings = settings;
    this.updateUI();
  });
}
```

---

## State Reset on Logout

```typescript
// AuthService
logout(): void {
  // Clear all state
  this.walletService.clearState();
  this.profileService.clearState();
  this.filterStateService.clearFilterState();
  
  // Clear tokens
  sessionStorage.removeItem('access_token');
  sessionStorage.removeItem('refresh_token');
  
  // Update auth state
  this.currentUserSubject.next(null);
  this.isAuthenticatedSubject.next(false);
  
  // Navigate to login
  this.router.navigate(['/login']);
}
```

---

## Quick Reference

| Pattern | Use Case | Example |
|---------|----------|---------|
| `BehaviorSubject` | State that needs initial value | User, settings, balance |
| `Subject` | Events without initial value | destroy$, click events |
| `ReplaySubject(1)` | Late subscribers need last value | One-time data fetch |
| `AsyncSubject` | Only final value matters | Completion events |