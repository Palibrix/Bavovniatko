import { get, put } from './base';

const ENDPOINTS = {
  profiles: '/user/profiles/',
  me: '/user/profiles/me/'
};

/**
 * Get the current user's profile
 *
 * @returns {Promise} Promise with user profile data
 */
export const getCurrentUserProfile = async () => {
  return get(ENDPOINTS.me);
};

/**
 * Get a user's profile by ID
 *
 * @param {string|number} id User ID
 * @returns {Promise} Promise with user profile data
 */
export const getUserProfile = async (id) => {
  return get(`${ENDPOINTS.profiles}${id}/`);
};

/**
 * Update current user's profile
 *
 * @param {Object} profileData Updated profile data
 * @returns {Promise} Promise with updated user data
 */
export const updateUserProfile = async (profileData) => {
  return put(ENDPOINTS.me, profileData);
};