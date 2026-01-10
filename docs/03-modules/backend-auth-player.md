# Backend - Auth and Player Management

## Responsibilities

- Authentication and JWT issuance
- Registration and email/phone verification
- Password reset and 2FA
- Player profiles and admin updates

## Key controllers

- AuthController, PublicAuthController
- PublicRegistrationController
- PasswordResetController
- EmailVerificationController, PhoneVerificationController
- TwoFactorAuthController
- PlayerController, PlayerAdminController
- PlayerProfileFieldController, PlayerProfilePictureController
- PlayerCommentController, PlayerTag controllers

## Data model highlights

- Player entity with status, KYC state, activation steps
- Player tags, profile fields, and profile updates
- Login history and audit logs

## Dependencies

- PostgreSQL for player records
- Redis for cache
- SendGrid/Twilio for verification
