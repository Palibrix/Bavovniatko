import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faList, faTh } from '@fortawesome/free-solid-svg-icons';

/**
 * Toolbar component for list views with view toggle and sorting options
 *
 * @param {Object} props Component properties
 * @param {number} props.totalCount Total number of items
 * @param {number} props.shownCount Number of items being shown
 * @param {string} props.viewMode Current view mode (list or grid)
 * @param {Function} props.onViewModeChange Callback when view mode changes
 * @param {string} props.sortBy Current sort field
 * @param {Function} props.onSortChange Callback when sort changes
 * @param {Array} props.sortOptions Available sort options
 */
const ListToolbar = ({
  totalCount,
  shownCount,
  viewMode = 'list',
  onViewModeChange,
  sortBy = 'name-asc',
  onSortChange,
  sortOptions = [
    { value: 'name-asc', label: 'Name: A to Z' },
    { value: 'name-desc', label: 'Name: Z to A' },
    { value: 'newest', label: 'Newest first' },
    { value: 'oldest', label: 'Oldest first' }
  ]
}) => {
  return (
    <div className="flex justify-between items-center mb-6 p-4 bg-white rounded-lg shadow-sm">
      <div className="text-sm text-gray-600">
        Showing <strong>{shownCount}</strong> of <strong>{totalCount}</strong> items
      </div>

      <div className="flex items-center gap-4">
        <div className="flex bg-gray-100 rounded-md overflow-hidden">
          <button
            onClick={() => onViewModeChange('list')}
            className={`flex items-center py-2 px-3 text-sm ${
              viewMode === 'list' 
                ? 'bg-primary text-white' 
                : 'text-gray-700 hover:bg-gray-200'
            }`}
          >
            <FontAwesomeIcon icon={faList} className="mr-2" />
            <span>List</span>
          </button>

          <button
            onClick={() => onViewModeChange('grid')}
            className={`flex items-center py-2 px-3 text-sm ${
              viewMode === 'grid' 
                ? 'bg-primary text-white' 
                : 'text-gray-700 hover:bg-gray-200'
            }`}
          >
            <FontAwesomeIcon icon={faTh} className="mr-2" />
            <span>Grid</span>
          </button>
        </div>

        <select
          value={sortBy}
          onChange={(e) => onSortChange(e.target.value)}
          className="py-2 px-3 border border-gray-300 rounded-md text-sm text-gray-700 bg-white"
        >
          {sortOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

ListToolbar.propTypes = {
  totalCount: PropTypes.number.isRequired,
  shownCount: PropTypes.number.isRequired,
  viewMode: PropTypes.oneOf(['list', 'grid']),
  onViewModeChange: PropTypes.func.isRequired,
  sortBy: PropTypes.string,
  onSortChange: PropTypes.func.isRequired,
  sortOptions: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired
    })
  )
};

export default ListToolbar;