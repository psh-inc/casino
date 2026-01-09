```markdown
# TypeScript Error Handling

## HTTP Error Handling Patterns

### Typed Error Handling with catchError

```typescript
initiateWithdrawal(request: WithdrawalRequest): Observable<WithdrawalResponse> {
  return this.http.post<WithdrawalResponse>(`${this.apiUrl}/withdrawals`, request).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 400 && error.error?.message?.includes('KYC verification required')) {
        this.handleKycRequired(error.error.message);
        return EMPTY;
      }
      if (error.status === 422) {
        return throwError(() => new ValidationError(error.error.details));
      }
      return throwError(() => error);
    })
  );
}
```

---

### WARNING: Silent Error Swallowing

**The Problem:**

```typescript
// BAD - Error disappears
getPlayers(): Observable<Player[]> {
  return this.http.get<Player[]>(this.apiUrl).pipe(
    catchError(error => {
      console.log(error);  // Only logs, no handling
      return of([]);       // Returns empty, user sees nothing
    })
  );
}
```

**Why This Breaks:**
1. User has no idea something failed
2. Empty data looks like "no results" not "error"
3. Debugging production issues becomes impossible

**The Fix:**

```typescript
// GOOD - Proper error handling
getPlayers(): Observable<Player[]> {
  return this.http.get<Player[]>(this.apiUrl).pipe(
    catchError((error: HttpErrorResponse) => {
      console.error('Failed to fetch players:', error);
      this.snackBar.open('Failed to load players. Please try again.', 'Dismiss');
      return throwError(() => error);  // Propagate for component handling
    })
  );
}
```

---

### Graceful Degradation Pattern

```typescript
// GOOD - Return defaults on non-critical failures
getSignupConfiguration(): Observable<SignupConfiguration> {
  return this.http.get<SignupConfiguration>(`${this.apiUrl}/signup-config`).pipe(
    catchError(error => {
      console.error('Failed to load signup configuration:', error);
      return of(this.getDefaultConfiguration());  // Fallback config
    })
  );
}

private getDefaultConfiguration(): SignupConfiguration {
  return {
    fields: [{ key: 'email', required: true, type: 'EMAIL' }],
    termsRequired: true
  };
}
```

---

### WARNING: Using `any` in Error Handlers

**The Problem:**

```typescript
// BAD - Losing type information
catchError((error: any) => {
  if (error.response.data.code === 'INVALID_TOKEN') { ... }
})
```

**Why This Breaks:**
1. No autocomplete for error properties
2. Typos in property names aren't caught
3. API changes break silently

**The Fix:**

```typescript
// GOOD - Typed error response
interface ApiError {
  status: string;
  code: string;
  message: string;
  timestamp: string;
  details?: { fields: Record<string, string> };
}

catchError((error: HttpErrorResponse) => {
  const apiError = error.error as ApiError;
  if (apiError.code === 'INVALID_TOKEN') { ... }
})
```

---

### Custom Error Classes

```typescript
export class ValidationError extends Error {
  constructor(public readonly fields: Record<string, string>) {
    super('Validation failed');
    this.name = 'ValidationError';
  }
}

export class AuthenticationError extends Error {
  constructor(message = 'Authentication required') {
    super(message);
    this.name = 'AuthenticationError';
  }
}

// Usage
catchError((error: HttpErrorResponse) => {
  if (error.status === 401) {
    return throwError(() => new AuthenticationError());
  }
  if (error.status === 422) {
    return throwError(() => new ValidationError(error.error.details.fields));
  }
  return throwError(() => error);
})
```

---

### Component Error State Pattern

```typescript
export class PlayerListComponent {
  players$ = new BehaviorSubject<Player[]>([]);
  error$ = new BehaviorSubject<string | null>(null);
  loading$ = new BehaviorSubject<boolean>(false);

  loadPlayers(): void {
    this.loading$.next(true);
    this.error$.next(null);
    
    this.playersService.getPlayers().pipe(
      finalize(() => this.loading$.next(false))
    ).subscribe({
      next: players => this.players$.next(players),
      error: (err: HttpErrorResponse) => {
        this.error$.next(this.getErrorMessage(err));
      }
    });
  }

  private getErrorMessage(error: HttpErrorResponse): string {
    if (error.status === 0) return 'Network error. Check your connection.';
    if (error.status === 403) return 'You do not have permission to view this.';
    if (error.status === 500) return 'Server error. Please try again later.';
    return error.error?.message ?? 'An unexpected error occurred.';
  }
}
```

---

### WARNING: Ignoring Promise Rejections

**The Problem:**

```typescript
// BAD - Unhandled promise rejection
async ngOnInit() {
  const data = await this.service.fetchData();  // No try/catch
}
```

**Why This Breaks:**
1. Unhandled promise rejections crash in strict mode
2. App state becomes undefined
3. User sees blank screen with no feedback

**The Fix:**

```typescript
// GOOD - Proper async/await error handling
async ngOnInit() {
  try {
    const data = await firstValueFrom(this.service.fetchData());
    this.data = data;
  } catch (error) {
    console.error('Failed to fetch data:', error);
    this.error = 'Failed to load data';
  }
}
```

---

### RxJS Error Recovery

```typescript
// Retry with exponential backoff
getData(): Observable<Data> {
  return this.http.get<Data>(this.apiUrl).pipe(
    retry({
      count: 3,
      delay: (error, retryCount) => timer(Math.pow(2, retryCount) * 1000)
    }),
    catchError(error => {
      console.error('All retries failed:', error);
      return throwError(() => error);
    })
  );
}
```

See the **angular** skill for interceptor-based global error handling.
```