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
 * Get the appropriate theme color based on component type
 *
 * @param {string} componentType Type of component (antennas, cameras, etc.)
 * @returns {string} Theme color name
 */
export const getComponentThemeColor = (componentType) => {
  const themes = {
    antennas: 'antenna',
    cameras: 'video',
    frames: 'frame',
    motors: 'propulsion',
    propellers: 'propulsion',
    receivers: 'control',
    transmitters: 'video',
    stacks: 'control',
    flight_controllers: 'control',
    speed_controllers: 'control'
  };

  return themes[componentType] || 'primary';
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

/**
 * Convert component data to a JSON string for copying
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

  return JSON.stringify(result, null, 2);
};

export default {
  getPrimaryImage,
  getComponentThemeColor,
  hasDocuments,
  hasDetails,
  componentToJson
};