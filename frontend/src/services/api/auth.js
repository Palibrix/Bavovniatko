import { post } from './base';

// Constants for token storage
const TOKEN_KEY = 'auth_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

// Endpoints
const ENDPOINTS = {
  login: '/auth/token/',
  register: '/auth/signup/',
  refreshToken: '/auth/token/refresh/',
  verifyToken: '/auth/token/verify/',
  logout: '/auth/token/blacklist/'
};

/**
 * Store authentication tokens in localStorage
 */
const storeTokens = (tokens) => {
  if (tokens.access) {
    localStorage.setItem(TOKEN_KEY, tokens.access);
  }
  if (tokens.refresh) {
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);
  }
};

/**
 * Remove authentication tokens from localStorage
 */
const removeTokens = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/**
 * Get stored tokens
 */
const getTokens = () => {
  return {
    access: localStorage.getItem(TOKEN_KEY),
    refresh: localStorage.getItem(REFRESH_TOKEN_KEY)
  };
};

/**
 * Authenticate user with username and password
 */
export const login = async (credentials) => {
  const response = await post(ENDPOINTS.login, credentials);
  storeTokens(response);
  return response;
};

/**
 * Register a new user
 */
export const register = async (userData) => {
  return await post(ENDPOINTS.register, userData);
};

/**
 * Logout user (blacklist current token)
 */
export const logout = async () => {
  const { refresh } = getTokens();
  if (!refresh) {
    return Promise.resolve({ success: true });
  }

  try {
    await post(ENDPOINTS.logout, { refresh });
  } finally {
    removeTokens();
  }

  return { success: true };
};

/**
 * Refresh the access token using the refresh token
 */
export const refreshToken = async () => {
  const { refresh } = getTokens();
  if (!refresh) {
    return Promise.reject(new Error('No refresh token available'));
  }

  const response = await post(ENDPOINTS.refreshToken, { refresh });
  if (response.access) {
    localStorage.setItem(TOKEN_KEY, response.access);
  }

  return response;
};

/**
 * Verify if the current token is valid
 */
export const verifyToken = async () => {
  const { access } = getTokens();
  if (!access) {
    return Promise.reject(new Error('No access token available'));
  }

  return await post(ENDPOINTS.verifyToken, { token: access });
};

/**
 * Check if user is authenticated (has tokens)
 */
export const isAuthenticated = () => {
  const { access, refresh } = getTokens();
  return !!access && !!refresh;
};

/**
 * Get the current access token
 */
export const getAccessToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export default {
  login,
  register,
  logout,
  refreshToken,
  verifyToken,
  isAuthenticated,
  getAccessToken
};