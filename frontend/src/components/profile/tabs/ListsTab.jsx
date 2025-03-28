import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLayerGroup, faCalendarAlt, faClock, faEye, faEdit, faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import LoadingSpinner from '../../common/LoadingSpinner';
import ErrorMessage from '../../common/ErrorMessage';
import { listsApi } from '../../../services/api';
import Toast from '../../common/Toast';

const ListsTab = ({ profileData }) => {
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState({ visible: false, message: '', type: '' });

  // Fetch real list data
  useEffect(() => {
    const fetchLists = async () => {
      try {
        setLoading(true);
        const response = await listsApi.getUserLists();

        // Check if response is paginated (has results property)
        const listsData = response.results || response;

        // Ensure we have an array
        setLists(Array.isArray(listsData) ? listsData : []);

        console.log('Lists data:', listsData); // For debugging
        setLoading(false);
      } catch (err) {
        console.error('Error fetching lists:', err);
        setError(err.message || 'Failed to load lists');
        setLoading(false);
      }
    };

    fetchLists();
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  const handleCreateList = () => {
    // This would open a modal or navigate to create list page
    setToast({
      visible: true,
      message: 'Create list functionality will be implemented soon',
      type: 'info'
    });
  };

  const handleViewList = (listId) => {
    // This would navigate to list detail page
    setToast({
      visible: true,
      message: 'View list functionality will be implemented soon',
      type: 'info'
    });
  };

  const handleEditList = (listId) => {
    // This would open edit modal
    setToast({
      visible: true,
      message: 'Edit list functionality will be implemented soon',
      type: 'info'
    });
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-primary">Your Lists</h2>
        <button
          onClick={handleCreateList}
          className="px-4 py-2 bg-secondary text-white rounded-lg hover:bg-opacity-90 transition-colors flex items-center gap-2"
        >
          <FontAwesomeIcon icon={faPlus} />
          Create New List
        </button>
      </div>

      {lists.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center shadow-sm">
          <div className="text-5xl text-gray-300 mb-6">
            <FontAwesomeIcon icon={faLayerGroup} />
          </div>
          <h3 className="text-xl font-semibold text-primary mb-2">No Lists Yet</h3>
          <p className="text-gray-500 mb-6 max-w-md mx-auto">
            Create your first list to organize drone components for your builds or to save items for later.
          </p>
          <button
            onClick={handleCreateList}
            className="px-4 py-2 bg-secondary text-white rounded-lg hover:bg-opacity-90 transition-colors"
          >
            Create Your First List
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {lists.map(list => (
            <div key={list.id} className="bg-white rounded-xl shadow-sm overflow-hidden border-t-4 border-t-primary transition-all hover:-translate-y-1 hover:shadow-md">
              <div className="p-5 border-b border-gray-100">
                <h3 className="text-lg font-semibold text-primary">{list.name}</h3>
                {list.description && (
                  <p className="text-sm text-gray-500 mt-1">{list.description}</p>
                )}
              </div>
              <div className="p-5">
                <div className="space-y-2 mb-5">
                  <div className="flex items-center text-sm text-gray-500">
                    <FontAwesomeIcon icon={faLayerGroup} className="w-4 text-center mr-3 text-primary" />
                    <span>{list.parts_count || 0} items</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <FontAwesomeIcon icon={faCalendarAlt} className="w-4 text-center mr-3 text-primary" />
                    <span>Created: {formatDate(list.created_at)}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <FontAwesomeIcon icon={faClock} className="w-4 text-center mr-3 text-primary" />
                    <span>Last updated: {formatDate(list.updated_at)}</span>
                  </div>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={() => handleViewList(list.id)}
                    className="flex-1 py-2 px-3 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors text-sm font-medium flex items-center justify-center gap-2"
                  >
                    <FontAwesomeIcon icon={faEye} />
                    View
                  </button>
                  <button
                    onClick={() => handleEditList(list.id)}
                    className="flex-1 py-2 px-3 border border-primary text-primary rounded-md hover:bg-gray-50 transition-colors text-sm font-medium flex items-center justify-center gap-2"
                  >
                    <FontAwesomeIcon icon={faEdit} />
                    Edit
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {toast.visible && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast({ ...toast, visible: false })}
        />
      )}
    </div>
  );
};

ListsTab.propTypes = {
  profileData: PropTypes.object.isRequired
};

export default ListsTab;