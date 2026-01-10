# API Contracts Map (Code-Derived)

This document maps the backend OpenAPI surface to controllers. It is generated from `specs/openapi/casino-core.json`, which is derived from the casino-b codebase.

- Total endpoints: 908
- Total tags: 143
- Source of truth: `casino-b/src/main/kotlin/com/casino/core/controller`
- Full contract: `specs/openapi/casino-core.json`

## Tags

- Admin
- AdminBanner
- AdminBonus
- AdminGame
- AdminLimit
- AdminPlayerStatus
- AdminPlayerTag
- AdminSelfExclusion
- AdminSimpleKyc
- AdminWageringManagement
- AdvancedBonus
- AggregationMonitoring
- Auth
- BetBy
- BetByAdmin
- BetByDebug
- BetByExternalApiTest
- BetByWallet
- BonusAdmin
- BonusAnalytics
- BonusBalance
- BonusLifecycleTest
- BonusManagement
- BonusOffer
- BonusSelection
- BonusTest
- CMSBanner
- CMSPromotionalBlock
- CMSStaticPage
- CacheAdmin
- CampaignAdmin
- CashierWebhook
- Cellxpert
- CellxpertAdmin
- ComplianceSettings
- Content
- ContentType
- CountryAvailabilityRestrictionAdmin
- CurrencyAdmin
- CustomerBonus
- CustomerPayment
- CustomerPortal
- CustomerResponsibleGambling
- DailyBreakdown
- Dashboard
- DepositWagering
- EmailVerification
- Favorites
- FreeSpins
- Game
- GameAdmin
- GameAnalytics
- GameAvailabilityRestrictionAdmin
- GameCallback
- GameCategory
- GameCategoryAdmin
- GameCountryConfig
- GameCountryConfigAdminPanel
- GameCountryConfigGameAdmin
- GameDiscovery
- GameLaunch
- GameLimits
- GameProvider
- GameProviderAdmin
- GameProviderSync
- GameRecommendation
- GameRestriction
- GameSession
- GameSessionAdmin
- KafkaAdmin
- LayoutPublic
- LegacyGameCallback
- LocaleAdmin
- LoginHistoryAdmin
- LogsExplorer
- Media
- MediaUpload
- MenuConfigurationAdmin
- MultilanguageDemo
- OptimizedPublicGame
- PageConfigurationAdmin
- PageConfigurationPublic
- PageLocaleOverrideAdmin
- PasswordReset
- PaymentAdmin
- PaymentMethod
- PaymentMethodAdmin
- PaymentWebhook
- PhoneVerification
- Player
- PlayerAdmin
- PlayerBonusRestriction
- PlayerCashierRestriction
- PlayerComment
- PlayerLimit
- PlayerProfileField
- PlayerProfilePicture
- PlayerProfileUpdate
- PlayerSimpleKyc
- PlayerStatistics
- Promotion
- ProviderAnalytics
- ProviderCallback
- PublicAuth
- PublicBanner
- PublicBonus
- PublicCashier
- PublicCms
- PublicGame
- PublicGameLaunch
- PublicRegistration
- PublicVendor
- RefundAdmin
- RegistrationConfig
- Reporting
- ReportingExport
- ReportingManagement
- SelfExclusion
- SignupConfigCacheDemo
- Smartico
- SmarticoIntegration
- SmarticoTestData
- SportsAuth
- Test
- TestData
- TestGamingData
- TestOptimized
- TestTranslation
- TimeSeries
- TransactionAdmin
- TranslationAdmin
- TranslationKeyAdmin
- TranslationPublic
- TwoFactorAuth
- V3PublicGame
- Vendor
- Wagering
- Wallet
- WalletCacheDemo
- WalletCacheTest
- WalletMetrics
- WidgetAdmin
- WidgetTranslation

## Admin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/admin/cache/clear` | Clear all Redis caches | AdminController | `AdminController_clearAllCaches_post_api_admin_cache_clear` |
| POST | `/api/admin/login` | Authenticate an admin user and generate JWT tokens | AdminController | `AdminController_authenticateAdmin_post_api_admin_login` |

## AdminBanner

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/banners` | getAllBanners | AdminBannerController | `AdminBannerController_getAllBanners_get_api_v1_admin_banners` |
| POST | `/api/v1/admin/banners` | createBanner | AdminBannerController | `AdminBannerController_createBanner_post_api_v1_admin_banners` |
| GET | `/api/v1/admin/banners/list` | getAllBannersList | AdminBannerController | `AdminBannerController_getAllBannersList_get_api_v1_admin_banners_list` |
| DELETE | `/api/v1/admin/banners/{id}` | deleteBanner | AdminBannerController | `AdminBannerController_deleteBanner_delete_api_v1_admin_banners_id_` |
| GET | `/api/v1/admin/banners/{id}` | getBannerById | AdminBannerController | `AdminBannerController_getBannerById_get_api_v1_admin_banners_id_` |
| PUT | `/api/v1/admin/banners/{id}` | updateBanner | AdminBannerController | `AdminBannerController_updateBanner_put_api_v1_admin_banners_id_` |
| PATCH | `/api/v1/admin/banners/{id}/active` | toggleBannerStatus | AdminBannerController | `AdminBannerController_toggleBannerStatus_patch_api_v1_admin_banners_id_active` |
| PATCH | `/api/v1/admin/banners/{id}/display-order` | updateBannerDisplayOrder | AdminBannerController | `AdminBannerController_updateBannerDisplayOrder_patch_api_v1_admin_banners_id_display_order` |

## AdminBonus

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/bonuses` | List all bonuses with pagination | AdminBonusController | `AdminBonusController_listBonuses_get_api_v1_admin_bonuses` |
| POST | `/api/v1/admin/bonuses` | Create a new bonus | AdminBonusController | `AdminBonusController_createBonus_post_api_v1_admin_bonuses` |
| GET | `/api/v1/admin/bonuses/awards` | List all bonus awards with pagination | AdminBonusController | `AdminBonusController_listAwards_get_api_v1_admin_bonuses_awards` |
| GET | `/api/v1/admin/bonuses/awards/{awardId}/wagering-transactions` | Get wagering transactions for a bonus award | AdminBonusController | `AdminBonusController_getAwardWageringTransactions_get_api_v1_admin_bonuses_awards_awardId_wagering_transactions` |
| GET | `/api/v1/admin/bonuses/check-name` | Check if bonus internal name (code) is available | AdminBonusController | `AdminBonusController_checkBonusName_get_api_v1_admin_bonuses_check_name` |
| POST | `/api/v1/admin/bonuses/players/{playerId}/awards/{awardId}/forfeit` | Admin forfeit a player's bonus award with cancellation note | AdminBonusController | `AdminBonusController_forfeitPlayerBonus_post_api_v1_admin_bonuses_players_playerId_awards_awardId_forfeit` |
| DELETE | `/api/v1/admin/bonuses/{id}` | Delete a bonus | AdminBonusController | `AdminBonusController_deleteBonus_delete_api_v1_admin_bonuses_id_` |
| GET | `/api/v1/admin/bonuses/{id}` | Get bonus details by ID | AdminBonusController | `AdminBonusController_getBonus_get_api_v1_admin_bonuses_id_` |
| PUT | `/api/v1/admin/bonuses/{id}` | Update an existing bonus | AdminBonusController | `AdminBonusController_updateBonus_put_api_v1_admin_bonuses_id_` |
| PUT | `/api/v1/admin/bonuses/{id}/activate` | Activate a bonus | AdminBonusController | `AdminBonusController_activateBonus_put_api_v1_admin_bonuses_id_activate` |
| PUT | `/api/v1/admin/bonuses/{id}/deactivate` | Deactivate a bonus | AdminBonusController | `AdminBonusController_deactivateBonus_put_api_v1_admin_bonuses_id_deactivate` |
| PATCH | `/api/v1/admin/bonuses/{id}/status` | Update bonus status | AdminBonusController | `AdminBonusController_updateBonusStatus_patch_api_v1_admin_bonuses_id_status` |

## AdminGame

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/games/batch` | getGamesBatch | AdminGameController | `AdminGameController_getGamesBatch_post_api_v1_admin_games_batch` |
| POST | `/api/v1/admin/games/filter` | filterGames | AdminGameController | `AdminGameController_filterGames_post_api_v1_admin_games_filter` |

## AdminLimit

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/responsible/limits/pending` | Get all pending limit changes waiting for cooling-off period to end | AdminLimitController | `AdminLimitController_getPendingLimitChanges_get_api_admin_responsible_limits_pending` |
| POST | `/api/admin/responsible/limits/player/{playerId}` | Admin sets a limit for a player (with required reason) | AdminLimitController | `AdminLimitController_adminSetLimit_post_api_admin_responsible_limits_player_playerId_` |
| PUT | `/api/admin/responsible/limits/process-pending` | Process all pending limit changes that are ready | AdminLimitController | `AdminLimitController_processPendingLimits_put_api_admin_responsible_limits_process_pending` |
| GET | `/api/admin/responsible/limits/statistics` | Get statistics about player limits | AdminLimitController | `AdminLimitController_getLimitStatistics_get_api_admin_responsible_limits_statistics` |
| DELETE | `/api/admin/responsible/limits/{limitId}` | Admin removal of a limit | AdminLimitController | `AdminLimitController_adminRemoveLimit_delete_api_admin_responsible_limits_limitId_` |
| PUT | `/api/admin/responsible/limits/{limitId}/override` | Admin override of a limit (bypass cooling period) | AdminLimitController | `AdminLimitController_adminOverrideLimit_put_api_admin_responsible_limits_limitId_override` |

## AdminPlayerStatus

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| DELETE | `/api/v1/admin/players/{playerId}/login-block` | unblockPlayerLogin | AdminPlayerStatusController | `AdminPlayerStatusController_unblockPlayerLogin_delete_api_v1_admin_players_playerId_login_block` |
| PUT | `/api/v1/admin/players/{playerId}/status` | updatePlayerStatus | AdminPlayerStatusController | `AdminPlayerStatusController_updatePlayerStatus_put_api_v1_admin_players_playerId_status` |
| GET | `/api/v1/admin/players/{playerId}/status-history` | getStatusHistory | AdminPlayerStatusController | `AdminPlayerStatusController_getStatusHistory_get_api_v1_admin_players_playerId_status_history` |
| GET | `/api/v1/admin/players/{playerId}/status-history/recent` | getRecentStatusChanges | AdminPlayerStatusController | `AdminPlayerStatusController_getRecentStatusChanges_get_api_v1_admin_players_playerId_status_history_recent` |
| PUT | `/api/v1/admin/players/{playerId}/test-account` | setTestAccountFlag | AdminPlayerStatusController | `AdminPlayerStatusController_setTestAccountFlag_put_api_v1_admin_players_playerId_test_account` |

## AdminPlayerTag

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/players/{playerId}/tags` | getPlayerTags | AdminPlayerTagController | `AdminPlayerTagController_getPlayerTags_get_api_v1_admin_players_playerId_tags` |
| POST | `/api/v1/admin/players/{playerId}/tags` | assignTagToPlayer | AdminPlayerTagController | `AdminPlayerTagController_assignTagToPlayer_post_api_v1_admin_players_playerId_tags` |
| POST | `/api/v1/admin/players/{playerId}/tags/bulk` | bulkAssignTags | AdminPlayerTagController | `AdminPlayerTagController_bulkAssignTags_post_api_v1_admin_players_playerId_tags_bulk` |
| GET | `/api/v1/admin/players/{playerId}/tags/history` | getTagHistory | AdminPlayerTagController | `AdminPlayerTagController_getTagHistory_get_api_v1_admin_players_playerId_tags_history` |
| DELETE | `/api/v1/admin/players/{playerId}/tags/{tagId}` | removeTagFromPlayer | AdminPlayerTagController | `AdminPlayerTagController_removeTagFromPlayer_delete_api_v1_admin_players_playerId_tags_tagId_` |
| GET | `/api/v1/admin/tags` | getAllTags | AdminPlayerTagController | `AdminPlayerTagController_getAllTags_get_api_v1_admin_tags` |
| POST | `/api/v1/admin/tags` | createTag | AdminPlayerTagController | `AdminPlayerTagController_createTag_post_api_v1_admin_tags` |
| GET | `/api/v1/admin/tags/usage` | getAllTagsWithUsage | AdminPlayerTagController | `AdminPlayerTagController_getAllTagsWithUsage_get_api_v1_admin_tags_usage` |
| DELETE | `/api/v1/admin/tags/{id}` | deleteTag | AdminPlayerTagController | `AdminPlayerTagController_deleteTag_delete_api_v1_admin_tags_id_` |
| GET | `/api/v1/admin/tags/{id}` | getTagById | AdminPlayerTagController | `AdminPlayerTagController_getTagById_get_api_v1_admin_tags_id_` |
| PUT | `/api/v1/admin/tags/{id}` | updateTag | AdminPlayerTagController | `AdminPlayerTagController_updateTag_put_api_v1_admin_tags_id_` |
| GET | `/api/v1/admin/tags/{tagId}/players` | getPlayersWithTag | AdminPlayerTagController | `AdminPlayerTagController_getPlayersWithTag_get_api_v1_admin_tags_tagId_players` |

## AdminSelfExclusion

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/responsible/exclusions` | Get all self-exclusions with optional filters | AdminSelfExclusionController | `AdminSelfExclusionController_getAllExclusions_get_api_admin_responsible_exclusions` |
| PUT | `/api/admin/responsible/exclusions/process-expired` | Process all expired exclusions | AdminSelfExclusionController | `AdminSelfExclusionController_processExpiredExclusions_put_api_admin_responsible_exclusions_process_expired` |
| GET | `/api/admin/responsible/exclusions/statistics` | Get statistics about self-exclusions | AdminSelfExclusionController | `AdminSelfExclusionController_getExclusionStatistics_get_api_admin_responsible_exclusions_statistics` |
| PUT | `/api/admin/responsible/exclusions/{exclusionId}/status` | Update exclusion status (e.g. for revoking) | AdminSelfExclusionController | `AdminSelfExclusionController_updateExclusionStatus_put_api_admin_responsible_exclusions_exclusionId_status` |

## AdminSimpleKyc

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/simple-kyc/bulk-approve` | Bulk approve KYC | AdminSimpleKycController | `AdminSimpleKycController_bulkApprove_post_api_v1_admin_simple_kyc_bulk_approve` |
| GET | `/api/v1/admin/simple-kyc/instructions` | Get verification instructions | AdminSimpleKycController | `AdminSimpleKycController_getInstructions_get_api_v1_admin_simple_kyc_instructions` |
| PUT | `/api/v1/admin/simple-kyc/instructions` | Update verification instructions | AdminSimpleKycController | `AdminSimpleKycController_updateInstructions_put_api_v1_admin_simple_kyc_instructions` |
| GET | `/api/v1/admin/simple-kyc/pending-reviews` | Get pending KYC reviews | AdminSimpleKycController | `AdminSimpleKycController_getPendingReviews_get_api_v1_admin_simple_kyc_pending_reviews` |
| GET | `/api/v1/admin/simple-kyc/players` | Get all players | AdminSimpleKycController | `AdminSimpleKycController_getAllPlayers_get_api_v1_admin_simple_kyc_players` |
| GET | `/api/v1/admin/simple-kyc/players/by-status` | Get players by status | AdminSimpleKycController | `AdminSimpleKycController_getPlayersByStatus_get_api_v1_admin_simple_kyc_players_by_status` |
| GET | `/api/v1/admin/simple-kyc/players/{playerId}` | Get player KYC details | AdminSimpleKycController | `AdminSimpleKycController_getPlayerKycDetails_get_api_v1_admin_simple_kyc_players_playerId_` |
| GET | `/api/v1/admin/simple-kyc/players/{playerId}/audit-log` | Get player audit log | AdminSimpleKycController | `AdminSimpleKycController_getPlayerAuditLog_get_api_v1_admin_simple_kyc_players_playerId_audit_log` |
| POST | `/api/v1/admin/simple-kyc/players/{playerId}/documents/review` | Review document | AdminSimpleKycController | `AdminSimpleKycController_reviewDocument_post_api_v1_admin_simple_kyc_players_playerId_documents_review` |
| POST | `/api/v1/admin/simple-kyc/players/{playerId}/final-review` | Final KYC review | AdminSimpleKycController | `AdminSimpleKycController_finalKycReview_post_api_v1_admin_simple_kyc_players_playerId_final_review` |
| GET | `/api/v1/admin/simple-kyc/search` | Search players | AdminSimpleKycController | `AdminSimpleKycController_searchPlayers_get_api_v1_admin_simple_kyc_search` |
| GET | `/api/v1/admin/simple-kyc/statistics` | Get KYC statistics | AdminSimpleKycController | `AdminSimpleKycController_getKycStatistics_get_api_v1_admin_simple_kyc_statistics` |

## AdminWageringManagement

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/wagering/deposit-wagering/{requirementId}/adjust-progress` | Manually adjust wagering progress for a deposit requirement | AdminWageringManagementController | `AdminWageringManagementController_adjustDepositWageringProgress_post_api_v1_admin_wagering_deposit_wagering_requirementId_adjust_progress` |
| POST | `/api/v1/admin/wagering/deposit-wagering/{requirementId}/complete` | Manually complete a deposit wagering requirement | AdminWageringManagementController | `AdminWageringManagementController_completeDepositWageringManually_post_api_v1_admin_wagering_deposit_wagering_requirementId_complete` |
| DELETE | `/api/v1/admin/wagering/deposit-wagering/{requirementId}/component/{componentId}` | Cancel wagering for a specific deposit (removes requirement entirely) | AdminWageringManagementController | `AdminWageringManagementController_cancelDepositComponent_delete_api_v1_admin_wagering_deposit_wagering_requirementId_component_componentId_` |
| POST | `/api/v1/admin/wagering/deposit-wagering/{requirementId}/component/{componentId}/complete` | Manually complete wagering for a specific deposit within a requirement | AdminWageringManagementController | `AdminWageringManagementController_completeDepositComponent_post_api_v1_admin_wagering_deposit_wagering_requirementId_component_componentId_complete` |
| GET | `/api/v1/admin/wagering/deposit-wagering/{requirementId}/components` | Get all deposit components within a merged wagering requirement | AdminWageringManagementController | `AdminWageringManagementController_getWageringComponents_get_api_v1_admin_wagering_deposit_wagering_requirementId_components` |
| GET | `/api/v1/admin/wagering/player/{playerId}/deposit-wagering/all` | Get all deposit wagering requirements for a player | AdminWageringManagementController | `AdminWageringManagementController_getAllDepositWageringRequirements_get_api_v1_admin_wagering_player_playerId_deposit_wagering_all` |
| GET | `/api/v1/admin/wagering/player/{playerId}/locked-funds` | Get detailed breakdown of locked funds | AdminWageringManagementController | `AdminWageringManagementController_getLockedFundsBreakdown_get_api_v1_admin_wagering_player_playerId_locked_funds` |
| GET | `/api/v1/admin/wagering/player/{playerId}/overview` | Get complete wagering overview for a player | AdminWageringManagementController | `AdminWageringManagementController_getWageringOverview_get_api_v1_admin_wagering_player_playerId_overview` |

## AdvancedBonus

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/bonuses/{bonusId}/reload-config` | Configure reload bonus settings | AdvancedBonusController | `AdvancedBonusController_configureReloadBonus_post_api_v1_admin_bonuses_bonusId_reload_config` |
| POST | `/api/v1/admin/bonuses/{bonusId}/schedule` | Configure bonus schedule for weekday bonuses | AdvancedBonusController | `AdvancedBonusController_configureBonusSchedule_post_api_v1_admin_bonuses_bonusId_schedule` |
| GET | `/api/v1/weekday-bonuses` | Get available weekday bonuses for current day | AdvancedBonusController | `AdvancedBonusController_getMyWeekdayBonuses_get_api_v1_weekday_bonuses` |

## AggregationMonitoring

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/aggregation/circuit-breaker` | getCircuitBreakerStatus | AggregationMonitoringController | `AggregationMonitoringController_getCircuitBreakerStatus_get_api_v1_admin_aggregation_circuit_breaker` |
| POST | `/api/v1/admin/aggregation/circuit-breaker/{jobName}/reset` | resetCircuitBreaker | AggregationMonitoringController | `AggregationMonitoringController_resetCircuitBreaker_post_api_v1_admin_aggregation_circuit_breaker_jobName_reset` |
| GET | `/api/v1/admin/aggregation/dashboard` | getDashboard | AggregationMonitoringController | `AggregationMonitoringController_getDashboard_get_api_v1_admin_aggregation_dashboard` |
| POST | `/api/v1/admin/aggregation/execute` | executeForDate | AggregationMonitoringController | `AggregationMonitoringController_executeForDate_post_api_v1_admin_aggregation_execute` |
| POST | `/api/v1/admin/aggregation/execute-range` | executeForDateRange | AggregationMonitoringController | `AggregationMonitoringController_executeForDateRange_post_api_v1_admin_aggregation_execute_range` |
| GET | `/api/v1/admin/aggregation/executions` | getExecutions | AggregationMonitoringController | `AggregationMonitoringController_getExecutions_get_api_v1_admin_aggregation_executions` |
| GET | `/api/v1/admin/aggregation/executions/{id}` | getExecution | AggregationMonitoringController | `AggregationMonitoringController_getExecution_get_api_v1_admin_aggregation_executions_id_` |
| GET | `/api/v1/admin/aggregation/failures` | getRecentFailures | AggregationMonitoringController | `AggregationMonitoringController_getRecentFailures_get_api_v1_admin_aggregation_failures` |
| GET | `/api/v1/admin/aggregation/health` | healthCheck | AggregationMonitoringController | `AggregationMonitoringController_healthCheck_get_api_v1_admin_aggregation_health` |
| GET | `/api/v1/admin/aggregation/latest-by-job` | getLatestByJob | AggregationMonitoringController | `AggregationMonitoringController_getLatestByJob_get_api_v1_admin_aggregation_latest_by_job` |
| GET | `/api/v1/admin/aggregation/statistics/{jobName}` | getJobStatistics | AggregationMonitoringController | `AggregationMonitoringController_getJobStatistics_get_api_v1_admin_aggregation_statistics_jobName_` |

