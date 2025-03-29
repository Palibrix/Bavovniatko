import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCog, faFan, faMicrochip, faTachometerAlt, faBroadcastTower,
  faBorderAll, faCamera, faSatelliteDish, faWifi, faChevronDown
} from '@fortawesome/free-solid-svg-icons';
import Dropdown, { DropdownSection } from '../common/Dropdown';
import { ROUTES } from '../../routes';

/**
 * Specialized dropdown for component categories in the header
 */
function ComponentsDropdown() {
  // Use location to determine active component
  const location = useLocation();
  const currentPath = location.pathname;

  // Custom trigger for the dropdown
  const dropdownTrigger = (
    <button className="text-light-text hover:text-secondary transition-colors flex items-center">
      Components
      <FontAwesomeIcon
        icon={faChevronDown}
        className="ml-2 text-xs"
      />
    </button>
  );

  // Component category definitions
  const categories = [
    {
      title: "Propulsion",
      items: [
        { name: "Motors", icon: faCog, type: "propulsion", path: ROUTES.COMPONENTS.MOTORS.LIST },
        { name: "Propellers", icon: faFan, type: "propulsion", path: ROUTES.COMPONENTS.PROPELLERS.LIST }
      ]
    },
    {
      title: "Control Systems",
      items: [
        { name: "Flight Controllers", icon: faMicrochip, type: "control", path: ROUTES.COMPONENTS.FLIGHT_CONTROLLERS.LIST },
        { name: "Speed Controllers", icon: faTachometerAlt, type: "control", path: ROUTES.COMPONENTS.SPEED_CONTROLLERS.LIST },
        { name: "Receivers", icon: faBroadcastTower, type: "control", path: ROUTES.COMPONENTS.RECEIVERS.LIST }
      ]
    },
    {
      title: "Structure & Communications",
      items: [
        { name: "Frames", icon: faBorderAll, type: "frame", path: ROUTES.COMPONENTS.FRAMES.LIST },
        { name: "Cameras", icon: faCamera, type: "video", path: ROUTES.COMPONENTS.CAMERAS.LIST },
        { name: "Transmitters", icon: faSatelliteDish, type: "video", path: ROUTES.COMPONENTS.TRANSMITTERS.LIST },
        { name: "Antennas", icon: faWifi, type: "antenna", path: ROUTES.COMPONENTS.ANTENNAS.LIST }
      ]
    }
  ];

  // Check if an item is active based on the current path
  const isItemActive = (path) => {
    if (path === "#") return false;
    return currentPath.startsWith(path);
  };

  return (
    <Dropdown trigger={dropdownTrigger} width="md">
      {categories.map((category, index) => (
        <DropdownSection key={index} title={category.title}>
          <div className="grid grid-cols-2 gap-2">
            {category.items.map((item, itemIndex) => (
              <ComponentMenuItem
                key={itemIndex}
                item={item}
                isActive={isItemActive(item.path)}
              />
            ))}
          </div>
        </DropdownSection>
      ))}
    </Dropdown>
  );
}

/**
 * Individual menu item for a component type
 */
function ComponentMenuItem({ item, isActive }) {
  // Get the appropriate color class based on component type
  const getIconBgColor = (type) => {
    const types = {
      propulsion: "bg-propulsion",
      control: "bg-control",
      frame: "bg-frame",
      video: "bg-video",
      antenna: "bg-antenna"
    };
    return types[type] || "bg-primary";
  };

  return (
    <Link
      to={item.path}
      className={`flex items-center p-2 rounded-md hover:bg-gray-100 w-full ${
        isActive ? `bg-gray-50` : 'text-gray-700'
      }`}
    >
      <div className={`w-8 h-8 min-w-[2rem] rounded-full flex justify-center items-center mr-3 text-white ${getIconBgColor(item.type)}`}>
        <FontAwesomeIcon icon={item.icon} className="text-sm" />
      </div>
      <span className={`text-sm font-medium ${isActive ? `text-${item.type} font-semibold` : ''}`}>
        {item.name}
        {isActive && <span className="ml-2 text-xs">•</span>}
      </span>
    </Link>
  );
}

export default ComponentsDropdown;