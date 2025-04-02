import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faExclamationTriangle, faBorderAll, faCog, faFan, faMicrochip, faTachometerAlt,
  faBroadcastTower, faCamera, faSatelliteDish, faWifi, faBatteryFull, faTrash
} from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';
import { getKeySpecsForComponentType } from '../../config/componentSpecs';

// Non-component drone properties to filter out
const NON_COMPONENT_PROPERTIES = [
  'model', 'manufacturer', 'description', 'type', 'images', 'documents',
  'total_weight', 'flight_duration', 'max_speed', 'control_range', 'max_altitude'
];

/**
 * Component mapping for category, icon, and drone property
 */
const COMPONENT_MAPPING = {
  frames: {
    displayName: 'Frame',
    icon: faBorderAll,
    theme: 'frames',
    droneProperty: 'frame'
  },
  motors: {
    displayName: 'Motors',
    icon: faCog,
    theme: 'motors',
    droneProperty: 'motor'
  },
  propellers: {
    displayName: 'Propellers',
    icon: faFan,
    theme: 'propellers',
    droneProperty: 'propeller'
  },
  batteries: {
    displayName: 'Battery',
    icon: faBatteryFull,
    theme: 'batteries',
    droneProperty: 'battery'
  },
  flight_controllers: {
    displayName: 'Flight Controller',
    icon: faMicrochip,
    theme: 'flight_controllers',
    droneProperty: 'flight_controller'
  },
  speed_controllers: {
    displayName: 'Speed Controller',
    icon: faTachometerAlt,
    theme: 'speed_controllers',
    droneProperty: 'speed_controller'
  },
  receivers: {
    displayName: 'Receiver',
    icon: faBroadcastTower,
    theme: 'receivers',
    droneProperty: 'receiver'
  },
  cameras: {
    displayName: 'Camera',
    icon: faCamera,
    theme: 'cameras',
    droneProperty: 'camera'
  },
  transmitters: {
    displayName: 'Video Transmitter',
    icon: faSatelliteDish,
    theme: 'transmitters',
    droneProperty: 'transmitter'
  },
  antennas_receiver: {
    displayName: 'Receiver Antenna',
    icon: faWifi,
    theme: 'antennas',
    droneProperty: 'antenna_receiver'
  },
  antennas_transmitter: {
    displayName: 'Transmitter Antenna',
    icon: faWifi,
    theme: 'antennas',
    droneProperty: 'antenna_transmitter'
  }
};

/**
 * Build overview component for showing selected components
 */