## Auth

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/auth/login` | Authenticate a player and generate JWT tokens | AuthController | `AuthController_authenticate_post_api_auth_login` |
| POST | `/api/auth/refresh` | Refresh an access token using a refresh token | AuthController | `AuthController_refreshToken_post_api_auth_refresh` |

## BetBy

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/sport/betby/bet/commit` | betCommit | BetByController | `BetByController_betCommit_post_api_v1_sport_betby_bet_commit` |
| POST | `/api/v1/sport/betby/bet/discard` | betDiscard | BetByController | `BetByController_betDiscard_post_api_v1_sport_betby_bet_discard` |
| POST | `/api/v1/sport/betby/bet/lost` | betLost | BetByController | `BetByController_betLost_post_api_v1_sport_betby_bet_lost` |
| POST | `/api/v1/sport/betby/bet/make` | makeBet | BetByController | `BetByController_makeBet_post_api_v1_sport_betby_bet_make` |
| POST | `/api/v1/sport/betby/bet/refund` | betRefund | BetByController | `BetByController_betRefund_post_api_v1_sport_betby_bet_refund` |
| POST | `/api/v1/sport/betby/bet/rollback` | betRollback | BetByController | `BetByController_betRollback_post_api_v1_sport_betby_bet_rollback` |
| POST | `/api/v1/sport/betby/bet/settlement` | betSettlement | BetByController | `BetByController_betSettlement_post_api_v1_sport_betby_bet_settlement` |
| POST | `/api/v1/sport/betby/bet/win` | betWin | BetByController | `BetByController_betWin_post_api_v1_sport_betby_bet_win` |
| POST | `/api/v1/sport/betby/bet_commit` | betCommit | BetByController | `BetByController_betCommit_post_api_v1_sport_betby_bet_commit_2` |
| POST | `/api/v1/sport/betby/bet_discard` | betDiscard | BetByController | `BetByController_betDiscard_post_api_v1_sport_betby_bet_discard_2` |
| POST | `/api/v1/sport/betby/bet_lost` | betLost | BetByController | `BetByController_betLost_post_api_v1_sport_betby_bet_lost_2` |
| POST | `/api/v1/sport/betby/bet_make` | makeBet | BetByController | `BetByController_makeBet_post_api_v1_sport_betby_bet_make_2` |
| POST | `/api/v1/sport/betby/bet_refund` | betRefund | BetByController | `BetByController_betRefund_post_api_v1_sport_betby_bet_refund_2` |
| POST | `/api/v1/sport/betby/bet_rollback` | betRollback | BetByController | `BetByController_betRollback_post_api_v1_sport_betby_bet_rollback_2` |
| POST | `/api/v1/sport/betby/bet_settlement` | betSettlement | BetByController | `BetByController_betSettlement_post_api_v1_sport_betby_bet_settlement_2` |
| POST | `/api/v1/sport/betby/bet_win` | betWin | BetByController | `BetByController_betWin_post_api_v1_sport_betby_bet_win_2` |
| GET | `/api/v1/sport/betby/ping` | ping | BetByController | `BetByController_ping_get_api_v1_sport_betby_ping` |
| POST | `/api/v1/sport/betby/player-segment` | playerSegment | BetByController | `BetByController_playerSegment_post_api_v1_sport_betby_player_segment` |
| POST | `/api/v1/sport/betby/player_segment` | playerSegment | BetByController | `BetByController_playerSegment_post_api_v1_sport_betby_player_segment_2` |
| POST | `/api/v1/sport/betby/status` | checkStatus | BetByController | `BetByController_checkStatus_post_api_v1_sport_betby_status` |

## BetByAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/sports/bets` | getBets | BetByAdminController | `BetByAdminController_getBets_get_api_v1_admin_sports_bets` |
| GET | `/api/v1/admin/sports/bets/{betId}` | getBetDetails | BetByAdminController | `BetByAdminController_getBetDetails_get_api_v1_admin_sports_bets_betId_` |
| POST | `/api/v1/admin/sports/bets/{betId}/settle` | settleBet | BetByAdminController | `BetByAdminController_settleBet_post_api_v1_admin_sports_bets_betId_settle` |
| GET | `/api/v1/admin/sports/bonuses/active` | getActiveBonuses | BetByAdminController | `BetByAdminController_getActiveBonuses_get_api_v1_admin_sports_bonuses_active` |
| GET | `/api/v1/admin/sports/health` | getIntegrationHealth | BetByAdminController | `BetByAdminController_getIntegrationHealth_get_api_v1_admin_sports_health` |
| GET | `/api/v1/admin/sports/players/{playerId}/limits` | getPlayerLimits | BetByAdminController | `BetByAdminController_getPlayerLimits_get_api_v1_admin_sports_players_playerId_limits` |
| POST | `/api/v1/admin/sports/players/{playerId}/limits/override` | overridePlayerLimits | BetByAdminController | `BetByAdminController_overridePlayerLimits_post_api_v1_admin_sports_players_playerId_limits_override` |
| GET | `/api/v1/admin/sports/stats` | getBettingStats | BetByAdminController | `BetByAdminController_getBettingStats_get_api_v1_admin_sports_stats` |
| POST | `/api/v1/admin/sports/sync/force` | forceSyncWithBetBy | BetByAdminController | `BetByAdminController_forceSyncWithBetBy_post_api_v1_admin_sports_sync_force` |
| GET | `/api/v1/admin/sports/transactions/audit` | getTransactionAudit | BetByAdminController | `BetByAdminController_getTransactionAudit_get_api_v1_admin_sports_transactions_audit` |
| GET | `/api/v1/admin/sports/webhook-logs` | getWebhookLogs | BetByAdminController | `BetByAdminController_getWebhookLogs_get_api_v1_admin_sports_webhook_logs` |
| POST | `/api/v1/admin/sports/webhook-logs/cleanup` | cleanupWebhookLogs | BetByAdminController | `BetByAdminController_cleanupWebhookLogs_post_api_v1_admin_sports_webhook_logs_cleanup` |
| GET | `/api/v1/admin/sports/webhook-logs/slow` | getSlowRequests | BetByAdminController | `BetByAdminController_getSlowRequests_get_api_v1_admin_sports_webhook_logs_slow` |
| GET | `/api/v1/admin/sports/webhook-logs/{logId}` | getWebhookLogById | BetByAdminController | `BetByAdminController_getWebhookLogById_get_api_v1_admin_sports_webhook_logs_logId_` |
| GET | `/api/v1/admin/sports/webhook-stats` | getWebhookStats | BetByAdminController | `BetByAdminController_getWebhookStats_get_api_v1_admin_sports_webhook_stats` |

## BetByDebug

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/debug/betby/assign` | Debug bonus assignment | BetByDebugController | `BetByDebugController_debugAssignBonus_post_api_debug_betby_assign` |
| GET | `/api/debug/betby/direct-test` | Debug: Direct HTTP test to BetBy (bypasses RestTemplate) | BetByDebugController | `BetByDebugController_directTest_get_api_debug_betby_direct_test` |
| GET | `/api/debug/betby/jwt-debug` | Debug: Show JWT structure being generated | BetByDebugController | `BetByDebugController_debugJwt_get_api_debug_betby_jwt_debug` |
| GET | `/api/debug/betby/ping` | Ping BetBy API | BetByDebugController | `BetByDebugController_ping_get_api_debug_betby_ping` |
| GET | `/api/debug/betby/player/{playerId}/details` | Get player details from BetBy | BetByDebugController | `BetByDebugController_getPlayerDetails_get_api_debug_betby_player_playerId_details` |
| GET | `/api/debug/betby/raw-templates` | Debug: Make raw templates request | BetByDebugController | `BetByDebugController_rawTemplatesRequest_get_api_debug_betby_raw_templates` |
| GET | `/api/debug/betby/template/{templateId}` | Get bonus template details | BetByDebugController | `BetByDebugController_getTemplate_get_api_debug_betby_template_templateId_` |
| GET | `/api/debug/betby/templates` | Get all bonus templates from BetBy | BetByDebugController | `BetByDebugController_getAllTemplates_get_api_debug_betby_templates` |

## BetByExternalApiTest

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/sports/external/bonus/assign` | assignBonus | BetByExternalApiTestController | `BetByExternalApiTestController_assignBonus_post_api_v1_admin_sports_external_bonus_assign` |
| DELETE | `/api/v1/admin/sports/external/bonus/revoke` | revokeBonus | BetByExternalApiTestController | `BetByExternalApiTestController_revokeBonus_delete_api_v1_admin_sports_external_bonus_revoke` |
| GET | `/api/v1/admin/sports/external/bonus/templates` | getBonusTemplates | BetByExternalApiTestController | `BetByExternalApiTestController_getBonusTemplates_get_api_v1_admin_sports_external_bonus_templates` |
| GET | `/api/v1/admin/sports/external/bonus/templates/{templateId}` | getBonusTemplate | BetByExternalApiTestController | `BetByExternalApiTestController_getBonusTemplate_get_api_v1_admin_sports_external_bonus_templates_templateId_` |
| GET | `/api/v1/admin/sports/external/bonus/{bonusId}` | getBonusDetails | BetByExternalApiTestController | `BetByExternalApiTestController_getBonusDetails_get_api_v1_admin_sports_external_bonus_bonusId_` |
| GET | `/api/v1/admin/sports/external/health` | Check External API health status | BetByExternalApiTestController | `BetByExternalApiTestController_checkHealth_get_api_v1_admin_sports_external_health` |
| GET | `/api/v1/admin/sports/external/ping` | Test BetBy External API connectivity | BetByExternalApiTestController | `BetByExternalApiTestController_ping_get_api_v1_admin_sports_external_ping` |
| GET | `/api/v1/admin/sports/external/player/{playerId}/bonuses` | getPlayerBonuses | BetByExternalApiTestController | `BetByExternalApiTestController_getPlayerBonuses_get_api_v1_admin_sports_external_player_playerId_bonuses` |
| GET | `/api/v1/admin/sports/external/player/{playerId}/details` | getPlayerDetails | BetByExternalApiTestController | `BetByExternalApiTestController_getPlayerDetails_get_api_v1_admin_sports_external_player_playerId_details` |
| GET | `/api/v1/admin/sports/external/player/{playerId}/segment` | getPlayerSegment | BetByExternalApiTestController | `BetByExternalApiTestController_getPlayerSegment_get_api_v1_admin_sports_external_player_playerId_segment` |

## BetByWallet

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/sports/wallet/balance` | getBalance | BetByWalletController | `BetByWalletController_getBalance_get_api_v1_sports_wallet_balance` |
| GET | `/api/v1/sports/wallet/balance/check` | checkBalance | BetByWalletController | `BetByWalletController_checkBalance_get_api_v1_sports_wallet_balance_check` |
| POST | `/api/v1/sports/wallet/release/{reservationId}` | releaseFunds | BetByWalletController | `BetByWalletController_releaseFunds_post_api_v1_sports_wallet_release_reservationId_` |
| POST | `/api/v1/sports/wallet/reserve` | reserveFunds | BetByWalletController | `BetByWalletController_reserveFunds_post_api_v1_sports_wallet_reserve` |
| GET | `/api/v1/sports/wallet/transactions` | getTransactions | BetByWalletController | `BetByWalletController_getTransactions_get_api_v1_sports_wallet_transactions` |
| GET | `/api/v1/sports/wallet/transactions/stats` | getTransactionStats | BetByWalletController | `BetByWalletController_getTransactionStats_get_api_v1_sports_wallet_transactions_stats` |

## BonusAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/sports/bonus/assign` | Assign bonus to players | BonusAdminController | `BonusAdminController_assignBonus_post_api_v1_admin_sports_bonus_assign` |
| POST | `/api/v1/admin/sports/bonus/revoke` | Revoke bonuses | BonusAdminController | `BonusAdminController_revokeBonus_post_api_v1_admin_sports_bonus_revoke` |
| POST | `/api/v1/admin/sports/bonus/sync` | Sync bonus templates from BetBy | BonusAdminController | `BonusAdminController_syncTemplates_post_api_v1_admin_sports_bonus_sync` |
| GET | `/api/v1/admin/sports/bonus/templates` | List locally synced sports bonus templates | BonusAdminController | `BonusAdminController_listTemplates_get_api_v1_admin_sports_bonus_templates` |

## BonusAnalytics

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/bonuses/analytics/top-performing` | Get top performing bonuses for date range | BonusAnalyticsController | `BonusAnalyticsController_getTopPerformingBonuses_get_api_v1_admin_bonuses_analytics_top_performing` |
| GET | `/api/v1/admin/bonuses/analytics/{bonusId}/performance` | Get bonus performance report for date range | BonusAnalyticsController | `BonusAnalyticsController_getBonusPerformanceReport_get_api_v1_admin_bonuses_analytics_bonusId_performance` |

## BonusBalance

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/bonus-balance` | Get player's active bonus balances | BonusBalanceController | `BonusBalanceController_getMyBonusBalances_get_api_v1_bonus_balance` |
| GET | `/api/v1/bonus-balance/player/{playerId}` | Get player bonus balance details (admin only) | BonusBalanceController | `BonusBalanceController_getPlayerBonusBalanceDetails_get_api_v1_bonus_balance_player_playerId_` |
| GET | `/api/v1/bonus-balance/summary` | Get player's bonus balance summary | BonusBalanceController | `BonusBalanceController_getMyBonusBalanceSummary_get_api_v1_bonus_balance_summary` |

## BonusLifecycleTest

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| DELETE | `/api/test/bonus-lifecycle/cleanup/{testRunId}` | cleanup | BonusLifecycleTestController | `BonusLifecycleTestController_cleanup_delete_api_test_bonus_lifecycle_cleanup_testRunId_` |
| POST | `/api/test/bonus-lifecycle/convert` | convertBonus | BonusLifecycleTestController | `BonusLifecycleTestController_convertBonus_post_api_test_bonus_lifecycle_convert` |
| POST | `/api/test/bonus-lifecycle/create-test-bonus` | createTestBonus | BonusLifecycleTestController | `BonusLifecycleTestController_createTestBonus_post_api_test_bonus_lifecycle_create_test_bonus` |
| POST | `/api/test/bonus-lifecycle/create-test-player` | createTestPlayer | BonusLifecycleTestController | `BonusLifecycleTestController_createTestPlayer_post_api_test_bonus_lifecycle_create_test_player` |
| POST | `/api/test/bonus-lifecycle/full-flow` | executeFullLifecycleTest | BonusLifecycleTestController | `BonusLifecycleTestController_executeFullLifecycleTest_post_api_test_bonus_lifecycle_full_flow` |
| GET | `/api/test/bonus-lifecycle/health` | health | BonusLifecycleTestController | `BonusLifecycleTestController_health_get_api_test_bonus_lifecycle_health` |
| GET | `/api/test/bonus-lifecycle/scenarios` | listScenarios | BonusLifecycleTestController | `BonusLifecycleTestController_listScenarios_get_api_test_bonus_lifecycle_scenarios` |
| POST | `/api/test/bonus-lifecycle/simulate-deposit` | simulateDeposit | BonusLifecycleTestController | `BonusLifecycleTestController_simulateDeposit_post_api_test_bonus_lifecycle_simulate_deposit` |
| POST | `/api/test/bonus-lifecycle/simulate-wagering` | simulateWagering | BonusLifecycleTestController | `BonusLifecycleTestController_simulateWagering_post_api_test_bonus_lifecycle_simulate_wagering` |
| GET | `/api/test/bonus-lifecycle/status/{playerId}` | checkStatus | BonusLifecycleTestController | `BonusLifecycleTestController_checkStatus_get_api_test_bonus_lifecycle_status_playerId_` |

## BonusManagement

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/bonuses/manual-award` | Manually award a bonus to a player | BonusManagementController | `BonusManagementController_manuallyAwardBonus_post_api_v1_admin_bonuses_manual_award` |
| GET | `/api/v1/admin/bonuses/search/by-tags` | Search bonuses by tags | BonusManagementController | `BonusManagementController_searchBonusesByTags_get_api_v1_admin_bonuses_search_by_tags` |
| POST | `/api/v1/admin/bonuses/{bonusId}/copy` | Copy a bonus to create a new one | BonusManagementController | `BonusManagementController_copyBonus_post_api_v1_admin_bonuses_bonusId_copy` |
| PUT | `/api/v1/admin/bonuses/{bonusId}/tags` | Update bonus tags | BonusManagementController | `BonusManagementController_updateBonusTags_put_api_v1_admin_bonuses_bonusId_tags` |

## BonusOffer

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/bonus-offers/claim` | Claim a bonus offer | BonusOfferController | `BonusOfferController_claimOffer_post_api_v1_bonus_offers_claim` |
| GET | `/api/v1/bonus-offers/my-offers` | Get my active bonus offers | BonusOfferController | `BonusOfferController_getMyOffers_get_api_v1_bonus_offers_my_offers` |

## BonusSelection

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/bonus-selection/available` | Get available bonuses for deposit selection | BonusSelectionController | `BonusSelectionController_getAvailableBonuses_get_api_v1_bonus_selection_available` |
| DELETE | `/api/v1/bonus-selection/cancel` | Cancel current bonus selection | BonusSelectionController | `BonusSelectionController_cancelSelection_delete_api_v1_bonus_selection_cancel` |
| GET | `/api/v1/bonus-selection/current` | Get current bonus selection | BonusSelectionController | `BonusSelectionController_getCurrentSelection_get_api_v1_bonus_selection_current` |
| POST | `/api/v1/bonus-selection/select` | Select a bonus for upcoming deposit | BonusSelectionController | `BonusSelectionController_selectBonus_post_api_v1_bonus_selection_select` |

## BonusTest

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/test/bonus/simulate-deposit` | Simulate a deposit completion event for testing bonus awards | BonusTestController | `BonusTestController_simulateDeposit_post_api_test_bonus_simulate_deposit` |

## CMSBanner

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/banners/active` | Get active banners for display (public endpoint) | CMSBannerController | `CMSBannerController_getActiveBanners_get_api_v1_banners_active` |
| GET | `/api/v1/cms/banners` | Get all banners from CMS | CMSBannerController | `CMSBannerController_getAllBanners_get_api_v1_cms_banners` |
| POST | `/api/v1/cms/banners` | Create banner through CMS | CMSBannerController | `CMSBannerController_createBanner_post_api_v1_cms_banners` |
| PUT | `/api/v1/cms/banners/{id}` | Update banner through CMS | CMSBannerController | `CMSBannerController_updateBanner_put_api_v1_cms_banners_id_` |

## CMSPromotionalBlock

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/cms/promotional-blocks` | Get all promotional blocks from CMS | CMSPromotionalBlockController | `CMSPromotionalBlockController_getAllPromotionalBlocks_get_api_v1_cms_promotional_blocks` |
| POST | `/api/v1/cms/promotional-blocks` | Create promotional block through CMS | CMSPromotionalBlockController | `CMSPromotionalBlockController_createPromotionalBlock_post_api_v1_cms_promotional_blocks` |
| PUT | `/api/v1/cms/promotional-blocks/{id}` | Update promotional block through CMS | CMSPromotionalBlockController | `CMSPromotionalBlockController_updatePromotionalBlock_put_api_v1_cms_promotional_blocks_id_` |
| GET | `/api/v1/promotional-blocks/active` | Get active promotional blocks for display (public endpoint) | CMSPromotionalBlockController | `CMSPromotionalBlockController_getActivePromotionalBlocks_get_api_v1_promotional_blocks_active` |
| GET | `/api/v1/promotional-blocks/placement/{placementTag}` | Get promotional block by placement tag (public endpoint) | CMSPromotionalBlockController | `CMSPromotionalBlockController_getPromotionalBlockByPlacement_get_api_v1_promotional_blocks_placement_placementTag_` |

## CMSStaticPage

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/cms/static-pages` | Get all static pages from CMS | CMSStaticPageController | `CMSStaticPageController_getAllStaticPages_get_api_v1_cms_static_pages` |
| POST | `/api/v1/cms/static-pages` | Create static page through CMS | CMSStaticPageController | `CMSStaticPageController_createStaticPage_post_api_v1_cms_static_pages` |
| PUT | `/api/v1/cms/static-pages/{id}` | Update static page through CMS | CMSStaticPageController | `CMSStaticPageController_updateStaticPage_put_api_v1_cms_static_pages_id_` |
| GET | `/api/v1/pages` | Get published static pages (public endpoint) | CMSStaticPageController | `CMSStaticPageController_getPublishedStaticPages_get_api_v1_pages` |
| GET | `/api/v1/pages/{slug}` | Get static page by slug (public endpoint) | CMSStaticPageController | `CMSStaticPageController_getStaticPageBySlug_get_api_v1_pages_slug_` |
| GET | `/api/v1/sitemap.xml` | Generate sitemap for static pages | CMSStaticPageController | `CMSStaticPageController_generateSitemap_get_api_v1_sitemap_xml` |

## CacheAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| DELETE | `/api/v1/admin/cache/clear` | Clear all caches (Redis + in-memory) | CacheAdminController | `CacheAdminController_clearAllCaches_delete_api_v1_admin_cache_clear` |
| DELETE | `/api/v1/admin/cache/clear/memory` | Clear only in-memory cache | CacheAdminController | `CacheAdminController_clearMemoryCache_delete_api_v1_admin_cache_clear_memory` |
| DELETE | `/api/v1/admin/cache/clear/redis` | Clear only Redis cache | CacheAdminController | `CacheAdminController_clearRedisCache_delete_api_v1_admin_cache_clear_redis` |
| GET | `/api/v1/admin/cache/health` | Cache health check | CacheAdminController | `CacheAdminController_getCacheHealth_get_api_v1_admin_cache_health` |
| GET | `/api/v1/admin/cache/metrics` | Get cache performance metrics | CacheAdminController | `CacheAdminController_getCacheMetrics_get_api_v1_admin_cache_metrics` |
| POST | `/api/v1/admin/cache/refresh` | Force refresh cache from database | CacheAdminController | `CacheAdminController_forceRefresh_post_api_v1_admin_cache_refresh` |
| POST | `/api/v1/admin/cache/refresh/conditional` | Smart refresh - only if cache is stale or outdated | CacheAdminController | `CacheAdminController_conditionalRefresh_post_api_v1_admin_cache_refresh_conditional` |
| POST | `/api/v1/admin/cache/refresh/redis` | Refresh in-memory cache from Redis | CacheAdminController | `CacheAdminController_refreshFromRedis_post_api_v1_admin_cache_refresh_redis` |
| GET | `/api/v1/admin/cache/stats` | Get detailed cache statistics | CacheAdminController | `CacheAdminController_getCacheStats_get_api_v1_admin_cache_stats` |
| GET | `/api/v1/admin/cache/status` | Get comprehensive cache status | CacheAdminController | `CacheAdminController_getCacheStatus_get_api_v1_admin_cache_status` |
| POST | `/api/v1/admin/cache/warmup` | Warm up cache by pre-loading common queries | CacheAdminController | `CacheAdminController_warmUpCache_post_api_v1_admin_cache_warmup` |

## CampaignAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/campaigns` | List campaigns | CampaignAdminController | `CampaignAdminController_listCampaigns_get_api_v1_admin_campaigns` |
| POST | `/api/v1/admin/campaigns` | createCampaign | CampaignAdminController | `CampaignAdminController_createCampaign_post_api_v1_admin_campaigns` |
| GET | `/api/v1/admin/campaigns/local` | getLocalCampaigns | CampaignAdminController | `CampaignAdminController_getLocalCampaigns_get_api_v1_admin_campaigns_local` |
| GET | `/api/v1/admin/campaigns/statistics` | Get campaign statistics | CampaignAdminController | `CampaignAdminController_getStatistics_get_api_v1_admin_campaigns_statistics` |
| GET | `/api/v1/admin/campaigns/vendors` | Get supported vendors | CampaignAdminController | `CampaignAdminController_getVendors_get_api_v1_admin_campaigns_vendors` |
| GET | `/api/v1/admin/campaigns/vendors/limits` | getVendorLimits | CampaignAdminController | `CampaignAdminController_getVendorLimits_get_api_v1_admin_campaigns_vendors_limits` |
| GET | `/api/v1/admin/campaigns/vendors/limits/enhanced` | getEnhancedVendorLimits | CampaignAdminController | `CampaignAdminController_getEnhancedVendorLimits_get_api_v1_admin_campaigns_vendors_limits_enhanced` |
| GET | `/api/v1/admin/campaigns/vendors/{vendor}/presets` | getGamePresets | CampaignAdminController | `CampaignAdminController_getGamePresets_get_api_v1_admin_campaigns_vendors_vendor_presets` |
| GET | `/api/v1/admin/campaigns/{campaignCode}` | Get campaign details | CampaignAdminController | `CampaignAdminController_getCampaignDetails_get_api_v1_admin_campaigns_campaignCode_` |
| POST | `/api/v1/admin/campaigns/{campaignCode}/cancel` | cancelCampaign | CampaignAdminController | `CampaignAdminController_cancelCampaign_post_api_v1_admin_campaigns_campaignCode_cancel` |
| POST | `/api/v1/admin/campaigns/{campaignCode}/players/add` | addPlayers | CampaignAdminController | `CampaignAdminController_addPlayers_post_api_v1_admin_campaigns_campaignCode_players_add` |
| POST | `/api/v1/admin/campaigns/{campaignCode}/players/remove` | removePlayers | CampaignAdminController | `CampaignAdminController_removePlayers_post_api_v1_admin_campaigns_campaignCode_players_remove` |
| GET | `/api/v1/admin/campaigns/{campaignCode}/sync-status` | getCampaignWithSyncStatus | CampaignAdminController | `CampaignAdminController_getCampaignWithSyncStatus_get_api_v1_admin_campaigns_campaignCode_sync_status` |

