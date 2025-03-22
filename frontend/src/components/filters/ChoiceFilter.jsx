import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import {themeClasses} from "../../utils/themeUtils";

/**
 * Checkbox-based filter with searchable options
 *
 * @param {Object} props Component properties
 * @param {Object} props.filter Filter configuration
 * @param {Array} props.activeValues Currently active values
 * @param {Function} props.onChange Callback when a value is selected
 * @param {Function} props.onRemove Callback when a value is removed
 * @param {string} props.themeColor Theme color for styling
 */
const ChoiceFilter = ({ filter, activeValues = [], onChange, onRemove, themeColor = 'primary' }) => {
  const themeClass = themeClasses[themeColor] || themeClasses.primary;
  const { id, label, field, options = [], searchable } = filter;
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredOptions, setFilteredOptions] = useState(options);

  // // Get base field name for comparison with active values
  // const baseFieldName = field.split('__').pop();
  //
  // // Special case for manufacturer
  // const isManufacturer = id === 'manufacturer';

  // Filter options when search term changes
  useEffect(() => {
    if (!searchTerm.trim()) {
      setFilteredOptions(options);
      return;
    }

    const lowercasedSearchTerm = searchTerm.toLowerCase();
    const filtered = options.filter(option =>
      option.display.toLowerCase().includes(lowercasedSearchTerm)
    );

    setFilteredOptions(filtered);
  }, [searchTerm, options]);

  // Handle checkbox change
  const handleCheckboxChange = (option) => {
    // Convert option value to string for consistent comparison
    const optionValueStr = option.value.toString();

    let activeValuesArray = [];

    if (Array.isArray(activeValues)) {
      activeValuesArray = activeValues;
    } else if (typeof activeValues === 'string' && activeValues.includes(',')) {
      // Handle comma-separated values from URL params
      activeValuesArray = activeValues.split(',');
    } else if (activeValues) {
      activeValuesArray = [activeValues];
    }
    // Check if this value is currently active
    const isActive = activeValuesArray.some(val => val?.toString() === optionValueStr);

    // Use the field ID from the filter definition (could be a nested path)
    if (isActive) {
      onRemove(optionValueStr);
    } else {
      onChange(optionValueStr);
    }
  };

  // Sort options by count (descending) and then alphabetically
  const sortedOptions = [...filteredOptions].sort((a, b) => {
    // First by count (higher first)
    if (b.count !== a.count) {
      return b.count - a.count;
    }
    // Then alphabetically
    return a.display.localeCompare(b.display);
  });

  // Limit initially shown options to avoid overwhelming users
  const maxVisibleOptions = 8;
  const [showAllOptions, setShowAllOptions] = useState(false);

  const visibleOptions = showAllOptions
    ? sortedOptions
    : sortedOptions.slice(0, maxVisibleOptions);

  const hasMoreOptions = sortedOptions.length > maxVisibleOptions;

  return (
    <div className="filter-option space-y-3">
      {/* Filter label */}
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>

      {/* Search box for searchable filters */}
      {searchable && (
        <div className="relative mb-3">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder={`Search ${label.toLowerCase()}...`}
            className="w-full pl-8 pr-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
          />
          <FontAwesomeIcon
            icon={faSearch}
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
          />
          {searchTerm && (
            <button
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              onClick={() => setSearchTerm('')}
            >
              ×
            </button>
          )}
        </div>
      )}

      {/* No options message */}
      {filteredOptions.length === 0 && (
        <div className="text-sm text-gray-500 italic">
          No options found{searchTerm ? ` for "${searchTerm}"` : ''}
        </div>
      )}

      {/* Checkbox list */}
      <div className={`space-y-2 ${options.length > 5 ? 'max-h-56 overflow-y-auto pr-2' : ''}`}>
        {visibleOptions.map(option => {
          // Convert option value to string for consistent comparison
          const optionValueStr = option.value.toString();

          let activeValuesArray = [];

          if (Array.isArray(activeValues)) {
            activeValuesArray = activeValues;
          } else if (typeof activeValues === 'string' && activeValues.includes(',')) {
            // Handle comma-separated values from URL params
            activeValuesArray = activeValues.split(',');
          } else if (activeValues) {
            activeValuesArray = [activeValues];
          }
          // Check if this value is selected
          const isChecked = activeValuesArray.some(val => val?.toString() === optionValueStr);

          return (
            <label
              key={optionValueStr}
              className="flex items-center cursor-pointer hover:bg-gray-50 p-1 rounded-md group"
            >
              <div className="relative flex items-center">
                <input
                  type="checkbox"
                  checked={isChecked}
                  onChange={() => handleCheckboxChange(option)}
                  className={`h-4 w-4 rounded border-gray-300 ${themeClass.text}`}
                />
                <span className="ml-2 text-sm text-gray-700 group-hover:text-gray-900">
                  {option.display}
                </span>
              </div>
              <span className="ml-auto text-xs px-1.5 py-0.5 bg-gray-100 text-gray-500 rounded">
                {option.count}
              </span>
            </label>
          );
        })}
      </div>

      {/* Show more/less button */}
      {hasMoreOptions && (
        <button
          className={`${themeClass.text} text-sm hover:underline mt-1 w-full text-left`}
          onClick={() => setShowAllOptions(!showAllOptions)}
        >
          {showAllOptions ? 'Show less' : `Show ${sortedOptions.length - maxVisibleOptions} more...`}
        </button>
      )}
    </div>
  );
};

ChoiceFilter.propTypes = {
  filter: PropTypes.shape({
    id: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    options: PropTypes.arrayOf(
      PropTypes.shape({
        value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
        display: PropTypes.string.isRequired,
        count: PropTypes.number.isRequired
      })
    ),
    searchable: PropTypes.bool
  }).isRequired,
  activeValues: PropTypes.array,
  onChange: PropTypes.func.isRequired,
  onRemove: PropTypes.func.isRequired,
  themeColor: PropTypes.string
};

export default ChoiceFilter;