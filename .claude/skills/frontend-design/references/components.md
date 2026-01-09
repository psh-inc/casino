# Component Styling Patterns

Consistent component styling maintains the casino's premium visual identity.

## Button System

### Primary Button (CTAs)

```scss
.btn-primary {
  @include button-primary;
  
  // Green gradient with glow
  background: linear-gradient(135deg, #2E8549 0%, #3AA660 50%, #5FBF7F 100%);
  color: $color-primary-dark;
  font-weight: 600;
  box-shadow: $shadow-md, $shadow-glow-gold;
  
  &:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: $shadow-lg, $shadow-glow-gold;
  }
}
```

### Ghost Button

```scss
.btn-ghost {
  @include button-base;
  background: transparent;
  color: $color-text-secondary;
  border: 1px solid $glass-border;
  
  &:hover {
    background: $glass-background;
    border-color: $color-green;
  }
}
```

### WARNING: Inconsistent Button Heights

**The Problem:**

```scss
// BAD - Different heights across buttons
.btn-small { padding: 4px 8px; }
.btn-normal { padding: 10px 20px; }
.btn-large { padding: 16px 32px; }
```

**Why This Breaks:**
1. Buttons misalign in flex/grid layouts
2. Touch targets may be too small on mobile
3. Visual inconsistency

**The Fix:**

```scss
// GOOD - Use consistent base with size modifiers
@mixin button-base {
  padding: $space-3 $space-6;  // 12px 24px
  min-height: 44px;  // Apple touch target minimum
  
  @media (max-width: $screen-md) {
    min-height: 48px;  // Google accessibility guideline
  }
}
```

## Card System

### Game Card

```scss
.game-card {
  position: relative;
  background: $glass-background;
  backdrop-filter: blur(10px);
  border: 1px solid $glass-border;
  border-radius: $radius-lg;
  overflow: hidden;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    border-color: rgba($color-green, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4),
                0 0 40px rgba($color-green, 0.1);
  }
}
```

### Badge System

```scss
.badge {
  padding: 4px 8px;
  border-radius: $radius-sm;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  backdrop-filter: blur(10px);
  
  &.hot {
    background: linear-gradient(135deg, rgba(255, 107, 53, 0.9), rgba(255, 143, 101, 0.9));
    box-shadow: 0 2px 8px rgba(255, 107, 53, 0.4);
  }
  
  &.new {
    background: linear-gradient(135deg, rgba($color-green-dark, 0.9), rgba($color-green, 0.9));
    box-shadow: 0 2px 8px rgba($color-green, 0.4);
  }
}
```

## Form Elements

### Input Fields

```scss
// CRITICAL: 16px font prevents iOS zoom on focus
input[type="text"],
input[type="email"],
input[type="password"],
textarea,
select {
  font-size: 16px !important;
  min-height: 44px;
  
  @media (max-width: $screen-md) {
    min-height: 48px;
  }
}
```

## Spinner/Loading States

```scss
.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 215, 0, 0.2);
  border-radius: 50%;
  border-top-color: $color-gold;
  animation: spin 1s ease-in-out infinite;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```