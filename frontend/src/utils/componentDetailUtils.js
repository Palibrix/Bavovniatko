/**
 * Utility functions for the enhanced component detail page
 */

/**
 * Get the primary image URL from a component or a placeholder
 *
 * @param {Object} item Component data with images array
 * @returns {string} Image URL
 */
export const getPrimaryImage = (item) => {
  if (item?.images && item.images.length > 0) {
    // Find image with order=0 or the first image
    const primaryImage = item.images.find(img => img.order === 0) || item.images[0];
    return primaryImage.image;
  }
  return '/api/placeholder/400/300'; // Placeholder if no image
};

/**
 * Check if a component has documents
 *
 * @param {Object} item Component data
 * @returns {boolean} True if component has documents
 */
export const hasDocuments = (item) => {
  return item?.documents && item.documents.length > 0;
};

/**
 * Check if a component has details
 *
 * @param {Object} item Component data
 * @param {string} componentType Type of component
 * @returns {boolean} True if component has details
 */
export const hasDetails = (item, componentType) => {
  switch (componentType) {
    case 'antennas':
      return item?.details && item.details.length > 0;
    case 'cameras':
      return item?.details && item.details.length > 0;
    case 'frames':
      return (
        (item?.camera_details && item.camera_details.length > 0) ||
        (item?.motor_details && item.motor_details.length > 0) ||
        (item?.vtx_details && item.vtx_details.length > 0)
      );
    case 'motors':
      return item?.details && item.details.length > 0;
    case 'receivers':
      return item?.details && item.details.length > 0;
    default:
      return false;
  }
};

// Helper to format specification values
export const formatSpecValue = (value) => {
    if (value === null || value === undefined) return 'N/A';

    if (typeof value === 'boolean') {
      return value ? 'Yes' : 'No';
    }

    if (typeof value === 'object') {
      // If it's an array, join with commas
      if (Array.isArray(value)) {
        return value.join(', ');
      }

      // If it has a type property, it might be a related object
      if (value.type) {
        return value.type;
      }

      // For other objects, stringify (but limit length)
      return JSON.stringify(value).substring(0, 50);
    }

    return value.toString();
  };

/**
 * Convert component data to a JSON string for copying
 * Includes all specifications and details data
 *
 * @param {Object} item Component data
 * @param {Array} specsConfig Specs configuration
 * @returns {string} JSON string
 */
export const componentToJson = (item, specsConfig) => {
  if (!item) return '{}';

  // Create base object with manufacturer and model
  const result = {
    manufacturer: item.manufacturer,
    model: item.model
  };

  // Add specs based on specsConfig
  if (specsConfig) {
    specsConfig.forEach(spec => {
      // Extract value using path
      const value = spec.path.split('.').reduce((obj, key) =>
        obj && obj[key] !== undefined ? obj[key] : null, item);

      if (value !== null && value !== undefined) {
        // Use formatter if available
        if (spec.formatter) {
          result[spec.label] = spec.formatter(value, item);
        } else if (spec.unit) {
          result[spec.label] = `${value} ${spec.unit}`;
        } else {
          result[spec.label] = value;
        }
      }
    });
  }

  // Add details data based on component type
  if (item.details && Array.isArray(item.details) && item.details.length > 0) {
    result.details = item.details.map(detail => {
      // Create a clean details object without circular references
      // const cleanDetail = { ...detail };
      const { created_at, updated_at, ...cleanDetail } = detail;

      // Remove any object references that might cause circular JSON
      if (cleanDetail.antenna) delete cleanDetail.antenna;
      if (cleanDetail.motor) delete cleanDetail.motor;
      if (cleanDetail.camera) delete cleanDetail.camera;
      if (cleanDetail.receiver) delete cleanDetail.receiver;

      return cleanDetail;
    });
  }

  // Add frame-specific details
  if (item.camera_details && Array.isArray(item.camera_details) && item.camera_details.length > 0) {
    result.camera_details = item.camera_details.map(camera => {
      const { created_at, updated_at, ...rest } = camera;
      return rest;
    });
  }

  if (item.motor_details && Array.isArray(item.motor_details) && item.motor_details.length > 0) {
    result.motor_details = item.motor_details.map(motor => {
      const { created_at, updated_at, ...rest } = motor;
      return rest;
    });
  }

  if (item.vtx_details && Array.isArray(item.vtx_details) && item.vtx_details.length > 0) {
    result.vtx_details = item.vtx_details.map(vtx => {
      const { created_at, updated_at, ...rest } = vtx;
      return rest;
    });
  }

  return JSON.stringify(result, null, 2);
};

export default {
  getPrimaryImage,
  hasDocuments,
  hasDetails,
  componentToJson,
  formatSpecValue
};