// Base API configuration and helper functions

// Base API URL - adjust this to match your Django backend
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api/v1';

// Global request options (can be extended for auth tokens later)
const defaultOptions = {
  headers: {
    'Content-Type': 'application/json',
  }
};

/**
 * Get token for authentication
 */
const getToken = () => {
  return localStorage.getItem('auth_token');
};

/**
 * Get default headers for requests
 */
const getHeaders = () => {
  const headers = {
    'Content-Type': 'application/json',
  };

  const token = getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};
/**
 * Core API request function that all other API calls will use
 *
 * @param {string} endpoint - API endpoint path (without base URL)
 * @param {Object} options - Fetch options and parameters
 * @returns {Promise} - Promise with response JSON data
 */
export async function apiRequest(endpoint, options = {}) {
  try {
    // Get current headers
    const headers = getHeaders();

    // Merge default options with any provided options
    const requestOptions = {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      }
    };

    // Make the request
    const response = await fetch(`${API_BASE_URL}${endpoint}`, requestOptions);
    console.log(response.url);

    // Extract validation function for status code if provided
    const validateStatus = options.validateStatus ||
      ((status) => status >= 200 && status < 300);

    // Handle non-2xx responses unless validated by validateStatus
    if (!validateStatus(response.status)) {
      // Try to get error message from response body
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        errorData = { detail: `HTTP Error ${response.status}` };
      }

      throw {
        status: response.status,
        statusText: response.statusText,
        data: errorData
      };
    }

    // For 204 No Content or empty responses, return success object
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return { success: true };
    }

    // Try to parse JSON response
    try {
      const data = await response.json();
      return data;
    } catch (error) {
      // Return success object for empty successful responses
      if (response.ok) {
        return { success: true };
      }
      throw {
        status: response.status,
        statusText: 'Invalid JSON response',
        message: 'Server returned invalid JSON'
      };
    }
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * Helper function for GET requests
 */
export function get(endpoint, params = {}) {
  // Build query string from params
  const queryString = Object.keys(params).length
    ? '?' + new URLSearchParams(params).toString()
    : '';

  return apiRequest(`${endpoint}${queryString}`, { method: 'GET' });
}

/**
 * Helper function for POST requests
 */
export function post(endpoint, data = {}) {
  return apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

/**
 * Helper function for PUT requests
 */
export function put(endpoint, data = {}) {
  return apiRequest(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

/**
 * Helper function for PATCH requests
 */
export function patch(endpoint, data = {}) {
  return apiRequest(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data)
  });
}

/**
 * Helper function for DELETE requests
 */
export function del(endpoint) {
  return apiRequest(endpoint, {
    method: 'DELETE',
    // Set validateStatus to true to prevent errors for 204 No Content responses
    validateStatus: (status) => (status >= 200 && status < 300) || status === 204
  }).catch(error => {
    // For 204 No Content responses which are common for DELETE operations
    if (error.status === 204) {
      return { success: true };
    }
    throw error;
  });
}
