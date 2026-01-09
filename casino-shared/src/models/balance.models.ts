/**
 * Balance-related TypeScript models matching Phase 3 backend DTOs
 * These models correspond to the Kotlin DTOs in the unified wallet system
 */

// Enums for balance states
export enum BalanceState {
  WITHDRAWABLE = 'WITHDRAWABLE',
  LOCKED_DEPOSIT = 'LOCKED_DEPOSIT',
  LOCKED_BONUS = 'LOCKED_BONUS',
  LOCKED_WAGERING = 'LOCKED_WAGERING'
}

// Enums for wagering types
export enum WageringType {
  NONE = 'NONE',
  SINGLE = 'SINGLE',
  MULTIPLE = 'MULTIPLE'
}

/**
 * Main player balance DTO matching backend PlayerBalanceDto
 */
export interface PlayerBalanceDto {
  playerId: number;
  totalBalance: string;  // BigDecimal as string for precision
  realBalance: string;
  bonusBalance: string;
  withdrawableBalance: string;
  playableBalance: string;
  balanceState: BalanceState;
  wageringType: WageringType;
  wageringRequirement?: string;
  wageringCompleted?: string;
  wageringProgress?: number;
  remainingWagering?: string;
  wageringMultiplier?: number;
  activeBonusId?: number;
  activeWageringSessionId?: number;
  canWithdraw: boolean;
  canPlay: boolean;
  canActivateBonus: boolean;
  canForfeitBonus: boolean;
  lastUpdated: string;  // ISO datetime string
  isLocked?: boolean;  // Added to match backend
  currency?: string;  // Currency code (e.g., USD, EUR)
}

/**
 * Deposit request DTO
 */
export interface DepositRequestDto {
  amount: string;  // BigDecimal as string
  wageringMultiplier?: string;  // Optional wagering requirement
  referenceId?: string;
  referenceType?: string;
}

/**
 * Deposit response DTO
 */
export interface DepositResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  depositAmount: string;
  wageringApplied: boolean;
  wageringRequirement?: string;
  transactionReference: string;
  message?: string;
  timestamp: string;
}

/**
 * Withdrawal request DTO
 */
export interface WithdrawalRequestDto {
  amount: string;  // BigDecimal as string
  withdrawalMethod: string;
  accountDetails?: { [key: string]: any };
  referenceId?: string;
}

/**
 * Withdrawal response DTO
 */
export interface WithdrawalResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  withdrawnAmount: string;
  remainingBalance: string;
  transactionReference: string;
  estimatedProcessingTime?: string;
  message?: string;
  timestamp: string;
}

/**
 * Bonus activation request DTO
 */
export interface BonusActivationRequestDto {
  bonusId: number;
  bonusAmount: string;
  wageringMultiplier: string;
  referenceId?: string;
}

/**
 * Bonus activation response DTO
 */
export interface BonusActivationResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  bonusId: number;
  bonusAmount: string;
  wageringRequirement: string;
  wageringSessionId: number;
  expiryDate?: string;
  message?: string;
  timestamp: string;
}

/**
 * Bonus forfeiture request DTO
 */
export interface BonusForfeitureRequestDto {
  reason?: string;
}

/**
 * Bonus forfeiture response DTO
 */
export interface BonusForfeitureResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  forfeitedBonusId: number;
  forfeitedAmount: string;
  reason?: string;
  timestamp: string;
}

/**
 * Wagering information DTO
 */
export interface WageringInfoDto {
  playerId: number;
  wageringSessionId: number;
  wageringRequirement: string;
  wageringProgress: string;
  remainingWagering: string;
  progressPercentage: number;
  wageringType: WageringType;
  activeBonusId?: number;
  startDate: string;
  lastContributionDate?: string;
  expiryDate?: string;
  isExpired: boolean;
  canContinue: boolean;
}

/**
 * Balance statistics DTO (Admin only)
 */
export interface BalanceStatisticsDto {
  totalPlayers: number;
  playersWithBalance: number;
  totalRealBalance: string;
  totalBonusBalance: string;
  totalWithdrawableBalance: string;
  playersWithActiveWagering: number;
  playersWithActiveBonuses: number;
  totalBalance?: string;
  timestamp: string;
}

/**
 * Player balance details DTO (Admin view)
 */
export interface PlayerBalanceDetailsDto {
  balance: PlayerBalanceDto;
  wageringInfo?: WageringInfoDto;
  recentTransactions: BalanceTransactionDto[];
  statisticsSummary: { [key: string]: any };
}

/**
 * Balance transaction DTO
 */
