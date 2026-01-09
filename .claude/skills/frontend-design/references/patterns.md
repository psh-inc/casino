# Design Patterns & Anti-Patterns

Guidelines for maintaining consistent, maintainable styling.

## DO: Use Design System Imports

```scss
// GOOD - Import design system at component level
@import '../../../styles/design-system.scss';

.my-component {
  @include card-base;
  padding: $space-6;
}
```

## DON'T: Duplicate Variable Definitions

```scss
// BAD - Redefining design tokens
$my-green: #3AA660;  // Duplicates $color-green

.button {
  background: $my-green;
}
```

## DO: Use Mixins for Repeated Patterns

```scss
// GOOD - Consistent glassmorphism application
.modal-content {
  @include glassmorphism;
  padding: $space-6;
}
```

## DON'T: Copy-Paste Glassmorphism Properties

```scss
// BAD - Manual property copying
.modal {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);  // Easy to forget
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### WARNING: Inline Styles in Templates

**The Problem:**

```html
<!-- BAD - Styling in template -->
<div style="background: #0A1E26; padding: 16px; border-radius: 20px;">
```

**Why This Breaks:**
1. Cannot use SCSS variables or mixins
2. No hover/responsive states possible
3. Impossible to maintain consistency

**The Fix:**

```html
<!-- GOOD - Use component class -->
<div class="feature-card">
```

```scss
.feature-card {
  background: $color-primary;
  padding: $space-4;
  border-radius: $radius-lg;
}
```

### WARNING: Using `!important` Excessively

**The Problem:**

```scss
// BAD - !important everywhere
.button {
  background: $color-green !important;
  color: white !important;
  padding: 16px !important;
}
```

**Why This Breaks:**
1. Creates specificity wars
2. Makes future overrides impossible
3. Indicates structural problems

**The Fix:**

```scss
// GOOD - Proper specificity through structure
.button-primary {
  background: $color-green;
  color: white;
  padding: $space-4;
}

// Only use !important for:
// 1. Third-party library overrides (Angular Material)
// 2. iOS Safari fixes
// 3. Print styles
```

### WARNING: z-index Without System

**The Problem:**

```scss
// BAD - Random z-index values
.dropdown { z-index: 999; }
.modal { z-index: 9999; }
.tooltip { z-index: 99999; }
```

**Why This Breaks:**
1. Unpredictable stacking order
2. Numbers become unmaintainable
3. Conflicts between components

**The Fix:**

```scss
// GOOD - Z-index scale from design system
$z-dropdown: 100;
$z-sticky: 200;
$z-overlay: 300;
$z-modal: 400;
$z-tooltip: 500;

.dropdown { z-index: $z-dropdown; }
.modal { z-index: $z-modal; }
.tooltip { z-index: $z-tooltip; }
```

## Mobile-First Pattern

```scss
// GOOD - Base styles for mobile, enhance for larger screens
.component {
  padding: $space-3;
  font-size: $text-sm;
  
  @media (min-width: $screen-md) {
    padding: $space-6;
    font-size: $text-base;
  }
  
  @media (min-width: $screen-lg) {
    padding: $space-8;
  }
}
```

## Admin vs Customer Frontend

### Admin (Tailwind CSS)

```html
<!-- casino-f uses Tailwind utility classes -->
<button class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-lg">
  Save
</button>
```

### Customer (SCSS Design System)

```scss
// casino-customer-f uses custom SCSS
.btn-primary {
  @include button-primary;
}
```

**NEVER** mix these approaches within a single frontend.