const BuildOverview = ({
  droneComponents,
  compatibilityIssues = [],
  missingComponents = [],
  onComponentAdd,
  onComponentRemove
}) => {
  return (
    <>
      <div className="p-6 overflow-y-auto flex-1">
        {/* Compatibility issues section */}
        {compatibilityIssues.length > 0 && (
          <div className="build-issues mb-5 border border-red-200 rounded-lg overflow-hidden">
            <div className="issues-header bg-red-100 p-3 flex justify-between items-center">
              <div className="issues-title text-red-800 font-semibold flex items-center gap-2">
                <FontAwesomeIcon icon={faExclamationTriangle} />
                Compatibility Issues
              </div>
              <div className="issues-count text-xs text-red-800">
                {compatibilityIssues.length} issue{compatibilityIssues.length !== 1 ? 's' : ''} found
              </div>
            </div>

            <div className="issues-list p-4">
              <div className="text-gray-500 italic">
                Compatibility checking will be implemented in the next stage.
              </div>
            </div>
          </div>
        )}

        {/* Selected components section */}
        <div className="components-summary mb-5 border border-gray-200 rounded-lg overflow-hidden">
          <div className="summary-header bg-gray-50 p-3 font-semibold text-primary border-b border-gray-200">
            Selected Components
          </div>

          <div className="summary-cards p-2">
            {Object.entries(droneComponents).map(([key, component]) => {
              // Skip non-component properties
              if (!component || typeof component !== 'object' || NON_COMPONENT_PROPERTIES.includes(key)) {
                return null;
              }

              // Find the mapping for this component type
              const mapping = Object.values(COMPONENT_MAPPING).find(m => m.droneProperty === key);
              if (!mapping) return null;

              const componentTheme = getEntityThemeClass(mapping.theme);

              return (
                <div key={key} className="summary-card flex items-center p-3 border-b border-gray-100 last:border-0">
                  <div className={`summary-icon w-10 h-10 rounded-full ${componentTheme.bg} text-white flex items-center justify-center font-semibold mr-3`}>
                    <FontAwesomeIcon icon={mapping.icon} />
                  </div>
                  <div className="summary-content flex-1">
                    <div className="summary-title font-medium">
                      {component.manufacturer ? `${component.manufacturer} ${component.model}` : component.model ? component.model : mapping.displayName}
                    </div>
                    <div className="summary-details text-xs text-gray-500 mt-1">
                      {getComponentShortSummary(component, key)}
                    </div>
                  </div>
                  <button
                    className="text-red-500 hover:text-red-700 ml-2"
                    onClick={() => onComponentRemove(key)}
                    title={`Remove ${mapping.displayName}`}
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                </div>
              );

              // return (
              //   <div key={key} className="summary-card flex items-center p-3 border-b border-gray-100 last:border-0">
              //     <div className={`summary-icon w-10 h-10 rounded-full ${componentTheme.bg} text-white flex items-center justify-center font-semibold mr-3`}>
              //       <FontAwesomeIcon icon={mapping.icon} />
              //     </div>
              //     <div className="summary-content flex-1">
              //       <div className="summary-title font-medium">
              //         {component.manufacturer ? `${component.manufacturer} ${component.model}` : component.model ? component.model : mapping.displayName}
              //       </div>
              //       <div className="summary-details text-xs text-gray-500 mt-1">
              //         {getComponentShortSummary(component, key)}
              //       </div>
              //     </div>
              //   </div>
              // );
            })}

            {Object.values(droneComponents).filter(component =>
              component && typeof component === 'object' &&
              !NON_COMPONENT_PROPERTIES.includes(Object.keys(component)[0])
            ).length === 0 && (
              <div className="p-4 text-gray-500 italic text-center">
                No components selected yet
              </div>
            )}
          </div>
        </div>

        {/* Missing components section */}
        {missingComponents.length > 0 && (
          <div className="missing-components border border-gray-200 rounded-lg overflow-hidden">
            <div className="missing-header bg-gray-50 p-3 font-semibold text-primary border-b border-gray-200">
              Missing Components
            </div>

            <div className="missing-list p-2">
              {missingComponents.map(component => {
                // Find this component in the mapping
                const categoryKey = Object.keys(COMPONENT_MAPPING).find(
                  key => COMPONENT_MAPPING[key].droneProperty === component
                );

                if (!categoryKey) return null;

                const mapping = COMPONENT_MAPPING[categoryKey];
                const componentTheme = getEntityThemeClass(mapping.theme);

                return (
                  <div key={component} className="missing-item flex items-center p-3 border-b border-gray-100 last:border-0">
                    <div className={`missing-icon w-10 h-10 rounded-full ${componentTheme.bg} text-white flex items-center justify-center font-semibold mr-3`}>
                      <FontAwesomeIcon icon={mapping.icon} />
                    </div>
                    <div className="missing-content flex-1 flex justify-between items-center">
                      <div className="missing-title font-medium">{mapping.displayName}</div>
                      <button
                        className={`${componentTheme.bg} text-white text-xs px-3 py-1.5 rounded hover:opacity-90 transition-opacity`}
                        onClick={() => onComponentAdd(categoryKey)}
                      >
                        Add
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </>
  );
};

// Helper function to generate a short summary for component cards using key specs
function getComponentShortSummary(component, componentKey) {
  let categoryType = Object.keys(COMPONENT_MAPPING).find(
    key => COMPONENT_MAPPING[key].droneProperty === componentKey
  );

  if (!categoryType) return '';

  // Special handling for antennas
  if (categoryType.startsWith('antennas_')) {
    categoryType = 'antennas';
  }

  // Get key specs for this component type
  const specs = getKeySpecsForComponentType(categoryType);
  if (!specs || specs.length === 0) return '';

  // Only use the first 2-3 specs for the summary
  const displaySpecs = specs.slice(0, 6);

  // Extract and format values
  const summaryParts = displaySpecs.map(spec => {
    let value = null;

    try {
      // Extract value using the path
      value = spec.path.split('.').reduce((obj, key) =>
        obj && obj[key] !== undefined ? obj[key] : null, component);

      // Format value
      if (value === null || value === undefined) return null;

      if (spec.formatter) {
        return spec.formatter(value, component);
      } else if (spec.unit) {
        return `${value}${spec.unit}`;
      } else {
        return value.toString();
      }
    } catch (error) {
      return null;
    }
  }).filter(Boolean); // Remove nulls

  return summaryParts.join(', ');
}

BuildOverview.propTypes = {
  droneComponents: PropTypes.object.isRequired,
  compatibilityIssues: PropTypes.array,
  missingComponents: PropTypes.array,
  onComponentAdd: PropTypes.func.isRequired,
  onComponentRemove: PropTypes.func.isRequired
};

export default BuildOverview;