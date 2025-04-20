import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLayerGroup, faCalendarAlt, faSyncAlt, faTrash, faEdit } from '@fortawesome/free-solid-svg-icons';

/**
 * Header component for list detail page
 */
const ListDetailHeader = ({ list, onRefresh, onEdit }) => {
  // Format date in a readable way
  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-6 border-t-4 border-t-primary">
      <div className="p-6">
        <div className="flex justify-between items-start mb-2">
          <h1 className="text-2xl font-bold text-primary">{list.name}</h1>

          <div className="flex gap-2">
            {onEdit && (
              <button
                onClick={onEdit}
                className="text-primary hover:bg-gray-100 p-2 rounded-md flex items-center gap-1"
                aria-label="Edit list"
                title="Edit list"
              >
                <FontAwesomeIcon icon={faEdit} />
                <span className="text-sm">Edit</span>
              </button>
            )}

            {onRefresh && (
              <button
                onClick={onRefresh}
                className="text-primary hover:text-gray-600 p-2"
                aria-label="Refresh list"
                title="Refresh list"
              >
                <FontAwesomeIcon icon={faSyncAlt} />
              </button>
            )}
          </div>
        </div>

        {list.description && (
          <p className="text-gray-600 mb-4">{list.description}</p>
        )}

        <div className="flex flex-wrap gap-4 text-sm text-gray-500">
          <div className="flex items-center">
            <FontAwesomeIcon icon={faLayerGroup} className="mr-2 text-primary" />
            <span>{list.parts_count} components</span>
          </div>

          <div className="flex items-center">
            <FontAwesomeIcon icon={faCalendarAlt} className="mr-2 text-primary" />
            <span>Created on {formatDate(list.created_at)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

ListDetailHeader.propTypes = {
  list: PropTypes.object.isRequired,
  onRefresh: PropTypes.func,
  onDelete: PropTypes.func,
  onEdit: PropTypes.func
};

export default ListDetailHeader;