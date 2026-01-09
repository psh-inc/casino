---
name: playwright
description: |
  Playwright E2E testing for customer frontend
  Use when: Writing E2E tests for Angular customer frontend, testing authentication flows, testing game listings, testing profile/KYC workflows
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Playwright Skill

E2E testing framework for the casino customer frontend (`casino-customer-f/`) using Playwright. Tests run against Angular 17 with standalone components, testing critical user flows including authentication, games listing, profile management, and KYC verification. The project uses multi-browser testing with mobile viewport support.

## Quick Start

### Running Tests

```bash
cd casino-customer-f
npx playwright test                    # Run all tests
npx playwright test --ui               # Interactive UI mode
npx playwright test --headed           # See browser while testing
npx playwright test e2e/auth.spec.ts   # Run specific test file
```

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:4201');
  });

  test('should perform action', async ({ page }) => {
    await page.getByRole('button', { name: 'Login' }).first().click();
    await expect(page.locator('.auth-modal-backdrop')).toBeVisible();
  });
});
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Locators | Target elements | `page.locator('.class')`, `page.getByRole()` |
| Assertions | Verify state | `await expect(el).toBeVisible()` |
| API Mocking | Stub backend | `page.route('**/api/**', handler)` |
| Screenshots | Visual debugging | `page.screenshot({ path: 'name.png' })` |
| Mobile Testing | Responsive tests | `page.setViewportSize({ width: 375, height: 667 })` |

## Common Patterns

### Login Flow Testing

```typescript
test('should login successfully', async ({ page }) => {
  await page.getByRole('button', { name: 'Login' }).first().click();
  await page.locator('input[formControlName="username"]').fill('testuser');
  await page.locator('input[formControlName="password"]').fill('Test1234');
  await page.locator('button[type="submit"]').click();
  
  await expect(page.locator('.user-balance-section')).toBeVisible({ timeout: 10000 });
});
```

### Mock API Responses

```typescript
await page.route('**/auth/player/login', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ token: 'mock-jwt-token' })
  });
});
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **angular** skill for component architecture patterns
- See the **typescript** skill for type definitions
- See the **jasmine** skill for unit testing (Playwright is for E2E only)