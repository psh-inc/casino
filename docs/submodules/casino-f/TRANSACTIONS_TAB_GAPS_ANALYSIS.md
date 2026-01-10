# Transactions Tab - Frontend-Backend Gaps Analysis

## Identified Gaps

### 1. **Missing Description Field in Backend Response**
- **Issue**: Transaction entity has `description` field, but `TransactionResponse` DTO doesn't include it
- **Impact**: Frontend displays "N/A" for description even when data exists
- **Location**: `PlayerService.getPlayerTransactions()` mapping

### 2. **Date Format Handling**
- **Issue**: Frontend sends ISO string from date picker, but date pickers typically return date-only values
- **Current**: `new Date(filters.startDate).toISOString()` - may include timezone issues
- **Backend**: Expects `LocalDateTime` but tries to parse ISO string directly
- **Impact**: Date filtering may not work correctly, especially with timezone differences

### 3. **Missing Status Filter**
- **Issue**: Frontend doesn't have status filter, but backend could support it
- **Impact**: Users cannot filter transactions by status (PENDING, COMPLETED, FAILED, etc.)
- **Backend**: Repository supports status filtering, but not exposed in endpoint

### 4. **Sorting Not Implemented**
- **Issue**: Frontend has Material table sorting (`matSort`) but doesn't send sort parameters to backend
- **Impact**: Sorting only works on client-side (current page), not server-side
- **Backend**: Supports sorting via Pageable, but frontend doesn't send sort params

### 5. **Reference Field Mapping**
- **Issue**: Backend returns `referenceId` and `referenceType` separately, frontend expects `reference`
- **Current**: Frontend shows `transaction.reference` but backend sends `referenceId`
- **Impact**: Reference information may not display correctly

### 6. **Amount Type Conversion**
- **Issue**: Frontend sends `number`, backend expects `BigDecimal`
- **Status**: Should work via Spring conversion, but explicit handling is better

### 7. **Date Parsing Edge Cases**
- **Issue**: Backend tries `LocalDateTime.parse(it)` which may fail for date-only strings
- **Impact**: Date filtering may fail silently or throw errors

## Fixes Required

1. ✅ Add `description` field to `TransactionResponse` DTO and mapping
2. ✅ Fix date format conversion in frontend (handle date-only vs datetime)
3. ✅ Add status filter to frontend UI and backend endpoint
4. ✅ Implement server-side sorting from frontend
5. ✅ Fix reference field mapping (use referenceId as reference)
6. ✅ Improve date parsing in backend to handle both date and datetime strings
7. ✅ Add proper error handling for invalid date formats

