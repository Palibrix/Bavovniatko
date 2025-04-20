import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faPlus } from '@fortawesome/free-solid-svg-icons';
import LoadingSpinner from '../common/LoadingSpinner';
import ComponentGallery from '../detail/ComponentGallery';
import KeySpecsPanel from '../detail/KeySpecsPanel';
import TabContainer from '../detail/TabContainer';
import SelectListsModal from '../lists/SelectListsModal';
import Toast from '../common/Toast';
import { getFullSpecsForComponentType } from '../../config/componentSpecs';
import { getEntityThemeClass} from '../../utils/themeUtils';
import {
  DescriptionTab,
  SpecificationsTab,
  DetailsTab,
  DocumentsTab
} from '../detail/tabs';

/**
 * Template for displaying detailed component information
 * with gallery, key specs, and tabbed content sections
 *
 * @param {Object} props Component properties
 * @param {string} props.componentType Type of component (antennas, cameras, etc.)
 * @param {Object} props.item The component data to display
 * @param {boolean} props.isRefreshing Whether data is currently being refreshed
 * @param {Function} props.onRefresh Function to call to refresh data
 * @param {Function} props.onAddToList Callback when "Add to List" button is clicked
 */
const ComponentDetailTemplate = ({
  componentType,
  item,
  isRefreshing = false,
  onRefresh,
  onAddToList
}) => {
  const [showListsModal, setShowListsModal] = useState(false);
  const [toast, setToast] = useState({ visible: false, message: '', type: '' });

  if (!item) {
    return <LoadingSpinner />;
  }

  // Get component theme color
  const themeClass = getEntityThemeClass(componentType);

  // Get specs configuration for this component type
  const specsConfig = getFullSpecsForComponentType(componentType);

  // Handle adding item to list
  const handleAddToList = () => {
    setShowListsModal(true);
  };

  // Handle list update success
  const handleListsUpdateSuccess = (result) => {
    setToast({
      visible: true,
      message: `Component ${result.added_to > 0 ? 'added to' : 'removed from'} ${result.added_to + result.removed_from} ${result.added_to + result.removed_from === 1 ? 'list' : 'lists'}`,
      type: 'success'
    });

    // Call the original callback if provided
    if (onAddToList) onAddToList(item);
  };

  // Get component type for API calls (convert plural to singular)
  const getApiComponentType = () => {
    // Convert plural to singular for API calls
    if (componentType.endsWith('s')) {
      // Handle special cases first
      if (componentType === 'antennas') return 'antenna';
      if (componentType === 'cameras') return 'camera';
      if (componentType === 'frames') return 'frame';
      if (componentType === 'propellers') return 'propeller';
      if (componentType === 'receivers') return 'receiver';
      if (componentType === 'transmitters') return 'transmitter';

      // Default: remove trailing 's'
      return componentType.slice(0, -1);
    }
    return componentType;
  };

  // Get component display name
  const getComponentName = () => {
    return item.manufacturer
      ? `${item.manufacturer} ${item.model}`
      : item.model || 'Component';
  };

  return (
    <div className="w-[92%] max-w-[1400px] mx-auto px-4 py-8">
      {/* Back button */}
      <Link
        to={`/components/${componentType}`}
        className="inline-flex items-center text-primary hover:text-gray-600 mb-6"
      >
        <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
        Back to {componentType.charAt(0).toUpperCase() + componentType.slice(1)}
      </Link>

      {/* Product header - moved outside columns */}
      <div className="mb-6 relative">
        <span className={`inline-block text-xs font-semibold text-white ${themeClass.bg} px-3 py-1 rounded-full uppercase tracking-wider mb-2`}>
          {item.manufacturer}
        </span>
        <h1 className="text-4xl font-bold text-primary">{item.model}</h1>

        {/* Add to List Button (top right position) */}
        <div className="absolute top-0 right-0">
          <button
            onClick={handleAddToList}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg ${themeClass.bg} text-white font-semibold transition-all hover:bg-opacity-90 hover:translate-y-[-2px] hover:shadow-md`}
          >
            <FontAwesomeIcon icon={faPlus} />
            Add to List
          </button>
        </div>
      </div>

      {/* Main content area with two columns */}
      <div className="flex flex-col lg:flex-row gap-10">
        {/* Left column - Gallery and Key Specs (sticky) */}
        <div className="w-full lg:w-5/12 lg:sticky lg:top-8 lg:self-start lg:max-h-[calc(100vh-4rem)] lg:overflow-y-auto pr-4">
          {/* Image gallery with thumbnails and navigation */}
          <ComponentGallery
            images={item.images}
            alt={`${item.manufacturer} ${item.model}`}
            componentType={componentType}
          />

          {/* Key specifications panel */}
          <KeySpecsPanel
            item={item}
            specsConfig={specsConfig}
            componentType={componentType}
          />
        </div>

        {/* Right column - Tabbed content */}
        <div className="flex-1">
          <TabContainer
            item={item}
            componentType={componentType}
            descriptionTab={<DescriptionTab item={item} componentType={componentType} />}
            specificationsTab={<SpecificationsTab item={item} specsConfig={specsConfig} componentType={componentType} />}
            detailsTab={<DetailsTab item={item} componentType={componentType} />}
            documentsTab={<DocumentsTab item={item} componentType={componentType} />}
          />
        </div>
      </div>

      {/* Lists selection modal */}
      <SelectListsModal
        isOpen={showListsModal}
        onClose={() => setShowListsModal(false)}
        componentType={getApiComponentType()}
        componentId={item.id}
        componentName={getComponentName()}
        onSuccess={handleListsUpdateSuccess}
      />

      {/* Toast notifications */}
      {toast.visible && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast({...toast, visible: false})}
        />
      )}
    </div>
  );
};

ComponentDetailTemplate.propTypes = {
  componentType: PropTypes.string.isRequired,
  item: PropTypes.object,
  isRefreshing: PropTypes.bool,
  onRefresh: PropTypes.func,
  onAddToList: PropTypes.func
};

export default ComponentDetailTemplate;