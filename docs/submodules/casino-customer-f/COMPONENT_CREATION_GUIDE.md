# Casino Customer Frontend - Component Creation Guide

## Project Structure Analysis

### 1. Technology Stack
- **Framework**: Angular 17+ with standalone components
- **Language**: TypeScript
- **Styling**: SCSS with Tailwind CSS
- **State Management**: RxJS (BehaviorSubjects and Observables)
- **HTTP Client**: Angular HttpClient with interceptors
- **Authentication**: JWT-based with refresh tokens
- **Material UI**: Angular Material for dialogs and UI components

### 2. Application Architecture

```
src/app/
├── core/                    # Core functionality (singleton services)
│   ├── components/         # Layout components (header, footer, etc.)
│   ├── constants/          # App-wide constants
│   ├── guards/            # Route guards (auth.guard.ts)
│   ├── interceptors/      # HTTP interceptors
│   ├── models/            # Core data models
│   └── services/          # Singleton services
├── features/              # Feature modules (lazy loaded)
│   ├── home/             # Home page feature
│   ├── games/            # Games feature
│   ├── promotions/       # Promotions feature
│   ├── account/          # Account management
│   └── kyc/              # KYC verification
├── shared/               # Shared components and utilities
│   ├── components/       # Reusable components
│   ├── widgets/          # Widget components
│   ├── ui/               # UI components (buttons, dropdowns)
│   └── services/         # Shared services
└── pages/                # Simple page components

```

## Authentication & Interceptors

### Authentication Flow
1. **JWT-based authentication** with access and refresh tokens
2. **AuthService** manages authentication state using BehaviorSubjects
3. **Auth Interceptor** automatically attaches JWT tokens to protected endpoints
4. **Token refresh** handled automatically on 401 responses
5. **Protected routes** use `authGuard` for route protection

### HTTP Interceptors Chain
```typescript
withInterceptors([
  translationInterceptor,  // Adds translation headers
  authInterceptor,        // Adds JWT token
  errorInterceptor,       // Global error handling
  loadingInterceptor      // Loading indicator management
])
```

## Creating New Pages/Components

### 1. Standalone Component Pattern

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subject, takeUntil } from 'rxjs';
// Import required services
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-my-feature',
  standalone: true,
  imports: [CommonModule, /* other imports */],
  templateUrl: './my-feature.component.html',
  styleUrl: './my-feature.component.scss'
})
export class MyFeatureComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  loading = false;
  error: string | null = null;
  
  constructor(
    private authService: AuthService
  ) {}
  
  ngOnInit(): void {
    this.loadData();
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  private loadData(): void {
    this.loading = true;
    // Implementation
  }
}
```

### 2. Service Pattern

```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '@environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MyService {
  private apiUrl = `${environment.apiUrl}/api/v1/my-endpoint`;
  
  // State management
  private dataSubject = new BehaviorSubject<any[]>([]);
  public data$ = this.dataSubject.asObservable();
  
  constructor(private http: HttpClient) {}
  
  getData(filters?: any): Observable<any> {
    let params = new HttpParams();
    // Add parameters
    
    return this.http.get<any>(this.apiUrl, { params }).pipe(
      map(response => response.data),
      catchError(this.handleError)
    );
  }
  
  private handleError(error: any): Observable<never> {
    console.error('API Error:', error);
    throw error;
  }
}
```

### 3. Adding Routes

```typescript
// In app.routes.ts
{
  path: 'my-feature',
  loadComponent: () => import('./features/my-feature/my-feature.component')
    .then(m => m.MyFeatureComponent),
  canActivate: [authGuard]  // Add if authentication required
}

