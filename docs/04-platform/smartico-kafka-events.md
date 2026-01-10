# Smartico Kafka Events

This document lists all Smartico Kafka topics and payload schemas as defined in code.

## Source Files

- `casino-b/src/main/kotlin/com/casino/core/kafka/constants/KafkaTopics.kt`
- `casino-b/src/main/kotlin/com/casino/core/kafka/events/**/*`
- `casino-b/src/main/kotlin/com/casino/core/kafka/service/*EventService.kt`
- `casino-b/src/main/kotlin/com/casino/core/kafka/util/SmarticoStatusMapper.kt`

Note: `casino.engagement.login.v1`, `casino.engagement.logout.v1`, and `casino.compliance.reality-check.v1` are defined as literal topic strings in `EngagementEventService` and `ComplianceEventService` (not in `KafkaTopics`).

## Base Event Envelope

All events extend `BaseEvent`:
- `eventId` (string)
- `eventType` (string, e.g., `casino.player.registered.v1`)
- `eventTimestamp` (ISO-8601 UTC string)
- `eventVersion` (string, default `1.0`)
- `brandId` (string)
- `userId` (string)
- `sessionId` (string, optional)
- `metadata` (`EventMetadata`)

`EventMetadata`:
- `sourceSystem` (string, default `casino-core`)
- `environment` (string, e.g., development/staging/production)
- `ipAddress` (string, optional)
- `userAgent` (string, optional)
- `country` (string, optional)
- `language` (string, optional)
- `correlationId` (string, optional)
- `deviceType` (string, optional)
- `platform` (string, optional)

## Topics and Payload Schemas

### Player Domain

Topic: `casino.player.registered.v1`
- Payload: `PlayerRegisteredPayload`
  - username, email, firstName, lastName, dateOfBirth, phoneNumber
  - registrationIp, walletCurrency, language, country
  - affiliateId, signUpCode
  - marketingOptIn, emailMarketing, smsMarketing, pushNotifications
  - registrationSource, registrationDevice
  - user_ext_id, ext_brand_id, dt_update
  - core_registration_date, core_account_status, core_user_language, core_wallet_currency, core_username
  - user_birthdate, user_country, user_email, user_phone
  - user_first_name, user_last_name, core_affiliate_id
  - core_is_email_disabled_by_platform, core_is_sms_disabled_by_platform
  - core_kyc_status

Topic: `casino.player.profile-updated.v1`
- Payload: `PlayerProfileUpdatedPayload`
  - updatedFields (map)
  - previousValues (map, optional)
  - updateReason
  - user_ext_id, ext_brand_id, dt_update
  - core_account_status, core_user_language, core_username, core_kyc_status

Topic: `casino.player.status-changed.v1`
- Payload: `PlayerStatusChangedPayload`
  - previousStatus, newStatus
  - reason, triggeredBy, expiresAt, notes

Topic: `casino.player.authenticated.v1`
- Payload: `PlayerAuthenticatedPayload`
  - username
  - loginMethod
  - twoFactorUsed
  - device, platform
  - isNewDevice, lastLoginAt

Topic: `casino.player.session-started.v1` and `casino.player.session-ended.v1`
- Payload: `PlayerSessionPayload`
  - sessionId
  - sessionStartTime, sessionEndTime
  - sessionDurationSeconds
  - device, platform
  - gamesPlayed
  - totalBets, totalWins, netResult

### Payment Domain

Topic: `casino.payment.deposit-created.v1`, `casino.payment.deposit-completed.v1`, `casino.payment.deposit-failed.v1`
- Payload: `DepositPayload`
  - paymentId, transactionId
  - amount, currency
  - originalAmount, originalCurrency, exchangeRate
  - paymentMethod, paymentProvider, providerTransactionId
  - status, declineReason
  - processingFeeAmount, processingFeeCurrency
  - isFirstDeposit, depositNumber
  - bonusEligible, bonusCode
  - walletBalanceBefore, walletBalanceAfter
  - user_ext_id, ext_brand_id, dt_finalized, deposit_status
  - payment_method, provider_name, deposit_code

