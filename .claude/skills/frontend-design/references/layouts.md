# Layout Patterns

Responsive layouts prioritize mobile-first design with progressive enhancement.

## Breakpoints

```scss
$screen-sm: 640px;   // Phones landscape
$screen-md: 768px;   // Tablets
$screen-lg: 1024px;  // Desktop
$screen-xl: 1280px;  // Large desktop
```

## Container Pattern

```scss
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 $space-4;
  
  @media (min-width: $screen-md) {
    padding: 0 $space-6;
  }
}
```

## Game Grid System

```scss
.game-grid {
  display: grid;
  gap: 16px;
  
  // Mobile: 2 columns
  grid-template-columns: repeat(2, 1fr);
  
  @media (min-width: $screen-sm) {
    grid-template-columns: repeat(3, 1fr);
  }
  
  @media (min-width: $screen-lg) {
    grid-template-columns: repeat(4, 1fr);
  }
  
  @media (min-width: $screen-xl) {
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
  }
}
```

## Spacing System

```scss
// 4px base unit
$space-1: 4px;
$space-2: 8px;
$space-3: 12px;
$space-4: 16px;
$space-6: 24px;
$space-8: 32px;
$space-12: 48px;

// Accessibility guidelines
$widget-spacing-mobile: 24px;
$widget-spacing-desktop: 40px;
$min-touch-target: 48px;
```

### WARNING: Hardcoded Spacing Values

**The Problem:**

```scss
// BAD - Magic numbers everywhere
.component {
  margin: 17px;
  padding: 23px 11px;
}
```

**Why This Breaks:**
1. Inconsistent visual rhythm
2. Difficult to maintain
3. Doesn't scale with design system updates

**The Fix:**

```scss
// GOOD - Use spacing tokens
.component {
  margin: $space-4;
  padding: $space-6 $space-3;
}
```

## Modal/Dialog Layouts

```scss
.modal-container {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  
  .modal-content {
    max-height: 90vh;
    max-width: calc(100vw - 32px);
    overflow-y: auto;
    
    @media (min-width: $screen-md) {
      max-height: 85vh;
      max-width: 800px;
    }
  }
}
```

## iOS Safari Fixes

```scss
// Fix viewport height issues
@supports (-webkit-touch-callout: none) {
  body {
    min-height: 100vh;
    min-height: -webkit-fill-available;
  }
  
  html {
    height: -webkit-fill-available;
  }
  
  .main-content {
    min-height: 100vh;
    min-height: -webkit-fill-available;
    padding-bottom: calc(64px + env(safe-area-inset-bottom, 0));
  }
}
```

## Scroll Behavior

```scss
html {
  scroll-behavior: smooth;
  
  @media (min-width: $screen-md) {
    scroll-padding-top: 8.5rem;  // Account for sticky header
  }
  
  @media (max-width: $screen-md) {
    scroll-padding-top: 4rem;
  }
}
```