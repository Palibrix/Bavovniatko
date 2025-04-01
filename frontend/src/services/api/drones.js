import {get, patch, post, put} from './base';

const ENDPOINTS = {
    drones: '/builds/drones/',
};

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

export function createDrone(droneData) {
    return post(ENDPOINTS.drones, droneData);
}

/**
 * Update an existing drone
 * @param {string|number} id - Drone ID
 * @param {Object} droneData - Updated drone data
 * @returns {Promise} - Promise with updated drone data
 */
export function updateDrone(id, droneData) {
    return put(`${ENDPOINTS.drones}${id}/`, droneData);
}

/**
 * Partially update a drone
 * @param {string|number} id - Drone ID
 * @param {Object} droneData - Partial drone data
 * @returns {Promise} - Promise with updated drone data
 */
export function patchDrone(id, droneData) {
    return patch(`${ENDPOINTS.drones}${id}/`, droneData);
}