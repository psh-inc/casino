```markdown
# TypeScript Patterns

## Idiomatic Patterns for Angular Casino Platform

### Pattern 1: String Literal Enums Matching Backend

```typescript
// GOOD - Matches Kotlin enum exactly
export enum TransactionType {
  DEPOSIT = 'DEPOSIT',
  WITHDRAWAL = 'WITHDRAWAL',
  GAME_BET = 'GAME_BET',
  GAME_WIN = 'GAME_WIN',
  BONUS_AWARD = 'BONUS_AWARD'
}
```

**Why:** The Spring Boot backend serializes enums as uppercase strings. Using matching string literal enums ensures type safety across the API boundary without runtime conversion.

### WARNING: Numeric Enums

**The Problem:**

```typescript
// BAD - Won't match backend JSON
export enum TransactionType {
  DEPOSIT,      // = 0
  WITHDRAWAL,   // = 1
  GAME_BET      // = 2
}
```

**Why This Breaks:**
1. Backend returns `"DEPOSIT"`, frontend expects `0`
2. API comparisons silently fail
3. Debugging becomes nightmare with mysterious mismatches

**The Fix:**

```typescript
// GOOD - String literal values
export enum TransactionType {
  DEPOSIT = 'DEPOSIT',
  WITHDRAWAL = 'WITHDRAWAL',
  GAME_BET = 'GAME_BET'
}
```

**When You Might Be Tempted:** When you want "simpler" enum syntax or are coming from C#/Java numeric enum habits.

---

### Pattern 2: Exhaustive Record Mappings

```typescript
// GOOD - Compile-time exhaustiveness
export const TRANSACTION_TYPE_LABELS: Record<TransactionType, string> = {
  [TransactionType.DEPOSIT]: 'Deposit',
  [TransactionType.WITHDRAWAL]: 'Withdrawal',
  [TransactionType.GAME_BET]: 'Bet',
  [TransactionType.GAME_WIN]: 'Win',
  [TransactionType.BONUS_AWARD]: 'Bonus'
};

// Usage in template
{{ TRANSACTION_TYPE_LABELS[transaction.type] }}
```

**Why:** Adding a new enum value forces you to update all `Record` mappings or get a compile error.

---

### Pattern 3: Observable Composition with Type Inference

```typescript
// GOOD - Types flow through operators
register(request: RegistrationRequest): Observable<RegistrationResponse> {
  return from(this.fingerprintService.generateFingerprint()).pipe(
    mergeMap(fingerprint => {
      const data = { ...request, fingerprint };
      return this.http.post<RegistrationResponse>(`${this.apiUrl}/signup`, data);
    }),
    tap(response => {
      this.storeTokens(response.accessToken, response.refreshToken);
      this.currentUserSubject.next({ playerId: response.playerId });
    }),
    catchError(error => throwError(() => error))
  );
}
```

---

### WARNING: Implicit Any in HTTP Responses

**The Problem:**

```typescript
// BAD - Response is `any`
getPlayers(): Observable<any> {
  return this.http.get(`${this.apiUrl}/players`);
}
```

**Why This Breaks:**
1. No autocomplete on response properties
2. Typos like `response.plalyer` won't be caught
3. Refactoring becomes dangerous without type safety

**The Fix:**

```typescript
// GOOD - Fully typed response
getPlayers(): Observable<Page<Player>> {
  return this.http.get<Page<Player>>(`${this.apiUrl}/players`);
}
```

---

### Pattern 4: Partial<T> for PATCH Operations

```typescript
// GOOD - Only send changed fields
patchPlayer(
  playerId: number,
  request: Partial<UpdatePlayerRequest>
): Observable<PlayerDetails> {
  return this.http.patch<PlayerDetails>(`${this.apiUrl}/${playerId}`, request);
}

// Usage
this.playersService.patchPlayer(123, { status: PlayerStatus.ACTIVE });
```

---

### Pattern 5: Literal Union Types for Component Props

```typescript
@Component({...})
export class GameGridComponent {
  @Input() view: 'grid' | 'list' = 'grid';
  @Input() sortBy: 'name' | 'popularity' | 'rtp' = 'popularity';
}
```

**Why:** Provides intellisense and catches invalid values at compile time rather than runtime.

---

### Pattern 6: Const Assertions for Readonly Data

```typescript
// GOOD - Immutable lookup table
export const VOLATILITY_CONFIG = {
  LOW: { color: '#4CAF50', label: 'Low Risk' },
  MEDIUM: { color: '#FF9800', label: 'Medium Risk' },
  HIGH: { color: '#F44336', label: 'High Risk' }
} as const;

type Volatility = keyof typeof VOLATILITY_CONFIG;
```

---

## Error Handling Conventions

See the **angular** skill for service-level error handling patterns with RxJS operators.
```