---
name: frontend-design
description: |
  Angular UI components with CSS styling and responsive design for the casino platform.
  Use when: Creating new UI components, styling pages, implementing responsive layouts,
  adding animations, or maintaining visual consistency across admin/customer frontends.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Frontend Design Skill

This skill covers Angular UI component design for a dual-frontend casino platform: Admin (Tailwind + SCSS) and Customer (premium dark theme with glassmorphism). The design system emphasizes type-safe component variants, accessibility compliance, and performance-optimized animations.

## Quick Start

### Button Component Pattern (Admin Frontend)

```typescript
// casino-f/src/app/shared/ui/ui-button.component.ts
@Component({
  selector: 'ui-button',
  standalone: true,
  template: `<button [ngClass]="buttonClasses()">...</button>`
})
export class UiButtonComponent {
  @Input() variant: 'primary' | 'secondary' | 'ghost' | 'danger' = 'primary';
  @Input() size: 'xs' | 'sm' | 'md' | 'lg' = 'md';

  buttonClasses = computed(() => {
    const base = 'inline-flex items-center justify-center gap-2 font-semibold transition-all rounded-lg';
    const variantClass = {
      primary: 'bg-primary-600 text-white hover:bg-primary-700',
      danger: 'bg-danger-600 text-white hover:bg-danger-700'
    };
    return `${base} ${variantClass[this.variant()]}`;
  });
}
```

### Casino Button with CVA (Customer Frontend)

```typescript
// casino-customer-f/src/app/shared/ui/button.component.ts
import { cva } from 'class-variance-authority';

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-all",
  {
    variants: {
      variant: {
        casino: "bg-gradient-to-r from-[#3aa660] to-[#52ea88] text-white",
        casinoPurple: "bg-gradient-to-r from-[#8b5cf6] to-[#a855f7] text-white"
      },
      size: { default: "h-9 px-4 py-2", lg: "h-10 rounded-md px-6" }
    }
  }
);
```

## Key Concepts

| Concept | Admin Frontend | Customer Frontend |
|---------|----------------|-------------------|
| Framework | Tailwind CSS + SCSS | Custom SCSS Design System |
| Theme | Light (indigo primary) | Dark casino (teal/green) |
| Components | `ui-*` prefix | Standalone components |
| Icons | Heroicons (via ui-icon) | Inline SVGs |
| Fonts | Roboto (14px base) | Rubik, Montserrat, Inter |
| Touch Target | 44px minimum | 48px minimum |

## Common Patterns

### Responsive Game Grid

**When:** Displaying game cards in the casino lobby

```scss
// casino-customer-f/src/app/features/games/components/casino-page/styles/_game-grid.scss
.game-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(2, 1fr);  // Mobile: 2 cols

  @media (min-width: 768px) { grid-template-columns: repeat(4, 1fr); }
  @media (min-width: 1280px) { grid-template-columns: repeat(6, 1fr); }
}
```

### Glassmorphism Card

**When:** Creating premium UI elements in customer frontend

```scss
@mixin glassmorphism {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
```

### Form Section (Admin)

**When:** Creating data entry forms in admin panel

```html
<div class="ui-section">
  <h3 class="ui-section-title">Player Details</h3>
  <div class="ui-form">
    <ui-form-field label="Email" [required]="true">
      <ui-input formControlName="email" type="email"></ui-input>
    </ui-form-field>
  </div>
</div>
```

## See Also

- [aesthetics](references/aesthetics.md) - Typography, colors, visual identity
- [components](references/components.md) - UI component patterns
- [layouts](references/layouts.md) - Grid systems, responsive breakpoints
- [motion](references/motion.md) - Animations, transitions
- [patterns](references/patterns.md) - Anti-patterns, best practices

## Related Skills

- See the **angular** skill for component architecture and RxJS patterns
- See the **typescript** skill for type-safe styling with CVA