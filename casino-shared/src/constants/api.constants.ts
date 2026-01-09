/**
 * API endpoint constants for Phase 3 unified wallet system
 * All endpoints follow the pattern: /api/v1/{resource}
 */

/**
 * Base API configuration
 */
export const API_CONFIG = {
  BASE_URL: '/api/v1',
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000
};

/**
 * Player balance endpoints
 */
export const BALANCE_ENDPOINTS = {
  // Player endpoints (accessible by PLAYER or ADMIN)
  GET_BALANCE: (playerId: number) => `/api/v1/players/${playerId}/balance`,
  DEPOSIT: (playerId: number) => `/api/v1/players/${playerId}/balance/deposit`,
  WITHDRAW: (playerId: number) => `/api/v1/players/${playerId}/balance/withdraw`,
  GET_WAGERING: (playerId: number) => `/api/v1/players/${playerId}/balance/wagering`,
  ACTIVATE_BONUS: (playerId: number) => `/api/v1/players/${playerId}/balance/bonus/activate`,
  FORFEIT_BONUS: (playerId: number) => `/api/v1/players/${playerId}/balance/bonus/forfeit`,
};

/**
 * Game transaction endpoints
 */
export const GAME_ENDPOINTS = {
  // Game provider endpoints (accessible by GAME_PROVIDER or ADMIN)
  PLACE_BET: (playerId: number) => `/api/v1/players/${playerId}/games/bet`,
  PROCESS_WIN: (playerId: number) => `/api/v1/players/${playerId}/games/win`,
  BET_AND_WIN: (playerId: number) => `/api/v1/players/${playerId}/games/bet-win`,
};

/**
 * Admin balance endpoints
 */
export const ADMIN_BALANCE_ENDPOINTS = {
  // Admin-only endpoints
  GET_STATISTICS: () => `/api/v1/admin/balance/statistics`,
  SEARCH_BALANCES: () => `/api/v1/admin/balance/search`,
  GET_TRANSACTIONS: () => `/api/v1/admin/balance/transactions`,
  GET_PLAYER_DETAILS: (playerId: number) => `/api/v1/admin/balance/players/${playerId}`,
  VALIDATE_INTEGRITY: () => `/api/v1/admin/balance/validate`,
};

/**
 * Authentication endpoints (existing system)
 */
export const AUTH_ENDPOINTS = {
  LOGIN: () => `/api/v1/auth/login`,
  REGISTER: () => `/api/v1/auth/register`,
  REFRESH_TOKEN: () => `/api/v1/auth/refresh`,
  LOGOUT: () => `/api/v1/auth/logout`,
  VERIFY_TOKEN: () => `/api/v1/auth/verify`,
};

/**
 * HTTP methods enum
 */
export enum HttpMethod {
  GET = 'GET',
  POST = 'POST',
  PUT = 'PUT',
  PATCH = 'PATCH',
  DELETE = 'DELETE'
}

/**
 * API response status codes
 */
export enum ApiStatusCode {
  OK = 200,
  CREATED = 201,
  NO_CONTENT = 204,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  CONFLICT = 409,
  UNPROCESSABLE_ENTITY = 422,
  INTERNAL_SERVER_ERROR = 500,
  SERVICE_UNAVAILABLE = 503
}

/**
 * API error codes from backend
 */
export enum ApiErrorCode {
  // Balance errors
  INSUFFICIENT_BALANCE = 'INSUFFICIENT_BALANCE',
  INVALID_AMOUNT = 'INVALID_AMOUNT',
  BALANCE_LOCKED = 'BALANCE_LOCKED',
  WAGERING_NOT_MET = 'WAGERING_NOT_MET',
  WITHDRAWAL_LIMIT_EXCEEDED = 'WITHDRAWAL_LIMIT_EXCEEDED',

  // Bonus errors
  BONUS_ALREADY_ACTIVE = 'BONUS_ALREADY_ACTIVE',
  BONUS_NOT_FOUND = 'BONUS_NOT_FOUND',
  BONUS_EXPIRED = 'BONUS_EXPIRED',
  BONUS_NOT_ELIGIBLE = 'BONUS_NOT_ELIGIBLE',

  // Transaction errors
  TRANSACTION_FAILED = 'TRANSACTION_FAILED',
  DUPLICATE_TRANSACTION = 'DUPLICATE_TRANSACTION',
  INVALID_TRANSACTION = 'INVALID_TRANSACTION',

  // Game errors
  GAME_NOT_AVAILABLE = 'GAME_NOT_AVAILABLE',
  INVALID_GAME_STATE = 'INVALID_GAME_STATE',
  BET_LIMIT_EXCEEDED = 'BET_LIMIT_EXCEEDED',

