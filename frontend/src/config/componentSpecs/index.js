import {antennaSpecs, antennaKeySpecs} from "./antennaSpecs";
import {cameraKeySpecs, cameraSpecs} from "./cameraSpecs";


// Export functions to get specs for a component type
export const getKeySpecsForComponentType = (type) => {
  const specsMap = {
    antennas: antennaKeySpecs,
    cameras: cameraKeySpecs,

    // Add more component types as needed
  };

  return specsMap[type] || [];
};

export const getFullSpecsForComponentType = (type) => {
  const specsMap = {
    antennas: antennaSpecs,
    cameras: cameraSpecs,

    // Add more component types as needed
  };

  return specsMap[type] || [];
};

// Generate tags for component cards based on component type and data
export const generateComponentTags = (componentType, item) => {
  if (!item) return [];

  switch(componentType) {
    case 'antennas':
      const tags = [];

      // Add connector types from details
      if (item.details && item.details.length > 0) {
        item.details.forEach(detail => {
          if (detail.connector_type && detail.connector_type.type) {
            tags.push(detail.connector_type.type);
          }
          if (detail.angle_type) {
            tags.push(detail.angle_type);
          }
          if (detail.weight) {
            tags.push(`${detail.weight}g`);
          }
        });
      }

      return tags;

    case 'cameras':
      return [
        item.output_type === 'A' ? 'Analog' : 'Digital',
        item.ratio,
        item.weight ? `${item.weight}g` : null
      ].filter(Boolean);

    // Add more component types as needed
    default:
      return [];
  }
};