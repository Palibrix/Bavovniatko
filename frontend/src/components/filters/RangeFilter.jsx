import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import {getEntityThemeClass} from "../../utils/themeUtils";

/**
 * Range filter component with min/max inputs, no slider
 *
 * @param {Object} props Component properties
 * @param {Object} props.filter Filter configuration
 * @param {string|number} props.minValue Current minimum value
 * @param {string|number} props.maxValue Current maximum value
 * @param {Function} props.onChange Callback when range values change
 * @param {Function} props.onRemove Callback to remove this filter
 * @param {string} props.componentType Theme color for styling
 */
const RangeFilter = ({
  filter,
  minValue = '',
  maxValue = '',
  onChange,
  onRemove,
  componentType
}) => {
  const { id, label, min, max, unit } = filter;

  // const themeClass = getEntityThemeClass(componentType);
  // Extract base field name
  const baseFieldName = filter.field.split('__').pop();

  // State for input values
  const [localMinValue, setLocalMinValue] = useState(minValue);
  const [localMaxValue, setLocalMaxValue] = useState(maxValue);

  // Get slider steps based on range
  const getStep = () => {
    const range = max - min;
    if (range <= 1) return 0.01; // Very fine steps for small ranges
    if (range <= 10) return 0.1; // Fine steps for small ranges
    if (range <= 100) return 1; // Integer steps for medium ranges
    return Math.ceil(range / 100); // Larger steps for big ranges
  };

  const step = getStep();

  // Update local input values when props change
  useEffect(() => {
    setLocalMinValue(minValue);
  }, [minValue]);

  useEffect(() => {
    setLocalMaxValue(maxValue);
  }, [maxValue]);

  // Apply min/max values when inputs are blurred
  const handleMinBlur = () => {
    // If the value is empty
    if (localMinValue === '') {
      // If both values are empty, remove the filter completely
      if (localMaxValue === '') {
        onRemove(baseFieldName);
        return;
      }
      // Otherwise just update with the empty min value
      onChange('', localMaxValue);
      return;
    }

    let validatedValue = localMinValue;

    // Validate value is a number and within min-max bounds
    if (validatedValue !== '') {
      validatedValue = Math.max(min, parseFloat(validatedValue));

      // Ensure min <= max
      if (localMaxValue !== '' && validatedValue > parseFloat(localMaxValue)) {
        validatedValue = parseFloat(localMaxValue);
      }

      // Format to match step precision
      validatedValue = parseFloat(validatedValue.toFixed(String(step).split('.')[1]?.length || 0));
    }

    setLocalMinValue(validatedValue);
    onChange(validatedValue, localMaxValue);
  };

  const handleMaxBlur = () => {
    // If the value is empty
    if (localMaxValue === '') {
      // If both values are empty, remove the filter completely
      if (localMinValue === '') {
        onRemove(baseFieldName);
        return;
      }
      // Otherwise just update with the empty max value
      onChange(localMinValue, '');
      return;
    }

    let validatedValue = localMaxValue;

    // Validate value is a number and within min-max bounds
    if (validatedValue !== '') {
      validatedValue = Math.min(max, parseFloat(validatedValue));

      // Ensure min <= max
      if (localMinValue !== '' && validatedValue < parseFloat(localMinValue)) {
        validatedValue = parseFloat(localMinValue);
      }

      // Format to match step precision
      validatedValue = parseFloat(validatedValue.toFixed(String(step).split('.')[1]?.length || 0));
    }

    setLocalMaxValue(validatedValue);
    onChange(localMinValue, validatedValue);
  };

  // Handle changes to input fields
  const handleMinChange = (e) => {
    setLocalMinValue(e.target.value);
  };

  const handleMaxChange = (e) => {
    setLocalMaxValue(e.target.value);
  };

  // Determine if the filter has any values set
  const isActive =
    localMinValue !== '' ||
    localMaxValue !== '';

  return (
    <div className="filter-option space-y-3">
      {/* Filter label and reset button */}
      <div className="flex justify-between items-center">
        <label className="block text-sm font-medium text-gray-700">
          {label}
        </label>
        {isActive && (
          <button
            onClick={() => onRemove(baseFieldName)}
            className="text-xs text-gray-500 hover:text-gray-700"
            title="Reset filter"
          >
            Reset
          </button>
        )}
      </div>

      {/* Min/Max inputs */}
      <div className="flex items-center space-x-2">
        <input
          type="number"
          placeholder={`Min (${min})`}
          value={localMinValue}
          onChange={handleMinChange}
          onBlur={handleMinBlur}
          min={min}
          max={max}
          step={step}
          className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
        />
        <span className="text-gray-500">-</span>
        <input
          type="number"
          placeholder={`Max (${max})`}
          value={localMaxValue}
          onChange={handleMaxChange}
          onBlur={handleMaxBlur}
          min={min}
          max={max}
          step={step}
          className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
        />
        {unit && <span className="text-sm text-gray-500">{unit}</span>}
      </div>

      {/* Range indicators */}
      <div className="flex justify-between text-xs text-gray-500">
        <span>{min}{unit && ` ${unit}`}</span>
        <span>{max}{unit && ` ${unit}`}</span>
      </div>
    </div>
  );
};

RangeFilter.propTypes = {
  filter: PropTypes.shape({
    id: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    field: PropTypes.string.isRequired,
    min: PropTypes.number.isRequired,
    max: PropTypes.number.isRequired,
    default_value: PropTypes.number,
    unit: PropTypes.string
  }).isRequired,
  minValue: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  maxValue: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  onChange: PropTypes.func.isRequired,
  onRemove: PropTypes.func.isRequired,
  themeColor: PropTypes.string
};

export default RangeFilter;