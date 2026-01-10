# Player Profile Page - Account History & Bet History Analysis

## Overview
This document analyzes the player management profile page in the admin panel (`cadmin`), specifically focusing on the **Account History** and **Bet History** tabs.

## Component Structure

### Main Profile Component
- **Location**: `cadmin/src/app/modules/player-management/player-details/player-details.component.ts`
- **Template**: `player-details.component.html`
- **Tabs Structure**: The profile page uses Material tabs with the following structure:
  - Profile Tab (index 0)
  - Wallet Tab (index 1)
  - **Account History Tab (index 2)** ← Focus of analysis
  - **Bet History Tab (index 3)** ← Focus of analysis
  - Game History Tab
  - Wagering Progress Tab
  - And more...

### Account History Tab Component
- **Component**: `PlayerAccountHistoryComponent`
- **Location**: `cadmin/src/app/modules/player-management/player-account-history/`
- **Selector**: `<app-player-account-history>`
- **Input**: `playerId` (number)

### Bet History Tab Component
- **Component**: `PlayerBetHistoryComponent`
- **Location**: `cadmin/src/app/modules/player-management/player-bet-history/`
- **Selector**: `<app-player-bet-history>`
- **Input**: `playerId` (number)

---

## 1. ACCOUNT HISTORY TAB

### Data Displayed

The Account History tab displays **all wallet transactions** for a player, including:

#### Table Columns:
1. **ID** - Transaction ID
2. **Type** - Transaction type (see types below)
3. **Amount** - Transaction amount with currency
4. **Date** - Creation timestamp
5. **Status** - Transaction status (using status chip component)
6. **Description** - Transaction description with optional reference

#### Transaction Types Supported:
- `DEPOSIT` - Player deposits
- `WITHDRAWAL` - Player withdrawals
- `GAME_BET` - Game betting transactions
- `GAME_WIN` - Game winning transactions
- `ADJUSTMENT` - Manual adjustments
- `JACKPOT_WIN` - Jackpot wins
- `GAME_OTHER` - Other game-related transactions
- `BATCH_UPDATE` - Batch updates
- `BONUS_CREDIT` - Bonus credits
- `SPORTS_BET` - Sports betting
- `SPORTS_WIN` - Sports winnings
- `SPORTS_REFUND` - Sports refunds
- `SPORTS_ROLLBACK` - Sports rollbacks
- `BONUS_BET` - Bonus bets
- `BONUS_WIN` - Bonus wins
- `BONUS_CONVERSION` - Bonus conversions
- `BONUS_EXPIRED` - Expired bonuses
- `BONUS_AWARDED` - Bonus awards

### Filtering Capabilities

The component provides an expandable filter panel with:

1. **Date Range Filter**
   - Start Date (date picker)
   - End Date (date picker)

2. **Type Filter**
   - Dropdown with all transaction types
   - "All Types" option to clear filter

3. **Amount Range Filter**
   - Min Amount (number input)
   - Max Amount (number input)

4. **Filter Actions**
   - Clear button - Resets all filters
   - Apply button - Applies filters (auto-applies on form change with debounce)

### Features

- **Pagination**: Material paginator with page size options (5, 10, 20, 50, 100)
- **Sorting**: Sortable columns (ID, Type, Amount, Date, Status)
- **Export**: Export button for CSV download
- **Auto-refresh**: Filters auto-apply with 500ms debounce
- **Visual Indicators**:
  - Credit transactions (deposits, wins) styled with `transaction-credit` class
  - Debit transactions (withdrawals, bets) styled with `transaction-debit` class

### Backend API

#### Endpoint
```
GET /api/players/{playerId}/transactions
```

#### Request Parameters
- `page` (default: 0) - Page number
- `size` (default: 20) - Page size
- `startDate` (optional) - ISO date string
- `endDate` (optional) - ISO date string
- `type` (optional) - TransactionType enum value
- `minAmount` (optional) - BigDecimal
- `maxAmount` (optional) - BigDecimal

#### Response Structure
```typescript
interface PlayerTransactions {
  playerId: number;
  username: string;
  transactions: {
    content: Transaction[];
    page: number;
    size: number;
    totalElements: number;
    totalPages: number;
    last: boolean;
  };
}

interface Transaction {
  id: number;
  type: string;
  amount: string;
  currency: string;
  status: string;
  createdAt: string;
  description?: string;
  reference?: string;
}
```

