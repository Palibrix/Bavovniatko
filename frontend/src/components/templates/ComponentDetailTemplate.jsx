import React from 'react';
import { Link } from 'react-router-dom';

/**
 * A reusable template for displaying details of any component type
 *
 * @param {Object} props - Component properties
 * @param {string} props.componentType - Type of component (antennas, cameras, etc.)
 * @param {Object} props.item - The component data to display
 * @param {Function} props.renderDetails - Function to render the specific details section
 * @param {boolean} props.isRefreshing - Whether data is currently being refreshed
 * @param {Function} props.onRefresh - Function to call to refresh data
 */
function ComponentDetailTemplate({
  componentType,
  item,
  renderDetails,
  isRefreshing = false,
  onRefresh
}) {
  return (
    <div className="w-[90%] max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-primary">{item.manufacturer} {item.model}</h1>

        {/* Refresh button */}
        {onRefresh && (
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors disabled:opacity-50"
          >
            {isRefreshing ? 'Refreshing...' : 'Refresh'}
          </button>
        )}
      </div>

      <Link to={`/components/${componentType}`} className="text-primary hover:text-primary-dark mb-6 inline-block">
        ← Back to {componentType}
      </Link>

      <div className="mt-6 bg-white rounded-lg shadow-sm p-6">
        <div className="mb-6 pb-4 border-b border-gray-100">
          <h2 className="text-xl font-semibold mb-3">Description</h2>
          {item.description ? (
            <div dangerouslySetInnerHTML={{ __html: item.description }} />
          ) : (
            <p className="text-gray-500">No description available</p>
          )}
        </div>

        {/* Render component-specific details using the provided function */}
        <div className="mb-6 pb-4 border-b border-gray-100">
          <h2 className="text-xl font-semibold mb-3">Specifications</h2>
          {renderDetails(item)}
        </div>

        {/* Images section - common to all components */}
        <div>
          <h2 className="text-xl font-semibold mb-3">Images</h2>
          {item.images && item.images.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {item.images.map((image, index) => (
                <img
                  key={index}
                  src={image.image}
                  alt={`${item.manufacturer} ${item.model}`}
                  className="rounded-md shadow-sm hover:shadow-md transition-shadow"
                />
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No images available</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ComponentDetailTemplate;