## CashierWebhook

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/payment/cashier/hook` | handleCashierWebhook | CashierWebhookController | `CashierWebhookController_handleCashierWebhook_post_api_payment_cashier_hook` |

## Cellxpert

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/cellxpert/activities` | getActivities | CellxpertController | `CellxpertController_getActivities_get_api_v1_cellxpert_activities` |
| GET | `/api/v1/cellxpert/health` | healthCheck | CellxpertController | `CellxpertController_healthCheck_get_api_v1_cellxpert_health` |
| GET | `/api/v1/cellxpert/players` | getPlayers | CellxpertController | `CellxpertController_getPlayers_get_api_v1_cellxpert_players` |
| POST | `/api/v1/cellxpert/refresh-activities` | refreshActivitiesView | CellxpertController | `CellxpertController_refreshActivitiesView_post_api_v1_cellxpert_refresh_activities` |
| GET | `/api/v1/cellxpert/transactions` | getTransactions | CellxpertController | `CellxpertController_getTransactions_get_api_v1_cellxpert_transactions` |

## CellxpertAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/cellxpert/activity/sync` | getActivitySync | CellxpertAdminController | `CellxpertAdminController_getActivitySync_get_api_v1_admin_cellxpert_activity_sync` |
| GET | `/api/v1/admin/cellxpert/config` | getConfiguration | CellxpertAdminController | `CellxpertAdminController_getConfiguration_get_api_v1_admin_cellxpert_config` |
| PUT | `/api/v1/admin/cellxpert/config` | updateConfiguration | CellxpertAdminController | `CellxpertAdminController_updateConfiguration_put_api_v1_admin_cellxpert_config` |
| GET | `/api/v1/admin/cellxpert/players` | getAllTrackedPlayers | CellxpertAdminController | `CellxpertAdminController_getAllTrackedPlayers_get_api_v1_admin_cellxpert_players` |
| GET | `/api/v1/admin/cellxpert/players/by-token/{token}` | getPlayerByToken | CellxpertAdminController | `CellxpertAdminController_getPlayerByToken_get_api_v1_admin_cellxpert_players_by_token_token_` |
| POST | `/api/v1/admin/cellxpert/refresh-view` | refreshActivityView | CellxpertAdminController | `CellxpertAdminController_refreshActivityView_post_api_v1_admin_cellxpert_refresh_view` |

## ComplianceSettings

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/compliance-settings` | Get all compliance settings | ComplianceSettingsController | `ComplianceSettingsController_getAllSettings_get_api_admin_compliance_settings` |
| PUT | `/api/admin/compliance-settings/bulk` | Bulk update settings | ComplianceSettingsController | `ComplianceSettingsController_bulkUpdateSettings_put_api_admin_compliance_settings_bulk` |
| GET | `/api/admin/compliance-settings/category/{category}` | Get settings by category | ComplianceSettingsController | `ComplianceSettingsController_getSettingsByCategory_get_api_admin_compliance_settings_category_category_` |
| GET | `/api/admin/compliance-settings/summary` | Get compliance settings summary | ComplianceSettingsController | `ComplianceSettingsController_getSettingsSummary_get_api_admin_compliance_settings_summary` |
| GET | `/api/admin/compliance-settings/{id}` | Get setting by ID | ComplianceSettingsController | `ComplianceSettingsController_getSettingById_get_api_admin_compliance_settings_id_` |
| PUT | `/api/admin/compliance-settings/{id}` | Update setting | ComplianceSettingsController | `ComplianceSettingsController_updateSetting_put_api_admin_compliance_settings_id_` |
| POST | `/api/admin/compliance-settings/{id}/toggle` | Toggle boolean setting | ComplianceSettingsController | `ComplianceSettingsController_toggleSetting_post_api_admin_compliance_settings_id_toggle` |

## Content

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/cms/content` | Get content items with filtering | ContentController | `ContentController_getContents_get_api_v1_cms_content` |
| POST | `/api/v1/cms/content` | Create new content item | ContentController | `ContentController_createContent_post_api_v1_cms_content` |
| GET | `/api/v1/cms/content/type/{contentType}/slug/{slug}` | Get content by content type and slug | ContentController | `ContentController_getContentBySlug_get_api_v1_cms_content_type_contentType_slug_slug_` |
| GET | `/api/v1/cms/content/{id}` | Get content item by ID | ContentController | `ContentController_getContent_get_api_v1_cms_content_id_` |
| PUT | `/api/v1/cms/content/{id}` | Update content item | ContentController | `ContentController_updateContent_put_api_v1_cms_content_id_` |
| POST | `/api/v1/cms/content/{id}/archive` | Archive content item | ContentController | `ContentController_archiveContent_post_api_v1_cms_content_id_archive` |
| POST | `/api/v1/cms/content/{id}/publish` | Publish content item | ContentController | `ContentController_publishContent_post_api_v1_cms_content_id_publish` |

## ContentType

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/cms/content-types` | Get all content types | ContentTypeController | `ContentTypeController_getAllContentTypes_get_api_v1_cms_content_types` |
| POST | `/api/v1/cms/content-types` | Create new content type definition | ContentTypeController | `ContentTypeController_createContentType_post_api_v1_cms_content_types` |
| GET | `/api/v1/cms/content-types/name/{name}` | Get content type by name | ContentTypeController | `ContentTypeController_getContentTypeByName_get_api_v1_cms_content_types_name_name_` |
| DELETE | `/api/v1/cms/content-types/{id}` | Delete content type | ContentTypeController | `ContentTypeController_deleteContentType_delete_api_v1_cms_content_types_id_` |
| GET | `/api/v1/cms/content-types/{id}` | Get content type by ID | ContentTypeController | `ContentTypeController_getContentType_get_api_v1_cms_content_types_id_` |
| PUT | `/api/v1/cms/content-types/{id}` | Update content type definition | ContentTypeController | `ContentTypeController_updateContentType_put_api_v1_cms_content_types_id_` |
| GET | `/api/v1/cms/content-types/{id}/export` | Export content type definition | ContentTypeController | `ContentTypeController_exportContentType_get_api_v1_cms_content_types_id_export` |

## CountryAvailabilityRestrictionAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/country-restrictions` | List all global country restrictions | CountryAvailabilityRestrictionAdminController | `CountryAvailabilityRestrictionAdminController_listCountryRestrictions_get_api_v1_admin_country_restrictions` |
| POST | `/api/v1/admin/country-restrictions` | Create a new global country restriction | CountryAvailabilityRestrictionAdminController | `CountryAvailabilityRestrictionAdminController_createCountryRestriction_post_api_v1_admin_country_restrictions` |
| GET | `/api/v1/admin/country-restrictions/country/{countryCode}` | Get global restriction for a specific country | CountryAvailabilityRestrictionAdminController | `CountryAvailabilityRestrictionAdminController_getCountryRestrictionByCode_get_api_v1_admin_country_restrictions_country_countryCode_` |
| DELETE | `/api/v1/admin/country-restrictions/{id}` | Delete a global country restriction | CountryAvailabilityRestrictionAdminController | `CountryAvailabilityRestrictionAdminController_deleteCountryRestriction_delete_api_v1_admin_country_restrictions_id_` |
| GET | `/api/v1/admin/country-restrictions/{id}` | Get a global country restriction by ID | CountryAvailabilityRestrictionAdminController | `CountryAvailabilityRestrictionAdminController_getCountryRestriction_get_api_v1_admin_country_restrictions_id_` |
| PUT | `/api/v1/admin/country-restrictions/{id}` | Update an existing global country restriction | CountryAvailabilityRestrictionAdminController | `CountryAvailabilityRestrictionAdminController_updateCountryRestriction_put_api_v1_admin_country_restrictions_id_` |

## CurrencyAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/currencies` | Get all currencies | CurrencyAdminController | `CurrencyAdminController_getAllCurrencies_get_api_v1_admin_currencies` |
| POST | `/api/v1/admin/currencies` | Create new currency | CurrencyAdminController | `CurrencyAdminController_createCurrency_post_api_v1_admin_currencies` |
| GET | `/api/v1/admin/currencies/active` | Get active currencies | CurrencyAdminController | `CurrencyAdminController_getActiveCurrencies_get_api_v1_admin_currencies_active` |
| DELETE | `/api/v1/admin/currencies/{id}` | Delete currency | CurrencyAdminController | `CurrencyAdminController_deleteCurrency_delete_api_v1_admin_currencies_id_` |
| GET | `/api/v1/admin/currencies/{id}` | Get currency by ID | CurrencyAdminController | `CurrencyAdminController_getCurrencyById_get_api_v1_admin_currencies_id_` |
| PUT | `/api/v1/admin/currencies/{id}` | Update currency | CurrencyAdminController | `CurrencyAdminController_updateCurrency_put_api_v1_admin_currencies_id_` |
| PATCH | `/api/v1/admin/currencies/{id}/toggle-status` | Toggle currency status | CurrencyAdminController | `CurrencyAdminController_toggleCurrencyStatus_patch_api_v1_admin_currencies_id_toggle_status` |

## CustomerBonus

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| PATCH | `/api/customer/bonuses/admin/bonus/{bonusId}/activation-type` | Update bonus activation type | CustomerBonusController | `CustomerBonusController_updateBonusActivationType_patch_api_customer_bonuses_admin_bonus_bonusId_activation_type` |
| GET | `/api/customer/bonuses/available` | Get available bonuses for the current player | CustomerBonusController | `CustomerBonusController_getAvailableBonuses_get_api_customer_bonuses_available` |
| POST | `/api/customer/bonuses/awards/{awardId}/forfeit` | Forfeit a bonus award | CustomerBonusController | `CustomerBonusController_forfeitBonus_post_api_customer_bonuses_awards_awardId_forfeit` |
| GET | `/api/customer/bonuses/balance` | Get player's bonus balance | CustomerBonusController | `CustomerBonusController_getBonusBalance_get_api_customer_bonuses_balance` |
| POST | `/api/customer/bonuses/claim-by-code` | Apply a promo code to become eligible for a bonus | CustomerBonusController | `CustomerBonusController_claimBonusByCode_post_api_customer_bonuses_claim_by_code` |
| POST | `/api/customer/bonuses/debug/create-offer/{bonusCode}` | Debug endpoint to manually create offer for a bonus | CustomerBonusController | `CustomerBonusController_debugCreateOffer_post_api_customer_bonuses_debug_create_offer_bonusCode_` |
| GET | `/api/customer/bonuses/history` | Get player's bonus history | CustomerBonusController | `CustomerBonusController_getBonusHistory_get_api_customer_bonuses_history` |
| GET | `/api/customer/bonuses/my-bonuses` | Get player's active and pending bonuses | CustomerBonusController | `CustomerBonusController_getMyBonuses_get_api_customer_bonuses_my_bonuses` |
| POST | `/api/customer/bonuses/{bonusId}/claim` | Claim a bonus | CustomerBonusController | `CustomerBonusController_claimBonus_post_api_customer_bonuses_bonusId_claim` |

## CustomerPayment

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/customer/payment/initiate-session` | initiatePaymentSession | CustomerPaymentController | `CustomerPaymentController_initiatePaymentSession_post_api_customer_payment_initiate_session` |

## CustomerPortal

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/customer/activity` | Get player's recent activity | CustomerPortalController | `CustomerPortalController_getRecentActivity_get_api_customer_activity` |
| POST | `/api/customer/change-password` | Change player's password | CustomerPortalController | `CustomerPortalController_changePassword_post_api_customer_change_password` |
| GET | `/api/customer/limits` | Get player's responsible gambling limits | CustomerPortalController | `CustomerPortalController_getPlayerLimits_get_api_customer_limits` |
| PUT | `/api/customer/marketing-preferences` | Update marketing preferences | CustomerPortalController | `CustomerPortalController_updateMarketingPreferences_put_api_customer_marketing_preferences` |
| GET | `/api/customer/profile` | Get current player's profile | CustomerPortalController | `CustomerPortalController_getProfile_get_api_customer_profile` |
| PUT | `/api/customer/profile` | Update player's profile | CustomerPortalController | `CustomerPortalController_updateProfile_put_api_customer_profile` |
| POST | `/api/customer/request-data-export` | Request personal data export (GDPR) | CustomerPortalController | `CustomerPortalController_requestDataExport_post_api_customer_request_data_export` |
| GET | `/api/customer/transactions` | Get player's transaction history. Supports multiple types comma-separated (e.g., type=GAME_BET,GAME_WIN) | CustomerPortalController | `CustomerPortalController_getTransactions_get_api_customer_transactions` |
| POST | `/api/customer/transactions/export` | Export player's transactions to PDF or Excel | CustomerPortalController | `CustomerPortalController_exportTransactions_post_api_customer_transactions_export` |
| GET | `/api/customer/transactions/overview` | Get player's transaction history for overview | CustomerPortalController | `CustomerPortalController_getTransactionsOverview_get_api_customer_transactions_overview` |
| GET | `/api/customer/transactions/recent` | Get player's recent transactions | CustomerPortalController | `CustomerPortalController_getRecentTransactions_get_api_customer_transactions_recent` |
| GET | `/api/customer/wallet-summary` | Get player's wallet summary | CustomerPortalController | `CustomerPortalController_getWalletSummary_get_api_customer_wallet_summary` |

## CustomerResponsibleGambling

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/customer/responsible-gambling/deposits/check` | checkDeposit | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_checkDeposit_post_api_customer_responsible_gambling_deposits_check` |
| GET | `/api/customer/responsible-gambling/deposits/limit-status` | getDepositLimitStatus | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_getDepositLimitStatus_get_api_customer_responsible_gambling_deposits_limit_status` |
| GET | `/api/customer/responsible-gambling/deposits/totals` | getDepositTotals | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_getDepositTotals_get_api_customer_responsible_gambling_deposits_totals` |
| GET | `/api/customer/responsible-gambling/limits` | Get all player limits | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_getPlayerLimits_get_api_customer_responsible_gambling_limits` |
| POST | `/api/customer/responsible-gambling/limits` | Set a new gambling limit | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_setLimit_post_api_customer_responsible_gambling_limits` |
| POST | `/api/customer/responsible-gambling/limits/quick-set` | Quickly set common limits | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_setQuickLimits_post_api_customer_responsible_gambling_limits_quick_set` |
| GET | `/api/customer/responsible-gambling/limits/summary` | Get limits summary | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_getLimitsSummary_get_api_customer_responsible_gambling_limits_summary` |
| DELETE | `/api/customer/responsible-gambling/limits/{limitId}` | Remove a gambling limit | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_removeLimit_delete_api_customer_responsible_gambling_limits_limitId_` |
| PUT | `/api/customer/responsible-gambling/limits/{limitId}` | Update an existing limit | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_updateLimit_put_api_customer_responsible_gambling_limits_limitId_` |
| GET | `/api/customer/responsible-gambling/self-exclusion` | Get self-exclusion status | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_getSelfExclusionStatus_get_api_customer_responsible_gambling_self_exclusion` |
| POST | `/api/customer/responsible-gambling/self-exclusion/cooling-off` | Set a cooling-off period (short-term break) | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_setCoolingOff_post_api_customer_responsible_gambling_self_exclusion_cooling_off` |
| POST | `/api/customer/responsible-gambling/self-exclusion/permanent` | Set permanent self-exclusion (minimum 6 months) | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_setPermanentSelfExclusion_post_api_customer_responsible_gambling_self_exclusion_permanent` |
| POST | `/api/customer/responsible-gambling/self-exclusion/temporary` | Set temporary self-exclusion (up to 6 months) | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_setTemporarySelfExclusion_post_api_customer_responsible_gambling_self_exclusion_temporary` |
| GET | `/api/customer/responsible-gambling/session/current` | getCurrentSessionStatus | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_getCurrentSessionStatus_get_api_customer_responsible_gambling_session_current` |
| GET | `/api/customer/responsible-gambling/settings/complete` | getCompleteSettings | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_getCompleteSettings_get_api_customer_responsible_gambling_settings_complete` |
| PUT | `/api/customer/responsible-gambling/settings/complete` | updateCompleteSettings | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_updateCompleteSettings_put_api_customer_responsible_gambling_settings_complete` |
| POST | `/api/customer/responsible-gambling/take-a-break` | Quick action to take a break (24h cooling-off) | CustomerResponsibleGamblingController | `CustomerResponsibleGamblingController_takeABreak_post_api_customer_responsible_gambling_take_a_break` |

## DailyBreakdown

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/reporting/daily-breakdown` | getDailyBreakdown | DailyBreakdownController | `DailyBreakdownController_getDailyBreakdown_get_api_v1_reporting_daily_breakdown` |
| GET | `/api/v1/reporting/daily-breakdown/available-metrics` | getAvailableMetrics | DailyBreakdownController | `DailyBreakdownController_getAvailableMetrics_get_api_v1_reporting_daily_breakdown_available_metrics` |
| GET | `/api/v1/reporting/daily-breakdown/date/{date}` | getDailyBreakdownForDate | DailyBreakdownController | `DailyBreakdownController_getDailyBreakdownForDate_get_api_v1_reporting_daily_breakdown_date_date_` |
| POST | `/api/v1/reporting/daily-breakdown/export` | exportDailyBreakdown | DailyBreakdownController | `DailyBreakdownController_exportDailyBreakdown_post_api_v1_reporting_daily_breakdown_export` |
| GET | `/api/v1/reporting/daily-breakdown/health` | healthCheck | DailyBreakdownController | `DailyBreakdownController_healthCheck_get_api_v1_reporting_daily_breakdown_health` |
| POST | `/api/v1/reporting/daily-breakdown/recalculate` | recalculateDailyBreakdown | DailyBreakdownController | `DailyBreakdownController_recalculateDailyBreakdown_post_api_v1_reporting_daily_breakdown_recalculate` |
| GET | `/api/v1/reporting/daily-breakdown/summary-cards` | getSummaryCards | DailyBreakdownController | `DailyBreakdownController_getSummaryCards_get_api_v1_reporting_daily_breakdown_summary_cards` |

