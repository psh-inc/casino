```markdown
# TypeScript Error Handling Reference

Error handling patterns for the casino platform's TypeScript code.

## Observable Error Handling

### Standard catchError Pattern

```typescript
login(username: string, password: string): Observable<LoginResponse> {
  return this.http.post<LoginResponse>(`${this.apiUrl}/login`, { username, password })
    .pipe(
      tap(response => {
        this.storeTokens(response.accessToken, response.refreshToken);
        this.isAuthenticatedSubject.next(true);
      }),
      catchError(error => {
        console.error('Login failed:', error);
        return throwError(() => error);
      })
    );
}
```

### Fallback Value Pattern

```typescript
checkNameExists(name: string): Observable<boolean> {
  return this.http.get<{ available: boolean }>(`${this.apiUrl}/check-name`, {
    params: { name }
  }).pipe(
    map(response => !response.available),
    catchError(() => of(false))  // Fallback to "doesn't exist"
  );
}

getAllItems(): Observable<Item[]> {
  return this.http.get<Page<Item>>(this.apiUrl).pipe(
    map(page => page.content),
    catchError(() => of([]))  // Empty array on error
  );
}
```

### WARNING: Silent catchError

**The Problem:**

```typescript
// BAD - Silently swallows errors
getData(): Observable<Data[]> {
  return this.http.get<Data[]>(url).pipe(
    catchError(() => of([]))  // No logging, no context
  );
}
```

**Why This Breaks:**
1. Errors are invisible - debugging is impossible
2. No metrics or monitoring for failures
3. Users see empty data without explanation

**The Fix:**

```typescript
// GOOD - Log before fallback
getData(): Observable<Data[]> {
  return this.http.get<Data[]>(url).pipe(
    catchError(error => {
      console.error('Failed to fetch data:', error);
      // Or: this.errorService.report(error);
      return of([]);
    })
  );
}
```

## Synchronous Error Handling

### Try-Catch for Parsing

```typescript
static decodeToken(token: string): JwtPayload | null {
  try {
    const cleanToken = token.replace('Bearer ', '');
    const parts = cleanToken.split('.');
    if (parts.length !== 3) {
      console.error('Invalid JWT format');
      return null;
    }
    const payload = parts[1];
    return JSON.parse(atob(payload));
  } catch (error) {
    console.error('Error decoding JWT:', error);
    return null;
  }
}
```

### WebSocket Message Handling

```typescript
private handleMessage(message: IMessage, type: string): void {
  try {
    const data = JSON.parse(message.body);
    this.processMessage(data, type);
  } catch (error) {
    console.error('Error handling WebSocket message:', error);
    // Don't rethrow - keep WebSocket connection alive
  }
}
```

### WARNING: Bare Try-Catch

**The Problem:**

```typescript
// BAD - Catches everything, including programming errors
try {
  const result = processData(input);
  return result.value;  // What if result is undefined?
} catch {
  return null;
}
```

**Why This Breaks:**
1. Hides bugs that should be fixed
2. `result.value` on undefined should crash, not silently fail
3. Makes debugging nearly impossible

**The Fix:**

```typescript
// GOOD - Catch specific expected errors
try {
  const result = JSON.parse(jsonString);
  return result;
} catch (error) {
  if (error instanceof SyntaxError) {
    console.error('Invalid JSON:', jsonString);
    return null;
  }
  throw error;  // Rethrow unexpected errors
}
```

## Type Guards for Safe Access

### Narrowing Unknown Types

```typescript
function isApiError(error: unknown): error is { message: string; code: string } {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    'code' in error
  );
}

// Usage
catchError((error: unknown) => {
  if (isApiError(error)) {
    this.showError(error.message);  // Type-safe access
  } else {
    this.showError('Unknown error occurred');
  }
  return throwError(() => error);
})
```

### Optional Chaining for Nested Access

```typescript
// GOOD - Safe property access
const firstName = response?.player?.firstName ?? 'Unknown';
const balance = wallet?.summary?.balance ?? 0;

// With methods
const playerId = this.authService.currentUser?.playerId;
```

## HTTP Error Interceptor Pattern

```typescript
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(
    private authService: AuthService,
    private notificationService: NotificationService
  ) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          this.authService.logout();
          return throwError(() => error);
        }

        if (error.status === 403) {
          this.notificationService.showError('Access denied');
        }

        if (error.status >= 500) {
          this.notificationService.showError('Server error. Please try again.');
        }

        return throwError(() => error);
      })
    );
  }
}
```

## Form Validation Errors

```typescript
interface ValidationError {
  field: string;
  message: string;
  code: string;
}

interface ApiErrorResponse {
  status: 'ERROR';
  code: string;
  message: string;
  details?: {
    fields: Record<string, string>;
  };
}

// Map API errors to form
handleValidationErrors(error: ApiErrorResponse, form: FormGroup): void {
  if (error.details?.fields) {
    Object.entries(error.details.fields).forEach(([field, message]) => {
      const control = form.get(field);
      if (control) {
        control.setErrors({ serverError: message });
      }
    });
  }
}
```

See the **angular** skill for form handling patterns.
```