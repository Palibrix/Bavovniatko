import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle, faCog } from '@fortawesome/free-solid-svg-icons';
import { getKeySpecsForComponentType } from '../../config/componentSpecs';

/**
 * List view item for component selection
 */
const ComponentListItem = ({
  component,
  categoryType,
  isCompatible,
  themeClass,
  currentMapping,
  onSelect
}) => {
  return (
    <div
      className={`flex border rounded-xl overflow-hidden transition-all hover:-translate-y-1 hover:shadow-md ${
        !isCompatible ? 'opacity-60' : ''
      }`}
    >
      {!isCompatible && (
        <div className="absolute top-2 right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-white text-xs">
          <FontAwesomeIcon icon={faExclamationTriangle} />
        </div>
      )}

      <div className={`w-16 ${themeClass.bg} flex items-center justify-center text-white font-bold text-2xl`}>
        <FontAwesomeIcon icon={currentMapping?.icon || faCog} />
      </div>

      <div className="flex-1 p-3">
        <h3 className="font-medium">{component.model}</h3>
        <div className="text-sm text-gray-500 mb-2">{component.manufacturer}</div>

        <div className="grid grid-cols-2 gap-x-8 gap-y-1">
          {renderComponentSpecs(component, categoryType)}
        </div>
      </div>

      <div className="w-24 flex items-center justify-center border-l">
        <button
          className={`${themeClass.bg} text-white px-3 py-1.5 rounded-lg hover:opacity-90 transition-opacity`}
          onClick={onSelect}
        >
          Add
        </button>
      </div>
    </div>
  );
};

// Helper function to render component specs in a list view
function renderComponentSpecs(component, categoryType) {
  // Use existing spec configurations from config/componentSpecs
  const specs = getKeySpecsForComponentType(categoryType === 'antennas_receiver' ||
                                        categoryType === 'antennas_transmitter' ?
                                        'antennas' : categoryType);

  // Show up to 6 specs in the list view
  const displaySpecs = specs.slice(0, 6);

  return displaySpecs.map((spec, index) => {
    const value = extractSpecValue(component, spec);

    return (
      <div key={index} className="flex justify-between text-sm">
        <span className="text-gray-500 mr-2">{spec.label}:</span>
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

ComponentListItem.propTypes = {
  component: PropTypes.object.isRequired,
  categoryType: PropTypes.string.isRequired,
  isCompatible: PropTypes.bool.isRequired,
  themeClass: PropTypes.object.isRequired,
  currentMapping: PropTypes.object,
  onSelect: PropTypes.func.isRequired
};

export default ComponentListItem;