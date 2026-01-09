```markdown
# TypeScript Modules Reference

Module organization and import patterns for the casino platform.

## Path Aliases

Both frontends use path aliases for cleaner imports:

### Admin Frontend (`casino-f/tsconfig.json`)

```json
{
  "compilerOptions": {
    "paths": {
      "@core/*": ["src/app/core/*"],
      "@shared/*": ["src/app/shared/*"],
      "@auth/*": ["src/app/auth/*"],
      "@modules/*": ["src/app/modules/*"],
      "@environments/*": ["src/environments/*"]
    }
  }
}
```

### Customer Frontend (`casino-customer-f/tsconfig.json`)

```json
{
  "compilerOptions": {
    "paths": {
      "@app/*": ["src/app/*"],
      "@core/*": ["src/app/core/*"],
      "@shared/*": ["src/app/shared/*"],
      "@environments/*": ["src/environments/*"]
    }
  }
}
```

## Import Patterns

### Using Path Aliases

```typescript
// GOOD - Clean imports with aliases
import { AuthService } from '@core/services/auth.service';
import { Player, PlayerStatus } from '@modules/player-management/player.model';
import { environment } from '@environments/environment';
```

### WARNING: Relative Path Overuse

**The Problem:**

```typescript
// BAD - Deep relative paths
import { AuthService } from '../../../core/services/auth.service';
import { Player } from '../../../../modules/player/player.model';
```

**Why This Breaks:**
1. Hard to read and understand location
2. Moving files breaks all imports
3. Easy to get wrong number of `../`

**The Fix:**

```typescript
// GOOD - Path aliases
import { AuthService } from '@core/services/auth.service';
import { Player } from '@modules/player-management/player.model';
```

## Barrel Files (Index Exports)

The shared library uses barrel files for organized exports:

### `casino-shared/src/index.ts`

```typescript
// Export all models
export * from './models/balance.models';
export * from './models/game.models';

// Export utilities
export * from './utils/jwt.utils';

// Export constants
export * from './constants/api.constants';

// Optional: namespace exports
import * as BalanceModels from './models/balance.models';
import * as JwtUtils from './utils/jwt.utils';

export default {
  BalanceModels,
  JwtUtils
};
```

### Consuming Barrel Files

```typescript
// Named imports (preferred)
import { WalletSummary, TransactionType } from '@casino/shared';

// Namespace import
import * as BalanceModels from '@casino/shared';
const summary: BalanceModels.WalletSummary = { ... };
```

### WARNING: Circular Barrel Imports

**The Problem:**

```typescript
// models/index.ts
export * from './player.model';
export * from './wallet.model';  // wallet imports from player

// wallet.model.ts
import { Player } from './index';  // BAD - circular through barrel
```

**Why This Breaks:**
1. Can cause undefined imports at runtime
2. TypeScript may not catch the issue
3. Order-dependent behavior

**The Fix:**

```typescript
// wallet.model.ts
import { Player } from './player.model';  // Direct import
```

## Strict Mode Configuration

### Shared Library (Strictest)

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "declaration": true
  }
}
```

### Customer Frontend (Production)

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

### Admin Frontend (Development Flexibility)

```json
{
  "compilerOptions": {
    "strict": false,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Feature Module Organization

```
modules/
├── player-management/
│   ├── player.model.ts          # Interfaces and enums
│   ├── player.service.ts        # HTTP service
│   ├── components/
│   │   ├── player-list/
│   │   └── player-detail/
│   └── player-management.module.ts
```

### Model File Structure

```typescript
// player.model.ts

// Enums first
export enum PlayerStatus {
  ACTIVE = 'ACTIVE',
  BLOCKED = 'BLOCKED'
}

// Interfaces next
export interface Player {
  id: number;
  status: PlayerStatus;
}

// Constants last
export const PLAYER_STATUS_LABELS: Record<PlayerStatus, string> = {
  [PlayerStatus.ACTIVE]: 'Active',
  [PlayerStatus.BLOCKED]: 'Blocked'
};
```

See the **angular** skill for component module patterns.
```