# Angular Data Fetching Patterns

## HTTP Service Pattern

All API calls go through typed services with proper error handling.

### Basic Service Structure

```typescript
@Injectable({ providedIn: 'root' })
export class PlayerService {
  private apiUrl = `${environment.apiUrl}/api/v1/players`;

  constructor(private http: HttpClient) {}

  list(page = 0, size = 20): Observable<Page<Player>> {
    const params = new HttpParams()
      .set('page', page)
      .set('size', size);
    return this.http.get<Page<Player>>(this.apiUrl, { params });
  }

  getById(id: number): Observable<Player> {
    return this.http.get<Player>(`${this.apiUrl}/${id}`);
  }

  create(request: CreatePlayerRequest): Observable<Player> {
    return this.http.post<Player>(this.apiUrl, request).pipe(
      catchError(error => {
        console.error('Create player failed:', error);
        return throwError(() => error);
      })
    );
  }

  update(id: number, request: UpdatePlayerRequest): Observable<Player> {
    return this.http.put<Player>(`${this.apiUrl}/${id}`, request);
  }
}
```

### Service with Caching (WalletV2Service Pattern)

```typescript
@Injectable({ providedIn: 'root' })
export class WalletV2Service implements OnDestroy {
  private playerBalance$ = new BehaviorSubject<PlayerBalanceDto | null>(null);
  private balanceRefreshTimer$ = timer(0, 30000);  // Auto-refresh every 30s
  private destroy$ = new Subject<void>();

  getPlayerBalance(): Observable<PlayerBalanceDto | null> {
    return this.playerBalance$.asObservable();
  }

  startBalanceRefresh(playerId: number): void {
    this.balanceRefreshTimer$.pipe(
      takeUntil(this.destroy$),
      switchMap(() => this.fetchPlayerBalance(playerId)),
      catchError(error => {
        console.error('Balance fetch error:', error);
        return of(null);
      })
    ).subscribe(balance => {
      if (balance) this.playerBalance$.next(balance);
    });
  }

  private fetchPlayerBalance(playerId: number): Observable<PlayerBalanceDto> {
    return this.http.get<PlayerBalanceDto>(`${this.apiUrl}/${playerId}/balance`);
  }

  clearCache(): void {
    this.playerBalance$.next(null);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

---

## WARNING: Subscribing Without Unsubscribing

**The Problem:**

```typescript
// BAD - Memory leak
ngOnInit(): void {
  this.playerService.list().subscribe(players => {
    this.players = players;
  });
}
```

**Why This Breaks:**
1. HTTP observables complete, but the subscription object persists
2. If this pattern is used with ongoing streams (WebSocket, timers), memory leaks occur
3. Callbacks may execute after component destruction

**The Fix:**

```typescript
// GOOD - With takeUntil
private destroy$ = new Subject<void>();

ngOnInit(): void {
  this.playerService.list().pipe(
    takeUntil(this.destroy$)
  ).subscribe(players => this.players = players);
}

ngOnDestroy(): void {
  this.destroy$.next();
  this.destroy$.complete();
}

// ALTERNATIVE - Use async pipe (preferred for simple cases)
players$ = this.playerService.list();
```

```html
<div *ngFor="let player of players$ | async">{{ player.name }}</div>
```

---

## WARNING: N+1 API Calls

**The Problem:**

```typescript
// BAD - One call per item
async loadPlayersWithWallets(): Promise<void> {
  const players = await firstValueFrom(this.playerService.list());
  for (const player of players) {
    player.wallet = await firstValueFrom(this.walletService.getByPlayerId(player.id));
  }
}
```

**Why This Breaks:**
1. 100 players = 101 API calls
2. Slow loading, poor UX
3. Server overload, rate limiting

**The Fix:**

```typescript
// GOOD - Backend returns combined data or use batch endpoint
this.playerService.listWithWallets().subscribe(players => {
  this.players = players;  // Wallet data included
});

// Or use forkJoin for parallel calls
const playerIds = [1, 2, 3];
forkJoin(playerIds.map(id => this.walletService.getByPlayerId(id))).subscribe(wallets => {
  // All wallets loaded in parallel
});
```

See the **spring-boot** skill for backend pagination patterns.

---

## RxJS Operators for Data Fetching

### switchMap for Dependent Calls

```typescript
// When playerId changes, cancel previous request and start new one
this.playerId$.pipe(
  switchMap(playerId => this.playerService.getById(playerId)),
  takeUntil(this.destroy$)
).subscribe(player => this.player = player);
```

### mergeMap for Parallel Operations

```typescript
// AuthService - generate fingerprint then login
login(request: LoginRequest): Observable<LoginResponse> {
  return from(this.fingerprintService.generateFingerprint()).pipe(
    mergeMap(fingerprint => {
      const loginData = { ...request, fingerprint };
      return this.http.post<LoginResponse>(`${this.authUrl}/login`, loginData);
    }),
    tap(response => this.handleLoginSuccess(response)),
    catchError(error => {
      console.error('Login error:', error);
      return throwError(() => error);
    })
  );
}
```

### finalize for Loading States

```typescript
loadGames(): void {
  this.isLoading = true;
  this.gameService.getGames(this.filters, this.pageSize, this.offset).pipe(
    takeUntil(this.destroy$),
    finalize(() => this.isLoading = false)  // Always runs, even on error
  ).subscribe({
    next: (response) => this.games = response.games,
    error: (error) => this.toast.error('Failed to load games')
  });
}
```

---

## Error Handling in Interceptors

```typescript
export const errorInterceptor: HttpInterceptorFn = (
  req: HttpRequest<any>,
  next: HttpHandlerFn
): Observable<HttpEvent<any>> => {
  const router = inject(Router);
  const authService = inject(AuthService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      switch (error.status) {
        case 401:
          if (!req.url.includes('/auth/login')) {
            authService.logout();
          }
          break;
        case 403:
          console.error('Access forbidden');
          break;
        case 500:
          console.error('Server error');
          break;
      }
      return throwError(() => error);
    })
  );
};
```

---

## Pagination Pattern

```typescript
loadData(): void {
  this.loading = true;
  this.service.list(this.pageIndex, this.pageSize).pipe(
    takeUntil(this.destroy$),
    finalize(() => this.loading = false)
  ).subscribe({
    next: (page) => {
      this.items = page.content;
      this.totalElements = page.totalElements;
    },
    error: (error) => console.error('Load failed:', error)
  });
}

onPageChange(event: { pageIndex: number; pageSize: number }): void {
  this.pageIndex = event.pageIndex;
  this.pageSize = event.pageSize;
  this.loadData();
}
```