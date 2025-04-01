import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faList, faTh, faSearch, faExclamationTriangle,
  faBorderAll, faCog, faFan, faMicrochip, faTachometerAlt,
  faBroadcastTower, faCamera, faSatelliteDish, faWifi, faBatteryFull
} from '@fortawesome/free-solid-svg-icons';
import { componentsApi } from '../../services/api';
import { getEntityThemeClass } from '../../utils/themeUtils';
import { getKeySpecsForComponentType } from '../../config/componentSpecs';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

// Universal component type mapping
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

// Non-component drone properties to filter out
const NON_COMPONENT_PROPERTIES = [
  'model', 'manufacturer', 'description', 'type', 'images', 'documents',
  'total_weight', 'flight_duration', 'max_speed', 'control_range', 'max_altitude'
];

/**
 * Middle panel for component selection in drone builder
 */
const ComponentSelectionPanel = ({
  selectedCategory,
  onSelectComponent,
  showBuildOverview,
  droneComponents,
  onBuildOverviewToggle,
  compatibilityIssues = [],
  missingComponents = [],
  completionPercentage
}) => {
  const [components, setComponents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [searchTerm, setSearchTerm] = useState('');
  const [showOnlyCompatible, setShowOnlyCompatible] = useState(true);

  // Get current component mapping
  const currentMapping = selectedCategory ? COMPONENT_MAPPING[selectedCategory] : null;
  const themeClass = currentMapping ? getEntityThemeClass(currentMapping.theme) : getEntityThemeClass('primary');

  // Fetch components for the selected category
  useEffect(() => {
    if (!selectedCategory || showBuildOverview) return;

    const fetchComponents = async () => {
      setLoading(true);
      setError(null);

      try {
        // Get the API type from the mapping
        const apiType = COMPONENT_MAPPING[selectedCategory].theme;

        // Fetch components from API
        const result = await componentsApi.getComponentList(apiType);
        setComponents(result.results || result);
      } catch (err) {
        console.error(`Error fetching ${selectedCategory}:`, err);
        setError(`Failed to load components. Please try again.`);
      } finally {
        setLoading(false);
      }
    };

    fetchComponents();
  }, [selectedCategory, showBuildOverview]);

  // Filter components based on search term and compatibility
  const filteredComponents = components.filter(component => {
    // Search filter
    const searchMatches = !searchTerm ||
      `${component.manufacturer || ''} ${component.model || ''}`.toLowerCase().includes(searchTerm.toLowerCase());

    // Compatibility filter - placeholder for now
    const compatibilityMatches = !showOnlyCompatible || true;

    return searchMatches && compatibilityMatches;
  });

  // Reset search when switching categories
  useEffect(() => {
    setSearchTerm('');
  }, [selectedCategory]);

  // Handle adding a component to the drone
  const handleComponentAdd = (component) => {
    if (!currentMapping) return;
    onSelectComponent(component, selectedCategory);
  };

  // If in build overview mode, render the overview panel
  if (showBuildOverview) {
    return (
      <div className="flex-1 bg-white rounded-3xl shadow-sm overflow-hidden flex flex-col">
        <div className="py-4 px-6 border-b border-gray-100 font-semibold text-primary flex justify-between items-center">
          <span>Build Overview</span>
          <button
            className="text-sm px-3 py-1.5 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
            onClick={() => onBuildOverviewToggle()}
          >
            Select Components
          </button>
        </div>

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
                        {/* Use getKeySpecsForComponentType for specs display */}
                        {getComponentShortSummary(component, key)}
                      </div>
                    </div>
                  </div>
                );
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
                          onClick={() => onBuildOverviewToggle(categoryKey)}
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
      </div>
    );
  }

  // Otherwise, render the component selection panel
  return (
    <div className="flex-1 bg-white rounded-3xl shadow-sm overflow-hidden flex flex-col">
      <div className="py-4 px-6 border-b border-gray-100 font-semibold text-primary flex justify-between items-center">
        <span>Select {currentMapping?.displayName || 'Component'}</span>
        <button
          className="text-sm px-3 py-1.5 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
          onClick={() => onBuildOverviewToggle()}
        >
          Build Overview
        </button>
      </div>

      {/* Filter and view controls */}
      <div className="filter-controls p-4 border-b border-gray-100 flex justify-between items-center">
        <div className="view-toggle flex bg-gray-100 rounded-lg overflow-hidden">
          <button
            className={`px-3 py-2 flex items-center gap-1.5 ${viewMode === 'list' ? `${themeClass.bg} text-white` : ''}`}
            onClick={() => setViewMode('list')}
          >
            <FontAwesomeIcon icon={faList} />
            List
          </button>
          <button
            className={`px-3 py-2 flex items-center gap-1.5 ${viewMode === 'grid' ? `${themeClass.bg} text-white` : ''}`}
            onClick={() => setViewMode('grid')}
          >
            <FontAwesomeIcon icon={faTh} />
            Grid
          </button>
        </div>

        <div className="filter-group flex items-center gap-2">
          {/* Search */}
          <div className="relative">
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-4 py-2 w-64 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
            />
            <FontAwesomeIcon icon={faSearch} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            {searchTerm && (
              <button
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                onClick={() => setSearchTerm('')}
              >
                ×
              </button>
            )}
          </div>

          {/* Compatibility toggle - placeholder for now */}
          <label className="flex items-center gap-2 border border-gray-200 px-3 py-2 rounded-lg cursor-pointer">
            <input
              type="checkbox"
              checked={showOnlyCompatible}
              onChange={(e) => setShowOnlyCompatible(e.target.checked)}
              className={`form-checkbox h-4 w-4 ${themeClass.text}`}
            />
            <span className="text-sm">Show only compatible</span>
          </label>
        </div>
      </div>

      {/* Component list/grid */}
      <div className={`flex-1 overflow-y-auto p-4 ${viewMode === 'grid' ? 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4' : 'flex flex-col gap-3'}`}>
        {loading && <LoadingSpinner />}

        {error && <ErrorMessage message={error} onRetry={() => setLoading(false)} />}

        {!loading && !error && filteredComponents.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            {searchTerm ? `No ${currentMapping?.displayName} found matching "${searchTerm}"` : `No ${currentMapping?.displayName} available`}
          </div>
        )}

        {!loading && !error && filteredComponents.map(component => {
          // Determine if component is compatible (placeholder)
          const isCompatible = true; // Will implement real compatibility later

          if (viewMode === 'grid') {
            // Grid view
            return (
              <div
                key={component.id}
                className={`border rounded-xl transition-all hover:-translate-y-1 hover:shadow-md ${
                  !isCompatible ? 'opacity-60' : ''
                }`}
              >
                {!isCompatible && (
                  <div className="absolute top-2 right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-white text-xs">
                    <FontAwesomeIcon icon={faExclamationTriangle} />
                  </div>
                )}

                <div className="p-3 bg-gray-50 border-b">
                  <h3 className="font-medium mb-1">{component.model}</h3>
                  <div className="text-sm text-gray-500">{component.manufacturer}</div>
                </div>

                <div className="p-3">
                  {renderComponentSpecsInCard(component, selectedCategory)}
                </div>

                <div className="p-3 bg-gray-50 border-t flex justify-between items-center">
                  <button className="text-sm text-gray-500 hover:text-primary">Details</button>
                  <button
                    className={`${themeClass.text} font-medium text-sm hover:underline`}
                    onClick={() => handleComponentAdd(component)}
                  >
                    Add
                  </button>
                </div>
              </div>
            );
          } else {
            // List view
            return (
              <div
                key={component.id}
                className={`flex border rounded-xl overflow-hidden transition-all hover:-translate-y-1 hover:shadow-md ${
                  !isCompatible ? 'opacity-60' : ''
                }`}
              >
                {!isCompatible && (
                  <div className="absolute top-2 right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-white text-xs">
                    <FontAwesomeIcon icon={faExclamationTriangle} />
                  </div>
                )}

                <div className={`w-16 ${themeClass.bg} flex items-center justify-center text-white font-bold text-2xl`}>
                  <FontAwesomeIcon icon={currentMapping?.icon || faCog} />
                </div>

                <div className="flex-1 p-3">
                  <h3 className="font-medium">{component.model}</h3>
                  <div className="text-sm text-gray-500 mb-2">{component.manufacturer}</div>

                  <div className="grid grid-cols-2 gap-x-8 gap-y-1">
                    {renderComponentSpecsInList(component, selectedCategory)}
                  </div>
                </div>

                <div className="w-24 flex items-center justify-center border-l">
                  <button
                    className={`${themeClass.bg} text-white px-3 py-1.5 rounded-lg hover:opacity-90 transition-opacity`}
                    onClick={() => handleComponentAdd(component)}
                  >
                    Add
                  </button>
                </div>
              </div>
            );
          }
        })}
      </div>
    </div>
  );
};