## Dashboard

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/dashboard/analytics/bonuses` | getBonusAnalytics | DashboardController | `DashboardController_getBonusAnalytics_get_api_v1_admin_dashboard_analytics_bonuses` |
| GET | `/api/v1/admin/dashboard/analytics/chart-categories` | getChartCategories | DashboardController | `DashboardController_getChartCategories_get_api_v1_admin_dashboard_analytics_chart_categories` |
| GET | `/api/v1/admin/dashboard/analytics/gaming` | getGamingAnalytics | DashboardController | `DashboardController_getGamingAnalytics_get_api_v1_admin_dashboard_analytics_gaming` |
| GET | `/api/v1/admin/dashboard/analytics/players` | getPlayerAnalytics | DashboardController | `DashboardController_getPlayerAnalytics_get_api_v1_admin_dashboard_analytics_players` |
| GET | `/api/v1/admin/dashboard/analytics/time-series` | getTimeSeriesData | DashboardController | `DashboardController_getTimeSeriesData_get_api_v1_admin_dashboard_analytics_time_series` |
| GET | `/api/v1/admin/dashboard/daily-breakdown` | getDailyBreakdown | DashboardController | `DashboardController_getDailyBreakdown_get_api_v1_admin_dashboard_daily_breakdown` |
| GET | `/api/v1/admin/dashboard/deposits` | getDepositMetrics | DashboardController | `DashboardController_getDepositMetrics_get_api_v1_admin_dashboard_deposits` |
| GET | `/api/v1/admin/dashboard/deposits/status-breakdown` | getDepositStatusBreakdown | DashboardController | `DashboardController_getDepositStatusBreakdown_get_api_v1_admin_dashboard_deposits_status_breakdown` |
| GET | `/api/v1/admin/dashboard/metrics` | getDashboardMetrics | DashboardController | `DashboardController_getDashboardMetrics_get_api_v1_admin_dashboard_metrics` |
| GET | `/api/v1/admin/dashboard/players/segmentation` | getPlayerSegmentation | DashboardController | `DashboardController_getPlayerSegmentation_get_api_v1_admin_dashboard_players_segmentation` |
| GET | `/api/v1/admin/dashboard/players/top-depositors` | getTopDepositors | DashboardController | `DashboardController_getTopDepositors_get_api_v1_admin_dashboard_players_top_depositors` |
| GET | `/api/v1/admin/dashboard/players/top-depositors/export` | exportTopDepositors | DashboardController | `DashboardController_exportTopDepositors_get_api_v1_admin_dashboard_players_top_depositors_export` |
| GET | `/api/v1/admin/dashboard/players/top-losers` | getTopLosers | DashboardController | `DashboardController_getTopLosers_get_api_v1_admin_dashboard_players_top_losers` |
| GET | `/api/v1/admin/dashboard/players/top-losers/export` | exportTopLosers | DashboardController | `DashboardController_exportTopLosers_get_api_v1_admin_dashboard_players_top_losers_export` |
| GET | `/api/v1/admin/dashboard/players/top-winners` | getTopWinners | DashboardController | `DashboardController_getTopWinners_get_api_v1_admin_dashboard_players_top_winners` |
| GET | `/api/v1/admin/dashboard/players/top-winners/export` | exportTopWinners | DashboardController | `DashboardController_exportTopWinners_get_api_v1_admin_dashboard_players_top_winners_export` |
| GET | `/api/v1/admin/dashboard/realtime` | getRealTimeMetrics | DashboardController | `DashboardController_getRealTimeMetrics_get_api_v1_admin_dashboard_realtime` |
| GET | `/api/v1/admin/dashboard/revenue` | getRevenueMetrics | DashboardController | `DashboardController_getRevenueMetrics_get_api_v1_admin_dashboard_revenue` |
| GET | `/api/v1/admin/dashboard/withdrawals` | getWithdrawalMetrics | DashboardController | `DashboardController_getWithdrawalMetrics_get_api_v1_admin_dashboard_withdrawals` |
| GET | `/api/v1/admin/dashboard/withdrawals/status-breakdown` | getWithdrawalStatusBreakdown | DashboardController | `DashboardController_getWithdrawalStatusBreakdown_get_api_v1_admin_dashboard_withdrawals_status_breakdown` |

## DepositWagering

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/deposit-wagering/admin/create` | Create deposit wagering requirement (Admin only) | DepositWageringController | `DepositWageringController_createDepositWagering_post_api_v1_deposit_wagering_admin_create` |
| GET | `/api/v1/deposit-wagering/admin/player/{playerId}` | Get deposit wagering status for specific player (Admin only) | DepositWageringController | `DepositWageringController_getPlayerDepositWageringStatus_get_api_v1_deposit_wagering_admin_player_playerId_` |
| GET | `/api/v1/deposit-wagering/admin/player/{playerId}/history` | Get player's deposit wagering history (Admin only) | DepositWageringController | `DepositWageringController_getPlayerDepositWageringHistory_get_api_v1_deposit_wagering_admin_player_playerId_history` |
| GET | `/api/v1/deposit-wagering/history` | Get player's deposit wagering history | DepositWageringController | `DepositWageringController_getMyDepositWageringHistory_get_api_v1_deposit_wagering_history` |
| GET | `/api/v1/deposit-wagering/status` | Get current deposit wagering status for authenticated player | DepositWageringController | `DepositWageringController_getMyDepositWageringStatus_get_api_v1_deposit_wagering_status` |
| GET | `/api/v1/deposit-wagering/summary` | Get player's deposit wagering summary statistics | DepositWageringController | `DepositWageringController_getMyWageringSummary_get_api_v1_deposit_wagering_summary` |
| POST | `/api/v1/deposit-wagering/{requirementId}/admin/cancel` | Cancel deposit wagering requirement (Admin only) | DepositWageringController | `DepositWageringController_cancelDepositWagering_post_api_v1_deposit_wagering_requirementId_admin_cancel` |
| POST | `/api/v1/deposit-wagering/{requirementId}/admin/check-completion` | Check and complete wagering requirement if met (Admin only) | DepositWageringController | `DepositWageringController_checkAndCompleteWagering_post_api_v1_deposit_wagering_requirementId_admin_check_completion` |
| POST | `/api/v1/deposit-wagering/{requirementId}/admin/expire` | Expire deposit wagering requirement (Admin only) | DepositWageringController | `DepositWageringController_expireDepositWagering_post_api_v1_deposit_wagering_requirementId_admin_expire` |
| GET | `/api/v1/deposit-wagering/{requirementId}/transactions` | Get wagering transactions for a specific requirement | DepositWageringController | `DepositWageringController_getWageringTransactions_get_api_v1_deposit_wagering_requirementId_transactions` |

## EmailVerification

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/email-verification/admin/send/{playerId}` | sendVerificationEmailToPlayer | EmailVerificationController | `EmailVerificationController_sendVerificationEmailToPlayer_post_api_v1_email_verification_admin_send_playerId_` |
| GET | `/api/v1/email-verification/admin/status/{playerId}` | getPlayerVerificationStatus | EmailVerificationController | `EmailVerificationController_getPlayerVerificationStatus_get_api_v1_email_verification_admin_status_playerId_` |
| POST | `/api/v1/email-verification/resend` | resendVerificationEmail | EmailVerificationController | `EmailVerificationController_resendVerificationEmail_post_api_v1_email_verification_resend` |
| POST | `/api/v1/email-verification/send` | sendVerificationEmail | EmailVerificationController | `EmailVerificationController_sendVerificationEmail_post_api_v1_email_verification_send` |
| GET | `/api/v1/email-verification/status` | getVerificationStatus | EmailVerificationController | `EmailVerificationController_getVerificationStatus_get_api_v1_email_verification_status` |
| GET | `/api/v1/email-verification/verify/{token}` | Verify email with token | EmailVerificationController | `EmailVerificationController_verifyEmail_get_api_v1_email_verification_verify_token_` |

## Favorites

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/favorites/cache/stats` | getCacheStats | FavoritesController | `FavoritesController_getCacheStats_get_api_v1_favorites_cache_stats` |
| DELETE | `/api/v1/favorites/games` | clearAllFavorites | FavoritesController | `FavoritesController_clearAllFavorites_delete_api_v1_favorites_games` |
| GET | `/api/v1/favorites/games` | getFavorites | FavoritesController | `FavoritesController_getFavorites_get_api_v1_favorites_games` |
| POST | `/api/v1/favorites/games/batch` | batchAddFavorites | FavoritesController | `FavoritesController_batchAddFavorites_post_api_v1_favorites_games_batch` |
| POST | `/api/v1/favorites/games/batch-status` | batchCheckFavoriteStatus | FavoritesController | `FavoritesController_batchCheckFavoriteStatus_post_api_v1_favorites_games_batch_status` |
| DELETE | `/api/v1/favorites/games/{gameId}` | removeFavorite | FavoritesController | `FavoritesController_removeFavorite_delete_api_v1_favorites_games_gameId_` |
| POST | `/api/v1/favorites/games/{gameId}` | addFavorite | FavoritesController | `FavoritesController_addFavorite_post_api_v1_favorites_games_gameId_` |
| GET | `/api/v1/favorites/games/{gameId}/status` | checkFavoriteStatus | FavoritesController | `FavoritesController_checkFavoriteStatus_get_api_v1_favorites_games_gameId_status` |
| GET | `/api/v1/favorites/stats` | getFavoritesStats | FavoritesController | `FavoritesController_getFavoritesStats_get_api_v1_favorites_stats` |

## FreeSpins

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/free-spins/balance` | Get my free spins balance | FreeSpinsController | `FreeSpinsController_getMyBalance_get_api_v1_free_spins_balance` |
| GET | `/api/v1/free-spins/history` | Get my free spins history | FreeSpinsController | `FreeSpinsController_getMyHistory_get_api_v1_free_spins_history` |
| POST | `/api/v1/free-spins/use` | Use free spins | FreeSpinsController | `FreeSpinsController_useSpins_post_api_v1_free_spins_use` |

## Game

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/games` | Get list of games with optional filtering | GameController | `GameController_getGames_get_api_games` |
| POST | `/api/games/bulk-update-types` | Bulk update game types from CSV file | GameController | `GameController_bulkUpdateGameTypes_post_api_games_bulk_update_types` |
| GET | `/api/games/featured` | Get featured games for a specific country | GameController | `GameController_getFeaturedGames_get_api_games_featured` |
| GET | `/api/games/new` | Get newly added games, optionally filtered by country | GameController | `GameController_getNewGames_get_api_games_new` |
| GET | `/api/games/popular` | Get popular games for a specific country based on popularity rank | GameController | `GameController_getPopularGames_get_api_games_popular` |
| POST | `/api/games/results` | Process game round result | GameController | `GameController_processGameResult_post_api_games_results` |
| POST | `/api/games/search` | Search games with advanced filters | GameController | `GameController_searchGames_post_api_games_search` |
| POST | `/api/games/sessions` | Create a new game session | GameController | `GameController_createGameSession_post_api_games_sessions` |
| GET | `/api/games/{id}` | Get game details by ID | GameController | `GameController_getGameDetails_get_api_games_id_` |

## GameAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/games` | Get all games with admin details | GameAdminController | `GameAdminController_getAllGames_get_api_admin_games` |
| POST | `/api/admin/games` | Create a new game | GameAdminController | `GameAdminController_createGame_post_api_admin_games` |
| GET | `/api/admin/games/by-ids` | Get games by multiple IDs | GameAdminController | `GameAdminController_getGamesByIds_get_api_admin_games_by_ids` |
| GET | `/api/admin/games/ranked` | Get games sorted by rank | GameAdminController | `GameAdminController_getGamesByRank_get_api_admin_games_ranked` |
| POST | `/api/admin/games/ranks/bulk` | Bulk update game ranks | GameAdminController | `GameAdminController_bulkUpdateRanks_post_api_admin_games_ranks_bulk` |
| GET | `/api/admin/games/sessions/export` | exportGameSessions | GameAdminController | `GameAdminController_exportGameSessions_get_api_admin_games_sessions_export` |
| GET | `/api/admin/games/transactions/export` | exportGameTransactions | GameAdminController | `GameAdminController_exportGameTransactions_get_api_admin_games_transactions_export` |
| DELETE | `/api/admin/games/{id}` | Delete a game | GameAdminController | `GameAdminController_deleteGame_delete_api_admin_games_id_` |
| GET | `/api/admin/games/{id}` | Get game details by ID | GameAdminController | `GameAdminController_getGameById_get_api_admin_games_id_` |
| PUT | `/api/admin/games/{id}` | Update an existing game | GameAdminController | `GameAdminController_updateGame_put_api_admin_games_id_` |
| PATCH | `/api/admin/games/{id}/rank` | Update game rank | GameAdminController | `GameAdminController_updateGameRank_patch_api_admin_games_id_rank` |

## GameAnalytics

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/analytics/games/best-performing` | Get best performing games by various metrics | GameAnalyticsController | `GameAnalyticsController_getBestPerformingGames_get_api_admin_analytics_games_best_performing` |
| POST | `/api/admin/analytics/games/generate-all` | Generate analytics for all games | GameAnalyticsController | `GameAnalyticsController_generateAllGameAnalytics_post_api_admin_analytics_games_generate_all` |
| GET | `/api/admin/analytics/games/{gameId}` | Get analytics for a specific game | GameAnalyticsController | `GameAnalyticsController_getGameAnalytics_get_api_admin_analytics_games_gameId_` |
| POST | `/api/admin/analytics/games/{gameId}/generate` | Generate analytics for a specific game | GameAnalyticsController | `GameAnalyticsController_generateGameAnalytics_post_api_admin_analytics_games_gameId_generate` |

## GameAvailabilityRestrictionAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/game-restrictions` | List game restrictions by game ID or country code | GameAvailabilityRestrictionAdminController | `GameAvailabilityRestrictionAdminController_listGameRestrictions_get_api_v1_admin_game_restrictions` |
| POST | `/api/v1/admin/game-restrictions` | Create a new game-specific country restriction | GameAvailabilityRestrictionAdminController | `GameAvailabilityRestrictionAdminController_createGameRestriction_post_api_v1_admin_game_restrictions` |
| GET | `/api/v1/admin/game-restrictions/check` | Check if a specific game-country restriction exists | GameAvailabilityRestrictionAdminController | `GameAvailabilityRestrictionAdminController_checkGameRestriction_get_api_v1_admin_game_restrictions_check` |
| DELETE | `/api/v1/admin/game-restrictions/{id}` | Delete a game-specific country restriction | GameAvailabilityRestrictionAdminController | `GameAvailabilityRestrictionAdminController_deleteGameRestriction_delete_api_v1_admin_game_restrictions_id_` |
| GET | `/api/v1/admin/game-restrictions/{id}` | Get a game-specific country restriction by ID | GameAvailabilityRestrictionAdminController | `GameAvailabilityRestrictionAdminController_getGameRestriction_get_api_v1_admin_game_restrictions_id_` |
| PUT | `/api/v1/admin/game-restrictions/{id}` | Update an existing game-specific country restriction | GameAvailabilityRestrictionAdminController | `GameAvailabilityRestrictionAdminController_updateGameRestriction_put_api_v1_admin_game_restrictions_id_` |

## GameCallback

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/callbacks/balance` | Handle balance updates | GameCallbackController | `GameCallbackController_handleBalanceUpdate_post_api_callbacks_balance` |
| POST | `/api/callbacks/error` | Handle game errors | GameCallbackController | `GameCallbackController_handleGameError_post_api_callbacks_error` |
| POST | `/api/callbacks/game-round` | Receive game round results | GameCallbackController | `GameCallbackController_handleGameRound_post_api_callbacks_game_round` |
| POST | `/api/callbacks/jackpot` | Handle jackpot wins | GameCallbackController | `GameCallbackController_handleJackpotWin_post_api_callbacks_jackpot` |
| GET | `/api/callbacks/ping` | Simple ping endpoint for monitoring | GameCallbackController | `GameCallbackController_ping_get_api_callbacks_ping` |
| POST | `/api/callbacks/session-recovery` | Handle session recovery requests | GameCallbackController | `GameCallbackController_handleSessionRecovery_post_api_callbacks_session_recovery` |
| POST | `/api/callbacks/session-transfer` | Handle session transfer between devices | GameCallbackController | `GameCallbackController_handleSessionTransfer_post_api_callbacks_session_transfer` |

## GameCategory

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/game-categories` | Get all active game categories | GameCategoryController | `GameCategoryController_getActiveCategories_get_api_game_categories` |
| GET | `/api/game-categories/{id}` | Get category by ID | GameCategoryController | `GameCategoryController_getCategoryById_get_api_game_categories_id_` |
| GET | `/api/game-categories/{id}/games` | Get active games in a specific category | GameCategoryController | `GameCategoryController_getGamesInCategory_get_api_game_categories_id_games` |
| GET | `/api/game-categories/{id}/subcategories` | Get subcategories for a given parent category | GameCategoryController | `GameCategoryController_getSubcategories_get_api_game_categories_id_subcategories` |

## GameCategoryAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/game-categories` | Get all game categories with optional filtering | GameCategoryAdminController | `GameCategoryAdminController_getAllCategories_get_api_admin_game_categories` |
| POST | `/api/admin/game-categories` | Create a new game category | GameCategoryAdminController | `GameCategoryAdminController_createCategory_post_api_admin_game_categories` |
| DELETE | `/api/admin/game-categories/{id}` | Delete a game category | GameCategoryAdminController | `GameCategoryAdminController_deleteCategory_delete_api_admin_game_categories_id_` |
| GET | `/api/admin/game-categories/{id}` | Get category by ID | GameCategoryAdminController | `GameCategoryAdminController_getCategoryById_get_api_admin_game_categories_id_` |
| PUT | `/api/admin/game-categories/{id}` | Update an existing game category | GameCategoryAdminController | `GameCategoryAdminController_updateCategory_put_api_admin_game_categories_id_` |
| GET | `/api/admin/game-categories/{id}/games` | Get games in a specific category | GameCategoryAdminController | `GameCategoryAdminController_getGamesInCategory_get_api_admin_game_categories_id_games` |
| POST | `/api/admin/game-categories/{id}/games` | Add games to a category | GameCategoryAdminController | `GameCategoryAdminController_addGamesToCategory_post_api_admin_game_categories_id_games` |
| DELETE | `/api/admin/game-categories/{id}/games/{gameId}` | Remove a game from a category | GameCategoryAdminController | `GameCategoryAdminController_removeGameFromCategory_delete_api_admin_game_categories_id_games_gameId_` |
| POST | `/api/admin/game-categories/{id}/reorder` | Reorder the display order of categories | GameCategoryAdminController | `GameCategoryAdminController_reorderCategories_post_api_admin_game_categories_id_reorder` |
| GET | `/api/admin/game-categories/{id}/subcategories` | Get subcategories for a given parent category | GameCategoryAdminController | `GameCategoryAdminController_getSubcategories_get_api_admin_game_categories_id_subcategories` |

## GameCountryConfig

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/games/country/featured` | Get featured games for a specific country | GameCountryConfigController | `GameCountryConfigController_getFeaturedGames_get_api_games_country_featured` |
| GET | `/api/games/country/popular-by-country` | Get popular games for a specific country | GameCountryConfigController | `GameCountryConfigController_getPopularGamesByCountry_get_api_games_country_popular_by_country` |
| GET | `/api/games/country/{id}/availability` | Check game availability for the current user's location | GameCountryConfigController | `GameCountryConfigController_checkGameAvailability_get_api_games_country_id_availability` |

## GameCountryConfigAdminPanel

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/admin/game-country/copy-configs` | Copy country configurations from one country to another | GameCountryConfigAdminPanelController | `GameCountryConfigAdminPanelController_copyCountryConfigurations_post_api_admin_game_country_copy_configs` |
| GET | `/api/admin/game-country/country/{countryCode}/stats` | Get game configuration statistics for a country | GameCountryConfigAdminPanelController | `GameCountryConfigAdminPanelController_getCountryGameStatistics_get_api_admin_game_country_country_countryCode_stats` |
| GET | `/api/admin/game-country/game/{gameId}` | Get all country configurations for a specific game | GameCountryConfigAdminPanelController | `GameCountryConfigAdminPanelController_getGameCountryConfigs_get_api_admin_game_country_game_gameId_` |
| POST | `/api/admin/game-country/game/{gameId}/default-configs` | Create default country configurations for a game | GameCountryConfigAdminPanelController | `GameCountryConfigAdminPanelController_createDefaultCountryConfigs_post_api_admin_game_country_game_gameId_default_configs` |
| POST | `/api/admin/game-country/update-sort-order/{countryCode}` | Update sort order for games in a country | GameCountryConfigAdminPanelController | `GameCountryConfigAdminPanelController_updateGamesSortOrder_post_api_admin_game_country_update_sort_order_countryCode_` |

## GameCountryConfigGameAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/admin/games/bulk-country-update` | Bulk update country configurations for multiple games | GameCountryConfigGameAdmin | `GameCountryConfigGameAdmin_bulkUpdateCountryConfigs_post_api_admin_games_bulk_country_update` |
| GET | `/api/admin/games/country/{country}` | Get all games with specific country configuration | GameCountryConfigGameAdmin | `GameCountryConfigGameAdmin_getGamesByCountryConfig_get_api_admin_games_country_country_` |
| GET | `/api/admin/games/{id}/country-config` | Get country configurations for a specific game | GameCountryConfigGameAdmin | `GameCountryConfigGameAdmin_getGameCountryConfigs_get_api_admin_games_id_country_config` |
| PUT | `/api/admin/games/{id}/country-config/{country}` | Update country configuration for a specific game | GameCountryConfigGameAdmin | `GameCountryConfigGameAdmin_updateGameCountryConfig_put_api_admin_games_id_country_config_country_` |
| POST | `/api/admin/games/{id}/country-config/{country}/featured` | Toggle featured status for a game in a country | GameCountryConfigGameAdmin | `GameCountryConfigGameAdmin_toggleGameFeaturedStatus_post_api_admin_games_id_country_config_country_featured` |
| POST | `/api/admin/games/{id}/country-config/{country}/popularity` | Update popularity rank for a game in a country | GameCountryConfigGameAdmin | `GameCountryConfigGameAdmin_updateGamePopularityRank_post_api_admin_games_id_country_config_country_popularity` |

## GameDiscovery

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/games/discovery/category/{categoryId}` | Get games by category | GameDiscoveryController | `GameDiscoveryController_getGamesByCategory_get_api_games_discovery_category_categoryId_` |
| GET | `/api/games/discovery/featured` | Get featured games for current location | GameDiscoveryController | `GameDiscoveryController_getFeaturedGames_get_api_games_discovery_featured` |
| GET | `/api/games/discovery/featured/{countryCode}` | Get featured games for a specific country | GameDiscoveryController | `GameDiscoveryController_getFeaturedGamesByCountry_get_api_games_discovery_featured_countryCode_` |
| GET | `/api/games/discovery/features` | Get games with specific features | GameDiscoveryController | `GameDiscoveryController_getGamesByFeatures_get_api_games_discovery_features` |
| GET | `/api/games/discovery/new` | Get new games, optionally filtered by country | GameDiscoveryController | `GameDiscoveryController_getNewGames_get_api_games_discovery_new` |
| GET | `/api/games/discovery/popular` | Get popular games for current location | GameDiscoveryController | `GameDiscoveryController_getPopularGames_get_api_games_discovery_popular` |
| GET | `/api/games/discovery/popular/{countryCode}` | Get popular games for a specific country | GameDiscoveryController | `GameDiscoveryController_getPopularGamesByCountry_get_api_games_discovery_popular_countryCode_` |
| GET | `/api/games/discovery/provider/{providerId}` | Get games by provider | GameDiscoveryController | `GameDiscoveryController_getGamesByProvider_get_api_games_discovery_provider_providerId_` |
| GET | `/api/games/discovery/recommended` | Get recommended games for the current player | GameDiscoveryController | `GameDiscoveryController_getRecommendedGames_get_api_games_discovery_recommended` |
| POST | `/api/games/discovery/search` | Search games with advanced filtering | GameDiscoveryController | `GameDiscoveryController_searchGames_post_api_games_discovery_search` |
| GET | `/api/games/discovery/{gameId}/availability` | Check if a game is available in a specific country | GameDiscoveryController | `GameDiscoveryController_checkGameAvailability_get_api_games_discovery_gameId_availability` |
| GET | `/api/games/discovery/{gameId}/similar` | Get similar games to a specific game | GameDiscoveryController | `GameDiscoveryController_getSimilarGames_get_api_games_discovery_gameId_similar` |

## GameLaunch

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/games/{id}/demo` | Launch game in demo mode | GameLaunchController | `GameLaunchController_launchGameDemo_post_api_games_id_demo` |
| POST | `/api/games/{id}/launch` | Launch game in real money mode | GameLaunchController | `GameLaunchController_launchGame_post_api_games_id_launch` |

## GameLimits

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/game-limits` | getGameLimits | GameLimitsController | `GameLimitsController_getGameLimits_get_api_v1_game_limits` |
| GET | `/api/v1/game-limits/batch` | getGameLimitsForMultipleGames | GameLimitsController | `GameLimitsController_getGameLimitsForMultipleGames_get_api_v1_game_limits_batch` |

## GameProvider

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/providers` | Get list of active game providers | GameProviderController | `GameProviderController_getActiveProviders_get_api_providers` |
| GET | `/api/providers/featured` | Get list of featured game providers | GameProviderController | `GameProviderController_getFeaturedProviders_get_api_providers_featured` |
| GET | `/api/providers/{id}` | Get basic information about a specific game provider | GameProviderController | `GameProviderController_getProviderInfo_get_api_providers_id_` |

## GameProviderAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/providers` | Get list of all game providers with pagination and filtering | GameProviderAdminController | `GameProviderAdminController_getAllProviders_get_api_admin_providers` |
| POST | `/api/admin/providers` | Create a new game provider | GameProviderAdminController | `GameProviderAdminController_createProvider_post_api_admin_providers` |
| GET | `/api/admin/providers/code/{providerCode}` | Get provider details by provider code | GameProviderAdminController | `GameProviderAdminController_getProviderByCode_get_api_admin_providers_code_providerCode_` |
| POST | `/api/admin/providers/sync/recover` | Manually recover interrupted syncs | GameProviderAdminController | `GameProviderAdminController_recoverInterruptedSyncs_post_api_admin_providers_sync_recover` |
| DELETE | `/api/admin/providers/{id}` | Delete a game provider | GameProviderAdminController | `GameProviderAdminController_deleteProvider_delete_api_admin_providers_id_` |
| GET | `/api/admin/providers/{id}` | Get detailed information about a specific game provider | GameProviderAdminController | `GameProviderAdminController_getProviderDetails_get_api_admin_providers_id_` |
| PUT | `/api/admin/providers/{id}` | Update an existing game provider | GameProviderAdminController | `GameProviderAdminController_updateProvider_put_api_admin_providers_id_` |
| GET | `/api/admin/providers/{id}/callbacks` | Get callback event logs | GameProviderAdminController | `GameProviderAdminController_getCallbackLogs_get_api_admin_providers_id_callbacks` |
| GET | `/api/admin/providers/{id}/statistics` | Get statistics for a specific game provider | GameProviderAdminController | `GameProviderAdminController_getProviderStatistics_get_api_admin_providers_id_statistics` |
| POST | `/api/admin/providers/{id}/sync-games` | Trigger game list synchronization | GameProviderAdminController | `GameProviderAdminController_syncProviderGames_post_api_admin_providers_id_sync_games` |
| GET | `/api/admin/providers/{id}/sync-history` | Get synchronization history for a provider | GameProviderAdminController | `GameProviderAdminController_getSyncHistory_get_api_admin_providers_id_sync_history` |
| GET | `/api/admin/providers/{id}/sync-status/{syncId}` | Get current status of a specific sync operation | GameProviderAdminController | `GameProviderAdminController_getSyncStatus_get_api_admin_providers_id_sync_status_syncId_` |
| POST | `/api/admin/providers/{id}/test-connection` | Test connection to provider API | GameProviderAdminController | `GameProviderAdminController_testProviderConnection_post_api_admin_providers_id_test_connection` |
| POST | `/api/admin/providers/{id}/whitelist-ip` | Add IP to provider whitelist | GameProviderAdminController | `GameProviderAdminController_whitelistProviderIp_post_api_admin_providers_id_whitelist_ip` |

## GameProviderSync

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/game-providers/sync/{syncHistoryId}/batches` | getSyncBatches | GameProviderSyncController | `GameProviderSyncController_getSyncBatches_get_api_v1_game_providers_sync_syncHistoryId_batches` |
| GET | `/api/v1/game-providers/sync/{syncHistoryId}/progress` | getSyncProgress | GameProviderSyncController | `GameProviderSyncController_getSyncProgress_get_api_v1_game_providers_sync_syncHistoryId_progress` |
| GET | `/api/v1/game-providers/sync/{syncHistoryId}/progress/live` | getSyncProgressLive | GameProviderSyncController | `GameProviderSyncController_getSyncProgressLive_get_api_v1_game_providers_sync_syncHistoryId_progress_live` |

## GameRecommendation

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/recommendations/favorite` | Mark/unmark a game as favorite | GameRecommendationController | `GameRecommendationController_toggleFavoriteGame_post_api_recommendations_favorite` |
| GET | `/api/recommendations/for-you` | Get personalized game recommendations | GameRecommendationController | `GameRecommendationController_getPersonalizedRecommendations_get_api_recommendations_for_you` |
| POST | `/api/recommendations/generate-similarities/{gameId}` | Generate similarity scores for a game | GameRecommendationController | `GameRecommendationController_generateGameSimilarities_post_api_recommendations_generate_similarities_gameId_` |
| GET | `/api/recommendations/popular` | Get popular games overall | GameRecommendationController | `GameRecommendationController_getPopularGames_get_api_recommendations_popular` |
| GET | `/api/recommendations/popular/by-country` | Get popular games by country | GameRecommendationController | `GameRecommendationController_getPopularGamesByCountry_get_api_recommendations_popular_by_country` |
| GET | `/api/recommendations/recently-played` | Get player's recently played games | GameRecommendationController | `GameRecommendationController_getRecentlyPlayedGames_get_api_recommendations_recently_played` |
| GET | `/api/recommendations/similar/{gameId}` | Get games similar to a specific game | GameRecommendationController | `GameRecommendationController_getSimilarGames_get_api_recommendations_similar_gameId_` |

## GameRestriction

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| PUT | `/api/v1/admin/game-restrictions/games/bulk-enabled` | Bulk enable or disable games | GameRestrictionController | `GameRestrictionController_bulkSetGamesEnabled_put_api_v1_admin_game_restrictions_games_bulk_enabled` |
| POST | `/api/v1/admin/game-restrictions/games/sync-status-from-enabled` | Bulk sync status from enabled field | GameRestrictionController | `GameRestrictionController_syncStatusFromEnabled_post_api_v1_admin_game_restrictions_games_sync_status_from_enabled` |
| PUT | `/api/v1/admin/game-restrictions/games/{gameId}/enabled` | Enable or disable a game globally | GameRestrictionController | `GameRestrictionController_setGameEnabled_put_api_v1_admin_game_restrictions_games_gameId_enabled` |
| PUT | `/api/v1/admin/game-restrictions/games/{gameId}/status` | Set game status (ACTIVE/INACTIVE) | GameRestrictionController | `GameRestrictionController_setGameStatus_put_api_v1_admin_game_restrictions_games_gameId_status` |
| GET | `/api/v1/admin/game-restrictions/players/{playerId}/games/{gameId}/available` | Check if a game is available for a player | GameRestrictionController | `GameRestrictionController_isGameAvailableForPlayer_get_api_v1_admin_game_restrictions_players_playerId_games_gameId_available` |
| GET | `/api/v1/admin/game-restrictions/players/{playerId}/restrictions` | Get all game restrictions for a player with full details | GameRestrictionController | `GameRestrictionController_getPlayerGameRestrictions_get_api_v1_admin_game_restrictions_players_playerId_restrictions` |
| POST | `/api/v1/admin/game-restrictions/players/{playerId}/restrictions` | Add a game restriction for a player | GameRestrictionController | `GameRestrictionController_addPlayerGameRestriction_post_api_v1_admin_game_restrictions_players_playerId_restrictions` |
| POST | `/api/v1/admin/game-restrictions/players/{playerId}/restrictions/bulk` | Bulk add game restrictions for a player | GameRestrictionController | `GameRestrictionController_bulkAddPlayerGameRestrictions_post_api_v1_admin_game_restrictions_players_playerId_restrictions_bulk` |
| DELETE | `/api/v1/admin/game-restrictions/players/{playerId}/restrictions/{gameId}` | Remove a game restriction for a player | GameRestrictionController | `GameRestrictionController_removePlayerGameRestriction_delete_api_v1_admin_game_restrictions_players_playerId_restrictions_gameId_` |

## GameSession

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/sessions/active` | Get player's active game sessions | GameSessionController | `GameSessionController_getActiveSessions_get_api_sessions_active` |
| DELETE | `/api/sessions/{id}` | End game session | GameSessionController | `GameSessionController_endSession_delete_api_sessions_id_` |
| PUT | `/api/sessions/{id}/keepalive` | Keep session alive | GameSessionController | `GameSessionController_keepSessionAlive_put_api_sessions_id_keepalive` |
| GET | `/api/sessions/{id}/status` | Check session status | GameSessionController | `GameSessionController_getSessionStatus_get_api_sessions_id_status` |

## GameSessionAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/sessions` | Get all game sessions with filtering options | GameSessionAdminController | `GameSessionAdminController_getAllSessions_get_api_admin_sessions` |
| DELETE | `/api/admin/sessions/{id}` | Force end game session (admin) | GameSessionAdminController | `GameSessionAdminController_forceEndSession_delete_api_admin_sessions_id_` |
| GET | `/api/admin/sessions/{id}` | Get detailed session information | GameSessionAdminController | `GameSessionAdminController_getSessionDetails_get_api_admin_sessions_id_` |

## KafkaAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/kafka/failed-events` | listFailedEvents | KafkaAdminController | `KafkaAdminController_listFailedEvents_get_api_v1_admin_kafka_failed_events` |
| POST | `/api/v1/admin/kafka/failed-events/bulk` | bulkOperation | KafkaAdminController | `KafkaAdminController_bulkOperation_post_api_v1_admin_kafka_failed_events_bulk` |
| DELETE | `/api/v1/admin/kafka/failed-events/{id}` | deleteEvent | KafkaAdminController | `KafkaAdminController_deleteEvent_delete_api_v1_admin_kafka_failed_events_id_` |
| GET | `/api/v1/admin/kafka/failed-events/{id}` | getFailedEvent | KafkaAdminController | `KafkaAdminController_getFailedEvent_get_api_v1_admin_kafka_failed_events_id_` |
| POST | `/api/v1/admin/kafka/failed-events/{id}/resolve` | resolveEvent | KafkaAdminController | `KafkaAdminController_resolveEvent_post_api_v1_admin_kafka_failed_events_id_resolve` |
| POST | `/api/v1/admin/kafka/failed-events/{id}/retry` | retryEvent | KafkaAdminController | `KafkaAdminController_retryEvent_post_api_v1_admin_kafka_failed_events_id_retry` |
| GET | `/api/v1/admin/kafka/health` | getHealth | KafkaAdminController | `KafkaAdminController_getHealth_get_api_v1_admin_kafka_health` |
| GET | `/api/v1/admin/kafka/metrics` | getMetrics | KafkaAdminController | `KafkaAdminController_getMetrics_get_api_v1_admin_kafka_metrics` |
| GET | `/api/v1/admin/kafka/metrics/statistics` | getStatistics | KafkaAdminController | `KafkaAdminController_getStatistics_get_api_v1_admin_kafka_metrics_statistics` |
| GET | `/api/v1/admin/kafka/metrics/topics` | getFailuresByTopic | KafkaAdminController | `KafkaAdminController_getFailuresByTopic_get_api_v1_admin_kafka_metrics_topics` |
| GET | `/api/v1/admin/kafka/retry-stats` | getRetryStats | KafkaAdminController | `KafkaAdminController_getRetryStats_get_api_v1_admin_kafka_retry_stats` |

## LayoutPublic

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/public/layout/header-footer` | Get header and footer configuration for customer frontend | LayoutPublicController | `LayoutPublicController_getHeaderFooterConfiguration_get_api_public_layout_header_footer` |

## LegacyGameCallback

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/callbacks/legacy/balance` | Handle balance updates (legacy) | LegacyGameCallbackController | `LegacyGameCallbackController_handleBalanceUpdate_post_api_callbacks_legacy_balance` |
| POST | `/api/callbacks/legacy/error` | Handle game errors (legacy) | LegacyGameCallbackController | `LegacyGameCallbackController_handleGameError_post_api_callbacks_legacy_error` |
| POST | `/api/callbacks/legacy/game-round` | Receive game round results (legacy) | LegacyGameCallbackController | `LegacyGameCallbackController_handleGameRound_post_api_callbacks_legacy_game_round` |
| POST | `/api/callbacks/legacy/jackpot` | Handle jackpot wins (legacy) | LegacyGameCallbackController | `LegacyGameCallbackController_handleJackpotWin_post_api_callbacks_legacy_jackpot` |

## LocaleAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/locales` | Get all locales | LocaleAdminController | `LocaleAdminController_getAllLocales_get_api_admin_locales` |
| POST | `/api/admin/locales` | Create locale | LocaleAdminController | `LocaleAdminController_createLocale_post_api_admin_locales` |
| GET | `/api/admin/locales/active` | Get active locales | LocaleAdminController | `LocaleAdminController_getActiveLocales_get_api_admin_locales_active` |
| GET | `/api/admin/locales/code/{code}` | Get locale by code | LocaleAdminController | `LocaleAdminController_getLocaleByCode_get_api_admin_locales_code_code_` |
| DELETE | `/api/admin/locales/{id}` | Delete locale | LocaleAdminController | `LocaleAdminController_deleteLocale_delete_api_admin_locales_id_` |
| GET | `/api/admin/locales/{id}` | Get locale by ID | LocaleAdminController | `LocaleAdminController_getLocaleById_get_api_admin_locales_id_` |
| PUT | `/api/admin/locales/{id}` | Update locale | LocaleAdminController | `LocaleAdminController_updateLocale_put_api_admin_locales_id_` |

## LoginHistoryAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/login-history` | Search login history with filters | LoginHistoryAdminController | `LoginHistoryAdminController_searchLoginHistory_get_api_v1_admin_login_history` |
| GET | `/api/v1/admin/login-history/by-fingerprint/{fingerprint}` | Get all login history for a specific fingerprint | LoginHistoryAdminController | `LoginHistoryAdminController_getLoginHistoryByFingerprint_get_api_v1_admin_login_history_by_fingerprint_fingerprint_` |
| GET | `/api/v1/admin/login-history/by-ip/{ipAddress}` | Get all login history from a specific IP address | LoginHistoryAdminController | `LoginHistoryAdminController_getLoginHistoryByIp_get_api_v1_admin_login_history_by_ip_ipAddress_` |
| GET | `/api/v1/admin/login-history/fraud-detection/duplicate-fingerprints` | Detect potential duplicate accounts by browser fingerprint | LoginHistoryAdminController | `LoginHistoryAdminController_detectDuplicateAccountsByFingerprint_get_api_v1_admin_login_history_fraud_detection_duplicate_fingerprints` |
| GET | `/api/v1/admin/login-history/fraud-detection/duplicate-ips` | Detect potential duplicate accounts by IP address | LoginHistoryAdminController | `LoginHistoryAdminController_detectDuplicateAccountsByIp_get_api_v1_admin_login_history_fraud_detection_duplicate_ips` |
| GET | `/api/v1/admin/login-history/player/{playerId}` | Get login history for a specific player | LoginHistoryAdminController | `LoginHistoryAdminController_getPlayerLoginHistory_get_api_v1_admin_login_history_player_playerId_` |
| GET | `/api/v1/admin/login-history/player/{playerId}/suspicious-activity` | Check if a player has suspicious login activity | LoginHistoryAdminController | `LoginHistoryAdminController_checkSuspiciousActivity_get_api_v1_admin_login_history_player_playerId_suspicious_activity` |
| GET | `/api/v1/admin/login-history/players-by-fingerprint` | Find all players who logged in with a specific fingerprint | LoginHistoryAdminController | `LoginHistoryAdminController_findPlayersByFingerprint_get_api_v1_admin_login_history_players_by_fingerprint` |
| GET | `/api/v1/admin/login-history/players-by-ip` | Find all players who logged in from a specific IP | LoginHistoryAdminController | `LoginHistoryAdminController_findPlayersByIp_get_api_v1_admin_login_history_players_by_ip` |

## LogsExplorer

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/logs/export` | exportLogs | LogsExplorerController | `LogsExplorerController_exportLogs_post_api_v1_admin_logs_export` |
| POST | `/api/v1/admin/logs/search` | searchLogs | LogsExplorerController | `LogsExplorerController_searchLogs_post_api_v1_admin_logs_search` |
| GET | `/api/v1/admin/logs/statistics` | getStatistics | LogsExplorerController | `LogsExplorerController_getStatistics_get_api_v1_admin_logs_statistics` |
| GET | `/api/v1/admin/logs/{id}` | getLogById | LogsExplorerController | `LogsExplorerController_getLogById_get_api_v1_admin_logs_id_` |

## Media

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/cms/media` | Get media assets with filtering | MediaController | `MediaController_getMediaAssets_get_api_v1_cms_media` |
| POST | `/api/v1/cms/media/upload` | Upload media asset to DigitalOcean Spaces | MediaController | `MediaController_uploadMedia_post_api_v1_cms_media_upload` |
| DELETE | `/api/v1/cms/media/{id}` | Delete media asset | MediaController | `MediaController_deleteMediaAsset_delete_api_v1_cms_media_id_` |
| GET | `/api/v1/cms/media/{id}` | Get media asset by ID | MediaController | `MediaController_getMediaAsset_get_api_v1_cms_media_id_` |

## MediaUpload

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/media/list` | List uploaded media files | MediaUploadController | `MediaUploadController_listMedia_get_api_admin_media_list` |
| POST | `/api/admin/media/upload` | Upload a media file | MediaUploadController | `MediaUploadController_uploadFile_post_api_admin_media_upload` |
| DELETE | `/api/admin/media/{mediaId}` | Delete a media file | MediaUploadController | `MediaUploadController_deleteMedia_delete_api_admin_media_mediaId_` |

## MenuConfigurationAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/cms/menus` | List all menu configurations | MenuConfigurationAdminController | `MenuConfigurationAdminController_listMenuConfigurations_get_api_admin_cms_menus` |
| POST | `/api/admin/cms/menus` | Create a new menu configuration | MenuConfigurationAdminController | `MenuConfigurationAdminController_createMenuConfiguration_post_api_admin_cms_menus` |
| GET | `/api/admin/cms/menus/by-name/{name}` | Get menu configuration by name | MenuConfigurationAdminController | `MenuConfigurationAdminController_getMenuConfigurationByName_get_api_admin_cms_menus_by_name_name_` |
| GET | `/api/admin/cms/menus/types` | Get available menu types | MenuConfigurationAdminController | `MenuConfigurationAdminController_getMenuTypes_get_api_admin_cms_menus_types` |
| DELETE | `/api/admin/cms/menus/{id}` | Delete menu configuration | MenuConfigurationAdminController | `MenuConfigurationAdminController_deleteMenuConfiguration_delete_api_admin_cms_menus_id_` |
| GET | `/api/admin/cms/menus/{id}` | Get menu configuration by ID | MenuConfigurationAdminController | `MenuConfigurationAdminController_getMenuConfiguration_get_api_admin_cms_menus_id_` |
| PUT | `/api/admin/cms/menus/{id}` | Update menu configuration | MenuConfigurationAdminController | `MenuConfigurationAdminController_updateMenuConfiguration_put_api_admin_cms_menus_id_` |
| POST | `/api/admin/cms/menus/{id}/duplicate` | Duplicate menu configuration | MenuConfigurationAdminController | `MenuConfigurationAdminController_duplicateMenuConfiguration_post_api_admin_cms_menus_id_duplicate` |
| POST | `/api/admin/cms/menus/{id}/localizations` | Add or update menu item localizations | MenuConfigurationAdminController | `MenuConfigurationAdminController_updateMenuLocalizations_post_api_admin_cms_menus_id_localizations` |
| GET | `/api/admin/cms/menus/{id}/localizations/{languageCode}` | Get menu localizations for specific language | MenuConfigurationAdminController | `MenuConfigurationAdminController_getMenuLocalizations_get_api_admin_cms_menus_id_localizations_languageCode_` |

## MultilanguageDemo

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/demo/multilang/cache-invalidate` | Invalidate translation cache | MultilanguageDemoController | `MultilanguageDemoController_invalidateCache_post_api_demo_multilang_cache_invalidate` |
| GET | `/api/demo/multilang/cache-test` | Test translation cache layers | MultilanguageDemoController | `MultilanguageDemoController_testTranslationCache_get_api_demo_multilang_cache_test` |
| GET | `/api/demo/multilang/page-resolution/{pageId}` | Test page configuration resolution | MultilanguageDemoController | `MultilanguageDemoController_testPageResolution_get_api_demo_multilang_page_resolution_pageId_` |
| GET | `/api/demo/multilang/performance-test` | Run performance test | MultilanguageDemoController | `MultilanguageDemoController_performanceTest_get_api_demo_multilang_performance_test` |
| POST | `/api/demo/multilang/translation-test` | Create test translation | MultilanguageDemoController | `MultilanguageDemoController_createTestTranslation_post_api_demo_multilang_translation_test` |
| GET | `/api/demo/multilang/widget-preview/{widgetId}` | Preview widget with translations | MultilanguageDemoController | `MultilanguageDemoController_previewWidgetTranslations_get_api_demo_multilang_widget_preview_widgetId_` |

## OptimizedPublicGame

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v2/public/games` | Get list of games with caching and optimization | OptimizedPublicGameController | `OptimizedPublicGameController_getGames_get_api_v2_public_games` |
| GET | `/api/v2/public/games/categories` | Get all active game categories with caching | OptimizedPublicGameController | `OptimizedPublicGameController_getCategories_get_api_v2_public_games_categories` |
| GET | `/api/v2/public/games/providers` | Get all active game providers with caching | OptimizedPublicGameController | `OptimizedPublicGameController_getProviders_get_api_v2_public_games_providers` |

## PageConfigurationAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/cms/pages` | List all page configurations | PageConfigurationAdminController | `PageConfigurationAdminController_listPageConfigurations_get_api_admin_cms_pages` |
| POST | `/api/admin/cms/pages` | Create a new page configuration | PageConfigurationAdminController | `PageConfigurationAdminController_createPageConfiguration_post_api_admin_cms_pages` |
| GET | `/api/admin/cms/pages/by-id/{id}` | Get page configuration by UUID | PageConfigurationAdminController | `PageConfigurationAdminController_getPageConfigurationById_get_api_admin_cms_pages_by_id_id_` |
| DELETE | `/api/admin/cms/pages/widgets/{widgetId}` | Delete widget | PageConfigurationAdminController | `PageConfigurationAdminController_deleteWidget_delete_api_admin_cms_pages_widgets_widgetId_` |
| PUT | `/api/admin/cms/pages/widgets/{widgetId}` | Update widget | PageConfigurationAdminController | `PageConfigurationAdminController_updateWidget_put_api_admin_cms_pages_widgets_widgetId_` |
| DELETE | `/api/admin/cms/pages/{pageId}` | Delete page configuration | PageConfigurationAdminController | `PageConfigurationAdminController_deletePageConfiguration_delete_api_admin_cms_pages_pageId_` |
| GET | `/api/admin/cms/pages/{pageId}` | Get page configuration by page ID | PageConfigurationAdminController | `PageConfigurationAdminController_getPageConfiguration_get_api_admin_cms_pages_pageId_` |
| PUT | `/api/admin/cms/pages/{pageId}` | Update page configuration | PageConfigurationAdminController | `PageConfigurationAdminController_updatePageConfiguration_put_api_admin_cms_pages_pageId_` |
| POST | `/api/admin/cms/pages/{pageId}/duplicate` | Duplicate page configuration | PageConfigurationAdminController | `PageConfigurationAdminController_duplicatePage_post_api_admin_cms_pages_pageId_duplicate` |
| GET | `/api/admin/cms/pages/{pageId}/preview` | Preview page configuration as HTML | PageConfigurationAdminController | `PageConfigurationAdminController_previewPage_get_api_admin_cms_pages_pageId_preview` |
| POST | `/api/admin/cms/pages/{pageId}/publish` | Publish page configuration | PageConfigurationAdminController | `PageConfigurationAdminController_publishPage_post_api_admin_cms_pages_pageId_publish` |
| POST | `/api/admin/cms/pages/{pageId}/unpublish` | Unpublish page configuration | PageConfigurationAdminController | `PageConfigurationAdminController_unpublishPage_post_api_admin_cms_pages_pageId_unpublish` |
| GET | `/api/admin/cms/pages/{pageId}/versions` | Get page version history | PageConfigurationAdminController | `PageConfigurationAdminController_getPageVersions_get_api_admin_cms_pages_pageId_versions` |
| POST | `/api/admin/cms/pages/{pageId}/versions/{versionNumber}/restore` | Restore page to specific version | PageConfigurationAdminController | `PageConfigurationAdminController_restoreVersion_post_api_admin_cms_pages_pageId_versions_versionNumber_restore` |
| POST | `/api/admin/cms/pages/{pageId}/widgets` | Add widget to page | PageConfigurationAdminController | `PageConfigurationAdminController_addWidget_post_api_admin_cms_pages_pageId_widgets` |
| PUT | `/api/admin/cms/pages/{pageId}/widgets/reorder` | Reorder widgets on page | PageConfigurationAdminController | `PageConfigurationAdminController_reorderWidgets_put_api_admin_cms_pages_pageId_widgets_reorder` |
| POST | `/api/admin/cms/pages/{pageId}/widgets/{widgetId}/assign` | Assign existing widget to page | PageConfigurationAdminController | `PageConfigurationAdminController_assignWidgetToPage_post_api_admin_cms_pages_pageId_widgets_widgetId_assign` |

