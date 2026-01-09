```markdown
# TypeScript Types Reference

Type patterns and best practices for the casino platform.

## String Enums

Always use string-valued enums for API compatibility:

```typescript
// GOOD - String values for backend compatibility
export enum BonusType {
  DEPOSIT = 'DEPOSIT',
  NTH_DEPOSIT = 'NTH_DEPOSIT',
  NO_DEPOSIT = 'NO_DEPOSIT'
}

export enum GameStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  MAINTENANCE = 'MAINTENANCE'
}
```

### WARNING: Numeric Enums

**The Problem:**

```typescript
// BAD - Numeric values cause issues
enum BonusType {
  DEPOSIT,      // 0
  NTH_DEPOSIT,  // 1
  NO_DEPOSIT    // 2
}
```

**Why This Breaks:**
1. Backend expects string values like `"DEPOSIT"`
2. JSON serializes to numbers, not strings
3. Debugging is harder - seeing `1` vs `"NTH_DEPOSIT"`

**The Fix:**

```typescript
// GOOD - Always use string values
export enum BonusType {
  DEPOSIT = 'DEPOSIT',
  NTH_DEPOSIT = 'NTH_DEPOSIT',
  NO_DEPOSIT = 'NO_DEPOSIT'
}
```

## Interface Definitions

### Basic Interface Pattern

```typescript
export interface Player {
  id: number;
  username: string;
  email: string;
  status: PlayerStatus;
  createdAt: string;             // ISO date string from backend
  lastLoginAt?: string;          // Optional fields use ?
  country?: string;
}
```

### Interface with Nested Objects

```typescript
export interface WalletSummary {
  balance: number;
  currency: string;
  bonusBalance: number;
  wageringRequirement?: {
    type: 'BONUS' | 'DEPOSIT';   // Inline union type
    totalRequired: number;
    totalWagered: number;
    progressPercentage: number;
  };
}
```

## Generic Interfaces

### Pagination Pattern

```typescript
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
```

### API Response Wrapper

```typescript
export interface ApiResponse<T> {
  data: T;
  status: 'SUCCESS' | 'ERROR';
  message?: string;
  timestamp: string;
}
```

## Mapped Types for Labels

Create display mappings from enums:

```typescript
export const GAME_TYPE_LABELS: Record<GameType, string> = {
  [GameType.SLOTS]: 'Slots',
  [GameType.TABLE_GAMES]: 'Table Games',
  [GameType.LIVE_CASINO]: 'Live Casino',
  [GameType.VIDEO_POKER]: 'Video Poker'
};

// Usage in template: {{ GAME_TYPE_LABELS[game.type] }}
```

### With Styling Information

```typescript
export const TRANSACTION_TYPE_STYLES: Record<TransactionType, { icon: string; class: string }> = {
  [TransactionType.DEPOSIT]: { icon: 'add_circle', class: 'success' },
  [TransactionType.WITHDRAWAL]: { icon: 'remove_circle', class: 'warning' },
  [TransactionType.GAME_BET]: { icon: 'casino', class: 'info' }
};
```

### WARNING: Using `any` for Display Mappings

**The Problem:**

```typescript
// BAD - No type safety
const labels: { [key: string]: string } = {
  SLOTS: 'Slots',
  TABLE: 'Table Games'
};
// Missing keys won't cause compile errors
```

**Why This Breaks:**
1. No compile-time check for missing enum values
2. Adding new enum value won't require updating map
3. Typos in keys go undetected

**The Fix:**

```typescript
// GOOD - Record<Enum, T> enforces all keys present
const labels: Record<GameType, string> = {
  [GameType.SLOTS]: 'Slots',
  // Compile error if any GameType is missing
};
```

## Union Types vs Enums

Use union types for small, inline sets:

```typescript
// Good for simple, limited options
type: 'BONUS' | 'DEPOSIT';
status: 'pending' | 'completed' | 'failed';

// Use enum when shared across files or has many values
export enum TransactionType {
  DEPOSIT = 'DEPOSIT',
  WITHDRAWAL = 'WITHDRAWAL',
  GAME_BET = 'GAME_BET',
  // ... 15 more values
}
```

## Index Signatures

For dynamic keys like currency-to-amount mappings:

```typescript
export interface DepositLimits {
  [currency: string]: {
    min: number;
    max: number;
  };
}

// Usage
const limits: DepositLimits = {
  EUR: { min: 10, max: 5000 },
  USD: { min: 10, max: 5000 }
};
```

See the **jpa** skill for corresponding Kotlin types.
```