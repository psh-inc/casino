```markdown
# TypeScript Modules

## Path Alias Configuration

Both frontends use TypeScript path aliases for organized imports.

### Admin Frontend (`casino-f/tsconfig.json`)

```json
{
  "compilerOptions": {
    "paths": {
      "@core/*": ["src/app/core/*"],
      "@shared/*": ["src/app/shared/*"],
      "@auth/*": ["src/app/auth/*"],
      "@layout/*": ["src/app/layout/*"],
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

---

### WARNING: Relative Import Chaos

**The Problem:**

```typescript
// BAD - Fragile relative paths
import { Player } from '../../../core/models/player.model';
import { PlayersService } from '../../../../services/players.service';
```

**Why This Breaks:**
1. Moving files requires updating every import
2. Refactoring is terrifying
3. Imports become unreadable at 4+ levels

**The Fix:**

```typescript
// GOOD - Path aliases
import { Player } from '@core/models/player.model';
import { PlayersService } from '@modules/player-management/players.service';
```

---

## Module Organization Pattern

### Feature Module Structure

```
modules/player-management/
├── components/
│   ├── player-list/
│   │   ├── player-list.component.ts
│   │   └── player-list.component.html
│   └── player-details/
├── models/
│   └── player.model.ts          # Interfaces, enums, types
├── services/
│   └── players.service.ts       # HTTP operations
├── guards/
│   └── player.guard.ts
├── player-management.module.ts
└── player-management-routing.module.ts
```

---

### Export Barrel Pattern

```typescript
// models/index.ts - Single export point
export * from './player.model';
export * from './wallet.model';
export * from './transaction.model';

// Usage
import { Player, Wallet, Transaction } from '@modules/player-management/models';
```

---

### WARNING: Circular Dependencies

**The Problem:**

```typescript
// player.service.ts
import { WalletService } from './wallet.service';

// wallet.service.ts
import { PlayerService } from './player.service';  // CIRCULAR!
```

**Why This Breaks:**
1. Runtime errors: `Cannot read property 'x' of undefined`
2. Webpack bundling issues
3. Initialization order becomes unpredictable

**The Fix:**

```typescript
// Option 1: Extract shared logic to third service
// shared.service.ts
export class SharedPlayerWalletService { ... }

// Option 2: Use dependency injection with interfaces
interface IPlayerService { getPlayer(id: number): Observable<Player>; }

// Option 3: Lazy injection
constructor(private injector: Injector) {}
get playerService() { return this.injector.get(PlayerService); }
```

---

### Model File Conventions

```typescript
// player.model.ts

// 1. Enums first
export enum PlayerStatus { ... }

// 2. Interfaces second
export interface Player { ... }
export interface PlayerDetails extends Player { ... }

// 3. Request/Response types
export interface CreatePlayerRequest { ... }
export interface UpdatePlayerRequest { ... }

// 4. Utility functions last
export function isPlayerActive(player: Player): boolean { ... }

// 5. Lookup tables at the end
export const PLAYER_STATUS_LABELS: Record<PlayerStatus, string> = { ... };
```

---

### WARNING: God Module

**The Problem:**

```typescript
// shared.module.ts with 50+ imports
@NgModule({
  declarations: [
    HeaderComponent, FooterComponent, SidebarComponent,
    ButtonComponent, InputComponent, SelectComponent,
    // ... 47 more components
  ],
  exports: [/* all of them */]
})
export class SharedModule {}
```

**Why This Breaks:**
1. Every feature imports the entire kitchen sink
2. Bundle size explodes
3. Change detection affects unrelated components

**The Fix:**

```typescript
// Split into focused modules
// ui/ui-buttons.module.ts
// ui/ui-forms.module.ts
// ui/ui-layout.module.ts

// Or use standalone components (Angular 17+)
@Component({
  standalone: true,
  imports: [ButtonComponent, InputComponent]  // Only what's needed
})
```

---

## Strict Mode Differences

| Setting | `casino-f` | `casino-customer-f` |
|---------|------------|---------------------|
| `strict` | `false` | `true` |
| `noImplicitAny` | `false` | `true` |
| `strictNullChecks` | `false` | `true` |

**Implication:** Customer frontend requires explicit null handling:

```typescript
// Customer frontend (strict mode)
const player = getPlayer();
console.log(player?.username ?? 'Unknown');  // Required

// Admin frontend (non-strict)
console.log(player.username);  // Allowed (but risky)
```

See the **angular** skill for component module patterns.
```