## PageConfigurationPublic

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/cms/pages` | List published pages | PageConfigurationPublicController | `PageConfigurationPublicController_listPublishedPages_get_api_cms_pages` |
| GET | `/api/cms/pages/layout/header-footer` | Get header and footer configuration | PageConfigurationPublicController | `PageConfigurationPublicController_getHeaderFooterConfiguration_get_api_cms_pages_layout_header_footer` |
| GET | `/api/cms/pages/{pageId}` | Get public page configuration | PageConfigurationPublicController | `PageConfigurationPublicController_getPublicPageConfiguration_get_api_cms_pages_pageId_` |
| GET | `/api/cms/pages/{pageId}/preview` | Preview page configuration (requires authentication) | PageConfigurationPublicController | `PageConfigurationPublicController_previewPageConfiguration_get_api_cms_pages_pageId_preview` |

## PageLocaleOverrideAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides` | listOverrides | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_listOverrides_get_api_admin_cms_pages_pageConfigurationId_locale_overrides` |
| POST | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides` | createOverride | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_createOverride_post_api_admin_cms_pages_pageConfigurationId_locale_overrides` |
| GET | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/locales` | getPublishedLocales | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_getPublishedLocales_get_api_admin_cms_pages_pageConfigurationId_locale_overrides_locales` |
| GET | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/locales/all` | getAllLocales | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_getAllLocales_get_api_admin_cms_pages_pageConfigurationId_locale_overrides_locales_all` |
| DELETE | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/{locale}` | deleteOverride | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_deleteOverride_delete_api_admin_cms_pages_pageConfigurationId_locale_overrides_locale_` |
| GET | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/{locale}` | getOverride | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_getOverride_get_api_admin_cms_pages_pageConfigurationId_locale_overrides_locale_` |
| PUT | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/{locale}` | updateOverride | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_updateOverride_put_api_admin_cms_pages_pageConfigurationId_locale_overrides_locale_` |
| POST | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/{locale}/archive` | archiveOverride | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_archiveOverride_post_api_admin_cms_pages_pageConfigurationId_locale_overrides_locale_archive` |
| POST | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/{locale}/publish` | publishOverride | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_publishOverride_post_api_admin_cms_pages_pageConfigurationId_locale_overrides_locale_publish` |
| POST | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/{locale}/unpublish` | unpublishOverride | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_unpublishOverride_post_api_admin_cms_pages_pageConfigurationId_locale_overrides_locale_unpublish` |
| POST | `/api/admin/cms/pages/{pageConfigurationId}/locale-overrides/{locale}/validate-widgets` | validateWidgetOverrides | PageLocaleOverrideAdminController | `PageLocaleOverrideAdminController_validateWidgetOverrides_post_api_admin_cms_pages_pageConfigurationId_locale_overrides_locale_validate_widgets` |

## PasswordReset

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/password-reset/request` | Request password reset | PasswordResetController | `PasswordResetController_requestPasswordReset_post_api_v1_password_reset_request` |
| POST | `/api/v1/password-reset/reset` | Reset password | PasswordResetController | `PasswordResetController_resetPassword_post_api_v1_password_reset_reset` |
| GET | `/api/v1/password-reset/validate/{token}` | Validate reset token | PasswordResetController | `PasswordResetController_validateToken_get_api_v1_password_reset_validate_token_` |

## PaymentAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/payments` | listPayments | PaymentAdminController | `PaymentAdminController_listPayments_get_api_admin_payments` |
| GET | `/api/admin/payments/{paymentId}` | getPaymentDetails | PaymentAdminController | `PaymentAdminController_getPaymentDetails_get_api_admin_payments_paymentId_` |

## PaymentMethod

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/payment-methods` | Get all available payment methods | PaymentMethodController | `PaymentMethodController_getAllPaymentMethods_get_api_payment_methods` |
| GET | `/api/payment-methods/{code}` | Get payment method details | PaymentMethodController | `PaymentMethodController_getPaymentMethod_get_api_payment_methods_code_` |

## PaymentMethodAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/payment-methods` | Get all payment methods for admin | PaymentMethodAdminController | `PaymentMethodAdminController_getAllPaymentMethods_get_api_admin_payment_methods` |
| POST | `/api/admin/payment-methods` | Create new payment method | PaymentMethodAdminController | `PaymentMethodAdminController_createPaymentMethod_post_api_admin_payment_methods` |
| DELETE | `/api/admin/payment-methods/{code}` | Delete payment method | PaymentMethodAdminController | `PaymentMethodAdminController_deletePaymentMethod_delete_api_admin_payment_methods_code_` |
| PUT | `/api/admin/payment-methods/{code}` | Update payment method | PaymentMethodAdminController | `PaymentMethodAdminController_updatePaymentMethod_put_api_admin_payment_methods_code_` |
| PATCH | `/api/admin/payment-methods/{code}/availability` | Update payment method availability | PaymentMethodAdminController | `PaymentMethodAdminController_updatePaymentMethodAvailability_patch_api_admin_payment_methods_code_availability` |
| PUT | `/api/admin/payment-methods/{code}/countries` | Update payment method country availability | PaymentMethodAdminController | `PaymentMethodAdminController_updatePaymentMethodCountries_put_api_admin_payment_methods_code_countries` |

## PaymentWebhook

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/payment/hook` | handlePaymentWebhook | PaymentWebhookController | `PaymentWebhookController_handlePaymentWebhook_post_api_payment_hook` |
| GET | `/api/payment/player/balance` | getPlayerBalance | PaymentWebhookController | `PaymentWebhookController_getPlayerBalance_get_api_payment_player_balance` |

## PhoneVerification

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/phone-verification/resend-code` | resendVerificationCode | PhoneVerificationController | `PhoneVerificationController_resendVerificationCode_post_api_v1_phone_verification_resend_code` |
| POST | `/api/v1/phone-verification/send-code` | sendVerificationCode | PhoneVerificationController | `PhoneVerificationController_sendVerificationCode_post_api_v1_phone_verification_send_code` |
| POST | `/api/v1/phone-verification/update-phone` | updatePhoneWithVerification | PhoneVerificationController | `PhoneVerificationController_updatePhoneWithVerification_post_api_v1_phone_verification_update_phone` |
| POST | `/api/v1/phone-verification/verify` | verifyPhone | PhoneVerificationController | `PhoneVerificationController_verifyPhone_post_api_v1_phone_verification_verify` |

## Player

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/players` | Get all players (admin only) | PlayerController | `PlayerController_getAllPlayers_get_api_players` |
| POST | `/api/players` | Register a new player | PlayerController | `PlayerController_registerPlayer_post_api_players` |
| POST | `/api/players/advanced-search` | Advanced player search with multiple filter criteria (admin only) | PlayerController | `PlayerController_advancedSearch_post_api_players_advanced_search` |
| GET | `/api/players/me` | Get current player details | PlayerController | `PlayerController_getCurrentPlayer_get_api_players_me` |
| GET | `/api/players/registration/signup-config` | Get signup configuration for registration form | PlayerController | `PlayerController_getSignupConfiguration_get_api_players_registration_signup_config` |
| GET | `/api/players/search` | Search players by username or email (admin only) | PlayerController | `PlayerController_searchPlayers_get_api_players_search` |
| GET | `/api/players/status/{status}` | Get players by status (admin only) | PlayerController | `PlayerController_getPlayersByStatus_get_api_players_status_status_` |
| GET | `/api/players/{id}` | Get player details by ID | PlayerController | `PlayerController_getPlayerById_get_api_players_id_` |
| PATCH | `/api/players/{id}` | Partial update of player profile information (admin only) | PlayerController | `PlayerController_patchPlayer_patch_api_players_id_` |
| GET | `/api/players/{id}/bets` | Get player bets (casino game rounds and sports bets) | PlayerController | `PlayerController_getPlayerBets_get_api_players_id_bets` |
| GET | `/api/players/{id}/bets/export` | exportPlayerBets | PlayerController | `PlayerController_exportPlayerBets_get_api_players_id_bets_export` |
| GET | `/api/players/{id}/games` | Get player game sessions with filters and statistics (player or admin only) | PlayerController | `PlayerController_getPlayerGames_get_api_players_id_games` |
| GET | `/api/players/{id}/transactions` | Get player transactions with optional filters (player or admin only) | PlayerController | `PlayerController_getPlayerTransactions_get_api_players_id_transactions` |
| GET | `/api/players/{id}/wallet` | Get player wallet details (player or admin only) | PlayerController | `PlayerController_getPlayerWallet_get_api_players_id_wallet` |
| POST | `/api/players/{playerId}/collect-fields` | Collect additional fields from player | PlayerController | `PlayerController_collectAdditionalFields_post_api_players_playerId_collect_fields` |
| GET | `/api/players/{playerId}/financial-summary` | Get player financial summary for header card display | PlayerController | `PlayerController_getPlayerFinancialSummary_get_api_players_playerId_financial_summary` |
| GET | `/api/players/{playerId}/missing-fields/{collectionPoint}` | Check missing required fields for collection point | PlayerController | `PlayerController_checkMissingFields_get_api_players_playerId_missing_fields_collectionPoint_` |

## PlayerAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/players` | Create a new player as an administrator | PlayerAdminController | `PlayerAdminController_createPlayer_post_api_v1_admin_players` |
| POST | `/api/v1/admin/players/export` | exportPlayers | PlayerAdminController | `PlayerAdminController_exportPlayers_post_api_v1_admin_players_export` |
| GET | `/api/v1/admin/players/status-counts` | getPlayerStatusCounts | PlayerAdminController | `PlayerAdminController_getPlayerStatusCounts_get_api_v1_admin_players_status_counts` |
| GET | `/api/v1/admin/players/{playerId}/statistics/aggregate` | getPlayerStatisticsAggregate | PlayerAdminController | `PlayerAdminController_getPlayerStatisticsAggregate_get_api_v1_admin_players_playerId_statistics_aggregate` |
| POST | `/api/v1/admin/players/{playerId}/wallet/adjust` | adjustWalletBalance | PlayerAdminController | `PlayerAdminController_adjustWalletBalance_post_api_v1_admin_players_playerId_wallet_adjust` |
| POST | `/api/v1/admin/players/{playerId}/wallet/deposit` | manualDeposit | PlayerAdminController | `PlayerAdminController_manualDeposit_post_api_v1_admin_players_playerId_wallet_deposit` |
| GET | `/api/v1/admin/players/{playerId}/wallet/manual-deposits` | getManualDepositHistory | PlayerAdminController | `PlayerAdminController_getManualDepositHistory_get_api_v1_admin_players_playerId_wallet_manual_deposits` |

## PlayerBonusRestriction

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/player-bonus-restrictions` | createRestriction | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_createRestriction_post_api_v1_admin_player_bonus_restrictions` |
| GET | `/api/v1/admin/player-bonus-restrictions/bonus/{bonusId}` | getBonusRestrictions | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_getBonusRestrictions_get_api_v1_admin_player_bonus_restrictions_bonus_bonusId_` |
| GET | `/api/v1/admin/player-bonus-restrictions/check` | checkRestriction | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_checkRestriction_get_api_v1_admin_player_bonus_restrictions_check` |
| GET | `/api/v1/admin/player-bonus-restrictions/player/{playerId}` | getPlayerRestrictions | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_getPlayerRestrictions_get_api_v1_admin_player_bonus_restrictions_player_playerId_` |
| GET | `/api/v1/admin/player-bonus-restrictions/player/{playerId}/all-bonuses-status` | getAllBonusesRestrictionStatus | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_getAllBonusesRestrictionStatus_get_api_v1_admin_player_bonus_restrictions_player_playerId_all_bonuses_status` |
| DELETE | `/api/v1/admin/player-bonus-restrictions/player/{playerId}/bonus/{bonusId}` | deleteRestrictionByPlayerAndBonus | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_deleteRestrictionByPlayerAndBonus_delete_api_v1_admin_player_bonus_restrictions_player_playerId_bonus_bonusId_` |
| DELETE | `/api/v1/admin/player-bonus-restrictions/player/{playerId}/restrict-all` | unrestrictAllBonuses | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_unrestrictAllBonuses_delete_api_v1_admin_player_bonus_restrictions_player_playerId_restrict_all` |
| POST | `/api/v1/admin/player-bonus-restrictions/player/{playerId}/restrict-all` | restrictAllBonuses | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_restrictAllBonuses_post_api_v1_admin_player_bonus_restrictions_player_playerId_restrict_all` |
| GET | `/api/v1/admin/player-bonus-restrictions/player/{playerId}/restricted-bonus-ids` | getRestrictedBonusIds | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_getRestrictedBonusIds_get_api_v1_admin_player_bonus_restrictions_player_playerId_restricted_bonus_ids` |
| DELETE | `/api/v1/admin/player-bonus-restrictions/{id}` | deleteRestriction | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_deleteRestriction_delete_api_v1_admin_player_bonus_restrictions_id_` |
| GET | `/api/v1/admin/player-bonus-restrictions/{id}` | getRestriction | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_getRestriction_get_api_v1_admin_player_bonus_restrictions_id_` |
| PUT | `/api/v1/admin/player-bonus-restrictions/{id}` | updateRestriction | PlayerBonusRestrictionController | `PlayerBonusRestrictionController_updateRestriction_put_api_v1_admin_player_bonus_restrictions_id_` |

## PlayerCashierRestriction

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/bonus-games-status` | getBonusGamesRestrictionStatus | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_getBonusGamesRestrictionStatus_get_api_v1_admin_player_cashier_restrictions_player_playerId_bonus_games_status` |
| GET | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/bonus-types-status` | getBonusTypesRestrictionStatus | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_getBonusTypesRestrictionStatus_get_api_v1_admin_player_cashier_restrictions_player_playerId_bonus_types_status` |
| GET | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/deposits-status` | getDepositsRestrictionStatus | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_getDepositsRestrictionStatus_get_api_v1_admin_player_cashier_restrictions_player_playerId_deposits_status` |
| DELETE | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-bonus-games` | unrestrictBonusGames | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_unrestrictBonusGames_delete_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_bonus_games` |
| POST | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-bonus-games` | restrictBonusGames | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_restrictBonusGames_post_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_bonus_games` |
| DELETE | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-bonus-types` | unrestrictBonusTypes | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_unrestrictBonusTypes_delete_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_bonus_types` |
| POST | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-bonus-types` | restrictBonusTypes | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_restrictBonusTypes_post_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_bonus_types` |
| DELETE | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-deposits` | unrestrictDeposits | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_unrestrictDeposits_delete_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_deposits` |
| POST | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-deposits` | restrictDeposits | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_restrictDeposits_post_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_deposits` |
| DELETE | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-withdrawals` | unrestrictWithdrawals | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_unrestrictWithdrawals_delete_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_withdrawals` |
| POST | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/restrict-withdrawals` | restrictWithdrawals | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_restrictWithdrawals_post_api_v1_admin_player_cashier_restrictions_player_playerId_restrict_withdrawals` |
| GET | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/status` | getCashierRestrictionsStatus | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_getCashierRestrictionsStatus_get_api_v1_admin_player_cashier_restrictions_player_playerId_status` |
| GET | `/api/v1/admin/player-cashier-restrictions/player/{playerId}/withdrawals-status` | getWithdrawalsRestrictionStatus | PlayerCashierRestrictionController | `PlayerCashierRestrictionController_getWithdrawalsRestrictionStatus_get_api_v1_admin_player_cashier_restrictions_player_playerId_withdrawals_status` |

## PlayerComment

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/players/{playerId}/comments` | getComments | PlayerCommentController | `PlayerCommentController_getComments_get_api_v1_admin_players_playerId_comments` |
| POST | `/api/v1/admin/players/{playerId}/comments` | createComment | PlayerCommentController | `PlayerCommentController_createComment_post_api_v1_admin_players_playerId_comments` |
| DELETE | `/api/v1/admin/players/{playerId}/comments/{commentId}` | deleteComment | PlayerCommentController | `PlayerCommentController_deleteComment_delete_api_v1_admin_players_playerId_comments_commentId_` |
| GET | `/api/v1/admin/players/{playerId}/comments/{commentId}` | getComment | PlayerCommentController | `PlayerCommentController_getComment_get_api_v1_admin_players_playerId_comments_commentId_` |
| PUT | `/api/v1/admin/players/{playerId}/comments/{commentId}` | updateComment | PlayerCommentController | `PlayerCommentController_updateComment_put_api_v1_admin_players_playerId_comments_commentId_` |

## PlayerLimit

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/players/{playerId}/responsible/limits` | Get all limits for a player | PlayerLimitController | `PlayerLimitController_getAllLimits_get_api_players_playerId_responsible_limits` |
| POST | `/api/players/{playerId}/responsible/limits` | Set a new player limit | PlayerLimitController | `PlayerLimitController_setLimit_post_api_players_playerId_responsible_limits` |
| GET | `/api/players/{playerId}/responsible/limits/summary` | Get summary of player limits | PlayerLimitController | `PlayerLimitController_getLimitsSummary_get_api_players_playerId_responsible_limits_summary` |
| DELETE | `/api/players/{playerId}/responsible/limits/{limitId}` | Remove a player limit | PlayerLimitController | `PlayerLimitController_removeLimit_delete_api_players_playerId_responsible_limits_limitId_` |
| GET | `/api/players/{playerId}/responsible/limits/{limitId}` | Get specific limit details | PlayerLimitController | `PlayerLimitController_getLimitById_get_api_players_playerId_responsible_limits_limitId_` |
| PUT | `/api/players/{playerId}/responsible/limits/{limitId}` | Update an existing limit | PlayerLimitController | `PlayerLimitController_updateLimit_put_api_players_playerId_responsible_limits_limitId_` |

## PlayerProfileField

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/player/profile/field-values` | Get player's profile field values | PlayerProfileFieldController | `PlayerProfileFieldController_getProfileFieldValues_get_api_v1_player_profile_field_values` |
| GET | `/api/v1/player/profile/fields` | Get profile fields configuration | PlayerProfileFieldController | `PlayerProfileFieldController_getProfileFields_get_api_v1_player_profile_fields` |
| PUT | `/api/v1/player/profile/update-fields` | Update player's profile field values | PlayerProfileFieldController | `PlayerProfileFieldController_updateProfileFields_put_api_v1_player_profile_update_fields` |

## PlayerProfilePicture

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| DELETE | `/api/v1/player/profile/picture` | deleteProfilePicture | PlayerProfilePictureController | `PlayerProfilePictureController_deleteProfilePicture_delete_api_v1_player_profile_picture` |
| GET | `/api/v1/player/profile/picture` | getProfilePicture | PlayerProfilePictureController | `PlayerProfilePictureController_getProfilePicture_get_api_v1_player_profile_picture` |
| POST | `/api/v1/player/profile/picture` | uploadProfilePicture | PlayerProfilePictureController | `PlayerProfilePictureController_uploadProfilePicture_post_api_v1_player_profile_picture` |

## PlayerProfileUpdate

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/player-profile-updates/preview` | previewProfileUpdate | PlayerProfileUpdateController | `PlayerProfileUpdateController_previewProfileUpdate_get_api_v1_admin_player_profile_updates_preview` |
| POST | `/api/v1/admin/player-profile-updates/update` | updateProfileFromDocument | PlayerProfileUpdateController | `PlayerProfileUpdateController_updateProfileFromDocument_post_api_v1_admin_player_profile_updates_update` |

## PlayerSimpleKyc

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| DELETE | `/api/v1/player/simple-kyc/cancel` | Cancel KYC request | PlayerSimpleKycController | `PlayerSimpleKycController_cancelKycRequest_delete_api_v1_player_simple_kyc_cancel` |
| DELETE | `/api/v1/player/simple-kyc/documents/address` | Cancel address document | PlayerSimpleKycController | `PlayerSimpleKycController_cancelAddressDocument_delete_api_v1_player_simple_kyc_documents_address` |
| POST | `/api/v1/player/simple-kyc/documents/address` | Upload address documents | PlayerSimpleKycController | `PlayerSimpleKycController_uploadAddressDocuments_post_api_v1_player_simple_kyc_documents_address` |
| DELETE | `/api/v1/player/simple-kyc/documents/identity` | Cancel identity document | PlayerSimpleKycController | `PlayerSimpleKycController_cancelIdentityDocument_delete_api_v1_player_simple_kyc_documents_identity` |
| POST | `/api/v1/player/simple-kyc/documents/identity` | Upload identity documents | PlayerSimpleKycController | `PlayerSimpleKycController_uploadIdentityDocuments_post_api_v1_player_simple_kyc_documents_identity` |
| POST | `/api/v1/player/simple-kyc/email/resend` | Resend email verification code | PlayerSimpleKycController | `PlayerSimpleKycController_resendEmailVerificationCode_post_api_v1_player_simple_kyc_email_resend` |
| POST | `/api/v1/player/simple-kyc/email/send-code` | Request email verification code | PlayerSimpleKycController | `PlayerSimpleKycController_sendEmailVerificationCode_post_api_v1_player_simple_kyc_email_send_code` |
| POST | `/api/v1/player/simple-kyc/email/verify` | Verify email code | PlayerSimpleKycController | `PlayerSimpleKycController_verifyEmailCode_post_api_v1_player_simple_kyc_email_verify` |
| POST | `/api/v1/player/simple-kyc/phone/resend` | Resend phone verification code | PlayerSimpleKycController | `PlayerSimpleKycController_resendPhoneVerificationCode_post_api_v1_player_simple_kyc_phone_resend` |
| POST | `/api/v1/player/simple-kyc/phone/send-code` | Request phone verification code | PlayerSimpleKycController | `PlayerSimpleKycController_sendPhoneVerificationCode_post_api_v1_player_simple_kyc_phone_send_code` |
| POST | `/api/v1/player/simple-kyc/phone/verify` | Verify phone code | PlayerSimpleKycController | `PlayerSimpleKycController_verifyPhoneCode_post_api_v1_player_simple_kyc_phone_verify` |
| GET | `/api/v1/player/simple-kyc/status` | Get KYC status | PlayerSimpleKycController | `PlayerSimpleKycController_getKycStatus_get_api_v1_player_simple_kyc_status` |
| POST | `/api/v1/player/simple-kyc/submit` | Submit KYC for review | PlayerSimpleKycController | `PlayerSimpleKycController_submitForReview_post_api_v1_player_simple_kyc_submit` |

