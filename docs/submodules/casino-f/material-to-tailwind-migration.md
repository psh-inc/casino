# Material-to-Tailwind Migration Plan (casino-f)

## Inventory Snapshot (Angular Material usage)
- Total templates with `<mat-*>`: 90+ (see `rg -l "<mat-" src`).
- High-traffic/complex flows:
  - Bonus flows: `components/bonus/bonus-form/**`, `bonus-list`, bonus dialogs.
  - Player management: cashier restrictions, wallet/bonus/history, KYC docs, comments, restrictions dialogs, session/bet history, duplicate accounts, fraud dashboard.
  - Payments/Refunds: `modules/payments/**`, `refund-*` dialogs/pages.
  - CMS Admin: pages, widgets, menus, translations, media dialogs.
  - Campaigns/Promotions/Banners/Registration config/Game management.
- Shell widgets still Material-based: paginator, stepper, tabs, chips, select, checkbox/radio, slide-toggle, card, menu, dialog, spinner, list/table.

## Migration Strategy
1) **Build missing Tailwind primitives (ui-*)**
   - Stepper, paginator, tabs, chip/badge set, radio group, slide-toggle, card/panel, menu, dialog/drawer, spinner/skeleton, table pagination controls.
   - Expose as standalone + Storybook, matching `ui-*` patterns (OnPush, signals).
2) **Create bridge shims for phased replacement**
   - Lightweight wrappers (`mat-*` compatibility components) that render Tailwind primitives so template churn can be incremental.
   - Global style overrides to neutralize remaining Material chrome during transition.
3) **Module-by-module migration (order)**
   1. Bonus creation wizard (stepper → ui-stepper; all form fields → ui-form-field/ui-input/ui-select/ui-checkbox/ui-date/ui-table; dialogs → ui-modal).
   2. Payments/Refunds (lists + dialogs + paginator → ui-table/ui-pagination).
   3. Player management (wallet/restrictions/KYC/history/duplicate accounts/fraud dashboard).
   4. CMS Admin (pages/widgets/menus/translations/media dialogs).
   5. Campaigns/Promotions/Banners/Registration config/Game management.
4) **Shared patterns**
   - Replace `mat-card` with Tailwind card shell; `mat-spinner` with Tailwind spinner; `mat-chip`/`mat-chip-list` with `ui-chip`/`ui-badge`; `mat-paginator` with `ui-pagination`.
   - Replace `mat-stepper` with `ui-stepper`; `mat-dialog` with `ui-modal`; `mat-menu` with `ui-menu`.
   - Replace `mat-select`/`mat-option` with `ui-select`/`ui-autocomplete`; `mat-slide-toggle` with `ui-switch`; `mat-radio` with new `ui-radio-group`.
5) **Validation & linting**
   - Extend no-raw-form-elements rule to also flag `<mat-*>`.
   - Storybook scenarios for each migrated flow; snapshot tests for new primitives.
6) **Removal**
   - Drop Material modules/imports per feature after migration; clean SCSS leftovers; tighten budgets once Material is gone.

## Next Execution Batch (recommended)
- Build `ui-stepper`, `ui-pagination`, `ui-tabs`, `ui-radio-group`, `ui-switch` parity with Material behaviors.
- Migrate Bonus wizard container + first two steps to Tailwind primitives as reference implementation.
- Migrate a payment/refund paginator to `ui-pagination`.
- Add lint autofix to replace `<mat-*>` with `ui-*` shims where available.