export interface BalanceTransactionDto {
  id: number;
  playerId: number;
  transactionType: string;
  amount: string;
  balanceType: string;
  balanceBefore: string;
  balanceAfter: string;
  referenceId?: string;
  referenceType?: string;
  description?: string;
  createdAt: string;
  metadata?: { [key: string]: any };
}

/**
 * Balance integrity report DTO (Admin)
 */
export interface BalanceIntegrityReportDto {
  playersChecked: number;
  issuesFound: number;
  issues: string[];
  timestamp: string;
}

/**
 * Balance adjustment request (Admin)
 */
export interface BalanceAdjustmentRequestDto {
  amount: string;
  adjustmentType: 'CREDIT' | 'DEBIT';
  balanceType: 'REAL' | 'BONUS';
  reason: string;
  applyWagering: boolean;
  wageringMultiplier?: string;
}

/**
 * Balance adjustment response (Admin)
 */
export interface BalanceAdjustmentResponseDto {
  success: boolean;
  balance: PlayerBalanceDto;
  adjustedAmount: string;
  adjustmentType: string;
  newBalance: string;
  reason: string;
  adminUsername: string;
  timestamp: string;
}

/**
 * Utility type for pagination
 */
export interface Page<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  size: number;
  number: number;
  first: boolean;
  last: boolean;
  numberOfElements: number;
  empty: boolean;
}

/**
 * Search filters for balance queries (Admin)
 */
export interface BalanceSearchFilter {
  playerId?: number;
  minBalance?: string;
  maxBalance?: string;
  balanceState?: BalanceState;
  wageringType?: WageringType;
  hasActiveBonus?: boolean;
  page: number;
  size: number;
  sort?: string;
}

/**
 * Transaction search filter (Admin)
 */
export interface TransactionSearchFilter {
  playerId?: number;
  transactionType?: string;
  startDate?: string;
  endDate?: string;
  minAmount?: string;
  maxAmount?: string;
  page: number;
  size: number;
  sort?: string;
}

// Type guards for runtime type checking
export function isPlayerBalanceDto(obj: any): obj is PlayerBalanceDto {
  return obj &&
    typeof obj.playerId === 'number' &&
    typeof obj.totalBalance === 'string' &&
    typeof obj.balanceState === 'string' &&
    typeof obj.canWithdraw === 'boolean';
}

export function isWageringInfoDto(obj: any): obj is WageringInfoDto {
  return obj &&
    typeof obj.playerId === 'number' &&
    typeof obj.wageringRequirement === 'string' &&
    typeof obj.progressPercentage === 'number';
}

// Utility functions for balance calculations
export class BalanceUtils {
  /**
   * Parse string balance to number for display
   * Note: For calculations, always use backend
   */
  static parseBalance(balance: string): number {
    return parseFloat(balance) || 0;
  }

  /**
   * Format balance for display with currency
   */
  static formatBalance(balance: string, currency: string = 'USD'): string {
    const value = BalanceUtils.parseBalance(balance);
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  }

  /**
   * Check if player can perform action based on balance state
   */
  static canPerformAction(state: BalanceState, action: 'withdraw' | 'play' | 'bonus'): boolean {
    switch (action) {
      case 'withdraw':
        return state === BalanceState.WITHDRAWABLE;
      case 'play':
        return state !== BalanceState.LOCKED_DEPOSIT;
      case 'bonus':
        return state === BalanceState.WITHDRAWABLE;
      default:
        return false;
    }
  }

  /**
   * Get balance state display information
   */
  static getBalanceStateInfo(state: BalanceState): {
    label: string;
    icon: string;
    color: string;
    description: string;
  } {
    switch (state) {
      case BalanceState.WITHDRAWABLE:
        return {
          label: 'Withdrawable',
          icon: 'check_circle',
          color: 'success',
          description: 'Your balance is available for withdrawal'
        };
      case BalanceState.LOCKED_DEPOSIT:
        return {
          label: 'Locked (Deposit)',
          icon: 'lock',
          color: 'warning',
          description: 'Balance locked due to recent deposit wagering requirement'
        };
      case BalanceState.LOCKED_BONUS:
        return {
          label: 'Locked (Bonus)',
          icon: 'card_giftcard',
          color: 'info',
          description: 'Balance locked due to active bonus wagering requirement'
        };
      case BalanceState.LOCKED_WAGERING:
        return {
          label: 'Locked (Wagering)',
          icon: 'casino',
          color: 'primary',
          description: 'Balance locked until wagering requirement is met'
        };
      default:
        return {
          label: 'Unknown',
          icon: 'help',
          color: 'default',
          description: 'Balance state unknown'
        };
    }
  }
}

export default {
  BalanceState,
  WageringType,
  BalanceUtils
};