// For feature with child routes
{
  path: 'my-feature',
  loadChildren: () => import('./features/my-feature/my-feature.routes')
    .then(m => m.myFeatureRoutes),
  canActivate: [authGuard]
}
```

## API Integration Patterns

### 1. Public vs Protected Endpoints
- **Public endpoints**: No authentication required (e.g., `/api/v1/public/*`)
- **Protected endpoints**: Require JWT token (automatically added by auth interceptor)

### 2. Error Handling
```typescript
this.myService.getData().subscribe({
  next: (data) => {
    this.data = data;
    this.loading = false;
  },
  error: (error) => {
    console.error('Error loading data:', error);
    this.error = error.userMessage || 'Failed to load data';
    this.loading = false;
  }
});
```

### 3. Loading States
Use `LoadingSpinnerComponent` for loading indicators:
```typescript
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

// In template
<app-loading-spinner *ngIf="loading"></app-loading-spinner>
```

## Common UI Components

### 1. Reusable Components
- **LoadingSpinnerComponent**: Loading indicator
- **ErrorDisplayComponent**: Error message display
- **LucideIconComponent**: Icon component
- **EmailVerificationBannerComponent**: Email verification prompt

### 2. Widget System
- **WidgetRendererComponent**: Renders CMS widgets dynamically
- Widget types: `BANNER_SECTION`, `GAMES_LIST`, `PROMO_NEWS`, `RICH_TEXT`, etc.

### 3. Material Dialog Pattern
```typescript
import { MatDialog } from '@angular/material/dialog';

constructor(private dialog: MatDialog) {}

openDialog(): void {
  const dialogRef = this.dialog.open(MyDialogComponent, {
    width: '600px',
    data: { /* pass data */ }
  });
  
  dialogRef.afterClosed().subscribe(result => {
    // Handle result
  });
}
```

## Best Practices

### 1. Memory Management
- Always unsubscribe using `takeUntil(destroy$)` pattern
- Use `async` pipe in templates when possible

### 2. Change Detection
- Use `ChangeDetectionStrategy.OnPush` for performance
- Use `BehaviorSubject` for state management

### 3. Type Safety
- Define interfaces for all API responses
- Use strict typing for component inputs/outputs

### 4. Error Handling
- Use global error interceptor for API errors
- Provide user-friendly error messages
- Log errors for debugging

### 5. Authentication
- Protected routes should use `authGuard`
- Check `isAuthenticated$` observable for auth state
- Handle token expiration gracefully

## Example: Creating a New Feature Page

### Step 1: Create Component
```bash
# Create new feature directory
mkdir -p src/app/features/my-feature/components
```

### Step 2: Create Component File
```typescript
// my-feature.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { MyFeatureService } from './services/my-feature.service';

@Component({
  selector: 'app-my-feature',
  standalone: true,
  imports: [CommonModule, LoadingSpinnerComponent],
  templateUrl: './my-feature.component.html',
  styleUrl: './my-feature.component.scss'
})
export class MyFeatureComponent implements OnInit {
  data$ = this.service.data$;
  loading = false;
  
  constructor(private service: MyFeatureService) {}
  
  ngOnInit(): void {
    this.loadData();
  }
  
  private loadData(): void {
    this.loading = true;
    this.service.loadData().subscribe({
      next: () => this.loading = false,
      error: () => this.loading = false
    });
  }
}
```

### Step 3: Add Route
```typescript
// app.routes.ts
{
  path: 'my-feature',
  loadComponent: () => import('./features/my-feature/my-feature.component')
    .then(m => m.MyFeatureComponent)
}
```

### Step 4: Create Service
```typescript
// services/my-feature.service.ts
@Injectable({ providedIn: 'root' })
export class MyFeatureService {
  private apiUrl = `${environment.apiUrl}/api/v1/my-feature`;
  private dataSubject = new BehaviorSubject<any[]>([]);
  public data$ = this.dataSubject.asObservable();
  
  constructor(private http: HttpClient) {}
  
  loadData(): Observable<any> {
    return this.http.get<any>(this.apiUrl).pipe(
      tap(data => this.dataSubject.next(data))
    );
  }
}
```

## Testing Checklist

- [ ] Component renders without errors
- [ ] API calls work with authentication
- [ ] Error states handled properly
- [ ] Loading states display correctly
- [ ] Unsubscribe on component destroy
- [ ] Route guards work as expected
- [ ] Responsive design works
- [ ] Accessibility requirements met