  // Auth errors
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  TOKEN_INVALID = 'TOKEN_INVALID',
  ACCESS_DENIED = 'ACCESS_DENIED',

  // General errors
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND',
  OPERATION_NOT_ALLOWED = 'OPERATION_NOT_ALLOWED',
  INTERNAL_ERROR = 'INTERNAL_ERROR'
}

/**
 * API request headers
 */
export const API_HEADERS = {
  CONTENT_TYPE: 'Content-Type',
  AUTHORIZATION: 'Authorization',
  ACCEPT: 'Accept',
  ACCEPT_LANGUAGE: 'Accept-Language',
  X_REQUEST_ID: 'X-Request-ID',
  X_CORRELATION_ID: 'X-Correlation-ID',
  X_PLAYER_ID: 'X-Player-ID',
  X_SESSION_ID: 'X-Session-ID'
};

/**
 * Content types
 */
export const CONTENT_TYPES = {
  JSON: 'application/json',
  FORM_URLENCODED: 'application/x-www-form-urlencoded',
  MULTIPART: 'multipart/form-data',
  TEXT: 'text/plain',
  HTML: 'text/html'
};

/**
 * Pagination defaults
 */
export const PAGINATION_DEFAULTS = {
  PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  MAX_PAGE_SIZE: 100,
  FIRST_PAGE: 0
};

/**
 * Cache configuration
 */
export const CACHE_CONFIG = {
  BALANCE_TTL: 30,         // 30 seconds for balance data
  STATISTICS_TTL: 300,     // 5 minutes for statistics
  TRANSACTIONS_TTL: 60,    // 1 minute for transactions
  WAGERING_TTL: 30,        // 30 seconds for wagering info
  DISABLE_CACHE: false     // Set to true to disable all caching
};

/**
 * WebSocket endpoints for real-time updates
 */
export const WEBSOCKET_ENDPOINTS = {
  BALANCE_UPDATES: '/ws/balance',
  GAME_EVENTS: '/ws/games',
  NOTIFICATIONS: '/ws/notifications'
};

/**
 * API endpoint builder utility
 */
export class ApiEndpointBuilder {
  private baseUrl: string;
  private queryParams: Map<string, string>;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.queryParams = new Map();
  }

  /**
   * Add query parameter
   */
  addParam(key: string, value: any): ApiEndpointBuilder {
    if (value !== undefined && value !== null && value !== '') {
      this.queryParams.set(key, String(value));
    }
    return this;
  }

  /**
   * Add multiple query parameters
   */
  addParams(params: { [key: string]: any }): ApiEndpointBuilder {
    Object.entries(params).forEach(([key, value]) => {
      this.addParam(key, value);
    });
    return this;
  }

  /**
   * Add pagination parameters
   */
  addPagination(page: number, size: number, sort?: string): ApiEndpointBuilder {
    this.addParam('page', page);
    this.addParam('size', size);
    if (sort) {
      this.addParam('sort', sort);
    }
    return this;
  }

  /**
   * Build the complete URL with query parameters
   */
  build(): string {
    if (this.queryParams.size === 0) {
      return this.baseUrl;
    }

    const queryString = Array.from(this.queryParams.entries())
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
      .join('&');

    return `${this.baseUrl}?${queryString}`;
  }
}

/**
 * Helper function to build API URL with query params
 */
export function buildApiUrl(endpoint: string, params?: { [key: string]: any }): string {
  const builder = new ApiEndpointBuilder(endpoint);
  if (params) {
    builder.addParams(params);
  }
  return builder.build();
}

/**
 * Helper function to check if status code indicates success
 */
export function isSuccessStatus(status: number): boolean {
  return status >= 200 && status < 300;
}

/**
 * Helper function to check if status code indicates client error
 */
export function isClientError(status: number): boolean {
  return status >= 400 && status < 500;
}

/**
 * Helper function to check if status code indicates server error
 */
export function isServerError(status: number): boolean {
  return status >= 500 && status < 600;
}

export default {
  API_CONFIG,
  BALANCE_ENDPOINTS,
  GAME_ENDPOINTS,
  ADMIN_BALANCE_ENDPOINTS,
  AUTH_ENDPOINTS,
  HttpMethod,
  ApiStatusCode,
  ApiErrorCode,
  API_HEADERS,
  CONTENT_TYPES,
  PAGINATION_DEFAULTS,
  CACHE_CONFIG,
  WEBSOCKET_ENDPOINTS,
  ApiEndpointBuilder,
  buildApiUrl,
  isSuccessStatus,
  isClientError,
  isServerError
};