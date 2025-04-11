import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationTriangle, faInfoCircle, faTimes, faUndo } from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';

/**
 * Modal to display hidden/dismissed compatibility issues
 */
const HiddenIssuesModal = ({ isOpen, onClose, issues, onRestoreIssue }) => {
  if (!isOpen) return null;

  // Get component badge for type
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

  // Get severity styling
  const getSeverityStyles = (severity) => {
    switch (severity) {
      case 'critical':
        return {
          icon: faExclamationTriangle,
          textColor: 'text-red-700',
          bgColor: 'bg-red-50'
        };
      case 'warning':
        return {
          icon: faExclamationTriangle,
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

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] flex flex-col">
        <div className="p-4 border-b border-gray-200 flex justify-between items-center">
          <h3 className="font-semibold text-lg">Hidden Compatibility Issues</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-800 transition-colors"
            aria-label="Close"
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>

        <div className="overflow-y-auto p-4 flex-grow">
          {issues.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              No hidden issues
            </div>
          ) : (
            <div className="space-y-4">
              {issues.map(issue => {
                const { icon, textColor, bgColor } = getSeverityStyles(issue.severity);

                return (
                  <div
                    key={issue.id}
                    className={`p-4 rounded-md ${bgColor} ${textColor} relative`}
                  >
                    <div className="flex items-center mb-2">
                      <FontAwesomeIcon icon={icon} className="mr-2" />
                      <div className="font-semibold">{issue.type}</div>
                      <div className="text-xs ml-2 bg-gray-200 rounded px-1 py-0.5 text-gray-700">
                        {issue.severity}
                      </div>

                      <button
                        onClick={() => onRestoreIssue(issue.id)}
                        className="ml-auto flex items-center px-3 py-1 bg-white rounded border border-gray-300 text-sm hover:bg-gray-50"
                      >
                        <FontAwesomeIcon icon={faUndo} className="mr-1" />
                        Restore
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
              })}
            </div>
          )}
        </div>

        <div className="p-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

HiddenIssuesModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  issues: PropTypes.array.isRequired,
  onRestoreIssue: PropTypes.func.isRequired
};

export default HiddenIssuesModal;