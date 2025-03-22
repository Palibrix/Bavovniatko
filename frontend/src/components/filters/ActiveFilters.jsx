import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';
import {getEntityThemeClass, themeClasses} from "../../utils/themeUtils";

/**
 * Component to display active filters with the ability to remove them
 *
 * @param {Object} props Component properties
 * @param {Array} props.filters Array of active filter data
 * @param {Function} props.onRemove Callback when a filter is removed
 * @param {string} props.componentType Theme color for styling
 */
const ActiveFilters = ({ filters = [], onRemove, componentType }) => {
    const themeClass = getEntityThemeClass(componentType)
  if (!filters || filters.length === 0) return null;

  // Group filters by their group title
  const groupedFilters = filters.reduce((acc, filter) => {
    const group = filter.group || 'Other';
    if (!acc[group]) acc[group] = [];
    acc[group].push(filter);
    return acc;
  }, {});

  // Handle filter removal click
  const handleRemoveClick = (filter) => {
    // For range filters, the value is an object with min/max
    if (typeof filter.value === 'object' && (filter.value.min !== undefined || filter.value.max !== undefined)) {
      // Pass the filter ID which is the base field name
      onRemove(filter.id, '');
    } else {
      // Pass both filter ID and value for choice filters
      onRemove(filter.id, filter.value);
    }
  };

  return (
    <div className="p-4 border-b border-gray-100">
      <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
        Active Filters
      </h3>

      {Object.entries(groupedFilters).map(([group, groupFilters]) => (
        <div key={group} className="mb-2 last:mb-0">
          <div className="text-xs text-gray-400 mb-1">{group}</div>
          <div className="flex flex-wrap gap-2">
            {groupFilters.map((filter, index) => (
              <div
                key={`${filter.id}-${index}`}
                className={`inline-flex items-center text-xs border ${themeClass.borderLight} rounded-full px-2.5 py-1 transition-colors`}
              >
                <span className="font-medium mr-1">{filter.label}:</span>
                <span>{filter.displayValue}</span>
                <button
                  onClick={() => handleRemoveClick(filter)}
                  className="ml-1.5 bg-white rounded-full w-4 h-4 flex items-center justify-center hover:bg-gray-100"
                  aria-label={`Remove ${filter.label} filter`}
                >
                  <FontAwesomeIcon
                    icon={faTimes}
                    className={`${themeClass.text} text-xs`}
                  />
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

ActiveFilters.propTypes = {
  filters: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      value: PropTypes.any.isRequired,
      label: PropTypes.string.isRequired,
      displayValue: PropTypes.string.isRequired,
      group: PropTypes.string
    })
  ),
  onRemove: PropTypes.func.isRequired,
  themeColor: PropTypes.string
};

export default ActiveFilters;