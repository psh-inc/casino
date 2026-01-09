# Angular Lifecycle & RxJS Patterns

Angular doesn't have "hooks" like React, but lifecycle methods and RxJS operators serve similar purposes.

## Lifecycle Methods

### OnInit - Component Initialization

```typescript
// GOOD - Load data after component initialization
export class GamesPageComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  games$ = new BehaviorSubject<Game[]>([]);
  
  ngOnInit(): void {
    this.gameService.getGames().pipe(
      takeUntil(this.destroy$)
    ).subscribe(games => this.games$.next(games));
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### WARNING: Forgetting OnDestroy

**The Problem:**

```typescript
// BAD - Memory leak: subscription never cleaned up
export class BadComponent implements OnInit {
  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe(isAuth => {
      this.isLoggedIn = isAuth;
    });
  }
}
```

**Why This Breaks:**
1. Observable keeps reference to component after destruction
2. Callback continues executing on destroyed component
3. Memory accumulates with each navigation

**The Fix:**

```typescript
// GOOD - Always implement OnDestroy with takeUntil
export class GoodComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  
  ngOnInit(): void {
    this.authService.isAuthenticated$.pipe(
      takeUntil(this.destroy$)
    ).subscribe(isAuth => this.isLoggedIn = isAuth);
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## RxJS Operators as "Hooks"

### switchMap - Cancel Previous Requests

```typescript
// Search with cancellation of stale requests
searchGames(term$: Observable<string>): Observable<Game[]> {
  return term$.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.http.get<Game[]>(`/api/games?q=${term}`))
  );
}
```

### combineLatest - Multiple Dependencies

```typescript
// Combine multiple observables
ngOnInit(): void {
  combineLatest([
    this.authService.currentUser$,
    this.walletService.getBalance()
  ]).pipe(
    takeUntil(this.destroy$)
  ).subscribe(([user, balance]) => {
    this.user = user;
    this.balance = balance;
  });
}
```

### WARNING: Using subscribe Inside subscribe

**The Problem:**

```typescript
// BAD - Nested subscriptions (callback hell)
this.authService.currentUser$.subscribe(user => {
  this.walletService.getBalance(user.id).subscribe(balance => {
    this.balance = balance;
  });
});
```

**Why This Breaks:**
1. Inner subscription not cleaned up properly
2. Creates new subscription on each outer emission
3. Impossible to reason about timing

**The Fix:**

```typescript
// GOOD - Use switchMap or mergeMap
this.authService.currentUser$.pipe(
  switchMap(user => this.walletService.getBalance(user.id)),
  takeUntil(this.destroy$)
).subscribe(balance => this.balance = balance);
```

## Async Pipe Pattern

```typescript
// Component class - expose observable
games$ = this.gameService.getGames();

// Template - async pipe handles subscription
<div *ngFor="let game of games$ | async; trackBy: trackByGameId">
  {{ game.name }}
</div>
```

The async pipe automatically subscribes and unsubscribes, eliminating manual cleanup.