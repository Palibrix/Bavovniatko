import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCode, faCheck } from '@fortawesome/free-solid-svg-icons';
import TabSection from '../TabSection';
import { componentToJson, formatSpecValue } from '../../../utils/componentDetailUtils';
import { getEntityThemeClass } from '../../../utils/themeUtils';

/**
 * Specifications tab content for component detail page
 * Shows all available specifications for the component
 */
const SpecificationsTab = ({ item, specsConfig, componentType, inPanel = false }) => {
  const [copySuccess, setCopySuccess] = useState(false);
  const themeClass = getEntityThemeClass(componentType);

  // Handle copy specs as JSON
  const handleCopySpecs = () => {
    const jsonString = componentToJson(item, specsConfig);

    navigator.clipboard.writeText(jsonString)
      .then(() => {
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      })
      .catch(err => {
        console.error('Failed to copy specs: ', err);
        alert('Failed to copy specifications to clipboard');
      });
  };

  // Copy button with success state
  const copyButton = (
    <button
      className={`${
        copySuccess 
          ? `${themeClass.bg} text-white` 
          : `${themeClass.text} hover:${themeClass.bgOpacity[10]}`
      } px-3 py-1 text-sm rounded transition-colors flex items-center gap-1`}
      onClick={handleCopySpecs}
    >
      <FontAwesomeIcon icon={copySuccess ? faCheck : faCode} />
      {copySuccess ? 'Copied!' : 'Copy JSON'}
    </button>
  );

  // Get specifications from specsConfig to ensure they're displayed nicely
  const getConfigSpecs = () => {
    return specsConfig.map(spec => {
      // Extract value using the path
      let value = spec.path.split('.').reduce((obj, key) =>
        obj && obj[key] !== undefined ? obj[key] : null, item);

      // Format the value based on spec configuration
      let formattedValue;
      if (spec.formatter) {
        formattedValue = spec.formatter(value, item);
      } else if (spec.unit) {
        formattedValue = (value) ? `${value} ${spec.unit}` : 'N/A';
      } else {
        formattedValue = formatSpecValue(value);
      }

      return {
        label: spec.label,
        value: formattedValue,
        icon: spec.icon
      };
    }).filter(Boolean);
  };

  const configSpecs = getConfigSpecs();

  // If this is being shown in a panel, we don't need to wrap it in TabSection
  const content = (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {/* Render specs from config first (with nice formatting) */}
      {configSpecs.map((spec, index) => (
        <div
          key={`config-${index}`}
          className="bg-gray-50 p-4 rounded-xl transition-all hover:bg-gray-100 hover:transform hover:-translate-y-1"
        >
          <div className="flex items-center gap-2 text-gray-500 text-sm mb-1">
            {spec.icon && (
              <FontAwesomeIcon icon={spec.icon} className={themeClass.text} />
            )}
            {spec.label}
          </div>
          <div className="font-semibold text-primary text-lg">
            {spec.value}
          </div>
        </div>
      ))}
    </div>
  );

  return inPanel ? content : (
    <TabSection
      title="Technical Specifications"
      componentType={componentType}
      headerActions={copyButton}
    >
      {content}
    </TabSection>
  );
};

SpecificationsTab.propTypes = {
  item: PropTypes.object.isRequired,
  specsConfig: PropTypes.array.isRequired,
  componentType: PropTypes.string.isRequired,
  inPanel: PropTypes.bool
};

export default SpecificationsTab;