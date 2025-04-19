import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faList, faTh } from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';

/**
 * Mapping from singular component types (from API) to plural form (for frontend)
 */
const COMPONENT_TYPE_MAPPING = {
  'antenna': 'antennas',
  'camera': 'cameras',
  'frame': 'frames',
  'motor': 'motors',
  'propeller': 'propellers',
  'receiver': 'receivers',
  'transmitter': 'transmitters',
  'flight_controller': 'flight_controllers',
  'speed_controller': 'speed_controllers',
  'stack': 'stacks'
};

/**
 * Filter bar for component types in a list
 */
const ComponentTypeFilter = ({
  activeType,
  onTypeChange,
  viewMode,
  onViewModeChange,
  sortBy,
  onSortChange,
  totalCount,
  typeCounts
}) => {
  // Convert component type to the format used by the theme system
  const getThemeComponentType = (type) => {
    if (type === 'all') return 'primary';
    return COMPONENT_TYPE_MAPPING[type] || `${type}s`;
  };

  // Convert keys in typeCounts from singular to plural
  const getNormalizedTypeCounts = () => {
    const normalized = {};
    Object.entries(typeCounts || {}).forEach(([key, value]) => {
      // Handle both singular and plural keys in typeCounts
      if (key in COMPONENT_TYPE_MAPPING) {
        normalized[key] = value;
      } else if (key.endsWith('s')) {
        // If already plural, use as is
        normalized[key.slice(0, -1)] = value;
      } else {
        normalized[key] = value;
      }
    });
    return normalized;
  };
  // Component types with their display names
    const componentTypes = [
    { id: 'all', label: 'All' },
    { id: 'antenna', label: 'Antennas' },
    { id: 'camera', label: 'Cameras' },
    { id: 'frame', label: 'Frames' },
    { id: 'motor', label: 'Motors' },
    { id: 'propeller', label: 'Propellers' },
    { id: 'receiver', label: 'Receivers' },
    { id: 'flight_controller', label: 'Flight Controllers' },
    { id: 'speed_controller', label: 'Speed Controllers' },
    { id: 'transmitter', label: 'Transmitters' }
  ];

  // Sort options
  const sortOptions = [
    { value: 'name-asc', label: 'Name: A to Z' },
    { value: 'name-desc', label: 'Name: Z to A' },
    { value: 'newest', label: 'Newest first' },
    { value: 'oldest', label: 'Oldest first' }
  ];

  // Get the count for a component type
  const getTypeCount = (type) => {
    if (type === 'all') return totalCount;

    const normalizedCounts = getNormalizedTypeCounts();
    return normalizedCounts[type] || 0;
  };

  return (
    <div className="mb-6">
      {/* Component type filters */}
      <div className="mb-4 flex flex-wrap gap-2">
        {componentTypes.map(type => {
          // Get theme class based on component type
          const themeClass = getEntityThemeClass(getThemeComponentType(type.id));
          const count = getTypeCount(type.id);

          return (
            <button
              key={type.id}
              className={`px-4 py-2 rounded-full transition-colors flex items-center gap-2 ${
                activeType === type.id 
                  ? `${themeClass.bg} text-white` 
                  : `${themeClass.text} border ${themeClass.border} hover:bg-gray-50`
              }`}
              onClick={() => onTypeChange(type.id)}
            >
              {type.label}
              <span className={`text-xs px-2 py-0.5 rounded-full ${
                activeType === type.id
                  ? 'bg-white bg-opacity-20 text-white'
                  : 'bg-gray-100'
              }`}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* View and sort controls */}
      <div className="flex justify-between items-center bg-white rounded-lg shadow-sm p-4">
        <div className="text-sm text-gray-600">
          Showing <strong>{totalCount}</strong> components
        </div>

        <div className="flex items-center gap-4">
          {/* View mode toggle */}
          <div className="flex bg-gray-100 rounded-md overflow-hidden">
            <button
              onClick={() => onViewModeChange('list')}
              className={`flex items-center py-2 px-3 text-sm ${
                viewMode === 'list' 
                  ? 'bg-primary text-white' 
                  : 'text-gray-700 hover:bg-gray-200'
              }`}
            >
              <FontAwesomeIcon icon={faList} className="mr-2" />
              <span>List</span>
            </button>

            <button
              onClick={() => onViewModeChange('grid')}
              className={`flex items-center py-2 px-3 text-sm ${
                viewMode === 'grid' 
                  ? 'bg-primary text-white' 
                  : 'text-gray-700 hover:bg-gray-200'
              }`}
            >
              <FontAwesomeIcon icon={faTh} className="mr-2" />
              <span>Grid</span>
            </button>
          </div>

          {/* Sort options */}
          <select
            value={sortBy}
            onChange={(e) => onSortChange(e.target.value)}
            className="py-2 px-3 border border-gray-300 rounded-md text-sm text-gray-700 bg-white"
          >
            {sortOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

ComponentTypeFilter.propTypes = {
  activeType: PropTypes.string.isRequired,
  onTypeChange: PropTypes.func.isRequired,
  viewMode: PropTypes.oneOf(['list', 'grid']).isRequired,
  onViewModeChange: PropTypes.func.isRequired,
  sortBy: PropTypes.string.isRequired,
  onSortChange: PropTypes.func.isRequired,
  totalCount: PropTypes.number.isRequired,
  typeCounts: PropTypes.object
};

ComponentTypeFilter.defaultProps = {
  typeCounts: {}
};

export default ComponentTypeFilter;