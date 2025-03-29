import { get } from './base';

// Base endpoints for component types
const ENDPOINTS = {
  antennas: '/components/antennas',
  cameras: '/components/cameras',
  frames: '/components/frames',
  motors: '/components/motors',
  propellers: '/components/propellers',
  receivers: '/components/receivers',
  transmitters: '/components/transmitters',
  stacks: '/components/stacks',
  flight_controllers: '/components/flight_controllers',
  speed_controllers: '/components/speed_controllers',
};

/**
 * Get filter options and counts for a component type
 *
 * @param {string} componentType - Type of component (antennas, cameras, etc.)
 * @param {Object} params - Optional query parameters (filter_id, search)
 * @returns {Promise} - Promise with filter options data
 */
export function getComponentFilterOptions(componentType, params = {}) {
  return get(`${ENDPOINTS[componentType]}/filter_options/`, params);
}

/**
 * API functions for components
 */
export function getComponentList(componentType, params = {}) {
  return get(`${ENDPOINTS[componentType]}`, params);
}

export function getComponentById(componentType, id, params = {}) {
  return get(`${ENDPOINTS[componentType]}/${id}/`, params);
}
