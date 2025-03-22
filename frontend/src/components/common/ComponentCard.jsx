import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import PropTypes from 'prop-types';
import { formatSpecValue } from "../../utils/componentDetailUtils";
import { themeClasses } from "../../utils/themeUtils";

/**
 * Reusable component card that supports both list and grid views
 *
 * @param {Object} props Component properties
 * @param {Object} props.item The component data to display
 * @param {string} props.viewMode Display mode ('list' or 'grid')
 * @param {string} props.componentType Type of component (antennas, cameras, etc.)
 * @param {string} props.detailUrl URL to the detail page
 * @param {Object} props.specsConfig Configuration for which specs to display
 * @param {Function} props.onAddToList Callback when add to list button is clicked
 */
const ComponentCard = ({
  item,
  viewMode = 'list',
  componentType,
  detailUrl,
  specsConfig,
  onAddToList
}) => {
  if (!item) return null;

  // Get the color theme based on component type
  const getComponentTheme = () => {
    const themes = {
      antennas: 'antenna',
      cameras: 'video',
      frames: 'frame',
      motors: 'propulsion',
      propellers: 'propulsion',
      receivers: 'control',
      transmitters: 'video',
      stacks: 'control',
      flight_controllers: 'control',
      speed_controllers: 'control',
      drones: 'drone'
    };

    return themes[componentType] || 'antenna';
  };

  const theme = getComponentTheme();
  const themeClass = themeClasses[theme] || themeClasses.primary;
  const isDrone = componentType === 'drones';

  // Get the primary image URL or a placeholder
  const getImageUrl = () => {
    if (item.images && item.images.length > 0) {
      // Find image with order=0 or the first image
      const primaryImage = item.images.find(img => img.order === 0) || item.images[0];
      return primaryImage.image;
    }
    return '/api/placeholder/180/180'; // Placeholder if no image
  };

  // Function to render specification value based on type
  const renderSpecValue = (spec, value) => {

      let formattedValue;
      if (spec.formatter) {
        formattedValue = spec.formatter(value, item);
      } else if (spec.unit) {
        formattedValue = (value) ? `${value} ${spec.unit}` : 'N/A';
      } else {
        formattedValue = formatSpecValue(value);
      }

    return formattedValue;
  };

  // Add to list handler with stop propagation to prevent navigation
  const handleAddToList = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (onAddToList) onAddToList(item);
  };

  // Render list view
  if (viewMode === 'list') {
    return (
        <Link
          to={detailUrl}
          className={`bg-white rounded-2xl overflow-hidden shadow-md transition-all duration-300 mb-4 flex flex-col border-t-4 border border-gray-200 ${themeClass.borderTop} hover:shadow-lg hover:-translate-y-1`}>
          <div className="flex items-center p-6 border-b border-gray-100">
            <div className="flex-1">
              {item.manufacturer ? (
                <span className={`inline-block text-xs font-semibold text-white ${themeClass.bg} px-3 py-1 rounded-full uppercase tracking-wider mb-2`}>
                  {item.manufacturer}
                </span>
              ) : isDrone ? (
                <span className={`inline-block text-xs font-semibold text-white ${themeClass.bg} px-3 py-1 rounded-full uppercase tracking-wider mb-2`}>
                  Custom Drone
                </span>
              ) : null}
              <h3 className="text-xl font-bold text-primary leading-snug">
                {item.model}
              </h3>
            </div>
            <button
                onClick={handleAddToList}
                className={themeClass.combined.actionButton + " px-5 py-2 rounded-lg font-semibold text-sm flex items-center gap-2 transition-all"}>
              <FontAwesomeIcon icon={faPlus}/>
              Add to List
            </button>
          </div>

          <div className="flex relative">
            <div className="w-56 min-w-56 p-6 flex items-center justify-center bg-gray-50 relative">
              <div className={`absolute top-0 bottom-0 right-0 w-0.5 ${themeClass.bg}`}></div>
              <img
                  src={getImageUrl()}
                  alt={`${item.manufacturer || ''} ${item.model}`}
                  className="max-w-full max-h-full object-contain transition-transform duration-300 group-hover:scale-105"
              />
            </div>

            <div className="flex-1 p-6">
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
                {isDrone ? 'SPECIFICATIONS' : 'SPECIFICATIONS'}
              </div>
              <div className="grid grid-cols-3 gap-5">
               {specsConfig.slice(0, 6).map((spec, index) => {
                  const value = spec.path.split('.').reduce((obj, key) =>
                    obj && obj[key] !== undefined ? obj[key] : null, item);

                  return renderSpecValue(spec, value) !== "N/A" ? (
                      <div
                          key={index}
                          className="bg-gray-50 p-2 rounded-lg transition-all border hover:bg-gray-100 hover:-translate-y-0.5"
                      >
                        <div className="flex items-center text-xs text-gray-500 mb-1 gap-1">
                          {spec.icon && (
                              <FontAwesomeIcon icon={spec.icon} className={themeClass.text}/>
                          )}
                          {spec.label}
                        </div>
                        <div className="font-semibold text-primary">
                          {renderSpecValue(spec, value)}
                        </div>
                      </div>
                  ) : null;
                })}
              </div>
            </div>
          </div>

          <div className="bg-gray-50 p-4 border-t border-gray-100 relative">
            <div className={`absolute top-0 left-0 right-0 h-0.5 ${themeClass.bg}`}></div>
            <div className="flex flex-wrap gap-2">
              {item.tags && item.tags.map((tag, index) => (
                  <span key={index}
                        className="bg-white text-gray-600 text-xs py-1 px-3 rounded-full border border-gray-200 hover:bg-gray-100 transition-colors">
                {tag}
              </span>
              ))}
            </div>
          </div>
        </Link>
    );
  }

  // Render grid view
  return (
      <Link
        to={detailUrl}
        className={`bg-white rounded-lg overflow-hidden shadow-sm transition-all duration-300 flex flex-col border-t-4 ${themeClass.borderTop}`}>
        <div className="p-6 h-52 min-h-52 flex items-center justify-center bg-gray-50">
        <img
          src={getImageUrl()}
          alt={`${item.manufacturer || ''} ${item.model}`}
          className="max-w-[90%] max-h-[90%] object-contain"
        />
      </div>

      <div className="p-6 flex flex-col flex-grow">
        <h3 className="text-lg font-semibold text-primary mb-3">
          {item.manufacturer ? `${item.manufacturer} ${item.model}` : item.model}
        </h3>

        <div className="grid grid-cols-2 gap-3 mb-6">
          {specsConfig.slice(0, 4).map((spec, index) => {
            const value = spec.path.split('.').reduce((obj, key) =>
              obj && obj[key] !== undefined ? obj[key] : null, item);

            return renderSpecValue(spec, value) !== "N/A" ? (
              <div key={index} className="flex flex-col">
                <span className="text-xs text-gray-500">{spec.label}</span>
                <span className="font-medium">{renderSpecValue(spec, value)}</span>
              </div>
            ): null;
          })}
        </div>

        <div className="flex justify-between mt-auto">
          <Link
            to={detailUrl}
            className={`${themeClass.text} text-sm font-medium hover:underline`}
          >
            View Details
          </Link>

          <button
            onClick={handleAddToList}
            className={`${themeClass.text} text-sm font-medium hover:underline flex items-center gap-1`}
          >
            <FontAwesomeIcon icon={faPlus} />
            Add to List
          </button>
        </div>
      </div>
    </Link>
  );
};

ComponentCard.propTypes = {
  item: PropTypes.object.isRequired,
  viewMode: PropTypes.oneOf(['list', 'grid']),
  componentType: PropTypes.string.isRequired,
  detailUrl: PropTypes.string.isRequired,
  specsConfig: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string.isRequired,
      path: PropTypes.string.isRequired,
      icon: PropTypes.object,
      unit: PropTypes.string,
      formatter: PropTypes.func
    })
  ).isRequired,
  onAddToList: PropTypes.func
};

export default ComponentCard;