import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

/**
 * Panel showing key specifications of a component
 *
 * @param {Object} props Component properties
 * @param {Object} props.item Component data
 * @param {Array} props.specsConfig Specs configuration from componentSpecs.js
 * @param {number} props.minSpecs Minimum number of specs to show (will pad with empty if needed)
 * @param {number} props.maxSpecs Maximum number of specs to show
 * @param {string} props.themeColor Theme color for styling
 */
const KeySpecsPanel = ({
  item,
  specsConfig,
  minSpecs = 4,
  maxSpecs = 6,
  themeColor = 'primary'
}) => {
  if (!item || !specsConfig) return null;

  // Get displayable specs (specs that have values in the item)
  const filteredSpecs = specsConfig.filter(spec => {
    const value = spec.path.split('.').reduce((obj, key) =>
      obj && obj[key] !== undefined ? obj[key] : null, item);
    return value !== null && value !== undefined;
  });

  // Use these specs, up to maxSpecs
  const keySpecs = filteredSpecs.slice(0, maxSpecs);

  // Ensure we have at least minSpecs slots (even if some are empty)
  const totalSlots = Math.max(keySpecs.length, minSpecs);

  // Create an array of length totalSlots, with keySpecs at the start and null values to fill
  const displaySpecs = Array(totalSlots).fill(null).map((_, i) => keySpecs[i] || null);

  return (
    <div className={`bg-white rounded-3xl shadow-sm overflow-hidden border-t-4 border-t-${themeColor}`}>
      <div className={`py-4 px-6 border-b border-gray-100 font-semibold text-${themeColor} bg-${themeColor} bg-opacity-5`}>
        Key Specifications
      </div>
      <div className="grid grid-cols-2 gap-4 p-6">
        {displaySpecs.map((spec, index) => {
          // If spec is null (padding slot), render an empty div to maintain grid structure
          if (!spec) {
            return <div key={`empty-${index}`} className="key-spec"></div>;
          }

          // Extract value using the path
          const value = spec.path.split('.').reduce((obj, key) =>
            obj && obj[key] !== undefined ? obj[key] : null, item);

          // Format the value based on spec configuration
          let formattedValue;
          if (spec.formatter) {
            formattedValue = spec.formatter(value, item);
          } else if (spec.unit) {
            formattedValue = `${value} ${spec.unit}`;
          } else {
            formattedValue = value;
          }

          return (
            <div key={index} className="key-spec">
              <div className="text-sm text-gray-500 flex items-center gap-1.5">
                {spec.icon && <FontAwesomeIcon icon={spec.icon} className={`text-${themeColor} text-xs`} />}
                {spec.label}
              </div>
              <div className="font-semibold text-primary">
                {formattedValue}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

KeySpecsPanel.propTypes = {
  item: PropTypes.object.isRequired,
  specsConfig: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string.isRequired,
      path: PropTypes.string.isRequired,
      icon: PropTypes.object,
      unit: PropTypes.string,
      formatter: PropTypes.func
    })
  ).isRequired,
  minSpecs: PropTypes.number,
  maxSpecs: PropTypes.number,
  themeColor: PropTypes.string
};

export default KeySpecsPanel;