Topic: `casino.payment.withdrawal-created.v1`, `casino.payment.withdrawal-completed.v1`, `casino.payment.withdrawal-failed.v1`
- Payload: `WithdrawalPayload`
  - paymentId, transactionId
  - amount, currency
  - paymentMethod, paymentProvider, providerTransactionId
  - status, declineReason
  - processingFeeAmount
  - kycRequired, kycStatus, verificationLevel
  - isFirstWithdrawal, withdrawalNumber
  - walletBalanceBefore, walletBalanceAfter
  - estimatedProcessingTime
  - user_ext_id, ext_brand_id, dt_finalized, withdrawal_status
  - withdrawal_method, provider_name

Topic: `casino.payment.refund-processed.v1`
- Uses `DepositEvent` / `WithdrawalEvent` publish flow in services with refund status mapping.

### Game Domain

Topic: `casino.game.session-started.v1`
- Payload: `GameSessionStartedPayload`
  - gameSessionId, gameId, gameName
  - gameType, gameProvider
  - currency, walletBalance
  - deviceType, platform
  - activeBonusId
  - isFreeSpins, freeSpinsRemaining
  - timestamp

Topic: `casino.game.bet-placed.v1`
- Payload: `BetPlacedPayload`
  - gameSessionId, gameRoundId
  - gameId, gameName, gameType, gameProvider
  - betAmount, currency
  - betType, betDetails
  - walletBalanceBefore, walletBalanceAfter
  - bonusBalanceUsed, freespinUsed
  - jackpotContribution
  - roundNumber, timestamp
  - user_ext_id, ext_brand_id, bet_date
  - bet_amount_real, bet_amount_bonus
  - game_name, game_id, game_category, game_provider
  - casino_game_ext_id, casino_game_type_ext_id, casino_game_provider_ext_id

Topic: `casino.game.win-awarded.v1`
- Payload: `BetWinPayload`
  - gameSessionId, gameRoundId
  - gameId, gameName, gameType, gameProvider
  - betAmount, winAmount, currency, netResult
  - multiplier, winType
  - isJackpot, jackpotType, jackpotAmount
  - walletBalanceBefore, walletBalanceAfter
  - bonusBalanceAdded
  - roundNumber, timestamp
  - user_ext_id, ext_brand_id, bet_date
  - bet_amount_real, bet_amount_bonus
  - win_amount_real, win_amount_bonus
  - game_name, game_id, game_category, game_provider
  - casino_game_ext_id, casino_game_type_ext_id, casino_game_provider_ext_id

Topic: `casino.game.round-completed.v1`
- Payload: `GameRoundCompletedPayload`
  - gameSessionId, gameRoundId
  - gameId, gameName, gameType, gameProvider
  - roundNumber
  - betAmount, winAmount, currency, netResult
  - roundOutcome, roundDurationSeconds
  - walletBalanceBefore, walletBalanceAfter
  - bonusWageringProgress
  - roundStartTime, roundEndTime
  - gameSpecificData

Topic: `casino.game.jackpot-won.v1`
- Payload: `JackpotWinPayload`
  - gameSessionId, gameRoundId
  - gameId, gameName, gameProvider
  - jackpotId, jackpotName, jackpotType
  - jackpotAmount, currency
  - triggeringBetAmount
  - jackpotPoolBefore, jackpotPoolAfter
  - isProgressive, networkJackpot
  - playerUsername
  - walletBalanceBefore, walletBalanceAfter
  - timestamp

### Sports Domain

Topic: `casino.sports.bet-placed.v1`
- Payload: `SportsBetPlacedPayload`
  - betId, betType
  - betAmount, currency
  - totalOdds, potentialWin
  - selectionCount, selections
  - sport, isCashoutEligible, isLiveBet
  - walletBalanceBefore, walletBalanceAfter
  - activeBonusId
  - timestamp
  - user_ext_id, ext_brand_id
  - bet_date, bet_amount_real, bet_amount_bonus
  - sport_bet_ext_id, sport_bet_type, sport_bet_status
  - sport_name, freebet_id, is_live, total_odds_decimal

Selections in `SportsBetPlacedPayload`:
- eventId, eventName, market, selection, odds, eventStartTime, league
- selection_ext_id, event_ext_id, sport_id, category_id, tournament_id
- is_live_selection

