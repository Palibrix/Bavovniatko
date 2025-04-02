import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBorderAll, faCog, faFan, faMicrochip, faTachometerAlt,
  faBroadcastTower, faCamera, faSatelliteDish, faWifi, faBatteryFull
} from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';
import { componentsApi } from '../../services/api';
import ComponentList from './ComponentList';
import BuildOverview from './BuildOverview';

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

    // Handle component selection
  const handleComponentSelect = (component) => {
    if (!currentMapping) return;
    onSelectComponent(component, selectedCategory);
  };

  // Handle component removal
  const handleComponentRemove = (componentKey) => {
    onSelectComponent(null, null, componentKey);
  };

  return (
    <div className="flex-1 bg-white rounded-3xl shadow-sm overflow-hidden flex flex-col">
      <div className="py-4 px-6 border-b border-gray-100 font-semibold text-primary flex justify-between items-center">
        <span>{showBuildOverview ? 'Build Overview' : `Select ${currentMapping?.displayName || 'Component'}`}</span>
        <button
          className="text-sm px-3 py-1.5 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
          onClick={() => onBuildOverviewToggle()}
        >
          {showBuildOverview ? 'Select Components' : 'Build Overview'}
        </button>
      </div>

      {showBuildOverview ? (
        <BuildOverview
          droneComponents={droneComponents}
          compatibilityIssues={compatibilityIssues}
          missingComponents={missingComponents}
          onComponentAdd={onBuildOverviewToggle}
          onComponentRemove={handleComponentRemove}
        />
      ) : (
        <ComponentList
          components={components}
          loading={loading}
          error={error}
          selectedCategory={selectedCategory}
          onSelectComponent={handleComponentSelect}
          showOnlyCompatible={showOnlyCompatible}
          setShowOnlyCompatible={setShowOnlyCompatible}
        />
      )}
    </div>
  );
};

// Component mapping
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