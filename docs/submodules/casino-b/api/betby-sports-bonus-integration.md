# BetBy Sports Bonus Integration Guide

This document provides comprehensive documentation for integrating sports bonuses with the BetBy sportsbook platform.

## Table of Contents

1. [Overview](#overview)
2. [Bonus Types](#bonus-types)
3. [Bonus Lifecycle States](#bonus-lifecycle-states)
4. [External API Methods](#external-api-methods)
5. [Issuing Bonuses](#issuing-bonuses)
6. [Template Configuration](#template-configuration)
7. [Backend Integration](#backend-integration)
8. [Bet Lifecycle with Bonuses](#bet-lifecycle-with-bonuses)
9. [Partner Implementation Requirements](#partner-implementation-requirements)
10. [Key Business Rules](#key-business-rules)
11. [Integration Flow](#integration-flow)

---

## Overview

BetBy provides a comprehensive Bonus API that allows Partners to:
- Create freebet templates using Backoffice
- Issue bonuses to players via API
- Query player bonuses
- Revoke unused bonuses

The bonus system supports two main types: **Freebets** and **Comboboost** bonuses.

---

## Bonus Types

### Freebet Types

| Type | Code | Description |
|------|------|-------------|
| Bet Refund | `bet_refund` | If bet loses, the stake is refunded to the player |
| Free Money | `free_money` | Free money bonus - full winnings paid |
| Stake Not Returned | `snr` | If bet wins, only profit is paid (stake is not returned) |

### Comboboost Types

| Type | Code | Description |
|------|------|-------------|
| Comboboost | `comboboost` | Player-specific multiplier bonus for combo/accumulator bets |
| Global Comboboost | `global_comboboost` | Multiplier bonus available to all players without granting |

### Bonus Type Values in BET_MAKE

When processing bets, the `bonus_type` field can have these values:
- `freebet_refund`
- `freebet_freemoney`
- `freebet_no_risk`
- `comboboost`
- `global_comboboost`

---

## Bonus Lifecycle States

| Status | Description |
|--------|-------------|
| `new` | Newly issued bonus, not yet activated by player |
| `active` | Activated by player, ready to be used but not used yet |
| `activated` | Successfully used on a bet (bet placed with this bonus) |
| `expired` | Cannot be used due to date range expiration |
| `revoked` | Cancelled by Partner via API or Backoffice |
| `done` | Bonus bet has been fully settled |

### State Transitions

```
[Issue Bonus] → NEW
                 ↓
         [Player Activates]
                 ↓
              ACTIVE
                 ↓
         [Player Places Bet]
                 ↓
            ACTIVATED
                 ↓
           [Bet Settles]
                 ↓
               DONE

Alternative paths:
- NEW/ACTIVE → REVOKED (via REVOKE_BONUS API)
- NEW/ACTIVE → EXPIRED (after to_time passes)
```

**Important**: Only bonuses in `NEW` or `ACTIVE` status can be revoked. Once a bonus is used (`ACTIVATED`), it cannot be revoked.

---

## External API Methods

All External API endpoints use POST method and require JWT authentication.

Base URL: `https://BETBY_EXTERNAL_API_URL/api/v1/external_api`

### Template Management

#### TEMPLATES - Get All Templates

**Endpoint**: `POST /bonus/templates`

**Request**:
```json
{
  "payload": {
    "operator_id": "1234567890123456789",
    "active": true
  }
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| operator_id | String | Yes | Unique Partner Identifier assigned by BetBy |
| active | Boolean | No | Filter: true=active only, false=inactive only, omit=all |

**Response**: Returns list of `<TemplateItem>` objects.

---

#### TEMPLATE - Get Single Template

**Endpoint**: `POST /bonus/template`

**Request**:
```json
{
  "payload": {
    "operator_id": "1234567890123456789",
    "template_id": "1657013872955142242"
  }
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| operator_id | String | Yes | Unique Partner Identifier assigned by BetBy |
| template_id | String | Yes | Template ID to retrieve |

---

### Player Bonus Management

#### PLAYER_BONUSES - Get Player's Bonuses

**Endpoint**: `POST /bonus/player_bonuses`

**Request**:
```json
{
  "payload": {
    "brand_id": "1234567890123456789",
    "external_player_id": "123456789"
  }
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| brand_id | String | Yes | Partner Website unique identifier assigned by BetBy |
| external_player_id | String | Yes | Unique identifier assigned to player on Partner side |

**Response**: Returns list of `<BonusItem>` objects.

---

#### BONUS - Get Single Bonus

**Endpoint**: `POST /bonus`

**Request**:
```json
{
  "payload": {
    "brand_id": "1234567890123456789",
    "bonus_id": "1657013872955142242"
  }
}
```

---

#### MASS_GIVE_BONUS - Issue Bonuses to Players

**Endpoint**: `POST /bonus/mass_give_bonus`

> **Note**: One request can contain a maximum of ~1000 players. Split larger batches.

**Request**:
```json
{
  "payload": {
    "brand_id": "1234567890123456789",
    "template_id": "1657013872955142242",
    "request_id": "unique_idempotency_key",
    "players_data": [
      {
        "external_player_id": "123456789",
        "currency": "USD",
        "amount": 900,
        "force_activated": false
      }
    ]
  }
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| brand_id | String | Yes | Partner Website unique identifier |
| template_id | String | Yes | Bonus template to use |
| request_id | String | No | Idempotency key for duplicate prevention |
| players_data | Array | Yes | List of players to receive bonus |

**PlayerDataItem**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| external_player_id | String | Yes | Player's ID on Partner side |
| currency | String | Yes | Currency code (see Currency Support appendix) |
| amount | Integer | Yes | **Amount in CENTS** (e.g., 900 = $9.00) |
| force_activated | Boolean | Yes | true=auto-activate, false=player must activate in "My Bets" |

---

#### REVOKE_BONUS - Revoke Bonuses

**Endpoint**: `POST /bonus/revoke_bonus`

> **Important**: Only `NEW` and `ACTIVE` bonuses can be revoked. Used bonuses cannot be revoked.

**Request**:
```json
{
  "payload": {
    "brand_id": "1234567890123456789",
    "bonuses_ids": [
      "1657013872955142242",
      "1657013872955142243"
    ]
  }
}
```

---

## Issuing Bonuses

### Basic Flow

1. Retrieve available templates using `TEMPLATES` method
2. Select appropriate template for the bonus campaign
3. Call `MASS_GIVE_BONUS` with player data
4. Handle response and store bonus IDs for tracking

### Example: Issue $10 Freebet to Players

```json
{
  "payload": {
    "brand_id": "1653815133341880320",
    "template_id": "1657013872955142242",
    "request_id": "campaign_2024_jan_welcome_001",
    "players_data": [
      {
        "external_player_id": "player_001",
        "currency": "USD",
        "amount": 1000,
        "force_activated": false
      },
      {
        "external_player_id": "player_002",
        "currency": "EUR",
        "amount": 1000,
        "force_activated": true
      }
    ]
  }
}
```

### Important Notes

1. **Amount is in CENTS**: `1000` = $10.00, `500` = $5.00
2. **Currency must match player's wallet currency**
3. **Use request_id for idempotency** to prevent duplicate bonus issuance
4. **force_activated**:
   - `false`: Player must manually activate in "My Bets" section
   - `true`: Bonus is immediately activated upon issuance

---

## Template Configuration

Templates are created in BetBy Backoffice and define the rules for bonuses.

### Template Structure

```json
{
  "id": "1684188993169788928",
  "name": "test_direct_tennis_live",
  "is_active": true,
  "max_bonus_number": 999999,
  "type": "freebet",
  "operator_id": "1657013002915142201",
  "brand_id": "1653815133341880320",
  "event_scheduled": 1646946993,
  "from_time": 1544436660,
  "to_time": 1544868660,
  "days_to_use": 3,
  "events_availability": true,
  "restrictions": {
    "restriction_events": [
      {
        "sport_id": null,
        "sport_type": null,
        "category_id": null,
        "tournament_id": null,
        "event_id": "1683937560088416256"
      }
    ],
    "type": "all"
  },
  "freebet_data": {
    "type": "bet_refund",
    "min_selection": 1,
    "max_selection": 1,
    "min_odd": 1.01,
    "max_odd": 1000
  },
  "descriptions": {
    "en": "Tennis Freebet",
    "de": "Tennis Freiwette"
  }
}
```

### Key Template Fields

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique template identifier |
| name | String | Template name (set in Backoffice) |
| is_active | Boolean | Whether template can be used for issuing |
| max_bonus_number | Integer | Max bonuses per player from this template |
| type | String | `freebet` or `comboboost` |
| from_time | Float | Unix timestamp - start of validity period |
| to_time | Float | Unix timestamp - end of validity period |
| days_to_use | Integer | Days player has to use bonus after activation |
| event_scheduled | Integer | For live bets - events started before this time can be bet on |

### Freebet Data Configuration

| Field | Type | Description |
|-------|------|-------------|
| type | String | `bet_refund`, `free_money`, or `snr` |
| min_selection | Integer | Minimum selections required in betslip |
| max_selection | Integer | Maximum selections allowed in betslip |
| min_odd | Float | Minimum odds per selection (e.g., 1.01) |
| max_odd | Float | Maximum odds per selection (e.g., 1000) |

### Comboboost Data Configuration

| Field | Type | Description |
|-------|------|-------------|
| min_odd | Float | Minimum odds per selection |
| multipliers | Array[Float] | List of multipliers based on number of selections |
| total_multiplier | Float | The multiplier applied to winnings |
| is_global | Boolean | If true, available to all players without granting |

### Restrictions Configuration

Restrictions can limit bonus usage to specific sports, categories, tournaments, or events.

| Field | Type | Description |
|-------|------|-------------|
| type | String | `all`, `live`, or `prematch` |
| restriction_events | Array | List of allowed sports/events |

---

## Backend Integration

When a player places a bet using a bonus, BetBy sends callback requests to the Partner's backend.

### BET_MAKE Request with Bonus

When a bet is placed with a bonus, these additional fields are included:

```json
{
  "amount": 100,
  "currency": "USD",
  "player_id": "1659297400285696000",
  "session_id": "aa8499f578b13e9147428c30ad8c63bd",
  "bonus_id": "1664976298830860288",
  "bonus_type": "comboboost",
  "potential_win": 497,
  "potential_comboboost_win": 50,
  "transaction": {
    "id": "1265023428769484821",
    "betslip_id": "1659603658884648961",
    "player_id": "1659299365132570624",
    "operator_id": "1657013002915142201",
    "operator_brand_id": "1653815133341880320",
    "ext_player_id": "1659297400285696000",
    "timestamp": 1538654560.2354896,
    "amount": 100,
    "currency": "USD",
    "operation": "bet",
    "bonus_id": "1664976298830860288"
  },
  "betslip": {
    "id": "1659603658884648961",
    "type": "3/3",
    "sum": 100,
    "k": "4.976244",
    "bets": [...]
  }
}
```

### Bonus-Related Fields in BET_MAKE

| Field | Type | Description |
|-------|------|-------------|
| bonus_id | String | Unique identifier of bonus used (optional) |
| bonus_type | String | Type of bonus: `freebet_refund`, `freebet_freemoney`, `freebet_no_risk`, `comboboost`, `global_comboboost` |
| potential_win | Integer | Potential winnings (excluding comboboost) |
| potential_comboboost_win | Integer | Additional winnings from comboboost (only if comboboost used) |

---

## Bet Lifecycle with Bonuses

```
BET_MAKE
   ↓
   Partner validates:
   - Player balance/bonus availability
   - Bonus eligibility (odds, selections, restrictions)
   - Hold bet amount
   ↓
[BetBy Risk Management]
   ↓
   ┌─────────────────────────────────┐
   ↓                                 ↓
BET_DISCARD                     BET_COMMIT
(Release held amount)           (Confirm bet accepted)
                                     ↓
                               [Bet is OPEN]
                                     ↓
              ┌──────────┬───────────┼───────────┐
              ↓          ↓           ↓           ↓
          BET_LOST    BET_WIN   BET_REFUND  BET_ROLLBACK
          (amt=0)   (credit)   (return stake) (reopen)
              ↓          ↓           ↓           ↓
              └──────────┴───────────┴───────────┘
                                ↓
                        [30 days delay]
                                ↓
                        BET_SETTLEMENT
                     (Bet closed, final)
```

### Settlement Statuses

| Status | Description |
|--------|-------------|
| won | Bet won |
| lost | Bet lost |
| canceled | Bet canceled |
| refund | Bet refunded |
| cashed out | Player cashed out early |
| half-won | Partial win (Asian handicap) |
| half-lost | Partial loss (Asian handicap) |

---

## Partner Implementation Requirements

### 1. BET_MAKE Handler

```kotlin
fun handleBetMake(request: BetMakeRequest): BetMakeResponse {
    // 1. Validate player exists
    val player = playerService.findByExternalId(request.extPlayerId)

    // 2. Check if bonus bet
    if (request.bonusId != null) {
        // Validate bonus is active and belongs to player
        // Validate bet meets bonus requirements (odds, selections)
        // Use bonus funds instead of real balance
    } else {
        // Check real money balance
    }

    // 3. Hold/deduct amount
    // 4. Return transaction ID
}
```

### 2. BET_WIN Handler (Bonus Considerations)

```kotlin
fun handleBetWin(request: BetWinRequest): BetWinResponse {
    val transaction = transactionService.find(request.betTransactionId)

    if (transaction.bonusId != null) {
        when (transaction.bonusType) {
            "freebet_refund", "freebet_freemoney" -> {
                // Credit full winnings (stake + profit)
                creditWinnings(transaction.playerId, request.amount)
            }
            "freebet_no_risk", "snr" -> {
                // Credit only profit (winnings - stake)
                val profit = request.amount - transaction.stakeAmount
                creditWinnings(transaction.playerId, profit)
            }
            "comboboost", "global_comboboost" -> {
                // Credit winnings including comboboost multiplier
                creditWinnings(transaction.playerId, request.amount)
            }
        }
    } else {
        // Regular bet - credit full amount
        creditWinnings(transaction.playerId, request.amount)
    }
}
```

### 3. Required Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /ping | GET | Health check |
| /bet/make | POST | Process bet placement |
| /bet/commit | POST | Confirm bet accepted (optional) |
| /bet/settlement | POST | Final bet closure notification |
| /bet/refund | POST | Return stake to player |
| /bet/win | POST | Credit winnings to player |
| /bet/lost | POST | Notify bet lost (amount=0) |
| /bet/discard | POST | Release held amount |
| /bet/rollback | POST | Reverse settlement |

---

## Key Business Rules

### Amount Handling
- **All API amounts are in CENTS**
- Example: `900` = $9.00, `1500` = $15.00
- Always convert before displaying to users

### Bonus Revocation
- Only `NEW` and `ACTIVE` bonuses can be revoked
- Once a bonus is used on a bet (`ACTIVATED`), it cannot be revoked
- Revoked bonuses change status to `REVOKED`

### Batch Limits
- `MASS_GIVE_BONUS` supports max ~1000 players per request
- Split larger campaigns into multiple requests

### Idempotency
- Use `request_id` in `MASS_GIVE_BONUS` to prevent duplicate issuance
- Same `request_id` will return same result without creating duplicates

### Template Validity
- Cannot issue bonuses after template's `to_time`
- Bonuses expire based on `days_to_use` after activation

### Betting Restrictions
- Bets must meet template's `min_odd`/`max_odd` requirements
- Selection count must be within `min_selection`/`max_selection` range
- Event/sport restrictions are enforced by BetBy

### Settlement Timing
- `BET_SETTLEMENT` is sent 30 days after `BET_WIN`/`BET_LOST`/`BET_REFUND`
- Rollbacks can occur during this 30-day period
- After `BET_SETTLEMENT`, bet cannot be reopened

---

## Integration Flow

### Complete Integration Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│                     BONUS SETUP PHASE                           │
├─────────────────────────────────────────────────────────────────┤
│ 1. Admin creates template in BetBy Backoffice                   │
│ 2. Platform calls TEMPLATES to sync available templates         │
│ 3. Store template IDs for bonus campaigns                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BONUS ISSUANCE PHASE                         │
├─────────────────────────────────────────────────────────────────┤
│ 4. Marketing triggers bonus campaign                            │
│ 5. Platform calls MASS_GIVE_BONUS with eligible players         │
│ 6. Store returned bonus IDs linked to players                   │
│ 7. Notify players of new bonus (optional)                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BONUS USAGE PHASE                          │
├─────────────────────────────────────────────────────────────────┤
│ 8. Player views bonus in "My Bets" section                      │
│ 9. Player activates bonus (if not force_activated)              │
│ 10. Player places bet with bonus                                │
│ 11. BetBy calls Partner's BET_MAKE with bonus_id                │
│ 12. Partner validates and processes bet                         │
│ 13. BetBy calls BET_COMMIT (bet accepted)                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   SETTLEMENT PHASE                              │
├─────────────────────────────────────────────────────────────────┤
│ 14. Event completes, bet settles                                │
│ 15. BetBy calls BET_WIN or BET_LOST                             │
│ 16. Partner credits winnings (per bonus type rules)             │
│ 17. Update bonus status to DONE                                 │
│ 18. After 30 days: BET_SETTLEMENT finalizes                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Error Handling

### Common Errors

| Error | Description | Resolution |
|-------|-------------|------------|
| TemplateNotFoundError | Template ID doesn't exist | Verify template_id from TEMPLATES call |
| BonusNotFoundError | Bonus ID doesn't exist | Verify bonus_id from PLAYER_BONUSES call |
| PlayerNotFoundError | Player doesn't exist in BetBy | Ensure player has been registered |
| TemplateExpiredError | Template validity period ended | Use active template |
| BonusAlreadyUsedError | Attempting to revoke used bonus | Only revoke NEW/ACTIVE bonuses |

### Error Response Format

```json
{
  "error": {
    "name": "TemplateNotFoundError",
    "description": "Template 1684188993169788922 not found"
  }
}
```

---

## Related Documentation

- [BetBy Integration Portal](https://docs-integration.sptenv.com/)
- [Admin Bonus Award Wagering Transactions](./admin-bonus-award-wagering-transactions.md)

---

*Last Updated: January 2025*
*Source: BetBy Integration Documentation (docs-integration.sptenv.com)*