Topic: `casino.sports.bet-settled.v1`
- Payload: `SportsBetSettledPayload`
  - betId, betType
  - betAmount, currency
  - totalOdds, settlementStatus
  - winAmount, netResult
  - selectionCount, selectionsSettled
  - sport, wasCashedOut, cashoutAmount
  - walletBalanceBefore, walletBalanceAfter
  - betPlacedAt, settledAt, timestamp
  - user_ext_id, ext_brand_id
  - bet_date, settlement_date
  - bet_amount_real, bet_amount_bonus
  - win_amount_real, win_amount_bonus
  - sport_bet_ext_id, sport_bet_type, sport_bet_status
  - sport_name, freebet_id, cashout_flag, total_odds_decimal, void_reason

Selections in `SportsBetSettledPayload`:
- eventId, eventName, market, selection, odds, status
- eventStartTime, eventSettledTime
- league, score
- selection_ext_id, event_ext_id, sport_id, category_id, tournament_id
- selection_status, is_live_selection

### Bonus Domain

Topic: `casino.bonus.offered.v1`
- Payload: `BonusOfferedPayload`
  - bonusId, bonusName, bonusType
  - bonusAmount, currency
  - wageringRequirement, wageringTarget
  - expiryDays, expiresAt
  - minimumDepositRequired
  - gameRestrictions
  - maxBetLimit
  - offeredReason, campaignId
  - timestamp

Topic: `casino.bonus.activated.v1`
- Payload: `BonusActivatedPayload`
  - bonusId, bonusName, bonusType
  - bonusAmount, currency
  - wageringTarget, wageringRemaining
  - activationDelay
  - timestamp

Topic: `casino.bonus.awarded.v1`
- Payload: `BonusAwardedPayload`
  - bonusId, bonusTemplateId, bonusName, bonusType
  - bonusAmount, currency
  - wageringRequirement, wageringTarget
  - bonusCode
  - triggerType, triggerEvent
  - eligibilityCriteria
  - validFrom, validUntil
  - maxWinCap
  - gameRestrictions
  - minDepositRequired
  - linkedDepositId
  - isFirstBonus
  - walletBalanceBefore
  - timestamp

Topic: `casino.bonus.wagering-updated.v1`
- Payload: `BonusWageringUpdatedPayload`
  - bonusId, bonusName, bonusType
  - wageringTarget, wageringCompleted, wageringRemaining
  - wageringPercentage
  - contributionAmount, betCount
  - lastBetAmount, lastBetGameId
  - currency
  - expiresAt, timeRemainingSeconds
  - updateReason
  - timestamp

Topic: `casino.bonus.wagering-completed.v1`
- Payload: `BonusCompletedPayload`
  - bonusId, bonusName, bonusType
  - originalBonusAmount, finalBonusBalance
  - convertedAmount, currency
  - wageringCompleted, wageringTarget
  - totalBetsCount, totalGamesPlayed
  - timeToComplete, conversionRate
  - maxWinCapApplied, cappedAmount
  - walletBalanceBefore, walletBalanceAfter
  - awardedAt, completedAt
  - timestamp

Topic: `casino.bonus.converted.v1`
- Payload: `BonusConvertedPayload`
  - bonusId, bonusName, bonusType
  - originalBonusAmount, finalConvertedAmount
  - conversionRate
  - wageringCompleted, wageringTarget
  - totalBetsPlaced
  - gamesPlayed
  - currency
  - activatedAt, convertedAt
  - durationDays
  - walletBalanceBefore, walletBalanceAfter
  - timestamp

Topic: `casino.bonus.forfeited.v1`
- Payload: `BonusForfeitedPayload`
  - bonusId, bonusName, bonusType
  - originalBonusAmount, remainingBonusBalance
  - currency
  - wageringCompleted, wageringRemaining
  - wageringPercentage
  - forfeitReason, forfeitedBy
  - timeActive, totalBetsCount
  - awardedAt, forfeitedAt
  - notes
  - timestamp

### Compliance Domain

Topic: `casino.compliance.kyc-submitted.v1`
- Payload: `KycSubmittedPayload`
  - requestId, verificationType
  - documentTypes, documentCount
  - verificationLevel
  - triggeredBy
  - triggerAmount, triggerCurrency
  - submittedAt