## PlayerStatistics

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/players/statistics/active-players` | getRecentActivePlayers | PlayerStatisticsController | `PlayerStatisticsController_getRecentActivePlayers_get_api_v1_admin_players_statistics_active_players` |
| POST | `/api/v1/admin/players/statistics/activity/cleanup` | cleanupOldActivityData | PlayerStatisticsController | `PlayerStatisticsController_cleanupOldActivityData_post_api_v1_admin_players_statistics_activity_cleanup` |
| POST | `/api/v1/admin/players/statistics/activity/flush` | flushActivityBuffer | PlayerStatisticsController | `PlayerStatisticsController_flushActivityBuffer_post_api_v1_admin_players_statistics_activity_flush` |
| POST | `/api/v1/admin/players/statistics/cleanup` | cleanupOldStatistics | PlayerStatisticsController | `PlayerStatisticsController_cleanupOldStatistics_post_api_v1_admin_players_statistics_cleanup` |
| GET | `/api/v1/admin/players/statistics/top-players` | getTopPlayersByVolume | PlayerStatisticsController | `PlayerStatisticsController_getTopPlayersByVolume_get_api_v1_admin_players_statistics_top_players` |
| GET | `/api/v1/admin/players/statistics/{playerId}` | getPlayerStatistics | PlayerStatisticsController | `PlayerStatisticsController_getPlayerStatistics_get_api_v1_admin_players_statistics_playerId_` |
| GET | `/api/v1/admin/players/statistics/{playerId}/activity` | getPlayerActivitySummary | PlayerStatisticsController | `PlayerStatisticsController_getPlayerActivitySummary_get_api_v1_admin_players_statistics_playerId_activity` |
| GET | `/api/v1/admin/players/statistics/{playerId}/aggregate` | getPlayerStatisticsAggregate | PlayerStatisticsController | `PlayerStatisticsController_getPlayerStatisticsAggregate_get_api_v1_admin_players_statistics_playerId_aggregate` |
| GET | `/api/v1/admin/players/statistics/{playerId}/multi-currency` | getPlayerStatisticsByCurrencies | PlayerStatisticsController | `PlayerStatisticsController_getPlayerStatisticsByCurrencies_get_api_v1_admin_players_statistics_playerId_multi_currency` |
| GET | `/api/v1/admin/players/statistics/{playerId}/verification-summary` | getVerificationStatistics | PlayerStatisticsController | `PlayerStatisticsController_getVerificationStatistics_get_api_v1_admin_players_statistics_playerId_verification_summary` |

## Promotion

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/promotions` | Get all promotions (admin) | PromotionController | `PromotionController_getAllPromotions_get_api_v1_admin_promotions` |
| POST | `/api/v1/admin/promotions` | Create a new promotion | PromotionController | `PromotionController_createPromotion_post_api_v1_admin_promotions` |
| GET | `/api/v1/admin/promotions/expired` | Get expired promotions | PromotionController | `PromotionController_getExpiredPromotions_get_api_v1_admin_promotions_expired` |
| GET | `/api/v1/admin/promotions/search` | Search promotions | PromotionController | `PromotionController_searchPromotions_get_api_v1_admin_promotions_search` |
| GET | `/api/v1/admin/promotions/upcoming` | Get upcoming promotions | PromotionController | `PromotionController_getUpcomingPromotions_get_api_v1_admin_promotions_upcoming` |
| DELETE | `/api/v1/admin/promotions/{id}` | Delete a promotion | PromotionController | `PromotionController_deletePromotion_delete_api_v1_admin_promotions_id_` |
| GET | `/api/v1/admin/promotions/{id}` | Get promotion by ID (admin) | PromotionController | `PromotionController_getPromotionById_get_api_v1_admin_promotions_id_` |
| PUT | `/api/v1/admin/promotions/{id}` | Update an existing promotion | PromotionController | `PromotionController_updatePromotion_put_api_v1_admin_promotions_id_` |
| POST | `/api/v1/admin/promotions/{id}/duplicate` | Duplicate a promotion | PromotionController | `PromotionController_duplicatePromotion_post_api_v1_admin_promotions_id_duplicate` |
| POST | `/api/v1/admin/promotions/{id}/toggle-home-screen` | Toggle promotion show on home screen status | PromotionController | `PromotionController_togglePromotionHomeScreenStatus_post_api_v1_admin_promotions_id_toggle_home_screen` |
| POST | `/api/v1/admin/promotions/{id}/toggle-status` | Toggle promotion active status | PromotionController | `PromotionController_togglePromotionStatus_post_api_v1_admin_promotions_id_toggle_status` |
| GET | `/api/v1/player/promotions` | Get active promotions for authenticated player (filtered by their country) | PromotionController | `PromotionController_getPlayerPromotions_get_api_v1_player_promotions` |
| GET | `/api/v1/player/promotions/type/{type}` | Get active promotions by type for authenticated player (filtered by their country) | PromotionController | `PromotionController_getPlayerPromotionsByType_get_api_v1_player_promotions_type_type_` |
| GET | `/api/v1/player/promotions/{id}` | Get promotion details for authenticated player (checks country restriction) | PromotionController | `PromotionController_getPlayerPromotionDetails_get_api_v1_player_promotions_id_` |
| GET | `/api/v1/promotions` | Get active promotions (public) | PromotionController | `PromotionController_getActivePromotions_get_api_v1_promotions` |
| GET | `/api/v1/promotions/country/{countryCode}` | Get active promotions available in a specific country | PromotionController | `PromotionController_getPromotionsForCountry_get_api_v1_promotions_country_countryCode_` |
| GET | `/api/v1/promotions/languages` | Get available languages for promotions | PromotionController | `PromotionController_getAvailableLanguages_get_api_v1_promotions_languages` |
| GET | `/api/v1/promotions/type/{type}` | Get active promotions by type (public) | PromotionController | `PromotionController_getPromotionsByType_get_api_v1_promotions_type_type_` |
| GET | `/api/v1/promotions/types` | Get available promotion types | PromotionController | `PromotionController_getPromotionTypes_get_api_v1_promotions_types` |
| GET | `/api/v1/promotions/{id}` | Get promotion details (public) | PromotionController | `PromotionController_getPromotionDetails_get_api_v1_promotions_id_` |

## ProviderAnalytics

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/analytics/providers/best-performing` | Get best performing providers by various metrics | ProviderAnalyticsController | `ProviderAnalyticsController_getBestPerformingProviders_get_api_admin_analytics_providers_best_performing` |
| POST | `/api/admin/analytics/providers/generate-all` | Generate analytics for all providers | ProviderAnalyticsController | `ProviderAnalyticsController_generateAllProviderAnalytics_post_api_admin_analytics_providers_generate_all` |
| GET | `/api/admin/analytics/providers/{providerId}` | Get analytics for a specific provider | ProviderAnalyticsController | `ProviderAnalyticsController_getProviderAnalytics_get_api_admin_analytics_providers_providerId_` |
| POST | `/api/admin/analytics/providers/{providerId}/generate` | Generate analytics for a specific provider | ProviderAnalyticsController | `ProviderAnalyticsController_generateProviderAnalytics_post_api_admin_analytics_providers_providerId_generate` |

## ProviderCallback

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/provider` | finishRound | ProviderCallbackController | `ProviderCallbackController_finishRound_post_api_v1_provider` |
| GET | `/api/v1/provider/{provider}/ping` | ping | ProviderCallbackController | `ProviderCallbackController_ping_get_api_v1_provider_provider_ping` |

## PublicAuth

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/auth/heartbeat` | Check session validity and get remaining time (OCP-483) | PublicAuthController | `PublicAuthController_heartbeat_get_api_v1_auth_heartbeat` |
| POST | `/api/v1/auth/login` | Login with username and password | PublicAuthController | `PublicAuthController_login_post_api_v1_auth_login` |
| POST | `/api/v1/auth/refresh` | Refresh access token | PublicAuthController | `PublicAuthController_refreshToken_post_api_v1_auth_refresh` |
| POST | `/api/v1/auth/verify-2fa` | Verify 2FA code and complete login | PublicAuthController | `PublicAuthController_verify2FA_post_api_v1_auth_verify_2fa` |

## PublicBanner

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/public/banners/active` | getActiveBanners | PublicBannerController | `PublicBannerController_getActiveBanners_get_api_v1_public_banners_active` |

## PublicBonus

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/public/bonuses/active` | List all active bonuses | PublicBonusController | `PublicBonusController_listActiveBonuses_get_api_public_bonuses_active` |
| GET | `/api/public/bonuses/player/{playerId}/awards` | Get player's bonus awards | PublicBonusController | `PublicBonusController_getPlayerBonusHistory_get_api_public_bonuses_player_playerId_awards` |

## PublicCashier

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/player/public/balance` | getCashierConfig | PublicCashierController | `PublicCashierController_getCashierConfig_get_api_player_public_balance` |

## PublicCms

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/public/cms/cache/stats` | getCacheStats | PublicCmsController | `PublicCmsController_getCacheStats_get_api_public_cms_cache_stats` |
| POST | `/api/public/cms/cache/warmup` | warmupCache | PublicCmsController | `PublicCmsController_warmupCache_post_api_public_cms_cache_warmup` |
| GET | `/api/public/cms/menus/{menuName}` | getMenu | PublicCmsController | `PublicCmsController_getMenu_get_api_public_cms_menus_menuName_` |
| GET | `/api/public/cms/pages` | List available pages | PublicCmsController | `PublicCmsController_listPages_get_api_public_cms_pages` |
| GET | `/api/public/cms/pages/{pageId}` | getPageConfiguration | PublicCmsController | `PublicCmsController_getPageConfiguration_get_api_public_cms_pages_pageId_` |

## PublicGame

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/public/games` | Get list of games with optional filtering | PublicGameController | `PublicGameController_getGames_get_api_public_games` |
| GET | `/api/public/games/categories` | Get all active game categories | PublicGameController | `PublicGameController_getCategories_get_api_public_games_categories` |
| GET | `/api/public/games/featured` | Get featured games | PublicGameController | `PublicGameController_getFeaturedGames_get_api_public_games_featured` |
| GET | `/api/public/games/filters` | Get available filter options with counts | PublicGameController | `PublicGameController_getFilterOptions_get_api_public_games_filters` |
| GET | `/api/public/games/new` | Get newly added games | PublicGameController | `PublicGameController_getNewGames_get_api_public_games_new` |
| GET | `/api/public/games/popular` | Get popular games | PublicGameController | `PublicGameController_getPopularGames_get_api_public_games_popular` |
| GET | `/api/public/games/providers` | Get all active game providers | PublicGameController | `PublicGameController_getProviders_get_api_public_games_providers` |
| GET | `/api/public/games/search` | Search games by name or provider | PublicGameController | `PublicGameController_searchGames_get_api_public_games_search` |
| GET | `/api/public/games/search-ranked` | Search games with custom ranking algorithm | PublicGameController | `PublicGameController_searchGamesWithRanking_get_api_public_games_search_ranked` |
| GET | `/api/public/games/types` | Get all available game types | PublicGameController | `PublicGameController_getGameTypes_get_api_public_games_types` |
| GET | `/api/public/games/{id}` | Get game details by ID | PublicGameController | `PublicGameController_getGameDetails_get_api_public_games_id_` |
| GET | `/api/public/games/{id}/stats` | Get game stats (RTP, volatility, bet limits, paylines) | PublicGameController | `PublicGameController_getGameStats_get_api_public_games_id_stats` |

## PublicGameLaunch

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/public/games/{id}/demo` | Launch game in demo mode (public endpoint - no auth required) | PublicGameLaunchController | `PublicGameLaunchController_launchGameDemo_post_api_public_games_id_demo` |

## PublicRegistration

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/public/registration/check-email` | checkEmail | PublicRegistrationController | `PublicRegistrationController_checkEmail_get_api_v1_public_registration_check_email` |
| GET | `/api/v1/public/registration/check-username` | checkUsername | PublicRegistrationController | `PublicRegistrationController_checkUsername_get_api_v1_public_registration_check_username` |
| GET | `/api/v1/public/registration/fields` | getRegistrationFields | PublicRegistrationController | `PublicRegistrationController_getRegistrationFields_get_api_v1_public_registration_fields` |
| POST | `/api/v1/public/registration/signup` | registerPlayer | PublicRegistrationController | `PublicRegistrationController_registerPlayer_post_api_v1_public_registration_signup` |
| GET | `/api/v1/public/registration/signup-config` | getSignupConfiguration | PublicRegistrationController | `PublicRegistrationController_getSignupConfiguration_get_api_v1_public_registration_signup_config` |
| POST | `/api/v1/public/registration/validate` | validateRegistration | PublicRegistrationController | `PublicRegistrationController_validateRegistration_post_api_v1_public_registration_validate` |

## PublicVendor

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/public/vendors` | getVendors | PublicVendorController | `PublicVendorController_getVendors_get_api_public_vendors` |
| GET | `/api/public/vendors/featured` | getFeaturedVendors | PublicVendorController | `PublicVendorController_getFeaturedVendors_get_api_public_vendors_featured` |
| GET | `/api/public/vendors/{id}` | getVendorDetails | PublicVendorController | `PublicVendorController_getVendorDetails_get_api_public_vendors_id_` |

## RefundAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/refunds` | listRefunds | RefundAdminController | `RefundAdminController_listRefunds_get_api_admin_refunds` |
| POST | `/api/admin/refunds` | createRefundRequest | RefundAdminController | `RefundAdminController_createRefundRequest_post_api_admin_refunds` |
| POST | `/api/admin/refunds/by-payment-uuid` | createRefundRequestByUuid | RefundAdminController | `RefundAdminController_createRefundRequestByUuid_post_api_admin_refunds_by_payment_uuid` |
| GET | `/api/admin/refunds/statistics` | getStatistics | RefundAdminController | `RefundAdminController_getStatistics_get_api_admin_refunds_statistics` |
| GET | `/api/admin/refunds/{id}` | getRefund | RefundAdminController | `RefundAdminController_getRefund_get_api_admin_refunds_id_` |
| PUT | `/api/admin/refunds/{id}/approve` | approveRefund | RefundAdminController | `RefundAdminController_approveRefund_put_api_admin_refunds_id_approve` |
| PUT | `/api/admin/refunds/{id}/process` | processRefund | RefundAdminController | `RefundAdminController_processRefund_put_api_admin_refunds_id_process` |
| PUT | `/api/admin/refunds/{id}/reject` | rejectRefund | RefundAdminController | `RefundAdminController_rejectRefund_put_api_admin_refunds_id_reject` |

## RegistrationConfig

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/registration-config/fields` | Get all registration fields | RegistrationConfigController | `RegistrationConfigController_getAllFields_get_api_admin_registration_config_fields` |
| POST | `/api/admin/registration-config/fields/reorder/{collectionPoint}` | Reorder fields for collection point | RegistrationConfigController | `RegistrationConfigController_reorderFields_post_api_admin_registration_config_fields_reorder_collectionPoint_` |
| GET | `/api/admin/registration-config/fields/{collectionPoint}` | Get fields for specific collection point | RegistrationConfigController | `RegistrationConfigController_getFieldsByCollectionPoint_get_api_admin_registration_config_fields_collectionPoint_` |
| PATCH | `/api/admin/registration-config/fields/{fieldId}/active` | Toggle field active status | RegistrationConfigController | `RegistrationConfigController_toggleFieldActive_patch_api_admin_registration_config_fields_fieldId_active` |
| DELETE | `/api/admin/registration-config/fields/{fieldId}/config/{collectionPoint}` | Remove field from collection point | RegistrationConfigController | `RegistrationConfigController_removeFieldFromCollectionPoint_delete_api_admin_registration_config_fields_fieldId_config_collectionPoint_` |
| PUT | `/api/admin/registration-config/fields/{fieldId}/config/{collectionPoint}` | Update field configuration for collection point | RegistrationConfigController | `RegistrationConfigController_updateFieldConfig_put_api_admin_registration_config_fields_fieldId_config_collectionPoint_` |
| GET | `/api/admin/registration-config/signup-config` | Get complete signup configuration | RegistrationConfigController | `RegistrationConfigController_getSignupConfiguration_get_api_admin_registration_config_signup_config` |

## Reporting

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/reporting/cache/refresh` | refreshCache | ReportingController | `ReportingController_refreshCache_post_api_v1_reporting_cache_refresh` |
| GET | `/api/v1/reporting/dashboard` | getDashboardMetrics | ReportingController | `ReportingController_getDashboardMetrics_get_api_v1_reporting_dashboard` |
| GET | `/api/v1/reporting/ftd` | getFtdMetrics | ReportingController | `ReportingController_getFtdMetrics_get_api_v1_reporting_ftd` |
| GET | `/api/v1/reporting/ftd/cohort` | getFtdCohortAnalysis | ReportingController | `ReportingController_getFtdCohortAnalysis_get_api_v1_reporting_ftd_cohort` |
| GET | `/api/v1/reporting/ftd/conversion` | getFtdConversionRate | ReportingController | `ReportingController_getFtdConversionRate_get_api_v1_reporting_ftd_conversion` |
| GET | `/api/v1/reporting/providers` | getProviderMetrics | ReportingController | `ReportingController_getProviderMetrics_get_api_v1_reporting_providers` |
| GET | `/api/v1/reporting/rankings` | getPlayerRankings | ReportingController | `ReportingController_getPlayerRankings_get_api_v1_reporting_rankings` |
| GET | `/api/v1/reporting/realtime` | getRealTimeMetrics | ReportingController | `ReportingController_getRealTimeMetrics_get_api_v1_reporting_realtime` |
| POST | `/api/v1/reporting/recalculate` | recalculateReportingData | ReportingController | `ReportingController_recalculateReportingData_post_api_v1_reporting_recalculate` |
| GET | `/api/v1/reporting/summary` | getSummaryStatistics | ReportingController | `ReportingController_getSummaryStatistics_get_api_v1_reporting_summary` |
| GET | `/api/v1/reporting/vendors/{vendorId}` | getVendorMetrics | ReportingController | `ReportingController_getVendorMetrics_get_api_v1_reporting_vendors_vendorId_` |

## ReportingExport

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/reporting/export/comprehensive/json` | exportToJson | ReportingExportController | `ReportingExportController_exportToJson_get_api_v1_reporting_export_comprehensive_json` |
| GET | `/api/v1/reporting/export/dashboard/excel` | exportDashboardToExcel | ReportingExportController | `ReportingExportController_exportDashboardToExcel_get_api_v1_reporting_export_dashboard_excel` |
| GET | `/api/v1/reporting/export/formats` | getExportFormats | ReportingExportController | `ReportingExportController_getExportFormats_get_api_v1_reporting_export_formats` |
| GET | `/api/v1/reporting/export/history` | getExportHistory | ReportingExportController | `ReportingExportController_getExportHistory_get_api_v1_reporting_export_history` |
| GET | `/api/v1/reporting/export/rankings/csv` | exportRankingsToCsv | ReportingExportController | `ReportingExportController_exportRankingsToCsv_get_api_v1_reporting_export_rankings_csv` |
| POST | `/api/v1/reporting/export/schedule` | scheduleReport | ReportingExportController | `ReportingExportController_scheduleReport_post_api_v1_reporting_export_schedule` |
| GET | `/api/v1/reporting/export/timeseries/csv` | exportTimeSeriesToCsv | ReportingExportController | `ReportingExportController_exportTimeSeriesToCsv_get_api_v1_reporting_export_timeseries_csv` |

## ReportingManagement

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/reporting-management/info` | getRecalculationInfo | ReportingManagementController | `ReportingManagementController_getRecalculationInfo_get_api_v1_admin_reporting_management_info` |
| POST | `/api/v1/admin/reporting-management/recalculate` | recalculateStatistics | ReportingManagementController | `ReportingManagementController_recalculateStatistics_post_api_v1_admin_reporting_management_recalculate` |
| POST | `/api/v1/admin/reporting-management/recalculate/{date}` | recalculateSingleDate | ReportingManagementController | `ReportingManagementController_recalculateSingleDate_post_api_v1_admin_reporting_management_recalculate_date_` |

## SelfExclusion

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/players/{playerId}/responsible/exclusions` | Get all exclusions for a player | SelfExclusionController | `SelfExclusionController_getPlayerExclusions_get_api_players_playerId_responsible_exclusions` |
| POST | `/api/players/{playerId}/responsible/exclusions/cooling-off` | Set a cooling-off period (short break) | SelfExclusionController | `SelfExclusionController_setCoolingOffPeriod_post_api_players_playerId_responsible_exclusions_cooling_off` |
| POST | `/api/players/{playerId}/responsible/exclusions/permanent` | Set a permanent exclusion | SelfExclusionController | `SelfExclusionController_setPermanentExclusion_post_api_players_playerId_responsible_exclusions_permanent` |
| GET | `/api/players/{playerId}/responsible/exclusions/status` | Check if player is currently excluded | SelfExclusionController | `SelfExclusionController_isPlayerExcluded_get_api_players_playerId_responsible_exclusions_status` |
| POST | `/api/players/{playerId}/responsible/exclusions/temporary` | Set a temporary exclusion (up to 6 months) | SelfExclusionController | `SelfExclusionController_setTemporaryExclusion_post_api_players_playerId_responsible_exclusions_temporary` |
| GET | `/api/players/{playerId}/responsible/exclusions/{exclusionId}` | Get specific exclusion details | SelfExclusionController | `SelfExclusionController_getExclusionById_get_api_players_playerId_responsible_exclusions_exclusionId_` |

## SignupConfigCacheDemo

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/demo/signup-cache/invalidate` | invalidateCaches | SignupConfigCacheDemoController | `SignupConfigCacheDemoController_invalidateCaches_post_api_demo_signup_cache_invalidate` |
| GET | `/api/demo/signup-cache/stats` | getCacheStatistics | SignupConfigCacheDemoController | `SignupConfigCacheDemoController_getCacheStatistics_get_api_demo_signup_cache_stats` |
| GET | `/api/demo/signup-cache/test-config` | testSignupConfigCaching | SignupConfigCacheDemoController | `SignupConfigCacheDemoController_testSignupConfigCaching_get_api_demo_signup_cache_test_config` |
| POST | `/api/demo/signup-cache/warmup` | warmupCaches | SignupConfigCacheDemoController | `SignupConfigCacheDemoController_warmupCaches_post_api_demo_signup_cache_warmup` |

