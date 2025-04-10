import {post} from './base';

const ENDPOINTS = {
    check: '/compatibility/check/',
    components: (componentType) => `/compatibility/components/${componentType}/`
};

/**
 * Check compatibility of a drone configuration
 *
 * @param {Object} configuration - Current component configuration
 * @param {Object} previousConfiguration - Previous configuration for incremental check
 * @param {Object} previousResults - Previous compatibility results
 * @returns {Promise} - Promise with compatibility results
 */
export const checkCompatibility = async (configuration, previousConfiguration = null, previousResults = null) => {
    const payload = {
        configuration
    };

    // Add optional params for incremental checks
    if (previousConfiguration) {
        payload.previous_configuration = previousConfiguration;
    }

    if (previousResults) {
        payload.previous_results = previousResults;
    }

    return post(ENDPOINTS.check, payload);
};

/**
 * Get components compatible with current configuration
 *
 * @param {string} componentType - Type of component to fetch
 * @param {Object} configuration - Current component configuration
 * @param {Object} filterParams - Optional filter parameters
 * @returns {Promise} - Promise with compatible components
 */
export const getCompatibleComponents = async (componentType, configuration, filterParams = {}) => {
    // Build the endpoint with query parameters if any
    let endpoint = ENDPOINTS.components(componentType);

    // Add filter parameters to the URL if provided
    if (Object.keys(filterParams).length > 0) {
        const queryString = new URLSearchParams(filterParams).toString();
        endpoint = `${endpoint}?${queryString}`;
    }

    return post(endpoint, {configuration});
};