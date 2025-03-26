import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLayerGroup, faCalendarAlt, faClock, faEye, faEdit, faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import LoadingSpinner from '../../common/LoadingSpinner';
import ErrorMessage from '../../common/ErrorMessage';
import Toast from '../../common/Toast';
import { listsApi } from '../../../services/api';
import CreateListModal from '../CreateListModal';

const ListsTab = ({ profileData }) => {
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [toast, setToast] = useState({ message: '', type: '', visible: false });

  useEffect(() => {
    fetchLists();
  }, []);

  const fetchLists = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await listsApi.getUserLists();
      setLists(response);
    } catch (err) {
      console.error('Error fetching lists:', err);
      setError('Failed to load lists. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateList = () => {
    setShowCreateModal(true);
  };

  const handleCreateSuccess = (newList) => {
    setLists(prev => [newList, ...prev]);
    setShowCreateModal(false);
    setToast({
      message: 'List created successfully',
      type: 'success',
      visible: true
    });
  };

  const handleListDelete = async (listId) => {
    // Confirm deletion
    if (!window.confirm('Are you sure you want to delete this list?')) {
      return;
    }

    try {
      await listsApi.deleteList(listId);
      // Remove from local state
      setLists(prev => prev.filter(list => list.id !== listId));
      setToast({
        message: 'List deleted successfully',
        type: 'success',
        visible: true
      });
    } catch (err) {
      console.error('Error deleting list:', err);
      setToast({
        message: 'Failed to delete list',
        type: 'error',
        visible: true
      });
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchLists} />;

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
                <div className="flex gap-2">
                  <button className="flex-1 py-2 px-3 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors text-sm font-medium flex items-center justify-center gap-2">
                    <FontAwesomeIcon icon={faEye} />
                    View
                  </button>
                  <button className="flex-1 py-2 px-3 border border-primary text-primary rounded-md hover:bg-gray-50 transition-colors text-sm font-medium flex items-center justify-center gap-2">
                    <FontAwesomeIcon icon={faEdit} />
                    Edit
                  </button>
                  <button
                    onClick={() => handleListDelete(list.id)}
                    className="p-2 text-gray-500 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors"
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {showCreateModal && (
        <CreateListModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleCreateSuccess}
        />
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