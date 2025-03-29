import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExternalLinkAlt, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
import TabSection from './TabSection';
import { getEntityThemeClass } from '../../utils/themeUtils';
import { getFullSpecsForComponentType } from '../../config/componentSpecs';
import { DescriptionTab, SpecificationsTab, DetailsTab, DocumentsTab } from './tabs';
import { hasDetails, hasDocuments } from '../../utils/componentDetailUtils';

/**
 * Panel for displaying information about a selected component
 *
 * @param {Object} props Component properties
 * @param {Object} props.item The component data
 * @param {string} props.componentType Component type (e.g., 'frame', 'motor')
 * @param {boolean} props.isBattery Whether this component is a battery
 * @param {Function} props.onClose Callback function when component is closed
 */
const ComponentInfoPanel = ({ item, componentType, isBattery = false, onClose }) => {
  const [activeTab, setActiveTab] = useState('description');
  const [displayedItem, setDisplayedItem] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const prevItemIdRef = useRef(null);
  const prevComponentTypeRef = useRef(null);
  const themeClass = getEntityThemeClass(componentType);

  // Effect to handle component changes and loading state
  useEffect(() => {
    // Check if the item or componentType has changed
    const itemIdChanged = item?.id !== prevItemIdRef.current;
    const typeChanged = componentType !== prevComponentTypeRef.current;

    // If something changed, update refs and set loading state
    if (itemIdChanged || typeChanged) {
      // Set loading state first
      setIsLoading(true);

      // Update refs
      prevItemIdRef.current = item?.id;
      prevComponentTypeRef.current = componentType;

      // Clear the current displayed item during transition to avoid showing old data
      setDisplayedItem(null);

      // Set a small timeout to ensure we don't get a double render with old data
      const timer = setTimeout(() => {
        // Update displayed item and clear loading state
        setDisplayedItem(item);
        setIsLoading(false);
      }, 50); // Small delay to ensure clean transition

      return () => clearTimeout(timer);
    } else if (item && !displayedItem) {
      // Initial load or if item is set but displayedItem is not
      setDisplayedItem(item);
      setIsLoading(false);
    }
  }, [item, componentType]);

  // Handle tab change
  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
  };

  // Track available specs
  const [specsConfig, setSpecsConfig] = useState([]);

  useEffect(() => {
    // Don't load specs config during loading state
    if (isLoading || !displayedItem) return;

    // Get specs for this component type
    const specs = getFullSpecsForComponentType(componentType);
    setSpecsConfig(specs || []);
  }, [componentType, displayedItem, isLoading]);

  // Show loading state
  if (isLoading || !displayedItem) {
    return (
      <div className="bg-white rounded-3xl shadow-sm overflow-hidden mt-6">
        <div className="py-4 px-6 border-b border-gray-100 flex justify-between items-center">
          <h3 className={`font-semibold ${themeClass.text}`}>Loading...</h3>
          <button
            onClick={onClose}
            className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-500"
            aria-label="Close component details"
          >
            <FontAwesomeIcon icon={faTimesCircle} />
          </button>
        </div>
        <div className="p-6 flex justify-center items-center h-48">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  // Determine if the component has details and documents
  const hasDetailsSection = hasDetails(displayedItem, componentType);
  const hasDocumentsSection = hasDocuments(displayedItem);

  // Get URL for viewing full component details
  const getComponentUrl = () => {
    if (isBattery) return null; // Batteries don't have detail pages
    return `/components/${componentType}/${displayedItem.id}`;
  };

  const componentUrl = getComponentUrl();

  // Get component display name
  const getComponentName = () => {
    if (!displayedItem) return '';
    return `${displayedItem.manufacturer ? `${displayedItem.manufacturer} ` : ''}${displayedItem.model}`;
  };

  return (
    <div className="bg-white rounded-3xl shadow-sm overflow-hidden mt-6">
      <div className="py-4 px-6 border-b border-gray-100 flex justify-between items-center">
        <h3 className={`font-semibold ${themeClass.text}`}>{getComponentName()}</h3>

        <div className="flex items-center gap-3">
          {/* View Full Details button - not shown for batteries */}
          {componentUrl && !isBattery && (
            <Link
              to={componentUrl}
              className={`inline-flex items-center px-4 py-2 rounded border ${themeClass.border} ${themeClass.text} text-sm font-medium hover:${themeClass.bg} hover:text-white transition-colors`}
            >
              <FontAwesomeIcon icon={faExternalLinkAlt} className="mr-2" />
              View Full Details
            </Link>
          )}

          {/* Close button */}
          <button
            onClick={() => onClose()}
            className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-500"
            aria-label="Close component details"
          >
            <FontAwesomeIcon icon={faTimesCircle} />
          </button>
        </div>
      </div>

      {/* Component tabs */}
      <div className="border-b border-gray-100">
        <div className="flex">
          <button
            className={`py-3 px-4 text-sm font-medium ${
              activeTab === 'description' 
                ? `${themeClass.text} border-b-2 ${themeClass.border}` 
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => handleTabChange('description')}
          >
            Description
          </button>

          <button
            className={`py-3 px-4 text-sm font-medium ${
              activeTab === 'specs' 
                ? `${themeClass.text} border-b-2 ${themeClass.border}` 
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => handleTabChange('specs')}
          >
            Specifications
          </button>

          {hasDetailsSection && (
            <button
              className={`py-3 px-4 text-sm font-medium ${
                activeTab === 'details' 
                  ? `${themeClass.text} border-b-2 ${themeClass.border}` 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => handleTabChange('details')}
            >
              Details
            </button>
          )}

          {hasDocumentsSection && (
            <button
              className={`py-3 px-4 text-sm font-medium ${
                activeTab === 'documents' 
                  ? `${themeClass.text} border-b-2 ${themeClass.border}` 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => handleTabChange('documents')}
            >
              Documents
            </button>
          )}
        </div>
      </div>

      {/* Tab content */}
      <div className="p-6">
        {activeTab === 'description' && (
          <div className="prose max-w-none">
            {displayedItem.description ? (
              <div dangerouslySetInnerHTML={{ __html: displayedItem.description }} />
            ) : (
              <p className="text-gray-500 italic">No description available for this component.</p>
            )}
          </div>
        )}

        {activeTab === 'specs' && specsConfig && specsConfig.length > 0 && (
          <SpecificationsTab
            item={displayedItem}
            specsConfig={specsConfig}
            componentType={componentType}
            inPanel={true}
          />
        )}

        {activeTab === 'details' && hasDetailsSection && (
          <DetailsTab
            item={displayedItem}
            componentType={componentType}
            inPanel={true}
          />
        )}

        {activeTab === 'documents' && hasDocumentsSection && (
          <DocumentsTab
            item={displayedItem}
            componentType={componentType}
            inPanel={true}
          />
        )}
      </div>
    </div>
  );
};

ComponentInfoPanel.propTypes = {
  item: PropTypes.object.isRequired,
  componentType: PropTypes.string.isRequired,
  isBattery: PropTypes.bool,
  onClose: PropTypes.func
};

export default ComponentInfoPanel;