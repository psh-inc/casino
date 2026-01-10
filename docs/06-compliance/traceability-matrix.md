# Compliance Traceability Matrix - Anjouan

| Requirement | Control | Evidence | Code/Doc Reference |
| --- | --- | --- | --- |
| Player identification and KYC | KYC workflow and document upload | KYC records; audit logs | casino-b/src/main/kotlin/com/casino/core/service/simple |
| Responsible gambling procedures | Limits, self-exclusion, reality checks | RG settings, logs | casino-b/src/main/kotlin/com/casino/core/service/responsible |
| Suspicious transaction reporting | AML workflows and transaction audit | SAR log; transaction history | casino-b/src/main/kotlin/com/casino/core/service, casino-b/src/main/kotlin/com/casino/core/domain/Transaction.kt |
| Reporting to Gaming Board | Admin reporting exports | Export logs | casino-b/src/main/kotlin/com/casino/core/controller/reporting |
| Advertising restrictions | CMS content controls | CMS audit logs | casino-b/src/main/kotlin/com/casino/core/domain/ContentAuditLog.kt |
| Systems supplier fit and proper | Vendor due diligence and approval | Procurement records | Non-code (vendor onboarding) |
| License renewal fees paid on time | Finance controls and reminders | Payment confirmations | Non-code (finance process) |
| No cash deposits or withdrawals | Payment method configuration and cashier flows | Payment method catalog; deposit/withdrawal logs | casino-b/src/main/kotlin/com/casino/core/domain/PaymentMethod.kt, casino-b/src/main/kotlin/com/casino/core/controller/PaymentMethodController.kt, casino-b/src/main/kotlin/com/casino/core/controller/WalletController.kt |
| Wagers cannot exceed deposited funds | Wallet balance checks on debits | Transaction logs; wallet balances | casino-b/src/main/kotlin/com/casino/core/service/WalletService.kt |
| Daily transaction and balance reporting | Admin reporting exports | Daily report exports | casino-b/src/main/kotlin/com/casino/core/controller/reporting |
| Service fee cap enforcement | Payment method fee configuration | Fee schedules; transaction fee logs | casino-b/src/main/kotlin/com/casino/core/domain/PaymentMethod.kt, casino-b/src/main/kotlin/com/casino/core/service/PaymentMethodService.kt |