Topic: `casino.compliance.kyc-approved.v1`
- Payload: `KycApprovedPayload`
  - requestId, verificationType
  - previousLevel, newLevel
  - approvedBy
  - aiConfidenceScore
  - processingTimeSeconds
  - submittedAt, approvedAt

Topic: `casino.compliance.kyc-rejected.v1`
- Payload: `KycRejectedPayload`
  - requestId, verificationType
  - rejectionReason, rejectionDetails
  - rejectedBy
  - aiConfidenceScore
  - canResubmit, resubmitAfter
  - processingTimeSeconds
  - submittedAt, rejectedAt

Topic: `casino.compliance.level-upgraded.v1`
- Payload: `VerificationLevelUpgradePayload`
  - previousLevel, newLevel
  - triggerReason
  - depositLimit, withdrawalLimit, monthlyLimit
  - benefits

Topic: `casino.compliance.limit-set.v1`
- Payload: `PlayerLimitSetPayload`
  - limitType, limitPeriod
  - limitAmount, limitCurrency
  - limitDuration
  - previousLimit
  - setBy
  - effectiveFrom
  - coolingOffPeriod

Topic: `casino.compliance.limit-reached.v1`
- Payload: `PlayerLimitReachedPayload`
  - limitType, limitPeriod
  - limitAmount, limitCurrency
  - currentAmount
  - actionTaken
  - resetAt

Topic: `casino.compliance.self-excluded.v1`
- Payload: `SelfExclusionPayload`
  - exclusionType
  - duration
  - reason
  - selectedOptions
  - startDate, endDate
  - canCancelEarly
  - supportOffered
  - helplineContacts

Topic: `casino.compliance.cooling-off.v1`
- Payload: `CoolingOffPayload`
  - duration
  - reason
  - startDate, endDate
  - canCancelEarly
  - reminderSent

Topic: `casino.compliance.reality-check.v1`
- Payload: `RealityCheckPayload`
  - sessionDuration
  - totalBets
  - totalWagered
  - totalWon
  - netPosition
  - currency
  - playerAction
  - checkInterval

### Engagement Domain

Topic: `casino.engagement.email-verified.v1`
- Payload: `EmailVerifiedPayload`
  - email, verificationMethod
  - verifiedAt
  - daysSinceRegistration

Topic: `casino.engagement.phone-verified.v1`
- Payload: `PhoneVerifiedPayload`
  - phoneNumber, countryCode
  - verificationMethod
  - verifiedAt
  - daysSinceRegistration

Topic: `casino.engagement.2fa-enabled.v1`
- Payload: `TwoFactorEnabledPayload`
  - method
  - enabledAt
  - daysSinceRegistration
  - triggeredBy

Topic: `casino.engagement.preferences-updated.v1`
- Payload: `PreferencesUpdatedPayload`
  - preferencesChanged (map)
  - communicationPreferences
  - gamePreferences
  - updatedAt

Topic: `casino.engagement.preferences-updated.v1` additional nested payloads:
- `CommunicationPreferences`: emailMarketing, smsMarketing, pushNotifications, bonusNotifications, transactionAlerts
- `GamePreferences`: favoriteGameTypes, favoriteProviders, oddsFormat, autoPlayEnabled, soundEnabled

Topic: `casino.engagement.login.v1`
- Payload: `PlayerLoginPayload`
  - loginMethod
  - ipAddress
  - userAgent
  - deviceType
  - platform
  - loginAt
  - daysSinceLastLogin
  - isNewDevice
  - failedAttempts

Topic: `casino.engagement.logout.v1`
- Payload: `PlayerLogoutPayload`
  - sessionDuration
  - totalBetsPlaced
  - totalDeposited
  - totalWithdrawn
  - currency
  - logoutReason
  - logoutAt

### System

Topic: `casino.dlq.all.v1`
- Dead letter queue for failed event publishing.

## Smartico Status Mapping

`SmarticoStatusMapper` defines status transforms:
- Player status to Smartico account status: ACTIVE, BLOCKED, SUSPENDED, SELF_EXCLUDED, PENDING.
- KYC status to Smartico: UNVERIFIED, PENDING, VERIFIED, REJECTED.
- Payment status to Smartico: COMPLETED, PENDING, FAILED.
- Language and currency codes are uppercased to ISO standards.
