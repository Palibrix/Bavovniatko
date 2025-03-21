import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faPlus } from '@fortawesome/free-solid-svg-icons';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import ComponentGallery from './ComponentGallery';
import KeySpecsPanel from './KeySpecsPanel';
import { getSpecsForComponentType } from '../../config/componentSpecs';
import { getComponentThemeColor } from '../../utils/componentDetailUtils';

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
  onAddToList,
  children
}) => {
  // State for active tab
  const [activeTab, setActiveTab] = useState('description');

  if (!item) {
    return <LoadingSpinner />;
  }

  // Get component theme color
  const themeColor = getComponentThemeColor(componentType);

  // Get specs configuration for this component type
  const specsConfig = getSpecsForComponentType(componentType);

  // No longer needed as we're using ComponentGallery

  // Handle adding item to list
  const handleAddToList = () => {
    if (onAddToList) {
      onAddToList(item);
    }
  };

  // Handle tab switching
  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
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
        <span className={`inline-block text-xs font-semibold text-white bg-${themeColor} px-3 py-1 rounded-full uppercase tracking-wider mb-2`}>
          {item.manufacturer}
        </span>
        <h1 className="text-4xl font-bold text-primary">{item.model}</h1>

        {/* Add to List Button (top right position) */}
        <div className="absolute top-0 right-0">
          <button
            onClick={handleAddToList}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg bg-${themeColor} text-white font-semibold transition-all hover:bg-opacity-90 hover:translate-y-[-2px] hover:shadow-md`}
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
            themeColor={themeColor}
          />

          {/* Key specifications panel */}
          <KeySpecsPanel
            item={item}
            specsConfig={specsConfig}
            themeColor={themeColor}
          />
        </div>

        {/* Right column - Tabbed content */}
        <div className="flex-1"> {/* Removed PT-7 as we moved the header out */}
          {/* Tab navigation */}
          <div className="bg-white rounded-3xl shadow-sm mb-6 flex overflow-hidden">
            <button
              className={`flex-1 py-4 px-6 font-medium transition-colors ${activeTab === 'description' ? `text-${themeColor} border-b-3 border-${themeColor} bg-${themeColor} bg-opacity-5` : 'text-gray-600 hover:bg-gray-50'}`}
              onClick={() => handleTabClick('description')}
            >
              Description
            </button>
            <button
              className={`flex-1 py-4 px-6 font-medium transition-colors ${activeTab === 'specs' ? `text-${themeColor} border-b-3 border-${themeColor} bg-${themeColor} bg-opacity-5` : 'text-gray-600 hover:bg-gray-50'}`}
              onClick={() => handleTabClick('specs')}
            >
              Specifications
            </button>
            <button
              className={`flex-1 py-4 px-6 font-medium transition-colors ${activeTab === 'details' ? `text-${themeColor} border-b-3 border-${themeColor} bg-${themeColor} bg-opacity-5` : 'text-gray-600 hover:bg-gray-50'}`}
              onClick={() => handleTabClick('details')}
            >
              Details
            </button>
            <button
              className={`flex-1 py-4 px-6 font-medium transition-colors ${activeTab === 'documents' ? `text-${themeColor} border-b-3 border-${themeColor} bg-${themeColor} bg-opacity-5` : 'text-gray-600 hover:bg-gray-50'}`}
              onClick={() => handleTabClick('documents')}
            >
              Documents
            </button>
          </div>

          {/* Tab content sections - placeholders for now */}
          <div className={`${activeTab === 'description' ? 'block' : 'hidden'}`}>
            <div className="bg-white rounded-3xl shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100 font-semibold text-primary relative">
                <div className={`absolute top-0 left-0 bottom-0 w-1 bg-${themeColor}`}></div>
                <h2 className="text-xl">Description</h2>
              </div>
              <div className="p-6">
                {/* Description content will be implemented in task 4 */}
                {item.description ? (
                  <div dangerouslySetInnerHTML={{ __html: item.description }} />
                ) : (
                  <p className="text-gray-500">No description available</p>
                )}
              </div>
            </div>
          </div>

          <div className={`${activeTab === 'specs' ? 'block' : 'hidden'}`}>
            <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100 font-semibold text-primary relative flex justify-between items-center">
                <div className={`absolute top-0 left-0 bottom-0 w-1 bg-${themeColor}`}></div>
                <h2 className="text-xl">Technical Specifications</h2>
                <button className={`text-${themeColor} px-3 py-1 text-sm rounded hover:bg-${themeColor} hover:bg-opacity-10`}>
                  Copy JSON
                </button>
              </div>
              <div className="p-6">
                {/* Specs content will be implemented in task 4 */}
                <p>Specifications will appear here</p>
              </div>
            </div>
          </div>

          <div className={`${activeTab === 'details' ? 'block' : 'hidden'}`}>
            <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100 font-semibold text-primary relative">
                <div className={`absolute top-0 left-0 bottom-0 w-1 bg-${themeColor}`}></div>
                <h2 className="text-xl">Details</h2>
              </div>
              <div className="p-6">
                {/* Details content will be implemented in task 4 */}
                <p>Component details will appear here</p>
              </div>
            </div>
          </div>

          <div className={`${activeTab === 'documents' ? 'block' : 'hidden'}`}>
            <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100 font-semibold text-primary relative">
                <div className={`absolute top-0 left-0 bottom-0 w-1 bg-${themeColor}`}></div>
                <h2 className="text-xl">Documents</h2>
              </div>
              <div className="p-6">
                {/* Documents content will be implemented in task 4 */}
                <p>Documents will appear here</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

ComponentDetailTemplate.propTypes = {
  componentType: PropTypes.string.isRequired,
  item: PropTypes.object,
  isRefreshing: PropTypes.bool,
  onRefresh: PropTypes.func,
  onAddToList: PropTypes.func,
  children: PropTypes.node
};

export default ComponentDetailTemplate;