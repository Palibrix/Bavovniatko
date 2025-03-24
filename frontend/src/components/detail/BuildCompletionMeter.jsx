import React from 'react';
import PropTypes from 'prop-types';

/**
 * Build completion meter component for drone detail page
 * Shows the percentage of required components installed
 *
 * @param {Object} props Component properties
 * @param {number} props.percentage Completion percentage (0-100)
 * @param {Array} props.missingComponents Array of missing component keys
 * @param {Object} props.themeClass Theme class object from themeUtils
 */
const BuildCompletionMeter = ({ percentage, missingComponents, themeClass }) => {
  // Format missing components for display
  const formatMissingComponentName = (key) => {
    // Convert key to display name (e.g., "flight_controller" to "Flight Controller")
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className={`bg-white rounded-3xl shadow-sm overflow-hidden border-t-4 ${themeClass.borderTop} mb-6`}>
      <div className={`py-4 px-6 border-b border-gray-100 font-semibold flex justify-between items-center ${themeClass.bgOpacity[5]}`}>
        <span className={themeClass.text}>Build Completion</span>
        <span className={`${themeClass.bg} text-white text-sm font-bold py-1 px-3 rounded-full`}>
          {percentage}%
        </span>
      </div>
      <div className="p-6">
        <div className="h-3 w-full bg-gray-100 rounded-full overflow-hidden mb-4">
          <div
            className={`h-full ${themeClass.bg} rounded-full`}
            style={{ width: `${percentage}%` }}
          ></div>
        </div>

        {missingComponents && missingComponents.length > 0 && (
          <div className="text-sm text-gray-500">
            <span className="font-medium">Required: </span>
            {missingComponents.map(formatMissingComponentName).join(', ')}
          </div>
        )}
      </div>
    </div>
  );
};

BuildCompletionMeter.propTypes = {
  percentage: PropTypes.number.isRequired,
  missingComponents: PropTypes.array,
  themeClass: PropTypes.object.isRequired
};

export default BuildCompletionMeter;