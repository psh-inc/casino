```markdown
# TypeScript Patterns

Idiomatic TypeScript patterns used throughout the casino platform's Angular frontends.

## Observable-Based Service Pattern

The standard pattern for services that communicate with the backend:

```typescript
@Injectable({ providedIn: 'root' })
export class BonusService {
  private apiUrl = `${environment.apiUrl}/v1/admin/bonuses`;

  constructor(private http: HttpClient) {}

  getBonuses(page = 0, size = 20, status?: BonusStatus): Observable<Page<BonusResponse>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('size', size.toString());

    if (status) {
      params = params.set('status', status);
    }

    return this.http.get<Page<any>>(this.apiUrl, { params }).pipe(
      map(response => ({
        ...response,
        content: response.content.map(this.mapToFrontend)
      }))
    );
  }
}
```

## State Management with BehaviorSubject

```typescript
// GOOD - Typed BehaviorSubject with public Observable
private currentUserSubject = new BehaviorSubject<User | null>(null);
public currentUser$ = this.currentUserSubject.asObservable();
public isAuthenticated$ = this.currentUserSubject.pipe(map(u => u !== null));

// Access synchronously when needed
public get currentUserValue(): User | null {
  return this.currentUserSubject.value;
}
```

### WARNING: Exposing BehaviorSubject Directly

**The Problem:**

```typescript
// BAD - Exposes mutable subject
public currentUser = new BehaviorSubject<User | null>(null);
```

**Why This Breaks:**
1. Any consumer can call `.next()` and corrupt state
2. Violates single-source-of-truth principle
3. Makes debugging state changes nearly impossible

**The Fix:**

```typescript
// GOOD - Private subject, public observable
private currentUserSubject = new BehaviorSubject<User | null>(null);
public currentUser$ = this.currentUserSubject.asObservable();
```

## Dependency Injection with inject()

Angular 17+ pattern using `inject()` function:

```typescript
@Injectable({ providedIn: 'root' })
export class AuthService implements OnDestroy {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly fingerprintService = inject(FingerprintService);
  private readonly localeId = inject(LOCALE_ID);

  private destroy$ = new Subject<void>();

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Static Utility Classes

Pattern for stateless utility functions:

```typescript
export class JwtUtils {
  static decodeToken(token: string): JwtPayload | null {
    try {
      const parts = token.replace('Bearer ', '').split('.');
      if (parts.length !== 3) return null;
      return JSON.parse(atob(parts[1]));
    } catch {
      return null;
    }
  }

  static isTokenExpired(token: string): boolean {
    const payload = this.decodeToken(token);
    if (!payload?.exp) return true;
    return Date.now() >= payload.exp * 1000;
  }
}
```

### WARNING: Instance Methods for Stateless Operations

**The Problem:**

```typescript
// BAD - Requires instantiation for stateless operations
class JwtHelper {
  decodeToken(token: string): JwtPayload | null { ... }
}
const helper = new JwtHelper(); // Unnecessary object
```

**Why This Breaks:**
1. Creates unnecessary objects
2. Implies state that doesn't exist
3. Harder to use in static contexts

**The Fix:**

```typescript
// GOOD - Static methods for stateless utilities
export class JwtUtils {
  static decodeToken(token: string): JwtPayload | null { ... }
}
// Usage: JwtUtils.decodeToken(token)
```

## Cleanup with takeUntil

**When:** Managing RxJS subscriptions in components/services

```typescript
@Component({ ... })
export class PlayerListComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.playerService.getPlayers().pipe(
      takeUntil(this.destroy$)
    ).subscribe(players => this.players = players);

    interval(60000).pipe(
      takeUntil(this.destroy$)
    ).subscribe(() => this.refresh());
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

See the **angular** skill for more RxJS patterns.
```