import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons';

import ComponentCard from '../common/ComponentCard';
import ListToolbar from '../common/ListToolbar';
import Pagination from '../common/Pagination';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

/**
 * Template for displaying a list of components with filtering, sorting, and pagination
 *
 * @param {Object} props Component properties
 * @param {string} props.title Page title
 * @param {string} props.componentType Type of component (antennas, cameras, etc.)
 * @param {Array} props.items Array of items to display
 * @param {Object} props.pagination Pagination information (page, totalPages, totalCount)
 * @param {Function} props.onPageChange Callback when page changes
 * @param {string} props.sortBy Current sort field
 * @param {Function} props.onSortChange Callback when sort changes
 * @param {boolean} props.isRefreshing Whether data is currently being refreshed
 * @param {Function} props.onRefresh Function to call to refresh data
 * @param {Object} props.specsConfig Configuration for which specs to display for this component type
 */
const ComponentListTemplate = ({
  title,
  componentType,
  items = [],
  pagination = { page: 1, totalPages: 1, totalCount: 0 },
  onPageChange,
  sortBy = 'name-asc',
  onSortChange,
  isRefreshing = false,
  onRefresh,
  specsConfig,
  filterSidebar
}) => {
  const [viewMode, setViewMode] = useState('list');

  // Get the appropriate theme color based on component type
  const getThemeColor = () => {
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
      speed_controllers: 'control'
    };

    return themes[componentType] || 'primary';
  };

  const themeColor = getThemeColor();

  // Handle adding an item to the user's list (placeholder function for now)
  const handleAddToList = (item) => {
    console.log(`Added ${item.manufacturer} ${item.model} to list`);
    // This would be implemented with actual list functionality
  };

  // Load saved view mode from localStorage
  useEffect(() => {
    const savedViewMode = localStorage.getItem(`${componentType}-view-mode`);
    if (savedViewMode) {
      setViewMode(savedViewMode);
    }
  }, [componentType]);

  // Save view mode to localStorage when it changes
  const handleViewModeChange = (mode) => {
    setViewMode(mode);
    localStorage.setItem(`${componentType}-view-mode`, mode);
  };

  // If items is null, show loading spinner
  if (!items && isRefreshing) {
    return <LoadingSpinner />;
  }

  return (
    <div className="w-[90%] max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-3xl font-bold text-primary relative pb-2 mb-1">
            {title}
            <span className={`absolute bottom-0 left-0 w-14 h-1 bg-${themeColor}`}></span>
          </h1>
          <Link to="/" className="text-primary hover:text-gray-600 inline-flex items-center">
            <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
            Back to Home
          </Link>
        </div>

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

      <div className="flex flex-col md:flex-row gap-8">
        {/* Filter sidebar placeholder - will be filled later */}
        {filterSidebar && (
          <div className="w-full md:w-72 md:flex-shrink-0">
            {filterSidebar}
          </div>
        )}

        {/* Main content */}
        <div className="flex-1">
          {/* Toolbar */}
          <ListToolbar
            totalCount={pagination.totalCount}
            shownCount={items.length}
            viewMode={viewMode}
            onViewModeChange={handleViewModeChange}
            sortBy={sortBy}
            onSortChange={onSortChange}
          />

          {items.length === 0 ? (
            <div className="bg-white rounded-lg p-8 text-center shadow-sm">
              <div className="text-gray-400 text-5xl mb-4">
                <FontAwesomeIcon icon={getComponentIcon(componentType)} />
              </div>
              <h3 className="text-xl font-semibold text-primary mb-2">No {title.toLowerCase()} found</h3>
              <p className="text-gray-600 mb-4">
                {filterSidebar
                  ? 'Try adjusting your filter criteria to see more results.'
                  : 'There are no items to display.'}
              </p>
              {filterSidebar && (
                <button
                  className="px-4 py-2 text-primary border border-primary rounded-md hover:bg-primary hover:text-white transition-colors"
                  onClick={() => {/* Clear filters function will go here */}}
                >
                  Clear All Filters
                </button>
              )}
            </div>
          ) : (
            <>
              {/* List view */}
              {viewMode === 'list' && (
                <div className="space-y-6">
                  {items.map(item => (
                    <ComponentCard
                      key={item.id}
                      item={item}
                      viewMode="list"
                      componentType={componentType}
                      detailUrl={`/components/${componentType}/${item.id}`}
                      specsConfig={specsConfig}
                      onAddToList={handleAddToList}
                    />
                  ))}
                </div>
              )}

              {/* Grid view */}
              {viewMode === 'grid' && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {items.map(item => (
                    <ComponentCard
                      key={item.id}
                      item={item}
                      viewMode="grid"
                      componentType={componentType}
                      detailUrl={`/components/${componentType}/${item.id}`}
                      specsConfig={specsConfig}
                      onAddToList={handleAddToList}
                    />
                  ))}
                </div>
              )}

              {/* Pagination */}
              {pagination.totalPages > 1 && (
                <Pagination
                  currentPage={pagination.page}
                  totalPages={pagination.totalPages}
                  onPageChange={onPageChange}
                  themeColor={themeColor}
                />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

// Helper function to get the appropriate icon for the component type
const getComponentIcon = (componentType) => {
  // This would return the appropriate FontAwesome icon based on component type
  // Implementation depends on what icons you choose to use
  return faArrowLeft; // Placeholder
};

ComponentListTemplate.propTypes = {
  title: PropTypes.string.isRequired,
  componentType: PropTypes.string.isRequired,
  items: PropTypes.array,
  pagination: PropTypes.shape({
    page: PropTypes.number.isRequired,
    totalPages: PropTypes.number.isRequired,
    totalCount: PropTypes.number.isRequired
  }),
  onPageChange: PropTypes.func,
  sortBy: PropTypes.string,
  onSortChange: PropTypes.func,
  isRefreshing: PropTypes.bool,
  onRefresh: PropTypes.func,
  specsConfig: PropTypes.array.isRequired,
  filterSidebar: PropTypes.node
};

export default ComponentListTemplate;