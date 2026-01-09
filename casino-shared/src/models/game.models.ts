/**
 * Game transaction models matching Phase 3 backend DTOs
 * For game provider integrations and bet/win processing
 */

import { PlayerBalanceDto } from './balance.models';

/**
 * Game bet request DTO
 */
export interface GameBetRequestDto {
  betAmount: string;  // BigDecimal as string
  gameRoundId: string;
  gameType: string;
  gameName?: string;
  referenceId?: string;
}

/**
 * Game bet response DTO
 */
export interface GameBetResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  betAmount: string;
  wageringContribution: string;
  wageringComplete: boolean;
  bonusUsed: string;
  realUsed: string;
  gameRoundId: string;
  message?: string;
  timestamp: string;
}

/**
 * Game win request DTO
 */
export interface GameWinRequestDto {
  winAmount: string;  // BigDecimal as string
  gameRoundId: string;
  gameType: string;
  gameName?: string;
  referenceId?: string;
}

/**
 * Game win response DTO
 */
export interface GameWinResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  winAmount: string;
  balanceType: 'REAL' | 'BONUS';
  gameRoundId: string;
  message?: string;
  timestamp: string;
}

/**
 * Combined bet and win request DTO
 */
export interface GameBetAndWinRequestDto {
  betAmount: string;
  winAmount: string;
  gameRoundId: string;
  gameType: string;
  gameName?: string;
  referenceId?: string;
}

/**
 * Combined bet and win response DTO
 */
export interface GameBetAndWinResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  betAmount: string;
  winAmount: string;
  netAmount: string;  // winAmount - betAmount
  wageringContribution: string;
  wageringComplete: boolean;
  gameRoundId: string;
  message?: string;
  timestamp: string;
}

/**
 * Game session info
 */
export interface GameSessionDto {
  sessionId: string;
  playerId: number;
  gameType: string;
  gameName: string;
  startTime: string;
  endTime?: string;
  totalBets: string;
  totalWins: string;
  netResult: string;
  roundsPlayed: number;
  isActive: boolean;
}

/**
 * Game types enum
 */
export enum GameType {
  SLOTS = 'SLOTS',
  ROULETTE = 'ROULETTE',
  BLACKJACK = 'BLACKJACK',
  BACCARAT = 'BACCARAT',
  POKER = 'POKER',
  DICE = 'DICE',
  LOTTERY = 'LOTTERY',
  SPORTS = 'SPORTS',
  LIVE_CASINO = 'LIVE_CASINO',
  INSTANT_WIN = 'INSTANT_WIN',
  OTHER = 'OTHER'
}

/**
 * Game provider configuration
 */
export interface GameProviderConfig {
  providerId: string;
  providerName: string;
  apiEndpoint: string;
  supportedGames: GameType[];
  isActive: boolean;
  requiresAuth: boolean;
  supportsWagering: boolean;
}

/**
 * Game round details
 */
export interface GameRoundDto {
  roundId: string;
  playerId: number;
  gameType: string;
  betAmount: string;
  winAmount: string;
  netResult: string;
  wageringContribution: string;
  timestamp: string;
  metadata?: { [key: string]: any };
}

/**
 * Wagering contribution info
 */
export interface WageringContributionDto {
  gameType: string;
  contributionPercentage: number;
  betAmount: string;
  contributionAmount: string;
  beforeProgress: string;
  afterProgress: string;
  remainingRequirement: string;
  isCompleted: boolean;
}

/**
 * Game statistics (for player dashboard)
 */
export interface GameStatisticsDto {
  playerId: number;
  periodStart: string;
  periodEnd: string;
  totalBets: string;
  totalWins: string;
  netResult: string;
  gamesPlayed: number;
  favoriteGame?: string;
  biggestWin?: string;
  wageringContributed: string;
  bonusesUsed: string;
}

/**
 * Utility functions for game transactions
 */
export class GameTransactionUtils {
  /**
   * Calculate net result from bet and win
   */
  static calculateNetResult(betAmount: string, winAmount: string): string {
    const bet = parseFloat(betAmount) || 0;
    const win = parseFloat(winAmount) || 0;
    return (win - bet).toFixed(2);
  }

  /**
   * Format game type for display
   */
  static formatGameType(gameType: GameType | string): string {
    const typeLabels: { [key: string]: string } = {
      SLOTS: 'Slot Games',
      ROULETTE: 'Roulette',
      BLACKJACK: 'Blackjack',
      BACCARAT: 'Baccarat',
      POKER: 'Poker',
      DICE: 'Dice Games',
      LOTTERY: 'Lottery',
      SPORTS: 'Sports Betting',
      LIVE_CASINO: 'Live Casino',
      INSTANT_WIN: 'Instant Win',
      OTHER: 'Other Games'
    };
    return typeLabels[gameType] || gameType;
  }

  /**
   * Get game type icon
   */
  static getGameTypeIcon(gameType: GameType | string): string {
    const icons: { [key: string]: string } = {
      SLOTS: 'casino',
      ROULETTE: 'circle',
      BLACKJACK: 'style',
      BACCARAT: 'diamond',
      POKER: 'playing_cards',
      DICE: 'dice',
      LOTTERY: 'confirmation_number',
      SPORTS: 'sports_soccer',
      LIVE_CASINO: 'live_tv',
      INSTANT_WIN: 'flash_on',
      OTHER: 'games'
    };
    return icons[gameType] || 'games';
  }

  /**
   * Check if bet amount is valid
   */
  static isValidBetAmount(amount: string, minBet: string = '0.01', maxBet: string = '10000'): boolean {
    const bet = parseFloat(amount);
    const min = parseFloat(minBet);
    const max = parseFloat(maxBet);
    return !isNaN(bet) && bet >= min && bet <= max;
  }

  /**
   * Format wagering contribution percentage
   */
  static formatContribution(percentage: number): string {
    return `${(percentage * 100).toFixed(0)}%`;
  }
}

export default {
  GameType,
  GameTransactionUtils
};