#### Backend Implementation
- **Controller**: `PlayerController.getPlayerTransactions()`
- **Service**: `PlayerService.getPlayerTransactions()`
- **Repository**: `TransactionRepository.findByWalletIdWithFilters()`
- **Security**: Requires `ADMIN` authority or player accessing their own data
- **Sorting**: Default sort by `createdAt DESC`

---

## 2. BET HISTORY TAB

### Data Displayed

The Bet History tab displays **game-specific transactions** (bets and wins) with detailed game information:

#### Table Columns:
1. **ID** - Transaction ID
2. **Type** - Transaction type (GAME_BET, GAME_WIN, BONUS_BET, BONUS_WIN)
3. **Game Name** - Name of the game
4. **Game Type** - Type/category of the game
5. **Provider** - Game provider name
6. **Amount** - Transaction amount with currency
7. **Balance Before** - Player balance before transaction
8. **Balance After** - Player balance after transaction
9. **Date** - Creation timestamp
10. **Status** - Transaction status (using status chip component)

### Filtering Capabilities

The component provides an expandable filter panel with:

1. **Transaction Category Filter**
   - Dropdown: `ALL`, `BET`, `WIN`
   - Filters by transaction type (BET includes GAME_BET and BONUS_BET, WIN includes GAME_WIN and BONUS_WIN)

2. **Game Filter**
   - Game ID (text input) - Filter by specific game ID

3. **Provider Filter**
   - Provider Code (text input) - Filter by game provider code

4. **Date Range Filter**
   - Start Date (date picker)
   - End Date (date picker)

5. **Amount Range Filter**
   - Min Amount (number input)
   - Max Amount (number input)

6. **Filter Actions**
   - Clear button - Resets all filters
   - Apply button - Applies filters (auto-applies on form change with debounce)

### Features

- **Pagination**: Material paginator with page size options (5, 10, 20, 50, 100)
- **Sorting**: Sortable columns (ID, Type, Game Name, Game Type, Provider, Amount, Balance Before, Balance After, Date, Status)
- **Export**: Export button for CSV download
- **Auto-refresh**: Filters auto-apply with 500ms debounce
- **Visual Indicators**:
  - WIN transactions styled with `transaction-credit` class
  - BET transactions styled with `transaction-debit` class
- **Game Context**: Shows game information (name, type, provider) for each transaction

### Backend API

#### Endpoint
```
GET /api/players/{playerId}/game-transactions
```

#### Request Parameters
- `page` (default: 0) - Page number
- `size` (default: 20) - Page size
- `transactionCategory` (optional) - `BET`, `WIN`, or `ALL`
- `gameId` (optional) - String game ID
- `providerCode` (optional) - Provider code string
- `startDate` (optional) - ISO date string
- `endDate` (optional) - ISO date string
- `minAmount` (optional) - BigDecimal
- `maxAmount` (optional) - BigDecimal

#### Response Structure
```typescript
interface PlayerBetHistory {
  playerId: number;
  username: string;
  transactions: {
    content: BetHistory[];
    page: number;
    size: number;
    totalElements: number;
    totalPages: number;
    last: boolean;
  };
}

interface BetHistory {
  id: number;
  uuid: string;
  amount: string;
  currency: string;
  type: string;  // GAME_BET, GAME_WIN, BONUS_BET, BONUS_WIN
  status: string;
  balanceBefore: string;
  balanceAfter: string;
  gameId?: string;
  gameName?: string;
  gameType?: string;
  providerName?: string;
  providerCode?: string;
  gameRoundId?: number;
  createdAt: string;
}
```

#### Backend Implementation
- **Controller**: `PlayerController.getPlayerBetHistory()`
- **Service**: `PlayerService.getPlayerBetHistory()`
- **Repository**: `TransactionRepository.findGameTransactionsByPlayerId()`
- **Security**: Requires `ADMIN` or `CMS_ADMIN` authority
- **Filtering Strategy**:
  - Initial fetch gets all game transactions for the player
  - Filtering by category, gameId, providerCode, dates, and amounts is done **in memory** (to avoid SQL type inference issues)
  - This means pagination happens after filtering, which may affect performance for large datasets

### Key Differences from Account History Tab

1. **Scope**: Bet History only shows game-related transactions (GAME_BET, GAME_WIN, BONUS_BET, BONUS_WIN), while Account History shows ALL wallet transactions
2. **Game Context**: Bet History includes game information (name, type, provider) and game round ID
3. **Balance Tracking**: Bet History shows balance before and after each transaction
4. **Filtering**: Bet History has additional filters for game ID and provider code
5. **Category Filter**: Bet History uses a simplified category filter (BET/WIN/ALL) instead of full transaction type list

