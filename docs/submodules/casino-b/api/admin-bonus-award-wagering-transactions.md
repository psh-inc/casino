# Admin Bonus Award Wagering Transactions

## Endpoint
GET `/api/v1/admin/bonuses/awards/{awardId}/wagering-transactions`

## Query Parameters
- `page` (default `0`)
- `size` (default `20`)

## Response
Returns a paginated list of wagering transactions for the specified bonus award.
If the award has no bonus balance or no transactions, the response is an empty page.

Fields per transaction:
- `id`
- `gameRoundId`
- `gameName`
- `betAmount`
- `contributionPercentage`
- `wageringContribution`
- `createdAt`

## Authorization
Requires `ADMIN` authority.
