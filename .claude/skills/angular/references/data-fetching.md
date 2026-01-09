# Data Fetching Patterns

This project uses Angular HttpClient with RxJS operators. No external data-fetching library like TanStack Query is used.

## Standard Service Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class GameService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/api/v1`;

  getGames(page = 0, size = 20): Observable<Page<Game>> {
    const params = new HttpParams()
      .set('page', page)
      .set('size', size);
    return this.http.get<Page<Game>>(`${this.apiUrl}/games`, { params });
  }

  getGameById(id: string): Observable<Game> {
    return this.http.get<Game>(`${this.apiUrl}/games/${id}`);
  }

  createGame(request: CreateGameRequest): Observable<Game> {
    return this.http.post<Game>(`${this.apiUrl}/games`, request);
  }
}
```

## Error Handling Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class WalletService {
  private snackBar = inject(MatSnackBar);
  private authService = inject(AuthService);

  deposit(amount: string): Observable<DepositResponse> {
    return this.http.post<DepositResponse>(`${this.apiUrl}/deposits`, { amount }).pipe(
      tap(response => {
        if (response.success) {
          this.snackBar.open('Deposit successful!', 'Close', { duration: 3000 });
        }
      }),
      catchError(error => this.handleError(error))
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let message = 'An error occurred';
    
    switch (error.status) {
      case 400:
        message = error.error?.message || 'Invalid request';
        break;
      case 401:
        this.authService.logout();
        message = 'Session expired';
        break;
      case 403:
        message = 'Access denied';
        break;
      case 404:
        message = 'Resource not found';
        break;
      default:
        message = error.error?.message || 'Server error';
    }
    
    this.snackBar.open(message, 'Close', { duration: 5000 });
    return throwError(() => new Error(message));
  }
}
```

## WARNING: No Loading/Error State Management

**The Problem:**

```typescript
// BAD - No loading indicator, no error handling
export class GamesComponent implements OnInit {
  games: Game[] = [];
  
  ngOnInit(): void {
    this.gameService.getGames().subscribe(games => {
      this.games = games;
    });
  }
}
```

**Why This Breaks:**
1. User sees nothing while loading
2. Errors silently fail
3. No way to retry failed requests

**The Fix:**

```typescript
// GOOD - Proper loading and error states
export class GamesComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  
  games: Game[] = [];
  loading = true;
  error: string | null = null;

  ngOnInit(): void {
    this.loadGames();
  }

  loadGames(): void {
    this.loading = true;
    this.error = null;
    
    this.gameService.getGames().pipe(
      takeUntil(this.destroy$),
      finalize(() => this.loading = false)
    ).subscribe({
      next: games => this.games = games,
      error: err => this.error = err.message
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Caching with BehaviorSubject

```typescript
@Injectable({ providedIn: 'root' })
export class PlayerService {
  private http = inject(HttpClient);
  private cache$ = new BehaviorSubject<Player | null>(null);
  private cacheTime = 0;
  private CACHE_DURATION = 30000; // 30 seconds

  getPlayer(id: number): Observable<Player> {
    const now = Date.now();
    
    if (this.cache$.value && (now - this.cacheTime) < this.CACHE_DURATION) {
      return of(this.cache$.value);
    }
    
    return this.http.get<Player>(`/api/v1/players/${id}`).pipe(
      tap(player => {
        this.cache$.next(player);
        this.cacheTime = now;
      })
    );
  }

  invalidateCache(): void {
    this.cache$.next(null);
    this.cacheTime = 0;
  }
}
```

## Auto-Refresh Pattern

```typescript
// From WalletService - refresh balance every 30 seconds
private balanceRefreshTimer$ = timer(0, 30000);

private startBalanceRefresh(playerId: number): void {
  this.balanceRefreshTimer$.pipe(
    takeUntil(this.destroy$),
    switchMap(() => this.fetchPlayerBalance(playerId)),
    catchError(error => {
      console.error('Balance refresh failed:', error);
      return of(null);
    })
  ).subscribe(balance => {
    if (balance) this.balance$.next(balance);
  });
}
```

See the **spring-boot** skill for backend API endpoint patterns.