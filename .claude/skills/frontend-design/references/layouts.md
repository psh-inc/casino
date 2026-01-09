# Layouts Reference

Grid systems, responsive breakpoints, and spatial composition for both frontends.

## Breakpoint Systems

### Admin Frontend

```scss
// casino-f/src/styles/_variables.scss
$breakpoint-xs: 0;
$breakpoint-sm: 600px;
$breakpoint-md: 960px;
$breakpoint-lg: 1280px;
$breakpoint-xl: 1920px;
```

Uses Tailwind's responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`

### Customer Frontend

```scss
// casino-customer-f/src/app/features/games/components/casino-page/styles/_variables.scss
$mobile-max: 767px;
$tablet-min: 768px;
$tablet-max: 1024px;
$desktop-min: 1025px;
```

### Responsive Mixins

```scss
// casino-customer-f/src/styles/_mixins.scss
@mixin mobile {
  @media (max-width: $mobile-max) { @content; }
}

@mixin tablet {
  @media (min-width: $tablet-min) and (max-width: $tablet-max) { @content; }
}

@mixin desktop {
  @media (min-width: $desktop-min) { @content; }
}

// Usage
.game-card {
  padding: 0.75rem;
  
  @include tablet { padding: 1rem; }
  @include desktop { padding: 1.25rem; }
}
```

## Grid Systems

### Game Grid - Progressive Columns

```scss
// casino-customer-f/src/app/features/games/components/casino-page/styles/_game-grid.scss
.game-grid {
  display: grid;
  gap: 1rem;
  
  // Mobile: 2 columns
  grid-template-columns: repeat(2, 1fr);
  
  // Small tablet: 3 columns
  @media (min-width: 640px) {
    grid-template-columns: repeat(3, 1fr);
  }
  
  // Tablet: 4 columns
  @media (min-width: 768px) {
    grid-template-columns: repeat(4, 1fr);
  }
  
  // Small desktop: 5 columns
  @media (min-width: 1024px) {
    grid-template-columns: repeat(5, 1fr);
  }
  
  // Desktop: 6 columns
  @media (min-width: 1280px) {
    grid-template-columns: repeat(6, 1fr);
  }
  
  // Large desktop: 7 columns
  @media (min-width: 1536px) {
    grid-template-columns: repeat(7, 1fr);
  }
}
```

### Admin Data Grid

```typescript
// Tailwind-based responsive grid for admin panels
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  <ui-card *ngFor="let player of players">...</ui-card>
</div>
```

## Spacing Scale

### 8px Base Unit System

```scss
// casino-f/src/styles/_variables.scss
$spacing-xs: 4px;   // 0.5 unit
$spacing-sm: 8px;   // 1 unit
$spacing-md: 16px;  // 2 units
$spacing-lg: 24px;  // 3 units
$spacing-xl: 32px;  // 4 units
$spacing-xxl: 48px; // 6 units
```

### Customer Frontend Spacing

```scss
// casino-customer-f/src/styles/design-system.scss
$space-1: 4px;
$space-2: 8px;
$space-3: 12px;
$space-4: 16px;
$space-6: 24px;
$space-8: 32px;

// Widget-specific spacing
$widget-spacing-mobile: 24px;
$widget-spacing-desktop: 40px;
```

## Container Patterns

### Centered Content Container

```scss
@mixin container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  
  @media (max-width: 768px) {
    padding: 0 1rem;
  }
}
```

### Section Component

```scss
// casino-f/src/styles.scss
@layer components {
  .ui-section {
    @apply rounded-xl border border-slate-200 bg-white p-4 shadow-sm;
  }
  
  .ui-section-title {
    @apply text-base font-semibold text-slate-900 mb-4;
  }
}
```

## WARNING: Magic Number Spacing

**The Problem:**

```scss
// BAD - Arbitrary spacing values
.card {
  padding: 17px;
  margin-bottom: 23px;
  gap: 7px;
}
```

**Why This Breaks:**
1. Inconsistent rhythm - Doesn't follow 8px grid
2. Unmaintainable - Hard to adjust globally
3. Visual discord - Elements don't align

**The Fix:**

```scss
// GOOD - Use spacing scale
.card {
  padding: $spacing-md;      // 16px
  margin-bottom: $spacing-lg; // 24px
  gap: $spacing-sm;          // 8px
}
```

## Z-Index System

### Admin Frontend

```scss
$z-index-drawer: 1200;
$z-index-modal: 1300;
$z-index-snackbar: 1400;
$z-index-tooltip: 1500;
```

### Customer Frontend

```scss
$z-dropdown: 100;
$z-sticky: 200;
$z-overlay: 300;
$z-modal: 400;
$z-tooltip: 500;
```

### WARNING: Arbitrary Z-Index Values

**The Problem:**

```scss
// BAD - Z-index wars
.dropdown { z-index: 9999; }
.modal { z-index: 99999; }
.tooltip { z-index: 999999; }
```

**Why This Breaks:**
1. Escalation - Each new element needs higher values
2. Unpredictable stacking - Elements overlap unexpectedly
3. Debugging nightmare - Hard to reason about order

**The Fix:**

```scss
// GOOD - Use established scale
.dropdown { z-index: $z-dropdown; }  // 100
.modal { z-index: $z-modal; }        // 400
.tooltip { z-index: $z-tooltip; }    // 500
```

## Touch Target Compliance

```scss
// Minimum touch target (Google accessibility standard)
$min-touch-target: 48px;

.filter-item-button {
  min-height: $min-touch-target;
  min-width: $min-touch-target;
  padding: 0.625rem 1rem;
}
```