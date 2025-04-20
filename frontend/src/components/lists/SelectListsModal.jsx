import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faCheck, faPlus, faSpinner } from '@fortawesome/free-solid-svg-icons';
import { listsApi } from '../../services/api';
import CreateListModal from './CreateListModal';

/**
 * Modal for selecting which lists a component should be in
 *
 * @param {Object} props Component properties
 * @param {boolean} props.isOpen Whether the modal is open
 * @param {Function} props.onClose Callback when modal is closed
 * @param {string} props.componentType Type of component (antennas, cameras, etc.)
 * @param {number} props.componentId ID of the component
 * @param {string} props.componentName Display name of the component
 * @param {Function} props.onSuccess Callback when lists are updated successfully
 */
const SelectListsModal = ({
  isOpen,
  onClose,
  componentType,
  componentId,
  componentName,
  onSuccess
}) => {
  // State
  const [lists, setLists] = useState([]);
  const [selectedListIds, setSelectedListIds] = useState([]);
  const [initialSelectedIds, setInitialSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Create list modal state
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Fetch lists when modal opens
  useEffect(() => {
    if (isOpen) {
      fetchLists();
    }
  }, [isOpen]);

  const fetchLists = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all user lists
      const response = await listsApi.getUserLists();
      const userLists = Array.isArray(response) ? response : (response.results || []);

      // For each list, determine if the component is already in it
      const listsWithMembership = await Promise.all(
        userLists.map(async (list) => {
          try {
            // Get components of this type in the list
            const items = await listsApi.getListItemsByType(list.id, componentType);

            // Check if this component is in the list
            const isInList = items.some(item =>
              item.component_id === componentId &&
              item.component_type === componentType
            );

            return {
              ...list,
              isInList
            };
          } catch (err) {
            console.error(`Error checking if component is in list ${list.id}:`, err);
            return {
              ...list,
              isInList: false
            };
          }
        })
      );

      setLists(listsWithMembership);

      // Set initially selected lists
      const initialIds = listsWithMembership
        .filter(list => list.isInList)
        .map(list => list.id);

      setSelectedListIds(initialIds);
      setInitialSelectedIds(initialIds);

      setLoading(false);
    } catch (err) {
      console.error('Error fetching lists:', err);
      setError('Failed to load your lists. Please try again.');
      setLoading(false);
    }
  };

  const handleToggleList = (listId) => {
    setSelectedListIds(prev => {
      if (prev.includes(listId)) {
        return prev.filter(id => id !== listId);
      } else {
        return [...prev, listId];
      }
    });
  };

  const handleCreateListSuccess = (newList) => {
    // Add the new list to our lists array
    setLists(prev => [{
      ...newList,
      isInList: false
    }, ...prev]);

    // Auto-select the new list
    setSelectedListIds(prev => [...prev, newList.id]);

    // Close the create modal
    setShowCreateModal(false);
  };

  const handleSave = async () => {
    try {
      setSubmitting(true);
      setError(null);

      // Call the backend to update which lists the component is in
      const result = await listsApi.setComponentLists(
        componentType,
        componentId,
        selectedListIds
      );

      setSubmitting(false);

      // Call the success callback with the result
      if (onSuccess) {
        onSuccess(result);
      }

      // Close the modal
      onClose();
    } catch (err) {
      console.error('Error updating lists:', err);
      setError('Failed to update lists. Please try again.');
      setSubmitting(false);
    }
  };

  // Don't render if modal is not open
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-md mx-4 overflow-hidden">
        <div className="flex justify-between items-center px-6 py-4 border-b border-gray-100">
          <h2 className="text-xl font-semibold text-primary">Add to Lists</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            aria-label="Close"
            disabled={submitting}
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>

        <div className="p-6">
          <p className="text-gray-600 mb-4">
            Select which lists you want to add <strong>{componentName}</strong> to:
          </p>

          {error && (
            <div className="bg-red-50 text-red-700 p-3 rounded-lg mb-4 text-sm">
              {error}
            </div>
          )}

          {loading ? (
            <div className="py-10 flex justify-center">
              <FontAwesomeIcon icon={faSpinner} spin size="lg" className="text-primary" />
            </div>
          ) : (
            <>
              <div className="max-h-64 overflow-y-auto border rounded-lg mb-4">
                {lists.length === 0 ? (
                  <div className="p-4 text-center text-gray-500">
                    You don't have any lists yet. Create your first list below.
                  </div>
                ) : (
                  <ul className="divide-y divide-gray-100">
                    {lists.map(list => (
                      <li key={list.id} className="p-0">
                        <label className="flex items-center p-3 cursor-pointer hover:bg-gray-50">
                          <input
                            type="checkbox"
                            checked={selectedListIds.includes(list.id)}
                            onChange={() => handleToggleList(list.id)}
                            className="form-checkbox h-5 w-5 text-primary rounded border-gray-300 focus:ring-primary"
                          />
                          <div className="ml-3 flex-1">
                            <span className="block font-medium text-primary">{list.name}</span>
                            {list.description && (
                              <span className="block text-sm text-gray-500">{list.description}</span>
                            )}
                            <span className="text-xs text-gray-400 mt-1 block">
                              {list.isInList ? (
                                <span className="text-green-600">
                                  Component is already in this list
                                </span>
                              ) : (
                                <span>Component is not in this list</span>
                              )}
                            </span>
                          </div>
                        </label>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <button
                type="button"
                onClick={() => setShowCreateModal(true)}
                className="mb-6 flex items-center text-primary hover:text-opacity-80 px-3 py-2 rounded-lg border border-primary hover:bg-gray-50"
              >
                <FontAwesomeIcon icon={faPlus} className="mr-2" />
                Create New List
              </button>
            </>
          )}

          <div className="flex justify-end gap-3 mt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
              disabled={submitting}
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSave}
              className="px-4 py-2 bg-primary text-white rounded-md hover:bg-opacity-90 flex items-center gap-2"
              disabled={submitting ||
                (selectedListIds.length === initialSelectedIds.length &&
                selectedListIds.every(id => initialSelectedIds.includes(id)))}
            >
              {submitting ? (
                <>
                  <FontAwesomeIcon icon={faSpinner} spin />
                  <span>Saving...</span>
                </>
              ) : (
                <>
                  <FontAwesomeIcon icon={faCheck} />
                  <span>Save</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Create List Modal */}
      <CreateListModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSuccess={handleCreateListSuccess}
      />
    </div>
  );
};

SelectListsModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  componentType: PropTypes.string.isRequired,
  componentId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  componentName: PropTypes.string.isRequired,
  onSuccess: PropTypes.func
};

export default SelectListsModal;