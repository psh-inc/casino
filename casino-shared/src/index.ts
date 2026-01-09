/**
 * Casino Shared Library
 * Shared models, utilities, and constants for casino frontend applications
 * Compatible with Phase 3 unified wallet infrastructure
 */

// Export all models
export * from './models/balance.models';
export * from './models/game.models';

// Export utilities
export * from './utils/jwt.utils';

// Export constants
export * from './constants/api.constants';

// Default export with namespaces
import * as BalanceModels from './models/balance.models';
import * as GameModels from './models/game.models';
import * as JwtUtils from './utils/jwt.utils';
import * as ApiConstants from './constants/api.constants';

export default {
  BalanceModels,
  GameModels,
  JwtUtils,
  ApiConstants
};