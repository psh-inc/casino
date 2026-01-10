# Backend - Games and Bonuses

## Responsibilities

- Game catalog and discovery
- Game launch and session tracking
- Game provider callbacks
- Bonus creation, claiming, and wagering lifecycle
- Free spins and promotions

## Key controllers

- GameController, PublicGameController
- GameAdminController, AdminGameController
- GameProviderController, GameProviderSyncController
- GameLaunchController, GameSessionController, GameCallbackController
- BonusManagementController, AdminBonusController
- BonusOfferController, BonusSelectionController
- AdvancedBonusController, BonusBalanceController
- PromotionController, FreeSpinsController

## Data model highlights

- Game, GameProvider, GameCategory, GameSession, GameRound
- Bonus, BonusReward, BonusDetails, WageringTransaction

## Dependencies

- Game provider APIs
- Kafka events (game and bonus domain)
- Redis caches for catalog
