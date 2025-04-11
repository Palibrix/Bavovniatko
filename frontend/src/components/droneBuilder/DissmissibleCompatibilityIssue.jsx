import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faExclamationTriangle,
  faExclamationCircle,
  faInfoCircle,
  faTimes
} from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';

/**
 * Component to display a dismissible compatibility issue
 */
const DismissibleCompatibilityIssue = ({ issue, onDismiss }) => {
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
    case 'recommendation':
      return {
        icon: faInfoCircle,
        textColor: 'text-blue-700',
        bgColor: 'bg-blue-50'
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
    <div className={`p-4 rounded-md ${bgColor} ${textColor} mb-3 relative`}>
      <div className="flex items-center mb-2">
        <FontAwesomeIcon icon={icon} className="mr-2" />
        <div className="font-semibold">{issue.type}</div>

        {/* Dismiss button */}
        <button
          onClick={() => onDismiss(issue.id)}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
          aria-label="Dismiss"
        >
          <FontAwesomeIcon icon={faTimes} />
        </button>
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

DismissibleCompatibilityIssue.propTypes = {
  issue: PropTypes.shape({
    id: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    severity: PropTypes.string,
    message: PropTypes.string.isRequired,
    component_refs: PropTypes.arrayOf(PropTypes.string)
  }).isRequired,
  onDismiss: PropTypes.func.isRequired
};

export default DismissibleCompatibilityIssue;