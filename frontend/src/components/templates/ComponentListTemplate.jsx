import React from 'react';
import { Link } from 'react-router-dom';

/**
 * A reusable template for displaying lists of any component type
 *
 * @param {Object} props - Component properties
 * @param {string} props.title - Page title
 * @param {string} props.componentType - Type of component (antennas, cameras, etc.)
 * @param {Array} props.items - Array of items to display
 * @param {Function} props.renderItem - Optional custom render function for list items
 * @param {boolean} props.isRefreshing - Whether data is currently being refreshed
 * @param {Function} props.onRefresh - Function to call to refresh data
 * @param {Object} props.filterOptions - Optional filter options for the API call
 */
function ComponentListTemplate({
  title,
  componentType,
  items = [],
  renderItem,
  isRefreshing = false,
  onRefresh,
  filterOptions = {}
}) {
  // Default item renderer if none is provided
  const defaultRenderItem = (item) => (
    <li key={item.id} className="p-3 hover:bg-gray-100 border-b border-gray-100">
      <Link to={`/components/${componentType}/${item.id}`}
            className="text-primary hover:text-primary-dark">
        {item.manufacturer} {item.model}
      </Link>
    </li>
  );

  // Use the provided renderItem function or fall back to the default
  const renderListItem = renderItem || defaultRenderItem;

  return (
    <div className="w-[90%] max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-primary">{title}</h1>

        {/* Refresh button */}
        {onRefresh && (
          <button
            onClick={() => onRefresh(filterOptions)}
            disabled={isRefreshing}
            className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors disabled:opacity-50"
          >
            {isRefreshing ? 'Refreshing...' : 'Refresh'}
          </button>
        )}
      </div>

      <Link to="/" className="text-primary hover:text-primary-dark mb-6 inline-block">
        ← Back to Home
      </Link>

      <div className="mt-6 bg-white rounded-lg shadow-sm p-6">
        {items.length === 0 ? (
          <p className="text-gray-500">No {componentType} found.</p>
        ) : (
          <ul className="divide-y divide-gray-100">
            {items.map(item => renderListItem(item))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default ComponentListTemplate;