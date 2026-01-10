# Backend - Wallet and Payments

## Responsibilities

- Multi-currency wallet balances
- Deposits and withdrawals
- Transaction history and auditing
- Cashier sessions and payment webhooks

## Key controllers

- WalletController
- TransactionAdminController
- PaymentAdminController, CustomerPaymentController
- PaymentMethodController, PaymentMethodAdminController
- CashierWebhookController, PaymentWebhookController
- RefundAdminController
- DepositWageringController

## Data model highlights

- Wallets with real, bonus, and locked balances
- Transactions and wagering transactions
- Cashier sessions

## Dependencies

- Payment provider APIs
- Kafka events (payment domain)
- PostgreSQL for wallet/transaction persistence
