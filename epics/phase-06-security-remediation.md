# Epic: Phase 06 - Security Remediation

## Objective

Address critical security gaps identified in CODE_REVIEW_SECURITY_ASSESSMENT_2025-12-14.md.

## Stories

- STORY-SEC-001: Remove secrets from repo and rotate keys
- STORY-SEC-002: Enforce provider authentication for balance-changing endpoints
- STORY-SEC-003: Secure WebSocket authentication and player identity binding
- STORY-SEC-004: Redact sensitive request/response logs
- STORY-SEC-005: Store KYC assets privately and use signed URLs

## Acceptance criteria

- No hard-coded secrets in repo
- Provider and WebSocket endpoints require auth
- Logging excludes sensitive payloads
- KYC assets are not publicly accessible
