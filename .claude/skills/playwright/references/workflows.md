# Playwright Workflows

Common testing workflows for the casino customer frontend.

## Test File Organization

```
casino-customer-f/
├── e2e/
│   ├── auth.spec.ts              # Authentication flows
│   ├── games-listing.spec.ts     # Games page tests
│   ├── test-profile.spec.ts      # Profile management
│   ├── test-kyc-dashboard.spec.ts # KYC verification
│   └── test-persistent-login.spec.ts # Session management
├── playwright.config.ts
└── package.json
```

## Authentication Test Workflow

### Complete Login Flow

```typescript
test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:4201');
  });

  test('should login and verify session', async ({ page }) => {
    // Open modal
    await page.getByRole('button', { name: 'Login' }).first().click();
    await expect(page.locator('.auth-modal-backdrop')).toBeVisible();
    
    // Fill credentials
    await page.locator('input[formControlName="username"]').fill('testplayer');
    await page.locator('input[formControlName="password"]').fill('Test1234');
    await page.locator('button[type="submit"]').click();
    
    // Verify logged in state
    await expect(page.locator('.auth-modal-backdrop')).not.toBeVisible({ timeout: 10000 });
    await expect(page.locator('.user-balance-section')).toBeVisible();
    await expect(page.locator('.user-menu-toggle .username')).toContainText('testplayer');
  });
});
```

### Persistent Login Testing

```typescript
test('should maintain session after reload', async ({ page }) => {
  // Login
  await loginUser(page, 'testplayer', 'Test1234');
  
  // Verify logged in
  await expect(page.locator('.user-balance-section')).toBeVisible();
  
  // Reload and verify session persists
  await page.reload();
  await page.waitForTimeout(2000);
  
  await expect(page.locator('.user-balance-section')).toBeVisible();
  await expect(page.locator('.user-menu-toggle .username')).toBeVisible();
});
```

## WARNING: Sharing State Between Tests

**The Problem:**

```typescript
// BAD - Tests depend on execution order
let authToken: string;

test('should login', async ({ page }) => {
  // Login and save token
  authToken = await page.evaluate(() => localStorage.getItem('accessToken'));
});

test('should use token', async ({ page }) => {
  // Fails if first test didn't run
  await page.evaluate(t => localStorage.setItem('accessToken', t), authToken);
});
```

**Why This Breaks:**
1. Tests must run in specific order
2. Parallel execution impossible
3. Single test failure cascades

**The Fix:**

```typescript
// GOOD - Each test is independent
test.describe.serial('Sequential tests', () => {
  let authToken: string;
  
  test.beforeAll(async ({ page }) => {
    // Setup shared state in beforeAll
    await loginAndGetToken(page);
  });
});

// Or use test fixtures
test('should access protected route', async ({ page }) => {
  await page.goto('http://localhost:4201');
  await page.evaluate(({ token }) => {
    localStorage.setItem('accessToken', token);
  }, { token: 'valid-jwt-token' });
  
  await page.goto('http://localhost:4201/account/profile');
});
```

## API Testing Workflow

```typescript
test.describe('Games API Tests', () => {
  test('should fetch games from public API', async ({ request }) => {
    const response = await request.get('http://localhost:8080/api/public/games');
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data).toHaveProperty('games');
    expect(data).toHaveProperty('total');
    expect(Array.isArray(data.games)).toBeTruthy();
  });

  test('should filter games by category', async ({ request }) => {
    const response = await request.get('http://localhost:8080/api/public/games?type=SLOTS');
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data).toHaveProperty('games');
  });
});
```

## Multi-Step Form Testing (Registration)

```typescript
test('should complete multi-step registration', async ({ page }) => {
  await page.getByRole('button', { name: 'Register' }).first().click();
  await page.waitForSelector('.step-title');
  
  // Step 1: Account Information
  await expect(page.locator('.step-title')).toContainText('Account Information');
  await page.locator('input#field-1').fill('testuser123');
  await page.locator('input#field-2').fill('test@example.com');
  await page.locator('input#field-3').fill('TestPassword123!');
  await page.locator('input#field-4').fill('TestPassword123!');
  await page.getByRole('button', { name: 'Next' }).click();
  
  // Step 2: Personal Information
  await expect(page.locator('.step-title')).toContainText('Personal Information');
  await page.locator('input#field-5').fill('1990-01-01');
  await page.getByRole('button', { name: 'Next' }).click();
  
  // Step 3: Terms
  await expect(page.locator('.step-title')).toContainText('Terms & Conditions');
  await page.locator('input#field-6').check();
  
  await expect(page.getByRole('button', { name: 'Create Account' })).toBeVisible();
});
```

## Network Request Monitoring

```typescript
test.describe.serial('Admin Bonus Creation', () => {
  let bonusCreationResponse: any = null;

  test.beforeAll(async ({ browser }) => {
    const page = await browser.newPage();
    
    // Monitor API responses
    page.on('response', async (response) => {
      if (response.url().includes('/api/') && response.url().includes('/bonus')) {
        bonusCreationResponse = {
          status: response.status(),
          body: await response.json().catch(() => null)
        };
      }
    });
    
    // Monitor failures
    page.on('requestfailed', (request) => {
      console.log(`Request failed: ${request.url()}`);
    });
  });
});
```

## Screenshot Workflow

```typescript
test('should capture KYC dashboard', async ({ page }) => {
  await page.goto('http://localhost:4201/kyc');
  
  // Full page screenshot
  await page.screenshot({ path: 'kyc-dashboard.png', fullPage: true });
  
  // Element screenshot
  const progressSection = page.locator('.progress-section');
  await progressSection.screenshot({ path: 'kyc-progress.png' });
});
```

## WARNING: Not Using baseURL

**The Problem:**

```typescript
// BAD - Hardcoded URLs everywhere
test('test 1', async ({ page }) => {
  await page.goto('http://localhost:4201/games');
});

test('test 2', async ({ page }) => {
  await page.goto('http://localhost:4201/profile');
});
```

**The Fix:**

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    baseURL: 'http://localhost:4201',
  },
});

// In tests - use relative URLs
test('test 1', async ({ page }) => {
  await page.goto('/games');
});
```

## Configuration Reference

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:4201',
    trace: 'on-first-retry',
  },
  
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
  ],
  
  webServer: [
    {
      command: 'npm run start -- --port 4201',
      url: 'http://localhost:4201',
      reuseExistingServer: !process.env.CI,
      timeout: 120 * 1000,
    },
    {
      command: 'cd ../casino-b && ./gradlew bootRun',
      url: 'http://localhost:8080',
      reuseExistingServer: !process.env.CI,
    }
  ],
});
```