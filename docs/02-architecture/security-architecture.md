# Security Architecture

## Authentication and authorization

- JWT authentication for API requests (OAuth2 Resource Server)
- Role-based access control for admin endpoints
- Two-factor authentication support (TOTP)

## Sensitive data handling

- Passwords hashed via BCrypt/Argon2
- KYC document storage via object storage (see MediaAssetService)
- PII should not be logged

## Known security gaps (from code review)

- Secrets committed to repo (application.yml, keys)
- Provider authentication disabled in ProviderSecurityService
- WebSocket endpoints allow unauthenticated access and client-supplied playerId
- Request/response logging includes sensitive data
- KYC assets stored with public read ACLs

See CODE_REVIEW_SECURITY_ASSESSMENT_2025-12-14.md for full details and remediation steps.

## Required remediation (short list)

- Remove secrets from repo and rotate keys
- Enforce provider auth with HMAC and replay protection
- Require JWT on WebSocket connect and bind playerId to principal
- Redact sensitive request/response logs
- Store KYC assets privately and use signed URLs
