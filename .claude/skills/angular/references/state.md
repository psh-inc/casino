# State Management Patterns

This project uses BehaviorSubject-based services for state management instead of NgRx/Akita.

## State Service Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class AuthService implements OnDestroy {
  // Private mutable state
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  private destroy$ = new Subject<void>();

  // Public read-only observables
  public currentUser$ = this.currentUserSubject.asObservable();
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  // State mutations through methods
  login(request: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>('/api/auth/login', request).pipe(
      tap(response => {
        this.storeTokens(response.token, response.refreshToken);
        this.currentUserSubject.next(this.parseUserFromToken(response.token));
        this.isAuthenticatedSubject.next(true);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
    this.router.navigate(['/']);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.currentUserSubject.complete();
    this.isAuthenticatedSubject.complete();
  }
}
```

## WARNING: Direct Subject Exposure

**The Problem:**

```typescript
// BAD - Exposing BehaviorSubject directly
@Injectable({ providedIn: 'root' })
export class BadService {
  public user$ = new BehaviorSubject<User | null>(null);
}

// Any component can now do:
this.badService.user$.next(hackedUser); // Breaks encapsulation!
```

**Why This Breaks:**
1. Any component can mutate state directly
2. No single source of truth
3. Impossible to debug state changes

**The Fix:**

```typescript
// GOOD - Private subject, public observable
@Injectable({ providedIn: 'root' })
export class GoodService {
  private userSubject = new BehaviorSubject<User | null>(null);
  public user$ = this.userSubject.asObservable(); // Read-only

  updateUser(user: User): void {
    // Controlled state mutation
    this.userSubject.next(user);
  }
}
```

## Multi-Value State Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class WalletService implements OnDestroy {
  private destroy$ = new Subject<void>();
  
  // Multiple related state values
  private playerId$ = new BehaviorSubject<number | null>(null);
  private balance$ = new BehaviorSubject<PlayerBalance | null>(null);
  private transactions$ = new BehaviorSubject<Transaction[]>([]);
  
  // Event stream (not state - use Subject, not BehaviorSubject)
  private balanceUpdate$ = new Subject<BalanceUpdateEvent>();

  // Combined state for convenience
  getWalletState(): Observable<WalletState> {
    return combineLatest([
      this.playerId$,
      this.balance$,
      this.transactions$
    ]).pipe(
      map(([playerId, balance, transactions]) => ({
        playerId,
        balance,
        transactions,
        isLoaded: balance !== null
      }))
    );
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    // Complete all subjects
    this.playerId$.complete();
    this.balance$.complete();
    this.transactions$.complete();
    this.balanceUpdate$.complete();
  }
}
```

## Derived State Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class GameSessionService {
  private activeSession$ = new BehaviorSubject<GameSession | null>(null);
  
  // Derived state using pipe operators
  hasActiveSession$ = this.activeSession$.pipe(
    map(session => session !== null)
  );
  
  sessionBalance$ = this.activeSession$.pipe(
    map(session => session?.balance ?? 0)
  );
  
  // Computed from multiple sources
  canPlaceBet$ = combineLatest([
    this.activeSession$,
    this.walletService.getBalance()
  ]).pipe(
    map(([session, wallet]) => 
      session !== null && 
      wallet !== null && 
      wallet.realBalance > 0
    )
  );
}
```

## WebSocket State Updates

```typescript
// Real-time state updates from WebSocket
@Injectable({ providedIn: 'root' })
export class RealtimeService implements OnDestroy {
  private destroy$ = new Subject<void>();
  
  constructor(
    private wsService: WebSocketService,
    private walletService: WalletService
  ) {
    this.subscribeToUpdates();
  }

  private subscribeToUpdates(): void {
    this.wsService.getBalanceUpdates().pipe(
      takeUntil(this.destroy$)
    ).subscribe(update => {
      // Update local state from WebSocket event
      this.walletService.updateBalance(update.newBalance);
    });
  }
}
```