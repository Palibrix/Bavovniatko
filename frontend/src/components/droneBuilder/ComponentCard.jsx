import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import { getKeySpecsForComponentType } from '../../config/componentSpecs';

/**
 * Grid view card for component selection
 */
const ComponentCard = ({ component, categoryType, isCompatible, themeClass, onSelect, compatibilityIssues = [] }) => {
  return (
    <div
      className={`border rounded-xl transition-all hover:-translate-y-1 hover:shadow-md ${
        !isCompatible ? 'opacity-60' : ''
      }`}
    >
      {!isCompatible && (
        <div
          className="absolute top-2 right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-white text-xs group cursor-help"
          title={compatibilityIssues.length > 0 ? compatibilityIssues[0].message : "Incompatible with current configuration"}
        >
          <FontAwesomeIcon icon={faExclamationTriangle} />
          {compatibilityIssues.length > 0 && (
            <div className="hidden group-hover:block absolute right-0 top-full mt-2 bg-white border border-gray-200 shadow-lg rounded-md p-3 w-64 z-10">
              <div className="text-red-600 font-medium mb-1">Compatibility Issues:</div>
              {compatibilityIssues.map((issue, idx) => (
                <div key={idx} className="text-sm text-gray-700 mb-1">
                  {issue.message}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="p-3 bg-gray-50 border-b">
        <h3 className="font-medium mb-1">{component.model}</h3>
        <div className="text-sm text-gray-500">{component.manufacturer}</div>
      </div>

      <div className="p-3">
        {renderComponentSpecs(component, categoryType)}
      </div>

      <div className="p-3 bg-gray-50 border-t flex justify-between items-center">
        <button className="text-sm text-gray-500 hover:text-primary">Details</button>
        <button
          className={`${themeClass.text} font-medium text-sm hover:underline`}
          onClick={onSelect}
        >
          Add
        </button>
      </div>
    </div>
  );
};

// Helper function to render component specs in a card
function renderComponentSpecs(component, categoryType) {
  // Use existing spec configurations from config/componentSpecs
  const specs = getKeySpecsForComponentType(categoryType === 'antennas_receiver' ||
                                        categoryType === 'antennas_transmitter' ?
                                        'antennas' : categoryType);

  // Show the first 3 specs
  const displaySpecs = specs.slice(0, 3);

  return displaySpecs.map((spec, index) => {
    const value = extractSpecValue(component, spec);

    return (
      <div key={index} className="flex justify-between text-sm mb-1.5">
        <span className="text-gray-500">{spec.label}</span>
        <span className="font-medium">{value}</span>
      </div>
    );
  });
}

// Helper function to extract spec value using spec configuration
function extractSpecValue(component, spec) {
  // Extract value using path
  let value = null;

  try {
    value = spec.path.split('.').reduce((obj, key) =>
      obj && obj[key] !== undefined ? obj[key] : null, component);

    // Format the value
    if (spec.formatter) {
      return spec.formatter(value, component);
    } else if (spec.unit && value !== null) {
      return `${value} ${spec.unit}`;
    } else if (value !== null) {
      return value.toString();
    }
  } catch (error) {
    // If there's an error extracting the value, return N/A
    console.error(`Error extracting spec value: ${error.message}`);
  }

  return 'N/A';
}

ComponentCard.propTypes = {
  component: PropTypes.object.isRequired,
  categoryType: PropTypes.string.isRequired,
  isCompatible: PropTypes.bool.isRequired,
  themeClass: PropTypes.object.isRequired,
  onSelect: PropTypes.func.isRequired,
  compatibilityIssues: PropTypes.array
};

export default ComponentCard;