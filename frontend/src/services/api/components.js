import { get } from './base';

// Base endpoints for component types
const ENDPOINTS = {
  antennas: '/components/antennas',
  cameras: '/components/cameras/',
  frames: '/components/frames/',
  motors: '/components/motors/',
  propellers: '/components/propellers/',
  receivers: '/components/receivers/',
  transmitters: '/components/transmitters/',
  stacks: '/components/stacks/',
  flightControllers: '/components/flight-controllers/',
  speedControllers: '/components/speed-controllers/',
};

/**
 * API functions for components
 */

// ========== Antennas ==========
/**
 * Get all antennas with optional filter parameters
 * 
 * @param {Object} params - Query parameters for filtering
 * @returns {Promise} - Promise with antenna data
 */
export function getAntennas(params = {}) {
  return get(ENDPOINTS.antennas, params);
}

/**
 * Get a specific antenna by ID
 * 
 * @param {string|number} id - Antenna ID
 * @returns {Promise} - Promise with antenna data
 */
export function getAntennaById(id) {
  return get(`${ENDPOINTS.antennas}/${id}/`);
}

// ========== Cameras ==========
/**
 * Get all cameras with optional filter parameters
 * 
 * @param {Object} params - Query parameters for filtering
 * @returns {Promise} - Promise with camera data
 */
export function getCameras(params = {}) {
  return get(ENDPOINTS.cameras, params);
}

/**
 * Get a specific camera by ID
 * 
 * @param {string|number} id - Camera ID
 * @returns {Promise} - Promise with camera data
 */
export function getCameraById(id) {
  return get(`${ENDPOINTS.cameras}${id}/`);
}

// ========== Frames ==========
/**
 * Get all frames with optional filter parameters
 * 
 * @param {Object} params - Query parameters for filtering
 * @returns {Promise} - Promise with frame data
 */
export function getFrames(params = {}) {
  return get(ENDPOINTS.frames, params);
}

/**
 * Get a specific frame by ID
 * 
 * @param {string|number} id - Frame ID
 * @returns {Promise} - Promise with frame data
 */
export function getFrameById(id) {
  return get(`${ENDPOINTS.frames}${id}/`);
}

// Add similar functions for other component types
// This pattern can be extended for all component types in your application

// Helper function to get any component type dynamically
export function getComponentsByType(type, params = {}) {
  if (!ENDPOINTS[type]) {
    throw new Error(`Unknown component type: ${type}`);
  }
  return get(ENDPOINTS[type], params);
}

export function getComponentById(type, id) {
  if (!ENDPOINTS[type]) {
    throw new Error(`Unknown component type: ${type}`);
  }
  return get(`${ENDPOINTS[type]}${id}/`);
}
