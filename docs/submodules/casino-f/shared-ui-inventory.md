# Shared UI Inventory (casino-f)

## Shared Components (Angular)
- `app-status-chip` (status-chip): badge/chip for status states.
- `app-command-palette` (command-palette): quick actions/search overlay.
- `app-country-restriction` (country-restriction): country restriction settings widget.
- `app-notifications` (notifications): toast + dropdown notification center.
- `app-page-header` (page-header): page title bar with optional back/button.
- `app-confirm-dialog` (confirm-dialog): confirm modal (Material-based).
- `app-wagering-progress` (wagering-progress): progress indicator widget.
- `app-empty-state` (empty-state): empty state display.
- `app-loading-spinner` (loading-spinner): loading indicator.

## Shared Primitives (ui-*)
- Buttons & CTAs: `ui-button` (variants, loading, icon-only).
- Data display: `ui-table` (sorting, paging, selection), `ui-badge`, `ui-chip`.
- Menus & overlays: `ui-menu` (checkbox/separator items), `ui-modal` (modal/drawer), `ui-toast` (stacked alerts).
- Inputs: `ui-input`, `ui-select`, `ui-textarea`, `ui-autocomplete`, `ui-date`, `ui-date-range`.
- Toggles: `ui-checkbox`, `ui-switch`.
- Rich inputs: `ui-rich-text`, `ui-codemirror`, `ui-file-upload`.
- Form chrome: `ui-form-field`.

## Gaps (no shared primitive yet)
- Notifications center glue code that wires ui-toast into `app-notifications`.
- Layout/pattern helpers (page shells, multi-column forms) — tracked in Storybook “Platform/Patterns”.
