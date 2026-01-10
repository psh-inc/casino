# Form Input Unification Plan (Admin SPA)

## Goal
Ship a single, consistent form look-and-feel across the admin by standardizing inputs, selects, textareas, checkboxes, radios, switches, sliders, date pickers, and rich text. Reduce per-page styling drift, speed up build-out, and keep validation/error patterns uniform.

## Current Landscape (high level)
- Angular Material heavy usage across CMS, payments, players, game management, and settings (`mat-form-field`, `mat-select`, `mat-checkbox`, `mat-slide-toggle`, `mat-datepicker`, `mat-autocomplete`, radios).
- Native inputs/selects sprinkled in dashboards, filters, bonus builder, and player list filters (custom CSS per component).
- Rich text: Angular Editor and Codemirror; CMS widgets use button toggles, color inputs, file inputs.
- Checkboxes/radios and toggles are implemented both via Material components and custom markup.

## Foundation Implemented (this change)
- Added Tailwind + forms plugin with shared tokens: `tailwind.config.js`, `postcss.config.js`.
- Global Tailwind import wired into `src/styles.scss`.
- Introduced `src/styles/tailwind.css` with reusable form utility classes:
  - `.ui-form` (vertical spacing), `.ui-section`/`.ui-section-title` (panel shell)
  - `.ui-field`, `.ui-label`, `.ui-optional`
  - Controls: `.ui-control` (inputs), `.ui-select`, `.ui-textarea`, `.ui-control-sm`
  - State: `.ui-error`, `.ui-helper`, `.ui-invalid`
  - Choice: `.ui-checkbox`, `.ui-radio`, `.ui-switch` (data-checked attr), `.ui-chips`/`.ui-chip`

## New Shared Primitives (added)
- Standalone, OnPush CVA components under `src/app/shared/ui/`: `ui-form-field`, `ui-input`, `ui-select`, `ui-textarea`, `ui-checkbox`, `ui-switch`, `ui-date`, `ui-date-range`, `ui-rich-text` (+ `UiModule` and barrel export).
- Tailwind-first visuals with Material datepicker bridge; validation/error/hint slots via `ui-form-field`.
- Storybook coverage under `src/stories/*` plus `FormPrimitives` demo.
- Custom ESLint rule (`local-rules/no-raw-form-elements`) to warn on new raw inputs/selects/textarea without `ui-*` or Material styling.

## Additional Primitives (this phase)
- `ui-autocomplete` (search/filter options), `ui-file-upload` (click/drag), `ui-codemirror` (code editor shell).
- Storybook stories for the new primitives and a11y addon enabled.
- Lint rule expanded to flag unwrapped editor/codemirror tags.

## New Migrations (this phase)
- Payments initiate form and refunds filter bar rebuilt with `ui-*` primitives and Tailwind layout.
- CMS content form basic info, and CMS page form slug/title/status sections now use `ui-*` wrappers and select inputs.

## Pilot Migrations
- Dashboard filter bar now uses `ui-input` + Tailwind button styling for period presets (`pages/dashboard/components/dashboard-filter-bar`).
- Player create form rebuilt with `ui-*` primitives, Tailwind layout, and preserved validation (`modules/player-management/player-create`).
- Payments refund dialog converted to `ui-*` controls with consistent helper/error states (`modules/payments/refund-dialog`).

## Unified Component Strategy
1) **Tokens & Utilities (done)**: Tailwind config + form utility classes for quick adoption.
2) **Angular Wrappers (next)**: Create lightweight primitives in `src/app/shared/ui/` that wrap functionality but render Tailwind-styled markup:
   - `UiFormField` (label, hint, error slot, required indicator)
   - `UiInput`, `UiTextarea`, `UiSelect` (single/multi), `UiNumber`, `UiPassword`
   - `UiCheckbox`, `UiRadioGroup`, `UiSwitch`
   - `UiSlider/Range`, `UiFile`, `UiDate`, `UiDateRange` (wrap Mat datepicker)
   - `UiAutocomplete`, `UiRichText` (wrap Angular Editor)
3) **Material Bridge**: Keep Angular Material behavior where needed (datepickers, autocompletes, menus) but apply the Tailwind shell so visual language stays consistent. Default `appearance="outline"` with Tailwind padding/radius.
4) **Layouts**: Provide layout helpers (`ui-section`, flex/grid gap presets) for 2/3-column form grids.

## Migration Plan (phased)
1. **Pilot**: Apply `.ui-*` classes in two low-risk places (e.g., dashboard filter bar and one modal) to validate tokens and spacing with existing theme.
2. **Shared Primitives**: Build `shared/ui` components listed above, plus Storybook/demo page (or a simple `/ui-preview` route) to lock visuals.
3. **High-traffic Forms**: Migrate player create/edit, payments/refunds, and CMS content/page forms to primitives. Replace ad-hoc SCSS with Tailwind utilities.
4. **Legacy Custom Forms**: Convert bonus builder and player list filters (currently native inputs/selects) to primitives; remove bespoke CSS once matched.
5. **Complex Controls**: Wrap Angular Editor/Codemirror with consistent header, border, focus, and error treatments; align file upload and color pickers.
6. **Enforcement**: Add lint rule/checklist to block new raw `<input>/<select>/<textarea>` without either `.ui-*` classes or `shared/ui` components; document recipes in this doc and in component READMEs.

## Usage Examples (with current utilities)
```html
<!-- Text -->
<div class="ui-field">
  <label class="ui-label">Title <span class="ui-optional">(optional)</span></label>
  <input class="ui-control" type="text" placeholder="Page title" />
  <p class="ui-helper">Shown on landing pages</p>
</div>

<!-- Select -->
<div class="ui-field">
  <label class="ui-label">Status</label>
  <select class="ui-select">
    <option>Draft</option>
    <option>Published</option>
  </select>
  <p class="ui-error">Required</p>
  <!-- Add .ui-invalid to control when showing errors -->
</div>

<!-- Switch using data-checked -->
<button class="ui-switch" type="button" [attr.data-checked]="enabled" (click)="enabled=!enabled"></button>
```

## Immediate Next Steps
- Build `shared/ui` primitives for inputs/selects/textarea/checkbox/switch with Tailwind classes above.
- Pilot migrate one filter bar + one CRUD form to the new primitives.
- Add Storybook/demo page for visual regression and team reference.
- Update contribution guidelines to require `.ui-*` or `shared/ui` wrappers for new forms.
