# Wallet API Documentation

This document summarizes wallet endpoints exposed by the backend.

## Base path

- /api/v1/players/{playerId}/wallet

## Endpoints

### Get wallet summary

- GET /api/v1/players/{playerId}/wallet/summary
- Response: wallet balances and status

### Manual deposit (admin)

- POST /api/v1/players/{playerId}/wallet/manual-deposit
- Requires admin authorization

### Withdraw

- POST /api/v1/players/{playerId}/wallet/withdraw
- Creates a withdrawal request

### Transaction history

- GET /api/v1/players/{playerId}/transactions
- Returns paginated transaction list

## Notes

- Amounts are represented as decimal with BigDecimal in backend.
- Wallet supports real, bonus, and locked balances.
- See Swagger UI for full request/response schemas.