// Helper function to render component specs in a card
function renderComponentSpecsInCard(component, categoryType) {
  // Use existing spec configurations from config/componentSpecs
  const specs = getKeySpecsForComponentType(categoryType === 'antennas_receiver' ||
                                          categoryType === 'antennas_transmitter' ?
                                          'antennas' : categoryType);

  // Show the first 3 specs
  const displaySpecs = specs.slice(0, 3);

  return displaySpecs.map((spec, index) => {
    const value = extractSpecValue(component, spec);

    return (
      <div key={index} className="flex justify-between text-sm mb-1.5">
        <span className="text-gray-500">{spec.label}</span>
        <span className="font-medium">{value}</span>
      </div>
    );
  });
}

// Helper function to render component specs in list view
function renderComponentSpecsInList(component, categoryType) {
  // Use existing spec configurations from config/componentSpecs
  const specs = getKeySpecsForComponentType(categoryType === 'antennas_receiver' ||
                                          categoryType === 'antennas_transmitter' ?
                                          'antennas' : categoryType);

  // Show up to 6 specs in the list view
  const displaySpecs = specs.slice(0, 6);

  return displaySpecs.map((spec, index) => {
    const value = extractSpecValue(component, spec);

    return (
      <div key={index} className="flex justify-between text-sm">
        <span className="text-gray-500 mr-2">{spec.label}:</span>
        <span className="font-medium">{value}</span>
      </div>
    );
  });
}

