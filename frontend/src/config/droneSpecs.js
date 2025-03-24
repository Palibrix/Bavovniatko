import {
  faClock, faWeightHanging, faTachometerAlt,
  faLocationArrow, faArrowUp, faMapMarkedAlt,
  faBolt, faPlane, faInfoCircle
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for drone specifications to display in list and detail views
 */

// DRONES - Key specs shown in cards and sidebar
export const droneKeySpecs = [
  {
    label: 'Flight Duration',
    path: 'flight_duration',
    icon: faClock,
    unit: 'min'
  },
  {
    label: 'Total Weight',
    path: 'total_weight',
    icon: faWeightHanging,
    unit: 'g'
  },
  {
    label: 'Max Speed',
    path: 'max_speed',
    icon: faTachometerAlt,
    unit: 'km/h'
  },
  {
    label: 'Control Range',
    path: 'control_range',
    icon: faLocationArrow,
    unit: 'm'
  },
  {
    label: 'Max Altitude',
    path: 'max_altitude',
    icon: faArrowUp,
    unit: 'm'
  }
];

// All drone specifications including key specs
export const droneSpecs = [
  // Include key specs first
  ...droneKeySpecs,

  // Additional specifications - only include drone-specific specs
  {
    label: 'Drone Type',
    path: 'type',
    icon: faPlane,
  }
];

// Generate tags for drone cards
export const generateDroneTags = (item) => {
  if (!item) return [];

  const tags = [];

  // Add drone type as a tag
  if (item.type) {
    const typeMap = {
      'photography': 'Photography',
      'sport': 'Sport',
      'freestyle': 'Freestyle',
      'another': 'Other'
    };

    tags.push(typeMap[item.type] || item.type);
  }

  // // Add component tags sparingly - just the main ones
  // if (item.frame && item.frame.manufacturer && item.frame.model) {
  //   tags.push(`${item.frame.manufacturer} Frame`);
  // } else if (item.frame && item.frame.model) {
  //   tags.push(`${item.frame.model} Frame`);
  // }
  //
  // // Add camera if available
  // if (item.camera && item.camera.model) {
  //   tags.push(`${item.camera.manufacturer || ''} Camera`.trim());
  // }

  return tags;
};

// Export functions to get specs for drones
export const getDroneKeySpecs = () => {
  return droneKeySpecs;
};

export const getDroneFullSpecs = () => {
  return droneSpecs;
};

export default {
  droneKeySpecs,
  droneSpecs,
  generateDroneTags,
  getDroneKeySpecs,
  getDroneFullSpecs
};