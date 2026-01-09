---
name: frontend-design
description: |
  Angular UI components with Material Design, SCSS design system, and responsive layouts.
  Use when: Creating new UI components, styling pages, implementing responsive layouts, adding animations, or maintaining visual consistency across admin/customer frontends.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Frontend-design Skill

This casino platform uses a dual-styling approach: **Tailwind CSS** for the admin frontend (`casino-f/`) and a **custom SCSS design system** for the customer frontend (`casino-customer-f/`). The customer frontend features a dark, premium casino aesthetic with glassmorphism effects, neon accents, and mobile-first responsive patterns.

## Quick Start

### Import Design System (Customer Frontend)

```scss
// Always import at the top of component styles
@import '../../../styles/design-system.scss';

.my-component {
  @include glassmorphism;
  background: $gradient-card;
  border-radius: $radius-lg;
  padding: $space-6;
  color: $color-text-primary;
}
```

### Glass Button Pattern

```scss
.glass-button {
  @include button-base;
  background: $glass-background;
  backdrop-filter: blur(10px);
  border: 1px solid $glass-border;
  color: $color-text-primary;
  
  &:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-2px);
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Design tokens | SCSS variables for colors, spacing, typography | `$color-green`, `$space-4` |
| Glassmorphism | Semi-transparent backgrounds with blur | `@include glassmorphism` |
| Neon glow | Text shadow effects for emphasis | `@include neon-glow($color-neon-teal)` |
| Mobile-first | 48px minimum touch targets, 16px font for iOS | `min-height: 44px` |

## Common Patterns

### Card Component

**When:** Creating any content container (games, promotions, user info)

```scss
.feature-card {
  @include card-base;
  padding: $space-6;
  
  .card-title {
    @include heading-style;
    font-size: $text-xl;
    margin-bottom: $space-4;
  }
  
  .card-content {
    @include body-text;
  }
}
```

### Responsive Grid

**When:** Displaying game lists, promotion grids

```scss
.game-grid {
  display: grid;
  gap: $space-4;
  grid-template-columns: repeat(2, 1fr);
  
  @media (min-width: $screen-md) {
    grid-template-columns: repeat(3, 1fr);
  }
  
  @media (min-width: $screen-lg) {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## See Also

- [aesthetics](references/aesthetics.md)
- [components](references/components.md)
- [layouts](references/layouts.md)
- [motion](references/motion.md)
- [patterns](references/patterns.md)

## Related Skills

- **angular** - For component architecture and reactive patterns
- **typescript** - For type-safe component interfaces