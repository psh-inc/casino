# Animation & Motion Patterns

Animations enhance user experience without sacrificing performance.

## Transition Standards

```scss
// Duration tokens
$transition-fast: 150ms;
$transition-base: 300ms;
$transition-slow: 500ms;

// Standard easing
$transition-standard: 300ms cubic-bezier(0.4, 0, 0.2, 1);
```

## Hover Effects

### Card Lift

```scss
.game-card {
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4),
                0 0 40px rgba($color-green, 0.1);
  }
}
```

### Button Feedback

```scss
.btn-primary {
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px) scale(1.05);
  }
  
  &:active {
    transform: translateY(0) scale(1);
  }
}
```

## Keyframe Animations

### Pulse Effect

```scss
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading-indicator {
  animation: pulse 2s ease-in-out infinite;
}
```

### Heartbeat (Favorite Button)

```scss
@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

.favorite-btn.active .heart-icon {
  animation: heartBeat 0.5s ease;
}
```

### Slide Animations

```scss
@keyframes slideLeft {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideRight {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

### Dropdown Animation

```scss
@keyframes dropdownSlideDown {
  from {
    opacity: 0;
    transform: translateY(-2px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
```

## Neon Glow Effect

```scss
@mixin neon-glow($color: $color-neon-teal) {
  text-shadow:
    0 0 10px $color,
    0 0 20px $color,
    0 0 30px $color,
    0 0 40px $color;
}

// Usage
.jackpot-amount {
  @include neon-glow($color-green);
}
```

### WARNING: Performance-Heavy Animations

**The Problem:**

```scss
// BAD - Animating expensive properties
.card {
  transition: all 0.3s ease;  // Includes width, height
  
  &:hover {
    width: 110%;
    box-shadow: 0 0 100px rgba(0, 0, 0, 0.8);
  }
}
```

**Why This Breaks:**
1. `width/height` triggers layout recalculation
2. Large box-shadows are GPU intensive
3. Causes frame drops on mobile

**The Fix:**

```scss
// GOOD - Only animate transform and opacity
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  will-change: transform;
  
  &:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  }
}
```

## Reduced Motion Support

```scss
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```