import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faCheck, faTrash } from '@fortawesome/free-solid-svg-icons';
import { listsApi } from '../../services/api';

/**
 * Modal for creating or editing a list
 *
 * @param {Object} props Component properties
 * @param {boolean} props.isOpen Whether the modal is open
 * @param {Function} props.onClose Callback when modal is closed
 * @param {Function} props.onSuccess Callback when list is created/updated successfully
 * @param {Object} props.list Optional list data for editing mode
 * @param {Function} props.onDelete Optional callback for delete action in edit mode
 */
const CreateListModal = ({ isOpen, onClose, onSuccess, list = null, onDelete = null }) => {
  // Determine if we're in edit mode
  const isEditMode = !!list;

  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Populate form data when list changes or modal opens
  useEffect(() => {
    if (isOpen && isEditMode) {
      setFormData({
        name: list.name || '',
        description: list.description || ''
      });
    } else if (isOpen && !isEditMode) {
      // Reset form in create mode
      setFormData({
        name: '',
        description: ''
      });
    }
  }, [isOpen, list, isEditMode]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: null
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'List name is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      let result;

      if (isEditMode) {
        // Update existing list
        result = await listsApi.updateList(list.id, formData);
      } else {
        // Create new list
        result = await listsApi.createList(formData);
      }

      // Call success callback with the result
      if (onSuccess) onSuccess(result);

      // Close modal
      onClose();

      // Only reset form for create mode - edit mode will be reset on next open
      if (!isEditMode) {
        setFormData({
          name: '',
          description: ''
        });
      }
    } catch (error) {
      // Handle API errors
      if (error.data && error.data.name) {
        setErrors(prev => ({
          ...prev,
          name: error.data.name
        }));
      } else {
        setErrors(prev => ({
          ...prev,
          form: `Failed to ${isEditMode ? 'update' : 'create'} list. Please try again.`
        }));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    // Reset form state and errors
    setErrors({});
    onClose();
  };

  const handleDelete = () => {
    if (onDelete) {
      onDelete();
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-md mx-4 overflow-hidden">
        <div className="flex justify-between items-center px-6 py-4 border-b border-gray-100">
          <h2 className="text-xl font-semibold text-primary">
            {isEditMode ? 'Edit List' : 'Create New List'}
          </h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600"
            aria-label="Close"
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          {errors.form && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
              {errors.form}
            </div>
          )}

          <div className="mb-4">
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              List Name*
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={`w-full px-3 py-2 border ${
                errors.name ? 'border-red-500' : 'border-gray-300'
              } rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary`}
              placeholder="Enter list name"
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name}</p>
            )}
          </div>

          <div className="mb-6">
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
              placeholder="Enter list description (optional)"
            ></textarea>
          </div>

          <div className="flex items-center justify-between">
            {/* Show delete button only in edit mode */}
            {isEditMode && onDelete && (
              <button
                type="button"
                onClick={handleDelete}
                className="px-4 py-2 text-red-600 border border-red-200 bg-red-50 rounded-md hover:bg-red-100 transition-colors flex items-center gap-2"
              >
                <FontAwesomeIcon icon={faTrash} />
                Delete List
              </button>
            )}

            <div className={`flex gap-3 ${isEditMode ? 'ml-auto' : ''}`}>
              <button
                type="button"
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
                onClick={handleClose}
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-primary text-white rounded-md hover:bg-opacity-90 flex items-center gap-2"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <span className="animate-pulse">{isEditMode ? 'Saving...' : 'Creating...'}</span>
                  </>
                ) : (
                  <>
                    <FontAwesomeIcon icon={faCheck} />
                    {isEditMode ? 'Save Changes' : 'Create List'}
                  </>
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

CreateListModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSuccess: PropTypes.func,
  list: PropTypes.object,
  onDelete: PropTypes.func
};

export default CreateListModal;