---

## Service Layer

### Frontend Service
- **Service**: `PlayersService`
- **Location**: `cadmin/src/app/modules/player-management/players.service.ts`

#### Methods Used:

1. **getPlayerTransactions()**
   ```typescript
   getPlayerTransactions(
     playerId: number,
     page: number = 0,
     size: number = 20,
     startDate?: string,
     endDate?: string,
     type?: string,
     minAmount?: number,
     maxAmount?: number
   ): Observable<PlayerTransactions>
   ```
   - Calls: `GET /api/players/{playerId}/transactions`

2. **getPlayerBetHistory()**
   ```typescript
   getPlayerBetHistory(
     playerId: number,
     page: number = 0,
     size: number = 20,
     transactionCategory?: string,
     gameId?: string,
     providerCode?: string,
     startDate?: string,
     endDate?: string,
     minAmount?: number,
     maxAmount?: number
   ): Observable<PlayerBetHistory>
   ```
   - Calls: `GET /api/players/{playerId}/game-transactions`

---

## Data Flow

### Account History Tab Flow:
1. Component receives `playerId` as `@Input()`
2. On init/change, calls `loadData()`
3. Service method `getPlayerTransactions()` builds HTTP params
4. HTTP GET request to `/api/players/{playerId}/transactions`
5. Backend `PlayerController` receives request
6. `PlayerService.getPlayerTransactions()` fetches from repository
7. `TransactionRepository.findByWalletIdWithFilters()` queries database
8. Response mapped to DTOs and returned
9. Frontend receives `PlayerTransactions` response
10. Component updates `transactions` array and pagination data
11. Material table displays data

### Bet History Tab Flow:
1. Component receives `playerId` as `@Input()`
2. On init/change, calls `loadData()`
3. Service method `getPlayerBetHistory()` builds HTTP params
4. HTTP GET request to `/api/players/{playerId}/game-transactions`
5. Backend `PlayerController` receives request
6. `PlayerService.getPlayerBetHistory()`:
   - Fetches all game transactions for player
   - Applies in-memory filters (category, gameId, providerCode, dates, amounts)
7. Response mapped to DTOs with game information
8. Frontend receives `PlayerBetHistory` response
9. Component updates `betHistory` array and pagination data
10. Material table displays data

---

## Performance Considerations

### Account History Tab:
- ✅ Database-level filtering (efficient)
- ✅ Pagination at database level
- ✅ Indexed queries on wallet_id, type, created_at

### Bet History Tab:
- ⚠️ In-memory filtering after fetching (may be inefficient for large datasets)
- ⚠️ Pagination happens after filtering (total count may be inaccurate)
- ✅ Uses LEFT JOIN to fetch game details in single query
- ⚠️ Consider moving filtering to database level for better performance

---

## Security

### Account History Tab:
- **Authorization**: `@PreAuthorize("hasAnyAuthority('PLAYER') and #id == authentication.principal.username or hasAnyAuthority('ADMIN')")`
- Players can only view their own transactions, admins can view any player's transactions

### Bet History Tab:
- **Authorization**: `@PreAuthorize("hasAnyAuthority('ADMIN', 'CMS_ADMIN')")`
- Only admin users can access bet history (more sensitive data)

---

## Future Enhancements

1. **Real-time Updates**: Consider WebSocket integration for live transaction updates
2. **Advanced Filtering**: Add more filter options (status, reference ID, etc.)
3. **Bulk Actions**: Add ability to perform bulk operations on transactions
4. **Transaction Details Modal**: Click on transaction to see full details
5. **Performance Optimization**: Move bet history filtering to database level

---

## Summary

### Account History Tab:
- Shows **all wallet transactions** (deposits, withdrawals, game transactions, bonuses, sports, etc.)
- 6 columns: ID, Type, Amount, Date, Status, Description
- Filters: Date range, Type, Amount range
- API: `GET /api/players/{id}/transactions`
- Access: Admin or player (own data)

### Bet History Tab:
- Shows **only game-related transactions** (bets and wins) with game context
- 10 columns: ID, Type, Game Name, Game Type, Provider, Amount, Balance Before, Balance After, Date, Status
- Filters: Category (BET/WIN/ALL), Game ID, Provider Code, Date range, Amount range
- API: `GET /api/players/{id}/game-transactions`
- Access: Admin only
- Includes balance tracking and game information

Both tabs use Material Design components, support pagination, sorting, and filtering, with auto-refresh on filter changes.

