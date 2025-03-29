import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBorderAll, faCog, faFan, faMicrochip, faTachometerAlt,
  faBroadcastTower, faCamera, faSatelliteDish, faWifi, faBatteryFull,
  faCheckCircle, faTimesCircle
} from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';

/**
 * Mapping of component types to their category and icon
 */
const COMPONENT_CONFIG = {
  frame: { category: 'frames', icon: faBorderAll, label: 'Frame' },
  motor: { category: 'motors', icon: faCog, label: 'Motors' },
  propeller: { category: 'propellers', icon: faFan, label: 'Propellers' },
  flight_controller: { category: 'flight_controllers', icon: faMicrochip, label: 'Flight Controller' },
  speed_controller: { category: 'speed_controllers', icon: faTachometerAlt, label: 'ESC' },
  receiver: { category: 'receivers', icon: faBroadcastTower, label: 'Receiver' },
  camera: { category: 'cameras', icon: faCamera, label: 'Camera' },
  transmitter: { category: 'transmitters', icon: faSatelliteDish, label: 'Video Transmitter' },
  antenna_receiver: { category: 'antennas', icon: faWifi, label: 'Receiver Antenna' },
  antenna_transmitter: { category: 'antennas', icon: faWifi, label: 'Transmitter Antenna' },
  battery: { category: 'propulsion', icon: faBatteryFull, label: 'Battery' }
};

/**
 * Component grid for displaying drone components
 *
 * @param {Object} props Component properties
 * @param {Object} props.item The drone data
 * @param {string} props.selectedComponent Currently selected component key
 * @param {Function} props.onSelectComponent Callback when component is selected
 */
const ComponentGrid = ({ item, selectedComponent, onSelectComponent }) => {
  const componentKeys = Object.keys(COMPONENT_CONFIG);

  // Debug the theme classes
  React.useEffect(() => {
    console.log("Theme classes in ComponentGrid:",
      Object.fromEntries(
        componentKeys.map(key => [
          key,
          getEntityThemeClass(COMPONENT_CONFIG[key].category)
        ])
      )
    );
  }, []);

  return (
    <div className="bg-white rounded-3xl shadow-sm overflow-hidden mb-6">
      <div className="py-4 px-6 border-b border-gray-100 font-semibold text-primary">
        Components
      </div>
      <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-4 max-h-96 overflow-y-auto">
        {componentKeys.map(key => {
          const config = COMPONENT_CONFIG[key];
          const component = item[key];
          const isInstalled = !!component;
          const isSelected = selectedComponent === key;

          // Get the theme class for this component category
          const themeClass = getEntityThemeClass(config.category);

          return (
            <div
              key={key}
              className={`flex flex-col p-5 bg-gray-50 rounded-xl cursor-pointer transition-all hover:-translate-y-1 border-l-4 ${
                isSelected ? `${themeClass.border} bg-gray-100` : 'border-transparent'
              } ${isInstalled ? '' : 'opacity-70'}`}
              onClick={() => onSelectComponent(key)}
            >
              <div className="flex items-center mb-3">
                <div className={`w-12 h-12 min-w-[3rem] rounded-full ${themeClass.bg} text-white flex items-center justify-center mr-4`}>
                  <FontAwesomeIcon icon={config.icon} size="lg" />
                </div>
                <div>
                  <div className="font-medium text-primary text-lg">{config.label}</div>
                  <div className="text-sm text-gray-600 mt-1">
                    {isInstalled ? `${component.manufacturer || ''} ${component.model}`.trim() : 'Not Installed'}
                  </div>
                </div>
              </div>
              <div className={`text-xs flex items-center mt-2 ${isInstalled ? 'text-green-600' : 'text-red-500'}`}>
                <FontAwesomeIcon icon={isInstalled ? faCheckCircle : faTimesCircle} className="mr-1" />
                {isInstalled ? 'Installed' : 'Missing'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

ComponentGrid.propTypes = {
  item: PropTypes.object.isRequired,
  selectedComponent: PropTypes.string,
  onSelectComponent: PropTypes.func.isRequired
};

export default ComponentGrid;