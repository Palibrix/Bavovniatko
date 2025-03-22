import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useSearchParams } from 'react-router-dom';
import { componentsApi } from '../../services/api';
import FilterGroup from './FilterGroup';
import ChoiceFilter from './ChoiceFilter';
import RangeFilter from './RangeFilter';
import ActiveFilters from './ActiveFilters';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import {getEntityThemeClass} from '../../utils/themeUtils';

/**
 * Main filter sidebar component that fetches filter options from API
 * and renders filter groups based on the metadata
 *
 * @param {Object} props Component properties
 * @param {string} props.componentType Type of component for themed styling
 */
const FilterSidebar = ({ componentType}) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [filterMetadata, setFilterMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeFilters, setActiveFilters] = useState({});

  const themeClass = getEntityThemeClass(componentType);
  // Initialize active filters from URL params on mount
useEffect(() => {
  const initialFilters = {};

  searchParams.forEach((value, key) => {
    // Skip pagination and sorting params
    if (key !== 'page' && key !== 'sort') {
      // Handle comma-separated values - must do this first!
      if (value.includes(',')) {
        initialFilters[key] = value.split(',');
      }
      // Single value case
      else if (!initialFilters[key]) {
        initialFilters[key] = value;
      }
      // Multiple values but not comma-separated (repeated params)
      else {
        if (Array.isArray(initialFilters[key])) {
          initialFilters[key].push(value);
        } else {
          initialFilters[key] = [initialFilters[key], value];
        }
      }
    }
  });

  setActiveFilters(initialFilters);
}, []);

  // Fetch filter options from API
  useEffect(() => {
    const fetchFilterOptions = async () => {
      try {
        setLoading(true);
        setError(null);

        // Use the component API to get filter options
        const result = await componentsApi.getComponentFilterOptions(componentType);
        setFilterMetadata(result);
      } catch (err) {
        console.error('Error fetching filter options:', err);
        setError(`Failed to load filters: ${err.message || 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };

    fetchFilterOptions();
  }, [componentType]);

  // Update URL when active filters change
  useEffect(() => {
    // Create a new URLSearchParams object to preserve pagination/sorting
    const newParams = new URLSearchParams(searchParams);

    // Remove all existing filter params (except pagination and sorting)
    Array.from(newParams.keys()).forEach(key => {
      if (key !== 'page' && key !== 'sort') {
        newParams.delete(key);
      }
    });

    // Add current active filters to URL
    Object.entries(activeFilters).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        // Join multiple values with commas for array values
        newParams.set(key, value.join(','));
      } else if (value !== null && value !== undefined && value !== '') {
        // Handle single values
        newParams.set(key, value);
      }
    });

    // If we're on page > 1, reset to page 1 when filters change
    if (newParams.get('page') && newParams.get('page') !== '1') {
      newParams.set('page', '1');
    }

    // Update URL with new params
    setSearchParams(newParams);
  }, [activeFilters]);

  // Handle adding a filter
  const handleFilterChange = (filterId, value, isRemove = false) => {
    setActiveFilters(prevFilters => {
      const newFilters = { ...prevFilters };

      // Extract base field name for range filters (e.g., "weight" from "details__weight")
      const baseFieldName = filterId.split('__').pop();

      // Handle removing a filter
      if (isRemove) {
        // For range filters, we need to remove both min and max
        if (filterId.includes('__') && (baseFieldName.endsWith('_min') || baseFieldName.endsWith('_max'))) {
          // Get the base field without _min/_max
          const baseField = baseFieldName.replace(/_min$|_max$/, '');
          delete newFilters[`${baseField}_min`];
          delete newFilters[`${baseField}_max`];
        }
        // When removing a base field (from X button in active filters)
        else if (!filterId.endsWith('_min') && !filterId.endsWith('_max') && (newFilters[`${filterId}_min`] || newFilters[`${filterId}_max`])) {
          // Remove both min and max variants
          delete newFilters[`${filterId}_min`];
          delete newFilters[`${filterId}_max`];
        }
        // For active filter tags, the filterId might be just the base field
        else if (filterId.includes('__')) {
          // Handle nested field removal
          const baseField = filterId.split('__').pop();
          if (Array.isArray(newFilters[baseField])) {
            newFilters[baseField] = newFilters[baseField].filter(val => val.toString() !== value.toString());
            if (newFilters[baseField].length === 0) {
              delete newFilters[baseField];
            }
          } else {
            delete newFilters[baseField];
          }
        }
        // Regular filters
        else if (Array.isArray(newFilters[filterId])) {
          newFilters[filterId] = newFilters[filterId].filter(val => val.toString() !== value.toString());
          if (newFilters[filterId].length === 0) {
            delete newFilters[filterId];
          }
        } else {
          delete newFilters[filterId];
        }
        return newFilters;
      }

      // Handle adding/updating a filter
      // For checkbox filters that support multiple values
      if (filterId.includes('__') || filterId === 'manufacturer') {
        // Extract the base field name
        const baseField = filterId.includes('__') ? filterId.split('__').pop() : filterId;

        if (!newFilters[baseField]) {
          newFilters[baseField] = [value];
        } else if (Array.isArray(newFilters[baseField])) {
          // Add value if it doesn't exist
          const valueStr = value.toString();
          if (!newFilters[baseField].some(v => v.toString() === valueStr)) {
            newFilters[baseField] = [...newFilters[baseField], value];
          }
        } else {
          // Convert to array if it's not already
          newFilters[baseField] = [newFilters[baseField], value];
        }
      }
      // For range filters
      else if (filterId.endsWith('_min') || filterId.endsWith('_max')) {
        // Ensure the value is correctly processed (parse if number, keep as is if not)
        let processedValue = value;
        if (value !== '' && !isNaN(value)) {
          processedValue = parseFloat(value);
        }

        // Set the value directly, ensuring it's not an array
        newFilters[filterId] = processedValue;
      }
      // For single value filters
      else {
        newFilters[filterId] = value;
      }

      return newFilters;
    });
  };

  // Clear all filters
  const clearAllFilters = () => {
    setActiveFilters({});
  };

  // Render the appropriate filter type
  const renderFilter = (filter) => {
    const { id, type, label, field } = filter;

    // Extract base field name for constructing filter params
    const baseFieldName = field.split('__').pop();

    switch (type) {
      case 'choice':
        return (
          <ChoiceFilter
            key={id}
            filter={filter}
            activeValues={activeFilters[baseFieldName] || []}
            onChange={(value) => handleFilterChange(field, value)}
            onRemove={(value) => handleFilterChange(field, value, true)}
            componentType={componentType}
          />
        );

      case 'range':
        const minKey = `${baseFieldName}_min`;
        const maxKey = `${baseFieldName}_max`;
        const minValue = activeFilters[minKey] || '';
        const maxValue = activeFilters[maxKey] || '';

        return (
          <RangeFilter
            key={id}
            filter={filter}
            minValue={minValue}
            maxValue={maxValue}
            onChange={(min, max) => {
              handleFilterChange(minKey, min);
              handleFilterChange(maxKey, max);
            }}
            onRemove={() => {
              handleFilterChange(baseFieldName, '', true);
            }}
            componentType={componentType}
          />
        );

      default:
        return null;
    }
  };

  // Get display names for active filters
  const getActiveFilterDisplayData = () => {
    if (!filterMetadata) return [];

    const activeFilterData = [];

    // Process all filter groups and their filters
    filterMetadata.groups?.forEach(group => {
      group.filters?.forEach(filter => {
        const { id, type, label, field, unit } = filter;

        // Get base field name for comparison with active filters
        const baseFieldName = field.split('__').pop();

        // Handle choice filters (including 'manufacturer')
        if ((type === 'choice' || baseFieldName === 'manufacturer') && activeFilters[baseFieldName]) {
          const values = Array.isArray(activeFilters[baseFieldName])
            ? activeFilters[baseFieldName]
            : [activeFilters[baseFieldName]];

          values.forEach(value => {
            // Find display name from options if available
            let displayValue = value;
            if (filter.options) {
              const option = filter.options.find(opt => opt.value?.toString() === value?.toString());
              if (option) displayValue = option.display;
            }

            activeFilterData.push({
              id: baseFieldName,
              value,
              label,
              displayValue,
              group: group.title,
              field // Add the original field for reference
            });
          });
        }

        // Handle range filters
        if (type === 'range') {
          const minKey = `${baseFieldName}_min`;
          const maxKey = `${baseFieldName}_max`;

          if (activeFilters[minKey] || activeFilters[maxKey]) {
            const minVal = activeFilters[minKey] || filter.min;
            const maxVal = activeFilters[maxKey] || filter.max;
            const displayValue = `${minVal}${unit ? ' ' + unit : ''} - ${maxVal}${unit ? ' ' + unit : ''}`;

            activeFilterData.push({
              id: baseFieldName, // Use base field ID for ranges
              value: { min: minVal, max: maxVal },
              label,
              displayValue,
              group: group.title,
              field // Add the original field for reference
            });
          }
        }
      });
    });

    return activeFilterData;
  };

  // Handle loading state
  if (loading && !filterMetadata) {
    return (
      <div className="w-full bg-white rounded-lg shadow-sm overflow-hidden p-6">
        <LoadingSpinner />
      </div>
    );
  }

  // Handle error state
  if (error) {
    return (
      <div className="w-full bg-white rounded-lg shadow-sm overflow-hidden p-4">
        <ErrorMessage message={error} />
      </div>
    );
  }

  // No filter metadata available
  if (!filterMetadata || !filterMetadata.groups) {
    return (
      <div className="w-full bg-white rounded-lg shadow-sm overflow-hidden p-6">
        <p className="text-gray-500 text-center">No filters available</p>
      </div>
    );
  }

  const activeFilterData = getActiveFilterDisplayData();
  const hasActiveFilters = activeFilterData.length > 0;

  return (
    <div className="w-full bg-white rounded-lg shadow-sm overflow-hidden">
      <div className={`p-4 flex justify-between items-center border-b border-gray-100 bg-gray-50`}>
        <h2 className={`text-lg font-semibold ${themeClass.text}`}>Filters</h2>
        <button
          onClick={clearAllFilters}
          disabled={!hasActiveFilters}
          className={`${themeClass.text} text-sm px-2 py-1 rounded-md hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          Clear All
        </button>
      </div>

      {/* Active Filters Section */}
      {hasActiveFilters && (
        <ActiveFilters
          filters={activeFilterData}
          onRemove={(filterId, value) => handleFilterChange(filterId, value, true)}
          componentType={componentType}
        />
      )}

      {/* Filter Groups */}
      {filterMetadata.groups.map((group) => (
        <FilterGroup
          key={group.id}
          title={group.title}
          initialExpanded={group.id === 'manufacturer'} // Expand manufacturer by default
          componentType={componentType}
        >
          {group.filters.map((filter) => renderFilter(filter))}
        </FilterGroup>
      ))}
    </div>
  );
};

FilterSidebar.propTypes = {
  componentType: PropTypes.string
};

export default FilterSidebar;