// Helper function to extract spec value using spec configuration
function extractSpecValue(component, spec) {
  // Extract value using path
  let value = null;

  try {
    value = spec.path.split('.').reduce((obj, key) =>
      obj && obj[key] !== undefined ? obj[key] : null, component);

    // Format the value
    if (spec.formatter) {
      return spec.formatter(value, component);
    } else if (spec.unit && value !== null) {
      return `${value} ${spec.unit}`;
    } else if (value !== null) {
      return value.toString();
    }
  } catch (error) {
    // If there's an error extracting the value, return N/A
    console.error(`Error extracting spec value: ${error.message}`);
  }

  return 'N/A';
}

// Helper function to generate a short summary for component cards
function getComponentShortSummary(component, componentKey) {
  let categoryType = Object.keys(COMPONENT_MAPPING).find(
    key => COMPONENT_MAPPING[key].droneProperty === componentKey
  );

  if (!categoryType) return '';

  // Special handling for antennas
  if (categoryType.startsWith('antennas_')) {
    categoryType = 'antennas';
  }

  // Generate a summary based on component type
  switch (categoryType) {
    case 'frames':
      return `${component.material || ''}, ${component.weight || 0}g`;
    case 'motors':
      if (component.details && component.details.length > 0) {
        return `${component.details[0].kv_per_volt || 0} KV, ${component.stator_diameter || ''}${component.stator_height || ''}`;
      }
      return `${component.stator_diameter || ''}${component.stator_height || ''}`;
    case 'cameras':
      return `${component.tvl || 0} TVL, ${component.fov || 0}° FOV`;
    case 'propellers':
      return `${component.size || 0}×${component.pitch || 0}, ${component.blade_count || 2} blades`;
    case 'flight_controllers':
      return `${component.microcontroller || ''}, ${component.gyro?.imu || 'N/A'}`;
    case 'speed_controllers':
      return `${component.cont_current || 0}A, ${component.esc_type === 'all' ? '4-in-1' : 'Single'}`;
    case 'receivers':
      const protocols = component.protocols?.map(p => p.type).join(', ') || 'N/A';
      return protocols;
    case 'transmitters':
      return `${component.max_power || 0}mW, ${component.channels_quantity || 0}ch`;
    case 'antennas':
      return `${component.center_frequency || 0}MHz, ${component.type?.type || 'N/A'}`;
    default:
      return '';
  }
}

ComponentSelectionPanel.propTypes = {
  selectedCategory: PropTypes.string,
  onSelectComponent: PropTypes.func.isRequired,
  showBuildOverview: PropTypes.bool.isRequired,
  droneComponents: PropTypes.object.isRequired,
  onBuildOverviewToggle: PropTypes.func.isRequired,
  compatibilityIssues: PropTypes.array,
  missingComponents: PropTypes.array,
  completionPercentage: PropTypes.number.isRequired
};

export default ComponentSelectionPanel;