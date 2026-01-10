# Backend - Responsible Gambling and KYC

## Responsibilities

- Simple KYC flow and document handling
- Responsible gambling limits and self-exclusion
- Compliance settings and reporting

## Key controllers

- PlayerSimpleKycController, AdminSimpleKycController
- PlayerLimitController, AdminLimitController
- SelfExclusionController, AdminSelfExclusionController
- ComplianceSettingsController

## Data model highlights

- PlayerLimit, SelfExclusion, PlayerRisk, RealityCheck
- Compliance settings and events

## Dependencies

- Object storage for KYC documents
- Kafka compliance topics
- Scheduled jobs for KYC monitoring
