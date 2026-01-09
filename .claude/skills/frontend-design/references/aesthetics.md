# Aesthetics Reference

Typography, color systems, and visual identity for the casino platform's dual-frontend architecture.

## Typography

### Admin Frontend (casino-f)

The admin panel uses Roboto for a clean, professional data-heavy interface.

```scss
// casino-f/src/styles/_variables.scss
$font-family-base: 'Roboto', 'Helvetica Neue', sans-serif;
$font-size-base: 14px;
$font-size-small: 12px;
$font-size-large: 16px;
$font-weight-regular: 400;
$font-weight-medium: 500;
$font-weight-bold: 700;
```

### Customer Frontend (casino-customer-f)

The customer-facing app uses a premium font stack for an upscale casino feel.

```scss
// casino-customer-f/src/styles/design-system.scss
$font-rubik: 'Rubik', sans-serif;        // Body text, readable at all sizes
$font-montserrat: 'Montserrat', sans-serif;  // Headings, strong presence
$font-inter: 'Inter', system-ui, sans-serif;  // UI elements, numbers
```

### WARNING: Mixing Font Stacks

**The Problem:**

```scss
// BAD - Using admin fonts in customer frontend
.game-title {
  font-family: 'Roboto', sans-serif;  // Wrong font for casino theme
}
```

**Why This Breaks:**
1. Visual inconsistency - Roboto feels corporate, not premium
2. Brand dilution - Rubik/Montserrat are the casino identity
3. User experience - Jarring font switches confuse users

**The Fix:**

```scss
// GOOD - Use the established font variables
.game-title {
  font-family: $font-montserrat;
  font-weight: 700;
  letter-spacing: -0.02em;
}
```

## Color System

### Admin Frontend - Light Theme

```scss
// casino-f/src/styles/_variables.scss
$primary-color: #1976d2;    // Blue - primary actions
$accent-color: #ff4081;     // Pink - accents
$success-color: #4caf50;    // Green - success states
$error-color: #f44336;      // Red - errors
$warning-color: #ff9800;    // Orange - warnings
```

Tailwind extension in `tailwind.config.js`:
```javascript
colors: {
  primary: colors.indigo,
  accent: colors.purple,
  success: colors.emerald,
  warning: colors.amber,
  danger: colors.red,
  muted: colors.slate
}
```

### Customer Frontend - Dark Casino Theme

```scss
// casino-customer-f/src/styles/design-system.scss
$color-primary: #0A1E26;        // Dark teal-black background
$color-background: #030A0D;     // Deep black with teal tint
$color-green: #3AA660;          // Primary green accent (gold equivalent)
$color-neon-teal: #00E5CC;      // Neon accents
$color-neon-green: #39FF14;     // High-energy highlights

// Text hierarchy
$color-text-primary: #FFFFFF;
$color-text-secondary: rgba(255, 255, 255, 0.87);
$color-text-disabled: rgba(255, 255, 255, 0.5);
```

### WARNING: Using Blue in Customer Frontend

**The Problem:**

```scss
// BAD - Blue doesn't match casino brand
.cta-button {
  background: #1976d2;  // Admin blue in customer app
}
```

**Why This Breaks:**
1. Brand inconsistency - Casino uses green/teal, not blue
2. Trust signal - Users associate colors with platforms
3. Design system violation - Breaks established patterns

**The Fix:**

```scss
// GOOD - Use casino green gradient
.cta-button {
  background: linear-gradient(135deg, $color-green, #52ea88);
  
  &:hover {
    box-shadow: $shadow-glow-gold;
  }
}
```

## Premium Effects

### Neon Glow Mixin

```scss
// Used for highlighting jackpots, wins, featured games
@mixin neon-glow($color: $color-neon-teal) {
  text-shadow:
    0 0 10px $color,
    0 0 20px $color,
    0 0 30px $color,
    0 0 40px $color;
}

// Shadow tokens
$shadow-glow-gold: 0 0 20px rgba(58, 166, 96, 0.4), 0 0 40px rgba(58, 166, 96, 0.2);
$shadow-glow-neon: 0 0 30px rgba(0, 245, 255, 0.4), 0 0 60px rgba(0, 245, 255, 0.2);
```

### Gradient System

```scss
// Primary action gradient
$gradient-gold: linear-gradient(135deg, #3AA660 0%, #52EA88 100%);

// Purple variant for special promotions
$gradient-purple: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);

// Subtle background gradients
$gradient-bg-subtle: linear-gradient(180deg, 
  rgba(10, 30, 38, 0.9) 0%, 
  rgba(3, 10, 13, 1) 100%
);
```

## Contrast Requirements

All text must meet WCAG AA standards:

| Context | Minimum Ratio | Example |
|---------|---------------|---------|
| Body text | 4.5:1 | White on #0A1E26 = 12.5:1 |
| Large text (18px+) | 3:1 | Secondary text on dark = 5.2:1 |
| UI components | 3:1 | Disabled states = 3.5:1 |

### WARNING: Low Contrast Text

**The Problem:**

```scss
// BAD - Insufficient contrast
.subtle-label {
  color: rgba(255, 255, 255, 0.3);  // Ratio ~2:1
}
```

**Why This Breaks:**
1. Accessibility failure - WCAG violation
2. Legal risk - ADA compliance issues
3. Poor UX - Users can't read the content

**The Fix:**

```scss
// GOOD - Meets AA standard
.subtle-label {
  color: $color-text-disabled;  // rgba(255, 255, 255, 0.5) = 4.6:1
}
```