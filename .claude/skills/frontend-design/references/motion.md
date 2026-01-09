# Motion Reference

Animations, transitions, and micro-interactions for the casino platform.

## Transition Timing

```scss
// casino-customer-f timing tokens
$transition-fast: 150ms;
$transition-base: 300ms;
$transition-slow: 500ms;

// Easing functions
$ease-out: cubic-bezier(0.4, 0, 0.2, 1);
$ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
$ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

## Core Animations

### Shimmer Loading Effect

```scss
// casino-customer-f/src/app/features/games/components/casino-page/styles/_animations.scss
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.game-card-skeleton {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.05) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

### Slide and Scale Entry

```scss
@keyframes slideInAndScale {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-content {
  animation: slideInAndScale 0.3s $ease-out forwards;
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

.dropdown-menu {
  animation: dropdownSlideDown 0.2s $ease-out;
}
```

### Wave Ripple Effect (Play Button)

```scss
@keyframes wave-1 {
  0% {
    width: 100%;
    height: 100%;
    opacity: 0.8;
    border-width: 2px;
  }
  100% {
    width: 140%;
    height: 140%;
    opacity: 0;
    border-width: 1px;
  }
}

.play-btn-main .wave-1 {
  position: absolute;
  border: 2px solid rgba(58, 166, 96, 0.5);
  border-radius: 50%;
  animation: wave-1 3s ease-out infinite;
}
```

## Hover Interactions

### Button Shine Effect

```scss
@mixin button-primary {
  position: relative;
  overflow: hidden;
  background: $gradient-gold;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.6s;
  }
  
  &:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: $shadow-lg, $shadow-glow-gold;
    
    &::before {
      left: 100%;
    }
  }
}
```

### Game Card Hover

```scss
.game-card {
  transition: transform $transition-base $ease-out, box-shadow $transition-base;
  
  &:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
    
    .game-overlay {
      opacity: 1;
    }
    
    .play-button {
      transform: scale(1);
      opacity: 1;
    }
  }
}
```

## WARNING: Animation Performance Issues

**The Problem:**

```scss
// BAD - Animating expensive properties
.card {
  transition: all 0.3s;  // Animates everything including layout
  
  &:hover {
    width: 110%;         // Triggers layout
    padding: 20px;       // Triggers layout
    left: 10px;          // Triggers layout
  }
}
```

**Why This Breaks:**
1. Layout thrashing - Forces browser to recalculate geometry
2. Paint storms - Expensive repaints on every frame
3. Jank - Visible stuttering, especially on mobile

**The Fix:**

```scss
// GOOD - Use compositor-only properties
.card {
  transition: transform 0.3s $ease-out, box-shadow 0.3s;
  will-change: transform;  // Hint to browser
  
  &:hover {
    transform: scale(1.05) translateY(-4px);  // GPU accelerated
    box-shadow: $shadow-lg;
  }
}
```

## WARNING: Overusing Animations

**The Problem:**

```scss
// BAD - Everything animates constantly
.badge {
  animation: pulse 1s infinite;
}
.button {
  animation: bounce 0.5s infinite;
}
.icon {
  animation: spin 2s infinite;
}
```

**Why This Breaks:**
1. Motion sickness - Some users get nauseous
2. Distraction - Constant movement hurts focus
3. Battery drain - Continuous animations consume power

**The Fix:**

```scss
// GOOD - Purposeful, triggered animations
.badge.is-new {
  animation: pulse 2s ease-out 3;  // Only 3 times, then stops
}

.button:active {
  animation: press 0.15s ease-out;  // Only on interaction
}

// Respect user preferences
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Loading States

### Skeleton Screen Pattern

```scss
.game-card-shimmer {
  .shimmer-thumbnail {
    aspect-ratio: 4/5;
    background: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0.05) 0%,
      rgba(255, 255, 255, 0.15) 50%,
      rgba(255, 255, 255, 0.05) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 12px;
  }
  
  .shimmer-title {
    height: 16px;
    width: 70%;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    margin-top: 8px;
  }
}
```