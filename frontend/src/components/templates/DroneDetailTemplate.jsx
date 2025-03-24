import { ROUTES } from '../../routes';import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faPlus } from '@fortawesome/free-solid-svg-icons';
import LoadingSpinner from '../common/LoadingSpinner';
import ComponentGallery from '../detail/ComponentGallery';
import TabContainer from '../detail/TabContainer';
import BuildCompletionMeter from '../detail/BuildCompletionMeter';
import ComponentGrid from '../detail/ComponentGrid';
import ComponentInfoPanel from '../detail/ComponentInfoPanel';
import { getDroneFullSpecs } from '../../config/droneSpecs';
import { getEntityThemeClass } from '../../utils/themeUtils';
import {
  DescriptionTab,
  SpecificationsTab,
  DocumentsTab
} from '../detail/tabs';

/**
 * Template for displaying detailed drone information
 * with gallery, components, and tabbed content sections
 *
 * @param {Object} props Component properties
 * @param {string} props.componentType Type of entity (drones)
 * @param {Object} props.item The drone data to display
 * @param {boolean} props.isRefreshing Whether data is currently being refreshed
 * @param {Function} props.onRefresh Function to call to refresh data
 * @param {Function} props.onAddToList Callback when "Add to List" button is clicked
 */
const DroneDetailTemplate = ({
  componentType,
  item,
  isRefreshing = false,
  onRefresh,
  onAddToList
}) => {
  const [selectedComponent, setSelectedComponent] = useState(null);

  if (!item) {
    return <LoadingSpinner />;
  }

  // Get drone theme color
  const themeClass = getEntityThemeClass(componentType);

  // Get specs configuration for the drone type
  const specsConfig = getDroneFullSpecs();

  // Calculate completion percentage
  const requiredComponents = ['frame', 'motor', 'propeller', 'flight_controller',
    'speed_controller', 'receiver', 'transmitter', 'antenna', 'camera', 'battery'];

  const presentComponents = requiredComponents.filter(comp => item[comp]);
  const completionPercentage = Math.round((presentComponents.length / requiredComponents.length) * 100);

  // Get missing components
  const missingComponents = requiredComponents.filter(comp => !item[comp]);

  // Handle adding item to list
  const handleAddToList = () => {
    if (onAddToList) {
      onAddToList(item);
    }
  };

  // Handle component selection
  const handleComponentSelect = (component) => {
    if (selectedComponent === component) {
      setSelectedComponent(null);
    } else {
      setSelectedComponent(component);
    }
  };

  // Determine the component that was selected
  const getComponentType = (type) => {
    const typeMapping = {
      'frame': 'frames',
      'motor': 'motors',
      'propeller': 'propellers',
      'flight_controller': 'flight_controllers',
      'speed_controller': 'speed_controllers',
      'receiver': 'receivers',
      'transmitter': 'transmitters',
      'camera': 'cameras',
      'antenna': 'antennas',
      'battery': 'propulsion',
    };

    return typeMapping[type] || `${type}s`; // Fallback to adding 's' if not mapped
  };
  const selectedComponentData = selectedComponent ? item[selectedComponent] : null;
  const selectedComponentType = selectedComponent ? getComponentType(selectedComponent) : '';

  return (
    <div className="w-[92%] max-w-[1400px] mx-auto px-4 py-8">
      {/* Back button */}
      <Link
        to={ROUTES.BUILDS.DRONES.LIST}
        className="inline-flex items-center text-primary hover:text-gray-600 mb-6"
      >
        <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
        Back to Builds
      </Link>

      {/* Product header - moved outside columns */}
      <div className="mb-6 relative">
        <span className={`inline-block text-xs font-semibold text-white ${themeClass.bg} px-3 py-1 rounded-full uppercase tracking-wider mb-2`}>
          {item.manufacturer || "Custom Drone"}
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
        {/* Left column - Gallery and Components */}
        <div className="w-full lg:w-5/12 flex flex-col pr-4">
          {/* Image gallery with thumbnails and navigation */}
          <ComponentGallery
            images={item.images}
            alt={`${item.manufacturer || 'Custom'} ${item.model}`}
            componentType={componentType}
          />

          {/* Build completion meter */}
          <BuildCompletionMeter
            percentage={completionPercentage}
            missingComponents={missingComponents}
            themeClass={themeClass}
          />

          {/* Components Grid */}
          <ComponentGrid
            item={item}
            selectedComponent={selectedComponent}
            onSelectComponent={handleComponentSelect}
          />
        </div>

        {/* Right column - Tabbed content */}
        <div className="flex-1 flex flex-col">
          {/* Main drone tabs */}
          <TabContainer
            item={item}
            componentType={componentType}
            descriptionTab={<DescriptionTab item={item} componentType={componentType} />}
            specificationsTab={<SpecificationsTab item={item} specsConfig={specsConfig} componentType={componentType} />}
            documentsTab={<DocumentsTab item={item} componentType={componentType} />}
          />

          {/* Selected component info */}
          {selectedComponentData && (
            <ComponentInfoPanel
              item={selectedComponentData}
              componentType={selectedComponentType}
              isBattery={selectedComponent === 'battery'}
              onClose={() => setSelectedComponent(null)}
            />
          )}
        </div>
      </div>
    </div>
  );
};

DroneDetailTemplate.propTypes = {
  componentType: PropTypes.string.isRequired,
  item: PropTypes.object,
  isRefreshing: PropTypes.bool,
  onRefresh: PropTypes.func,
  onAddToList: PropTypes.func
};

export default DroneDetailTemplate;