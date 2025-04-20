import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLayerGroup, faSearch } from '@fortawesome/free-solid-svg-icons';
import ComponentCard from '../common/ComponentCard';
import { getKeySpecsForComponentType } from '../../config/componentSpecs';
import { ROUTES } from '../../routes';

/**
 * Grid or list view of components in a list
 */
const COMPONENT_TYPE_MAPPING = {
  'antenna': 'antennas',
  'camera': 'cameras',
  'frame': 'frames',
  'motor': 'motors',
  'propeller': 'propellers',
  'receiver': 'receivers',
  'transmitter': 'transmitters',
  'flight_controller': 'flight_controllers',
  'speed_controller': 'speed_controllers',
  'stack': 'stacks'
};

const ListItemGrid = ({
  items,
  viewMode,
  onRemoveItem,
  emptyState
}) => {
  // Convert component type from singular to plural form
  const getPluralComponentType = (type) => {
    return COMPONENT_TYPE_MAPPING[type] || `${type}s`;
  };

  // If there are no items, show empty state
  if (!items || items.length === 0) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-sm">
        <div className="text-5xl text-gray-300 mb-6">
          <FontAwesomeIcon icon={faLayerGroup} />
        </div>
        <h3 className="text-xl font-semibold text-primary mb-2">
          {emptyState.title || "No components found"}
        </h3>
        <p className="text-gray-500 mb-6 max-w-md mx-auto">
          {emptyState.message || "Try adjusting your filters or add components to this list."}
        </p>
        <div className="flex justify-center gap-4">
          <Link
            to={ROUTES.HOME}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 transition-colors"
          >
            <FontAwesomeIcon icon={faSearch} className="mr-2" />
            Browse Components
          </Link>
        </div>
      </div>
    );
  }

    // Handler to create the correct route for a component
  const getComponentRoute = (item) => {
    const componentType = getPluralComponentType(item.component_type);
    const componentId = item.component_id;

    // Get the route based on component type
    let route = '';
    switch (componentType) {
      case 'antennas':
        route = ROUTES.COMPONENTS.ANTENNAS.DETAIL;
        break;
      case 'cameras':
        route = ROUTES.COMPONENTS.CAMERAS.DETAIL;
        break;
      case 'frames':
        route = ROUTES.COMPONENTS.FRAMES.DETAIL;
        break;
      case 'motors':
        route = ROUTES.COMPONENTS.MOTORS.DETAIL;
        break;
      case 'propellers':
        route = ROUTES.COMPONENTS.PROPELLERS.DETAIL;
        break;
      case 'receivers':
        route = ROUTES.COMPONENTS.RECEIVERS.DETAIL;
        break;
      case 'flight_controllers':
        route = ROUTES.COMPONENTS.FLIGHT_CONTROLLERS.DETAIL;
        break;
      case 'speed_controllers':
        route = ROUTES.COMPONENTS.SPEED_CONTROLLERS.DETAIL;
        break;
      case 'transmitters':
        route = ROUTES.COMPONENTS.TRANSMITTERS.DETAIL;
        break;
      default:
        return '#';
    }

    return route.replace(':id', componentId);
  };

  return (
    <div className={viewMode === 'grid'
      ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      : "space-y-6"
    }>
      {items.map((item, index) => {
        // Convert component type to plural form for compatibility
        const pluralComponentType = getPluralComponentType(item.component_type);

        // Get the specs config for this component type
        const specsConfig = getKeySpecsForComponentType(pluralComponentType);

        const componentData = item.component_data
        componentData.image_url = item.image_url || undefined

        return (
          <ComponentCard
            key={`${item.component_type}-${item.component_id}-${index}`}
            item={componentData}
            viewMode={viewMode}
            entityType={pluralComponentType}
            detailUrlTemplate={getComponentRoute(item)}
            specsConfig={specsConfig}
            isInList={true}
            onRemoveFromList={() => onRemoveItem(item)}
          />
        );
      })}
    </div>
  );
};

ListItemGrid.propTypes = {
  items: PropTypes.arrayOf(PropTypes.shape({
    component_type: PropTypes.string.isRequired,
    component_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    display_name: PropTypes.string.isRequired,
    image_url: PropTypes.string,
    added_at: PropTypes.string
  })),
  viewMode: PropTypes.oneOf(['list', 'grid']).isRequired,
  onRemoveItem: PropTypes.func,
  emptyState: PropTypes.shape({
    title: PropTypes.string,
    message: PropTypes.string
  })
};

ListItemGrid.defaultProps = {
  emptyState: {
    title: "No components found",
    message: "Try adjusting your filters or add components to this list."
  }
};

export default ListItemGrid;