import {
  faBroadcastTower, faArrowsAltH, faSignal,
  faTags, faCompass, faSyncAlt, faPlug,
  faWeightHanging, faAngleUp, faMicrochip, faCog,
  faCamera, faRuler, faFan, faBatteryFull,
  faWaveSquare, faChartPie, faRocket
} from '@fortawesome/free-solid-svg-icons';

import { droneKeySpecs, droneFullSpecs, generateDroneTags } from './droneSpecs';

/**
 * Configuration for component specifications to display in list and detail views
 * Each component type has configurations for:
 * - keySpecs: Shown in the sidebar key specs panel (4-6 most important specs)
 * - fullSpecs: All specifications shown in the specifications tab
 */

// ANTENNAS
export const antennaKeySpecs = [
  {
    label: 'Center Frequency',
    path: 'center_frequency',
    icon: faBroadcastTower,
    unit: 'MHz'
  },
  {
    label: 'Gain',
    path: 'gain',
    icon: faSignal,
    unit: 'dBi'
  },
  {
    label: 'Polarization',
    path: 'type.polarization',
    icon: faSyncAlt
  },
  {
    label: 'Type',
    path: 'type.type',
    icon: faTags
  },
      {
    label: 'Bandwidth',
    path: 'bandwidth',
    icon: faArrowsAltH,
    // Special formatter to combine bandwidth_min and bandwidth_max
    formatter: (_, item) => `${item.bandwidth_min} - ${item.bandwidth_max} MHz`
  },
];

export const antennaSpecs = [
  ...antennaKeySpecs,

  {
    label: 'Direction',
    path: 'type.direction',
    icon: faCompass
  },
  {
    label: 'SWR',
    path: 'swr',
    icon: faWaveSquare
  },
  {
    label: 'Radiation Efficiency',
    path: 'radiation',
    icon: faChartPie,
    unit: '%'
  }
];

// CAMERAS
export const cameraKeySpecs = [
  {
    label: 'Resolution',
    path: 'tvl',
    icon: faCamera,
    unit: 'TVL'
  },
  {
    label: 'Voltage',
    path: 'voltage',
    icon: faBatteryFull,
    formatter: (_, item) => `${item.voltage_min} - ${item.voltage_max}V`
  },
  {
    label: 'FOV',
    path: 'fov',
    icon: faArrowsAltH,
    unit: '°'
  },
  {
    label: 'Aspect Ratio',
    path: 'ratio',
    icon: faRuler
  }
];

export const cameraSpecs = [
  ...cameraKeySpecs,
  {
    label: 'Output Type',
    path: 'output_type',
    icon: faPlug,
    formatter: (value) => value === 'A' ? 'Analog' : value === 'D' ? 'Digital' : value
  },
  {
    label: 'Light Sensitivity',
    path: 'light_sens',
    icon: faSignal
  },
  {
    label: 'Weight',
    path: 'weight',
    icon: faWeightHanging,
    unit: 'g'
  }
];

// MOTORS
export const motorKeySpecs = [
  {
    label: 'Size',
    path: 'stator_size',
    icon: faRuler,
    formatter: (_, item) => `${item.stator_diameter}${item.stator_height}`
  },
  {
    label: 'KV Rating',
    path: 'details.0.kv_per_volt',
    icon: faCog,
    unit: 'KV'
  },
  {
    label: 'Max Power',
    path: 'details.0.max_power',
    icon: faBatteryFull,
    unit: 'W'
  },
  {
    label: 'Weight',
    path: 'details.0.weight',
    icon: faWeightHanging,
    unit: 'g'
  }
];

export const motorSpecs = [
  ...motorKeySpecs,
  {
    label: 'Configuration',
    path: 'configuration',
    icon: faMicrochip
  },
  {
    label: 'Mounting',
    path: 'mount_dimensions',
    icon: faRuler,
    formatter: (_, item) => `${item.mount_width}x${item.mount_height} mm`
  },
  {
    label: 'Peak Current',
    path: 'details.0.peak_current',
    icon: faRocket,
    unit: 'A'
  }
];

// PROPELLERS
export const propellerKeySpecs = [
  {
    label: 'Size',
    path: 'size',
    icon: faRuler,
    unit: '"'
  },
  {
    label: 'Pitch',
    path: 'pitch',
    icon: faAngleUp,
    unit: '"'
  },
  {
    label: 'Blade Count',
    path: 'blade_count',
    icon: faFan
  },
  {
    label: 'Weight',
    path: 'weight',
    icon: faWeightHanging,
    unit: 'g'
  }
];

export const propellerSpecs = [
  ...propellerKeySpecs
];

// Export functions to get specs for a component type
export const getKeySpecsForComponentType = (type) => {
  const specsMap = {
    antennas: antennaKeySpecs,
    cameras: cameraKeySpecs,
    motors: motorKeySpecs,
    propellers: propellerKeySpecs,
    // Add more component types as needed
  };

  return specsMap[type] || [];
};

export const getFullSpecsForComponentType = (type) => {
  const specsMap = {
    antennas: antennaSpecs,
    cameras: cameraSpecs,
    motors: motorSpecs,
    propellers: propellerSpecs,
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