## Smartico

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/smartico/bonuses/activate` | activateBonus | SmarticoController | `SmarticoController_activateBonus_post_api_v1_smartico_bonuses_activate` |
| GET | `/api/v1/smartico/bonuses/active` | getActiveBonuses | SmarticoController | `SmarticoController_getActiveBonuses_get_api_v1_smartico_bonuses_active` |

## SmarticoIntegration

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/integration/smartico/games` | getGamesForSmartico | SmarticoIntegrationController | `SmarticoIntegrationController_getGamesForSmartico_get_api_v1_integration_smartico_games` |

## SmarticoTestData

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/smartico-test/generate-all-and-publish` | generateAllAndPublish | SmarticoTestDataController | `SmarticoTestDataController_generateAllAndPublish_post_api_v1_admin_smartico_test_generate_all_and_publish` |
| POST | `/api/v1/admin/smartico-test/generate-and-publish-payments` | generateAndPublishPayments | SmarticoTestDataController | `SmarticoTestDataController_generateAndPublishPayments_post_api_v1_admin_smartico_test_generate_and_publish_payments` |
| POST | `/api/v1/admin/smartico-test/generate-and-publish-sports-bets` | generateAndPublishSportsBets | SmarticoTestDataController | `SmarticoTestDataController_generateAndPublishSportsBets_post_api_v1_admin_smartico_test_generate_and_publish_sports_bets` |
| POST | `/api/v1/admin/smartico-test/publish-all` | publishAllTestData | SmarticoTestDataController | `SmarticoTestDataController_publishAllTestData_post_api_v1_admin_smartico_test_publish_all` |
| POST | `/api/v1/admin/smartico-test/publish-bulk` | publishBulkTestData | SmarticoTestDataController | `SmarticoTestDataController_publishBulkTestData_post_api_v1_admin_smartico_test_publish_bulk` |
| POST | `/api/v1/admin/smartico-test/publish-comprehensive-test` | publishComprehensiveTest | SmarticoTestDataController | `SmarticoTestDataController_publishComprehensiveTest_post_api_v1_admin_smartico_test_publish_comprehensive_test` |
| POST | `/api/v1/admin/smartico-test/publish-payment-events` | publishPaymentEvents | SmarticoTestDataController | `SmarticoTestDataController_publishPaymentEvents_post_api_v1_admin_smartico_test_publish_payment_events` |
| POST | `/api/v1/admin/smartico-test/publish-realistic-sample` | publishRealisticSample | SmarticoTestDataController | `SmarticoTestDataController_publishRealisticSample_post_api_v1_admin_smartico_test_publish_realistic_sample` |
| POST | `/api/v1/admin/smartico-test/publish-sports-events` | publishSportsEvents | SmarticoTestDataController | `SmarticoTestDataController_publishSportsEvents_post_api_v1_admin_smartico_test_publish_sports_events` |
| GET | `/api/v1/admin/smartico-test/status` | getStatus | SmarticoTestDataController | `SmarticoTestDataController_getStatus_get_api_v1_admin_smartico_test_status` |

## SportsAuth

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/sports/guest-token` | getGuestToken | SportsAuthController | `SportsAuthController_getGuestToken_get_api_v1_sports_guest_token` |
| GET | `/api/v1/sports/health` | healthCheck | SportsAuthController | `SportsAuthController_healthCheck_get_api_v1_sports_health` |
| POST | `/api/v1/sports/refresh-token` | refreshBetByToken | SportsAuthController | `SportsAuthController_refreshBetByToken_post_api_v1_sports_refresh_token` |
| GET | `/api/v1/sports/token` | getBetByToken | SportsAuthController | `SportsAuthController_getBetByToken_get_api_v1_sports_token` |

## Test

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/test/populate-payment-data` | populatePaymentData | TestController | `TestController_populatePaymentData_post_api_test_populate_payment_data` |
| POST | `/api/test/populate-payment-transaction-data` | populatePaymentTransactionData | TestController | `TestController_populatePaymentTransactionData_post_api_test_populate_payment_transaction_data` |

## TestData

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/admin/test-data/cellxpert/setup` | setupCellxpertTestData | TestDataController | `TestDataController_setupCellxpertTestData_post_api_v1_admin_test_data_cellxpert_setup` |

## TestGamingData

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/test-gaming-data/check-gaming-data` | checkGamingData | TestGamingDataController | `TestGamingDataController_checkGamingData_get_api_v1_admin_test_gaming_data_check_gaming_data` |
| POST | `/api/v1/admin/test-gaming-data/generate` | generateTestGamingData | TestGamingDataController | `TestGamingDataController_generateTestGamingData_post_api_v1_admin_test_gaming_data_generate` |
| POST | `/api/v1/admin/test-gaming-data/generate-game-sessions` | generateGameSessionsWithTransactions | TestGamingDataController | `TestGamingDataController_generateGameSessionsWithTransactions_post_api_v1_admin_test_gaming_data_generate_game_sessions` |

## TestOptimized

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/test/optimized-games` | testOptimizedGames | TestOptimizedController | `TestOptimizedController_testOptimizedGames_get_api_test_optimized_games` |
| GET | `/api/test/optimized-games-v2` | testOptimizedGamesV2 | TestOptimizedController | `TestOptimizedController_testOptimizedGamesV2_get_api_test_optimized_games_v2` |
| GET | `/api/test/simple-optimized-games` | testSimpleOptimizedGames | TestOptimizedController | `TestOptimizedController_testSimpleOptimizedGames_get_api_test_simple_optimized_games` |

## TestTranslation

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/test/translations/check` | checkTranslations | TestTranslationController | `TestTranslationController_checkTranslations_get_api_test_translations_check` |
| POST | `/api/test/translations/create-test-data` | createTestData | TestTranslationController | `TestTranslationController_createTestData_post_api_test_translations_create_test_data` |
| POST | `/api/test/translations/test-create-with-translations` | testCreateWithTranslations | TestTranslationController | `TestTranslationController_testCreateWithTranslations_post_api_test_translations_test_create_with_translations` |

## TimeSeries

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/reporting/timeseries/deposits/by-provider` | getDepositsByProvider | TimeSeriesController | `TimeSeriesController_getDepositsByProvider_get_api_v1_reporting_timeseries_deposits_by_provider` |
| GET | `/api/v1/reporting/timeseries/ggr/by-vendor` | getGgrByVendor | TimeSeriesController | `TimeSeriesController_getGgrByVendor_get_api_v1_reporting_timeseries_ggr_by_vendor` |
| GET | `/api/v1/reporting/timeseries/granularities` | getAvailableGranularities | TimeSeriesController | `TimeSeriesController_getAvailableGranularities_get_api_v1_reporting_timeseries_granularities` |
| GET | `/api/v1/reporting/timeseries/metrics` | getAvailableMetrics | TimeSeriesController | `TimeSeriesController_getAvailableMetrics_get_api_v1_reporting_timeseries_metrics` |
| POST | `/api/v1/reporting/timeseries/multi` | getMultipleTimeSeries | TimeSeriesController | `TimeSeriesController_getMultipleTimeSeries_post_api_v1_reporting_timeseries_multi` |
| GET | `/api/v1/reporting/timeseries/withdrawals/by-provider` | getWithdrawalsByProvider | TimeSeriesController | `TimeSeriesController_getWithdrawalsByProvider_get_api_v1_reporting_timeseries_withdrawals_by_provider` |
| GET | `/api/v1/reporting/timeseries/{metric}` | getTimeSeries | TimeSeriesController | `TimeSeriesController_getTimeSeries_get_api_v1_reporting_timeseries_metric_` |
| GET | `/api/v1/reporting/timeseries/{metric}/compare` | getComparativeTimeSeries | TimeSeriesController | `TimeSeriesController_getComparativeTimeSeries_get_api_v1_reporting_timeseries_metric_compare` |

## TransactionAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/transactions/export` | exportTransactions | TransactionAdminController | `TransactionAdminController_exportTransactions_get_api_v1_admin_transactions_export` |

## TranslationAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/admin/translations` | Create translation | TranslationAdminController | `TranslationAdminController_createTranslation_post_api_admin_translations` |
| POST | `/api/admin/translations/bulk-update` | Bulk update translations | TranslationAdminController | `TranslationAdminController_bulkUpdateTranslations_post_api_admin_translations_bulk_update` |
| GET | `/api/admin/translations/export` | Export translations | TranslationAdminController | `TranslationAdminController_exportTranslations_get_api_admin_translations_export` |
| POST | `/api/admin/translations/import` | Import translations | TranslationAdminController | `TranslationAdminController_importTranslations_post_api_admin_translations_import` |
| GET | `/api/admin/translations/key/{keyId}` | Get translations for key | TranslationAdminController | `TranslationAdminController_getTranslationsForKey_get_api_admin_translations_key_keyId_` |
| GET | `/api/admin/translations/locale/{localeId}` | Get translations for locale | TranslationAdminController | `TranslationAdminController_getTranslationsForLocale_get_api_admin_translations_locale_localeId_` |
| GET | `/api/admin/translations/unverified/{localeId}` | Get unverified translations | TranslationAdminController | `TranslationAdminController_getUnverifiedTranslations_get_api_admin_translations_unverified_localeId_` |
| DELETE | `/api/admin/translations/{id}` | Delete translation | TranslationAdminController | `TranslationAdminController_deleteTranslation_delete_api_admin_translations_id_` |
| GET | `/api/admin/translations/{id}` | Get translation by ID | TranslationAdminController | `TranslationAdminController_getTranslationById_get_api_admin_translations_id_` |
| PUT | `/api/admin/translations/{id}` | Update translation | TranslationAdminController | `TranslationAdminController_updateTranslation_put_api_admin_translations_id_` |

## TranslationKeyAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/translation-keys` | getAllKeys | TranslationKeyAdminController | `TranslationKeyAdminController_getAllKeys_get_api_admin_translation_keys` |
| POST | `/api/admin/translation-keys` | createKey | TranslationKeyAdminController | `TranslationKeyAdminController_createKey_post_api_admin_translation_keys` |
| GET | `/api/admin/translation-keys/categories` | getCategories | TranslationKeyAdminController | `TranslationKeyAdminController_getCategories_get_api_admin_translation_keys_categories` |
| GET | `/api/admin/translation-keys/key/{key}` | getKeyByKey | TranslationKeyAdminController | `TranslationKeyAdminController_getKeyByKey_get_api_admin_translation_keys_key_key_` |
| DELETE | `/api/admin/translation-keys/{id}` | deleteKey | TranslationKeyAdminController | `TranslationKeyAdminController_deleteKey_delete_api_admin_translation_keys_id_` |
| GET | `/api/admin/translation-keys/{id}` | getKeyById | TranslationKeyAdminController | `TranslationKeyAdminController_getKeyById_get_api_admin_translation_keys_id_` |
| PUT | `/api/admin/translation-keys/{id}` | updateKey | TranslationKeyAdminController | `TranslationKeyAdminController_updateKey_put_api_admin_translation_keys_id_` |

## TranslationPublic

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/public/translations/locale/{localeCode}` | getTranslationsByLocale | TranslationPublicController | `TranslationPublicController_getTranslationsByLocale_get_api_public_translations_locale_localeCode_` |
| GET | `/api/public/translations/locales` | getActiveLocales | TranslationPublicController | `TranslationPublicController_getActiveLocales_get_api_public_translations_locales` |

## TwoFactorAuth

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/two-factor/disable` | disableTwoFactor | TwoFactorAuthController | `TwoFactorAuthController_disableTwoFactor_post_api_v1_two_factor_disable` |
| POST | `/api/v1/two-factor/enable` | enableTwoFactor | TwoFactorAuthController | `TwoFactorAuthController_enableTwoFactor_post_api_v1_two_factor_enable` |
| POST | `/api/v1/two-factor/initiate-activation` | initiateActivation | TwoFactorAuthController | `TwoFactorAuthController_initiateActivation_post_api_v1_two_factor_initiate_activation` |
| POST | `/api/v1/two-factor/initiate-deactivation` | initiateDeactivation | TwoFactorAuthController | `TwoFactorAuthController_initiateDeactivation_post_api_v1_two_factor_initiate_deactivation` |
| POST | `/api/v1/two-factor/send-login-code` | sendLoginCode | TwoFactorAuthController | `TwoFactorAuthController_sendLoginCode_post_api_v1_two_factor_send_login_code` |
| GET | `/api/v1/two-factor/status` | getTwoFactorStatus | TwoFactorAuthController | `TwoFactorAuthController_getTwoFactorStatus_get_api_v1_two_factor_status` |

## V3PublicGame

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v3/public/games` | getGames | V3PublicGameController | `V3PublicGameController_getGames_get_api_v3_public_games` |
| GET | `/api/v3/public/games/category/{categoryId}` | Get games by category | V3PublicGameController | `V3PublicGameController_getGamesByCategory_get_api_v3_public_games_category_categoryId_` |
| GET | `/api/v3/public/games/featured` | Get featured games | V3PublicGameController | `V3PublicGameController_getFeaturedGames_get_api_v3_public_games_featured` |
| GET | `/api/v3/public/games/features` | Get games by features | V3PublicGameController | `V3PublicGameController_getGamesByFeatures_get_api_v3_public_games_features` |
| GET | `/api/v3/public/games/new` | Get new games | V3PublicGameController | `V3PublicGameController_getNewGames_get_api_v3_public_games_new` |
| GET | `/api/v3/public/games/popular` | Get popular games | V3PublicGameController | `V3PublicGameController_getPopularGames_get_api_v3_public_games_popular` |
| GET | `/api/v3/public/games/provider/{providerId}` | Get games by provider | V3PublicGameController | `V3PublicGameController_getGamesByProvider_get_api_v3_public_games_provider_providerId_` |
| GET | `/api/v3/public/games/search` | Search games by name | V3PublicGameController | `V3PublicGameController_searchGames_get_api_v3_public_games_search` |
| GET | `/api/v3/public/games/search-ranked` | Search games with custom ranking algorithm | V3PublicGameController | `V3PublicGameController_searchGamesWithRanking_get_api_v3_public_games_search_ranked` |
| GET | `/api/v3/public/games/stats` | Get filtering statistics | V3PublicGameController | `V3PublicGameController_getFilterStats_get_api_v3_public_games_stats` |

## Vendor

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/vendors` | getAllVendors | VendorController | `VendorController_getAllVendors_get_api_admin_vendors` |
| GET | `/api/admin/vendors/by-subtype` | getVendorsBySubtype | VendorController | `VendorController_getVendorsBySubtype_get_api_admin_vendors_by_subtype` |
| GET | `/api/admin/vendors/ordered` | getAllVendorsOrdered | VendorController | `VendorController_getAllVendorsOrdered_get_api_admin_vendors_ordered` |
| PUT | `/api/admin/vendors/reorder` | reorderVendors | VendorController | `VendorController_reorderVendors_put_api_admin_vendors_reorder` |
| GET | `/api/admin/vendors/{vendorId}` | getVendorById | VendorController | `VendorController_getVendorById_get_api_admin_vendors_vendorId_` |
| PUT | `/api/admin/vendors/{vendorId}` | updateVendor | VendorController | `VendorController_updateVendor_put_api_admin_vendors_vendorId_` |
| POST | `/api/admin/vendors/{vendorId}/activate` | activateVendor | VendorController | `VendorController_activateVendor_post_api_admin_vendors_vendorId_activate` |
| POST | `/api/admin/vendors/{vendorId}/deactivate` | deactivateVendor | VendorController | `VendorController_deactivateVendor_post_api_admin_vendors_vendorId_deactivate` |
| GET | `/api/admin/vendors/{vendorId}/games` | getGamesByVendor | VendorController | `VendorController_getGamesByVendor_get_api_admin_vendors_vendorId_games` |
| GET | `/api/vendors/active` | getActiveVendors | VendorController | `VendorController_getActiveVendors_get_api_vendors_active` |

## Wagering

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/wagering/balance/{balanceId}` | Get wagering details for a specific bonus balance | WageringController | `WageringController_getBonusWageringDetails_get_api_v1_wagering_balance_balanceId_` |
| POST | `/api/v1/wagering/convert` | Convert bonus to real money | WageringController | `WageringController_convertBonusToRealMoney_post_api_v1_wagering_convert` |
| GET | `/api/v1/wagering/history` | Get player's wagering transaction history | WageringController | `WageringController_getMyWageringHistory_get_api_v1_wagering_history` |

## Wallet

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/payments/deposits` | Create a deposit request | WalletController | `WalletController_createDeposit_post_api_payments_deposits` |
| POST | `/api/payments/withdrawals` | Create a withdrawal request | WalletController | `WalletController_createWithdrawal_post_api_payments_withdrawals` |
| GET | `/api/wallets/{playerId}/balance` | Get player wallet balance | WalletController | `WalletController_getWalletBalance_get_api_wallets_playerId_balance` |
| GET | `/api/wallets/{playerId}/transactions` | Get player transactions | WalletController | `WalletController_getTransactions_get_api_wallets_playerId_transactions` |
| GET | `/api/wallets/{playerId}/transactions/overview` | Get player overview transactions (deposits, withdrawals, adjustments, bonuses) | WalletController | `WalletController_getOverviewTransactions_get_api_wallets_playerId_transactions_overview` |

## WalletCacheDemo

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/demo/wallet-cache/test/{playerId}` | testWalletCache | WalletCacheDemoController | `WalletCacheDemoController_testWalletCache_get_api_demo_wallet_cache_test_playerId_` |

## WalletCacheTest

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/wallet-cache-test/cache-stats` | getCacheStats | WalletCacheTestController | `WalletCacheTestController_getCacheStats_get_api_admin_wallet_cache_test_cache_stats` |
| POST | `/api/admin/wallet-cache-test/test-read-performance` | testReadPerformance | WalletCacheTestController | `WalletCacheTestController_testReadPerformance_post_api_admin_wallet_cache_test_test_read_performance` |
| POST | `/api/admin/wallet-cache-test/test-update-performance` | testUpdatePerformance | WalletCacheTestController | `WalletCacheTestController_testUpdatePerformance_post_api_admin_wallet_cache_test_test_update_performance` |

## WalletMetrics

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/wallet-metrics/all` | getAllMetrics | WalletMetricsController | `WalletMetricsController_getAllMetrics_get_api_admin_wallet_metrics_all` |
| GET | `/api/admin/wallet-metrics/cache-stats` | getCacheStats | WalletMetricsController | `WalletMetricsController_getCacheStats_get_api_admin_wallet_metrics_cache_stats` |
| GET | `/api/admin/wallet-metrics/rate-limit/{playerId}` | getRateLimitStatus | WalletMetricsController | `WalletMetricsController_getRateLimitStatus_get_api_admin_wallet_metrics_rate_limit_playerId_` |
| GET | `/api/admin/wallet-metrics/throughput` | getThroughput | WalletMetricsController | `WalletMetricsController_getThroughput_get_api_admin_wallet_metrics_throughput` |
| POST | `/api/admin/wallet-metrics/warm-cache` | warmCache | WalletMetricsController | `WalletMetricsController_warmCache_post_api_admin_wallet_metrics_warm_cache` |

## WidgetAdmin

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| GET | `/api/admin/cms/widgets` | Get all widgets with optional filtering | WidgetAdminController | `WidgetAdminController_getAllWidgets_get_api_admin_cms_widgets` |
| POST | `/api/admin/cms/widgets/create-standalone` | Create standalone widget (not attached to any page) | WidgetAdminController | `WidgetAdminController_createStandaloneWidget_post_api_admin_cms_widgets_create_standalone` |
| GET | `/api/admin/cms/widgets/statistics` | Get widget usage statistics | WidgetAdminController | `WidgetAdminController_getWidgetStatistics_get_api_admin_cms_widgets_statistics` |
| GET | `/api/admin/cms/widgets/templates` | Get widget templates | WidgetAdminController | `WidgetAdminController_getWidgetTemplates_get_api_admin_cms_widgets_templates` |
| POST | `/api/admin/cms/widgets/templates` | Create widget template | WidgetAdminController | `WidgetAdminController_createWidgetTemplate_post_api_admin_cms_widgets_templates` |
| DELETE | `/api/admin/cms/widgets/templates/{templateId}` | Delete widget template | WidgetAdminController | `WidgetAdminController_deleteWidgetTemplate_delete_api_admin_cms_widgets_templates_templateId_` |
| PUT | `/api/admin/cms/widgets/templates/{templateId}` | Update widget template | WidgetAdminController | `WidgetAdminController_updateWidgetTemplate_put_api_admin_cms_widgets_templates_templateId_` |
| GET | `/api/admin/cms/widgets/types` | Get available widget types | WidgetAdminController | `WidgetAdminController_getWidgetTypes_get_api_admin_cms_widgets_types` |
| GET | `/api/admin/cms/widgets/{widgetId}` | Get widget details by ID | WidgetAdminController | `WidgetAdminController_getWidget_get_api_admin_cms_widgets_widgetId_` |
| PUT | `/api/admin/cms/widgets/{widgetId}` | Update widget | WidgetAdminController | `WidgetAdminController_updateWidget_put_api_admin_cms_widgets_widgetId_` |
| POST | `/api/admin/cms/widgets/{widgetId}/duplicate` | Duplicate a widget | WidgetAdminController | `WidgetAdminController_duplicateWidget_post_api_admin_cms_widgets_widgetId_duplicate` |
| PATCH | `/api/admin/cms/widgets/{widgetId}/status` | Toggle widget status | WidgetAdminController | `WidgetAdminController_updateWidgetStatus_patch_api_admin_cms_widgets_widgetId_status` |

## WidgetTranslation

| Method | Path | Summary | Controller | Operation ID |
| --- | --- | --- | --- | --- |
| POST | `/api/admin/widget-translations/bulk-update` | bulkUpdateTranslations | WidgetTranslationController | `WidgetTranslationController_bulkUpdateTranslations_post_api_admin_widget_translations_bulk_update` |
| GET | `/api/admin/widget-translations/coverage-report` | getTranslationCoverageReport | WidgetTranslationController | `WidgetTranslationController_getTranslationCoverageReport_get_api_admin_widget_translations_coverage_report` |
| GET | `/api/admin/widget-translations/export` | exportWidgetTranslations | WidgetTranslationController | `WidgetTranslationController_exportWidgetTranslations_get_api_admin_widget_translations_export` |
| GET | `/api/admin/widget-translations/keys/{translationKey}/widgets` | getWidgetsUsingTranslationKey | WidgetTranslationController | `WidgetTranslationController_getWidgetsUsingTranslationKey_get_api_admin_widget_translations_keys_translationKey_widgets` |
| GET | `/api/admin/widget-translations/widgets/{widgetId}/keys` | getWidgetTranslationKeys | WidgetTranslationController | `WidgetTranslationController_getWidgetTranslationKeys_get_api_admin_widget_translations_widgets_widgetId_keys` |
| POST | `/api/admin/widget-translations/widgets/{widgetId}/preview` | previewWidgetWithTranslations | WidgetTranslationController | `WidgetTranslationController_previewWidgetWithTranslations_post_api_admin_widget_translations_widgets_widgetId_preview` |

