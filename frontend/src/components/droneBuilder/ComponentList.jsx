import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faList, faTh, faSearch, faBorderAll, faCog, faFan,
  faMicrochip, faTachometerAlt, faBroadcastTower, faCamera,
  faSatelliteDish, faWifi, faBatteryFull
} from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';
import ComponentCard from './ComponentCard';
import ComponentListItem from './ComponentListItem';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

/**
 * Component list with grid/list view toggle and search
 */
const ComponentList = ({
  components,
  loading,
  error,
  selectedCategory,
  onSelectComponent,
  showOnlyCompatible,
  setShowOnlyCompatible,
  gridColumns = 3,
  droneComponents,
  componentCompatibility
}) => {
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [searchTerm, setSearchTerm] = useState('');

  // Get current component mapping
  const currentMapping = selectedCategory ? COMPONENT_MAPPING[selectedCategory] : null;
  const themeClass = currentMapping ? getEntityThemeClass(currentMapping.theme) : getEntityThemeClass('primary');

  // Determine if a component is compatible with current configuration
  const isComponentCompatible = (component) => {
    // If component has compatibility info from API
    if (component.compatibility) {
      return component.compatibility.is_compatible;
    }

    // Without direct compatibility info, check if there are issues involving this component type
    if (!componentCompatibility) return true;

    // For camera-frame compatibility (current focus)
    const pairKeys = Object.keys(componentCompatibility);

    // For the component type we're currently viewing
    if (selectedCategory === 'cameras' && droneComponents.frame) {
      // Check camera_frame compatibility
      return componentCompatibility['camera_frame']?.is_compatible !== false;
    }

    if (selectedCategory === 'frames' && droneComponents.camera) {
      // Check camera_frame compatibility
      return componentCompatibility['camera_frame']?.is_compatible !== false;
    }

    // By default, assume compatible
    return true;
  };

  // Filter components based on search term and compatibility
  const filteredComponents = components.filter(component => {
    // Search filter
    const searchMatches = !searchTerm ||
      `${component.manufacturer || ''} ${component.model || ''}`.toLowerCase().includes(searchTerm.toLowerCase());

    // Compatibility filter - only apply if checkbox is checked
    const compatibilityMatches = !showOnlyCompatible || isComponentCompatible(component);

    return searchMatches && compatibilityMatches;
  });

  // Get grid classes based on column count
  const getGridClasses = () => {
    if (viewMode !== 'grid') return 'flex flex-col gap-3';

    return gridColumns === 2
      ? 'grid grid-cols-1 sm:grid-cols-2 gap-4'
      : 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4';
  };

  return (
    <>
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
      <div className={`flex-1 overflow-y-auto p-4 ${getGridClasses()}`}>
        {loading && <LoadingSpinner />}

        {error && <ErrorMessage message={error} />}

        {!loading && !error && filteredComponents.length === 0 && (
          <div className="text-center text-gray-500 py-8 col-span-full">
            {searchTerm ? `No ${currentMapping?.displayName} found matching "${searchTerm}"` : `No ${currentMapping?.displayName} available`}
          </div>
        )}

                {!loading && !error && filteredComponents.map(component => {
          // Determine if component is compatible
          const isCompatible = isComponentCompatible(component);

          return viewMode === 'grid' ? (
            <ComponentCard
              key={component.id}
              component={component}
              categoryType={selectedCategory}
              isCompatible={isCompatible}
              themeClass={themeClass}
              onSelect={() => onSelectComponent(component, selectedCategory)}
              compatibilityIssues={component.compatibility?.issues || []}
            />
          ) : (
            <ComponentListItem
              key={component.id}
              component={component}
              categoryType={selectedCategory}
              isCompatible={isCompatible}
              themeClass={themeClass}
              currentMapping={currentMapping}
              onSelect={() => onSelectComponent(component, selectedCategory)}
              compatibilityIssues={component.compatibility?.issues || []}
            />
          );
        })}
      </div>
    </>
  );
};

// Mapping of component types to display properties
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

ComponentList.propTypes = {
  components: PropTypes.array.isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.string,
  selectedCategory: PropTypes.string.isRequired,
  onSelectComponent: PropTypes.func.isRequired,
  showOnlyCompatible: PropTypes.bool.isRequired,
  setShowOnlyCompatible: PropTypes.func.isRequired,
  gridColumns: PropTypes.number,
  droneComponents: PropTypes.object,
  componentCompatibility: PropTypes.object
};

export default ComponentList;