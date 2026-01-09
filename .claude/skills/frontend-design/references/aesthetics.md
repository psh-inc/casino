# Design Aesthetics

The casino platform uses a **premium dark theme** with teal-black backgrounds and green accents. This creates an immersive gaming atmosphere while maintaining accessibility.

## Color System

### Primary Palette

```scss
// Dark teal-black backgrounds
$color-primary: #0A1E26;
$color-background: #030A0D;
$color-surface: #0A1E26;
$color-surface-light: #0F2936;

// Green accent system (primary action color)
$color-green: #3AA660;
$color-green-light: #5FBF7F;
$color-green-dark: #2E8549;
```

### Neon Accents

```scss
// Use sparingly for emphasis
$color-neon-teal: #00E5CC;
$color-neon-green: #39FF14;
$color-neon-blue: #00F5FF;
$color-neon-purple: #9D4EDD;
```

### WARNING: Generic Color Choices

**The Problem:**

```scss
// BAD - Generic colors that don't match casino aesthetic
.button {
  background: #3b82f6;  // Generic blue
  color: white;
}
```

**Why This Breaks:**
1. Inconsistent visual identity across the platform
2. Blue doesn't convey action in a green-themed interface
3. Players associate green with wins/money in casino contexts

**The Fix:**

```scss
// GOOD - Use design system colors
.button {
  background: $gradient-gold;  // Maps to green gradient
  color: $color-primary-dark;
}
```

## Typography

### Font Stack

```scss
$font-rubik: 'Rubik', sans-serif;      // Body text
$font-roboto: 'Roboto', sans-serif;    // Buttons, UI
$font-montserrat: 'Montserrat', sans-serif; // Headings, CTAs
$font-inter: 'Inter', system-ui, sans-serif; // Fallback
```

### Hierarchy

```scss
h1 { font-size: $text-4xl; font-weight: 700; } // 36px
h2 { font-size: $text-3xl; font-weight: 600; } // 30px
h3 { font-size: $text-2xl; font-weight: 600; } // 24px
body { font-size: $text-base; }                // 16px
```

### Text Colors

```scss
$color-text-primary: #FFFFFF;
$color-text-secondary: rgba(255, 255, 255, 0.87);
$color-text-disabled: rgba(255, 255, 255, 0.5);
$color-text-hint: rgba(255, 255, 255, 0.38);
```

## Glassmorphism

The signature visual style uses frosted glass effects:

```scss
@mixin glassmorphism {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}
```

### WARNING: Overusing Blur Effects

**The Problem:**

```scss
// BAD - Multiple nested blur effects
.card {
  backdrop-filter: blur(10px);
  
  .inner-card {
    backdrop-filter: blur(10px);  // Stacks poorly
  }
}
```

**Why This Breaks:**
1. Performance degradation on mobile devices
2. Unpredictable visual stacking
3. Safari requires `-webkit-` prefix

**The Fix:**

```scss
// GOOD - Apply glassmorphism at container level only
.card {
  @include glassmorphism;
  
  .inner-card {
    background: rgba(255, 255, 255, 0.03);  // Lighter, no blur
    border: 1px solid $glass-border;
  }
}
```