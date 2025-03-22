import { get } from './base';

const ENDPOINTS = {
  drones: '/builds/drones/',
};

// ========== Drones ==========
/**
 * Get all drones with optional filter parameters
 *
 * @param {Object} params - Query parameters for filtering
 * @returns {Promise} - Promise with drone data
 */
export function getDrones(params = {}) {
  return get(ENDPOINTS.drones, params);
}

/**
 * Get a specific drone by ID
 *
 * @param {string|number} id - Drone ID
 * @returns {Promise} - Promise with drone data
 */
export function getDroneById(id) {
  return get(`${ENDPOINTS.drones}${id}/`);
}