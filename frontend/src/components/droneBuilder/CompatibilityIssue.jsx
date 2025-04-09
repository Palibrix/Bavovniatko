import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle, faExclamationCircle, faInfoCircle } from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';

/**
 * Component to display a compatibility issue
 */
const CompatibilityIssue = ({ issue }) => {
  // Determine severity styling
  const getSeverityStyles = () => {
    switch (issue.severity) {
      case 'critical':
        return {
          icon: faExclamationTriangle,
          textColor: 'text-red-700',
          bgColor: 'bg-red-50'
        };
      case 'warning':
        return {
          icon: faExclamationCircle,
          textColor: 'text-amber-700',
          bgColor: 'bg-amber-50'
        };
      default:
        return {
          icon: faInfoCircle,
          textColor: 'text-blue-700',
          bgColor: 'bg-blue-50'
        };
    }
  };

  const { icon, textColor, bgColor } = getSeverityStyles();

  // Get theme classes for affected components
  const getComponentBadge = (componentType) => {
    // Map internal component types to display names and themes
    const typeMap = {
      'camera': { label: 'Camera', theme: 'video' },
      'frame': { label: 'Frame', theme: 'frame' },
      'motor': { label: 'Motor', theme: 'propulsion' },
      'propeller': { label: 'Propeller', theme: 'propulsion' },
      'flight_controller': { label: 'Flight Controller', theme: 'control' },
      'speed_controller': { label: 'Speed Controller', theme: 'control' },
      'receiver': { label: 'Receiver', theme: 'control' },
      'transmitter': { label: 'Transmitter', theme: 'video' },
      'antenna_receiver': { label: 'Receiver Antenna', theme: 'antenna' },
      'antenna_transmitter': { label: 'Transmitter Antenna', theme: 'antenna' },
      'battery': { label: 'Battery', theme: 'propulsion' }
    };

    const componentInfo = typeMap[componentType] || { label: componentType, theme: 'primary' };
    const themeClass = getEntityThemeClass(componentInfo.theme);

    return (
      <span
        key={componentType}
        className={`px-2 py-1 rounded-md text-xs font-medium ${themeClass.bg} text-white mr-2`}
      >
        {componentInfo.label}
      </span>
    );
  };

  return (
    <div className={`p-4 rounded-md ${bgColor} ${textColor} mb-3`}>
      <div className="flex items-center mb-2">
        <FontAwesomeIcon icon={icon} className="mr-2" />
        <div className="font-semibold">{issue.type}</div>
      </div>

      {issue.component_refs && issue.component_refs.length > 0 && (
        <div className="mb-2 flex flex-wrap">
          {issue.component_refs.map(componentType => getComponentBadge(componentType))}
        </div>
      )}

      <div className="text-sm">{issue.message}</div>
    </div>
  );
};

CompatibilityIssue.propTypes = {
  issue: PropTypes.shape({
    type: PropTypes.string.isRequired,
    severity: PropTypes.string,
    message: PropTypes.string.isRequired,
    component_refs: PropTypes.arrayOf(PropTypes.string)
  }).isRequired
};

export default CompatibilityIssue;