```markdown
# TypeScript Types

## Type Definition Patterns

### Interface vs Type Alias

```typescript
// GOOD - Use interfaces for object shapes
export interface Player {
  id: number;
  username: string;
  status: PlayerStatus;
  createdAt: string;
}

// GOOD - Use type for unions, intersections, computed types
export type PlayerStatus = 'ACTIVE' | 'PENDING' | 'BLOCKED';
export type PlayerWithWallet = Player & { wallet: Wallet };
```

**When to use which:**
- `interface`: Objects, DTOs, API responses (can be extended)
- `type`: Unions, mapped types, complex compositions

---

### Generic Page Response Pattern

```typescript
// Reusable pagination interface
export interface Page<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  size: number;
  number: number;
  first: boolean;
  last: boolean;
}

// Usage
getPlayers(): Observable<Page<Player>> { ... }
getTransactions(): Observable<Page<Transaction>> { ... }
```

---

### WARNING: Using `any` for API Responses

**The Problem:**

```typescript
// BAD - Defeats TypeScript's purpose
interface ApiResponse {
  data: any;
  meta: any;
}
```

**Why This Breaks:**
1. No compile-time validation of property access
2. Runtime errors surface only in production
3. Impossible to refactor safely

**The Fix:**

```typescript
// GOOD - Specific types
interface ApiResponse<T> {
  data: T;
  meta: PaginationMeta;
}

interface PaginationMeta {
  page: number;
  size: number;
  totalElements: number;
}
```

---

### Discriminated Unions for State

```typescript
// GOOD - Type-safe state handling
type LoadingState<T> = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

// Type guard
function isSuccess<T>(state: LoadingState<T>): state is { status: 'success'; data: T } {
  return state.status === 'success';
}
```

---

### Optional Fields for Backward Compatibility

```typescript
export interface CampaignListItem {
  currencyCode?: string;      // Legacy: single currency
  currencyCodes?: string[];   // New: multiple currencies
  
  // Computed helper
  getCurrencies(): string[] {
    return this.currencyCodes ?? (this.currencyCode ? [this.currencyCode] : []);
  }
}
```

**Why:** APIs evolve. Optional fields with fallbacks prevent breaking changes.

---

### WARNING: Stringly-Typed Code

**The Problem:**

```typescript
// BAD - Magic strings everywhere
function getStatusColor(status: string): string {
  if (status === 'active') return 'green';
  if (status === 'pending') return 'yellow';
  return 'gray';
}
```

**Why This Breaks:**
1. No autocomplete for valid values
2. Typos like `'activ'` fail silently
3. Backend changes require manual hunting

**The Fix:**

```typescript
// GOOD - Type-safe enum
export enum PlayerStatus {
  ACTIVE = 'ACTIVE',
  PENDING = 'PENDING'
}

function getStatusColor(status: PlayerStatus): string {
  switch (status) {
    case PlayerStatus.ACTIVE: return 'green';
    case PlayerStatus.PENDING: return 'yellow';
  }
}
```

---

### Utility Types for API Operations

```typescript
// Pick specific fields for create
type CreatePlayerRequest = Pick<Player, 'username' | 'email' | 'password'>;

// Omit server-generated fields
type UpdatePlayerRequest = Omit<Player, 'id' | 'createdAt'>;

// Make all fields optional for patch
type PatchPlayerRequest = Partial<UpdatePlayerRequest>;
```

---

### Index Signatures with Constraints

```typescript
// GOOD - Exhaustive enum mapping
export const STATUS_COLORS: { [K in PlayerStatus]: string } = {
  [PlayerStatus.ACTIVE]: '#4CAF50',
  [PlayerStatus.PENDING]: '#FF9800',
  [PlayerStatus.BLOCKED]: '#F44336'
  // Compile error if any status is missing
};
```

---

### Complex Event Types (WebSocket)

```typescript
export interface BalanceUpdateEvent {
  playerId: number;
  previousBalance: string;  // String for precision
  newBalance: string;
  currency: string;
  changeType: BalanceChangeType;
  timestamp: string;
}

export enum BalanceChangeType {
  DEPOSIT = 'DEPOSIT',
  GAME_BET = 'GAME_BET',
  GAME_WIN = 'GAME_WIN',
  BONUS_AWARD = 'BONUS_AWARD'
}
```

See the **kotlin** skill for backend event class alignment.
```