/**
 * JWT Utilities for extracting claims from tokens
 * Handles player ID, roles, and other claims from Phase 3 JWT structure
 */

/**
 * JWT Token payload structure from Phase 3 backend
 */
export interface JwtPayload {
  sub: string;           // Username (subject)
  userId?: number;       // User ID
  playerId?: number;     // Player ID (optional, only for players)
  roles?: string[];      // User roles (PLAYER, ADMIN, GAME_PROVIDER, etc.)
  iat: number;          // Issued at timestamp
  exp: number;          // Expiration timestamp
}

/**
 * User roles enum matching backend
 */
export enum UserRole {
  PLAYER = 'PLAYER',
  ADMIN = 'ADMIN',
  CMS_ADMIN = 'CMS_ADMIN',
  GAME_PROVIDER = 'GAME_PROVIDER',
  SUPPORT = 'SUPPORT',
  FINANCE = 'FINANCE',
  MARKETING = 'MARKETING'
}

/**
 * JWT utility class for token operations
 */
export class JwtUtils {
  /**
   * Decode JWT token without verification (client-side only)
   * For production, token verification happens on the backend
   */
  static decodeToken(token: string): JwtPayload | null {
    try {
      // Remove 'Bearer ' prefix if present
      const cleanToken = token.replace('Bearer ', '');

      // Split token into parts
      const parts = cleanToken.split('.');
      if (parts.length !== 3) {
        console.error('Invalid JWT format');
        return null;
      }

      // Decode payload (second part)
      const payload = parts[1];
      const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
      return JSON.parse(decodedPayload) as JwtPayload;
    } catch (error) {
      console.error('Error decoding JWT:', error);
      return null;
    }
  }

  /**
   * Extract player ID from JWT token
   */
  static getPlayerIdFromToken(token: string): number | null {
    const payload = this.decodeToken(token);
    return payload?.playerId || null;
  }

  /**
   * Extract user ID from JWT token
   */
  static getUserIdFromToken(token: string): number | null {
    const payload = this.decodeToken(token);
    return payload?.userId || null;
  }

  /**
   * Extract username from JWT token
   */
  static getUsernameFromToken(token: string): string | null {
    const payload = this.decodeToken(token);
    return payload?.sub || null;
  }

  /**
   * Extract roles from JWT token
   */
  static getRolesFromToken(token: string): string[] {
    const payload = this.decodeToken(token);
    return payload?.roles || [];
  }

  /**
   * Check if token has specific role
   */
  static hasRole(token: string, role: UserRole | string): boolean {
    const roles = this.getRolesFromToken(token);
    return roles.includes(role);
  }

  /**
   * Check if token has any of the specified roles
   */
  static hasAnyRole(token: string, roles: (UserRole | string)[]): boolean {
    const userRoles = this.getRolesFromToken(token);
    return roles.some(role => userRoles.includes(role));
  }

  /**
   * Check if token has all specified roles
   */
  static hasAllRoles(token: string, roles: (UserRole | string)[]): boolean {
    const userRoles = this.getRolesFromToken(token);
    return roles.every(role => userRoles.includes(role));
  }

  /**
   * Check if token is expired
   */
  static isTokenExpired(token: string): boolean {
    const payload = this.decodeToken(token);
    if (!payload || !payload.exp) {
      return true;
    }

    // Compare with current time (exp is in seconds, Date.now() is in milliseconds)
    const expirationTime = payload.exp * 1000;
    return Date.now() >= expirationTime;
  }

  /**
   * Get token expiration time
   */
  static getTokenExpiration(token: string): Date | null {
    const payload = this.decodeToken(token);
    if (!payload || !payload.exp) {
      return null;
    }

    return new Date(payload.exp * 1000);
  }

  /**
   * Get time until token expires in seconds
   */
  static getTimeUntilExpiration(token: string): number {
    const payload = this.decodeToken(token);
    if (!payload || !payload.exp) {
      return 0;
    }

    const expirationTime = payload.exp * 1000;
    const timeUntilExpiry = expirationTime - Date.now();
    return Math.max(0, Math.floor(timeUntilExpiry / 1000));
  }

