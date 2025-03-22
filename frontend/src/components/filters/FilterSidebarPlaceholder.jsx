import React from 'react';
import PropTypes from 'prop-types';
import {themeClasses} from "../../utils/themeUtils";

/**
 * Placeholder component for the filter sidebar
 * This will be replaced with a real implementation later
 *
 * @param {Object} props Component properties
 * @param {string} props.componentType Type of component for theming
 */
const FilterSidebarPlaceholder = ({ componentType = 'antennas' }) => {
  // Get the theme color based on component type
  const getThemeColor = () => {
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
      speed_controllers: 'control',
      drones: 'drones'
    };

    return themes[componentType] || 'primary';
  };

  const themeColor = getThemeColor();
  const themeClass = themeClasses[themeColor] || themeClasses.primary;

  return (
    <div className="w-full bg-white rounded-lg shadow-sm overflow-hidden">
      <div className="p-5 flex justify-between items-center border-b border-gray-100 bg-gray-50">
        <h2 className={`text-lg font-semibold ${themeClass.text}`}>Filters</h2>
        <button
          className={`${themeClass.text} text-sm px-2 py-1 rounded-md hover:bg-gray-100`}
        >
          Clear All
        </button>
      </div>

      <div className="p-5 border-b border-gray-100">
        <div className="bg-gray-100 animate-pulse h-6 w-1/3 rounded mb-3"></div>
        <div className="bg-gray-100 animate-pulse h-10 w-full rounded mb-4"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-3/4 rounded mb-2"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-2/3 rounded mb-2"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-1/2 rounded"></div>
      </div>

      <div className="p-5 border-b border-gray-100">
        <div className="bg-gray-100 animate-pulse h-6 w-1/2 rounded mb-3"></div>
        <div className="bg-gray-100 animate-pulse h-20 w-full rounded mb-4"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-full rounded mb-2"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-full rounded"></div>
      </div>

      <div className="p-5">
        <div className="bg-gray-100 animate-pulse h-6 w-2/5 rounded mb-3"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-2/3 rounded mb-2"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-1/2 rounded mb-2"></div>
        <div className="bg-gray-100 animate-pulse h-4 w-3/4 rounded"></div>
      </div>

      <div className="p-4 bg-gray-50 border-t border-gray-100 text-center">
        <div className={`text-xs ${themeClass.text}`}>
          Filter functionality coming soon
        </div>
      </div>
    </div>
  );
};

FilterSidebarPlaceholder.propTypes = {
  componentType: PropTypes.string
};

export default FilterSidebarPlaceholder;