  /**
   * Check if user is a player (has PLAYER role and playerId)
   */
  static isPlayer(token: string): boolean {
    const payload = this.decodeToken(token);
    return payload !== null &&
           payload.playerId !== undefined &&
           payload.playerId !== null &&
           (payload.roles?.includes(UserRole.PLAYER) ?? false);
  }

  /**
   * Check if user is an admin (has ADMIN role)
   */
  static isAdmin(token: string): boolean {
    return this.hasRole(token, UserRole.ADMIN);
  }

  /**
   * Check if user is a game provider
   */
  static isGameProvider(token: string): boolean {
    return this.hasRole(token, UserRole.GAME_PROVIDER);
  }

  /**
   * Get all claims from token as a readable object
   */
  static getAllClaims(token: string): {
    username: string | null;
    userId: number | null;
    playerId: number | null;
    roles: string[];
    issuedAt: Date | null;
    expiresAt: Date | null;
    isExpired: boolean;
  } {
    const payload = this.decodeToken(token);

    return {
      username: payload?.sub || null,
      userId: payload?.userId || null,
      playerId: payload?.playerId || null,
      roles: payload?.roles || [],
      issuedAt: payload?.iat ? new Date(payload.iat * 1000) : null,
      expiresAt: payload?.exp ? new Date(payload.exp * 1000) : null,
      isExpired: this.isTokenExpired(token)
    };
  }

  /**
   * Format token for authorization header
   */
  static formatAuthorizationHeader(token: string): string {
    // Add Bearer prefix if not present
    if (!token.startsWith('Bearer ')) {
      return `Bearer ${token}`;
    }
    return token;
  }

  /**
   * Extract token from authorization header
   */
  static extractTokenFromHeader(authHeader: string): string | null {
    if (!authHeader) {
      return null;
    }

    // Check if header starts with 'Bearer '
    if (authHeader.startsWith('Bearer ')) {
      return authHeader.substring(7);
    }

    // Return as-is if no Bearer prefix (assume it's just the token)
    return authHeader;
  }
}

/**
 * Storage service for managing JWT tokens in browser
 */
export class TokenStorageService {
  private static readonly TOKEN_KEY = 'auth_token';
  private static readonly REFRESH_TOKEN_KEY = 'refresh_token';

  /**
   * Store access token
   */
  static setToken(token: string): void {
    if (typeof window !== 'undefined') {
      sessionStorage.setItem(this.TOKEN_KEY, token);
    }
  }

  /**
   * Get stored access token
   */
  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  /**
   * Store refresh token (in more secure storage)
   */
  static setRefreshToken(token: string): void {
    if (typeof window !== 'undefined') {
      // Use httpOnly cookie in production, localStorage for development
      localStorage.setItem(this.REFRESH_TOKEN_KEY, token);
    }
  }

  /**
   * Get refresh token
   */
  static getRefreshToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.REFRESH_TOKEN_KEY);
    }
    return null;
  }

  /**
   * Clear all tokens (logout)
   */
  static clearTokens(): void {
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem(this.TOKEN_KEY);
      localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    }
  }

  /**
   * Check if user is authenticated (has valid token)
   */
  static isAuthenticated(): boolean {
    const token = this.getToken();
    return token !== null && !JwtUtils.isTokenExpired(token);
  }

  /**
   * Get current user's player ID
   */
  static getCurrentPlayerId(): number | null {
    const token = this.getToken();
    return token ? JwtUtils.getPlayerIdFromToken(token) : null;
  }

  /**
   * Get current user's roles
   */
  static getCurrentUserRoles(): string[] {
    const token = this.getToken();
    return token ? JwtUtils.getRolesFromToken(token) : [];
  }

  /**
   * Check if current user has specific role
   */
  static currentUserHasRole(role: UserRole | string): boolean {
    const token = this.getToken();
    return token ? JwtUtils.hasRole(token, role) : false;
  }
}

export default {
  JwtUtils,
  TokenStorageService,
  UserRole
};