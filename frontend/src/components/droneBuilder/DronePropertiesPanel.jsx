import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faFileUpload, faImage, faExclamationTriangle, faCheckCircle
} from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';

/**
 * Right panel for drone properties in the drone builder
 */
const DronePropertiesPanel = ({
  droneData,
  onChange,
  onImageAdd,
  onImageRemove,
  selectedComponent,
  componentType
}) => {
  const themeClass = getEntityThemeClass('drone');
  const [statusMessage, setStatusMessage] = useState(null);

  // Show status message for a few seconds
  const showStatus = (message, isError = false) => {
    setStatusMessage({
      text: message,
      isError
    });

    setTimeout(() => {
      setStatusMessage(null);
    }, 3000);
  };

  // Handle drone property changes
  const handleChange = (field, value) => {
    onChange({
      ...droneData,
      [field]: value
    });
  };

  // Handle file input changes for images
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check file type
    if (!file.type.startsWith('image/')) {
      showStatus('Please select an image file', true);
      return;
    }

    // Check file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      showStatus('Image must be smaller than 5MB', true);
      return;
    }

    // Process the file
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = reader.result;

      // Add image to drone data
      onImageAdd(base64String);
      showStatus('Image added successfully');
    };

    reader.onerror = () => {
      showStatus('Error reading file', true);
    };

    reader.readAsDataURL(file);
  };

  // Handle document upload for drone
  const handleDocumentChange = (e) => {
    // This is a placeholder. In the real implementation,
    // we would handle document uploads similar to images.
    showStatus('Document upload will be implemented in the next version');
  };

  const isDetailsVisible = selectedComponent === null;

  return (
    <div className="w-full flex flex-col gap-6">
      {/* Drone Properties */}
      {isDetailsVisible && (
        <div className="bg-white rounded-3xl shadow-sm overflow-hidden">
          <div className="py-4 px-6 border-b border-gray-100 font-semibold text-primary">
            Drone Properties
          </div>

          <div className="p-6">
            {/* Status message */}
            {statusMessage && (
              <div className={`mb-4 p-3 rounded-lg flex items-center ${
                statusMessage.isError ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
              }`}>
                <FontAwesomeIcon
                  icon={statusMessage.isError ? faExclamationTriangle : faCheckCircle}
                  className="mr-2"
                />
                {statusMessage.text}
              </div>
            )}

            {/* Basic Information */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold mb-3 text-primary">Basic Information</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Drone Name</label>
                  <input
                    type="text"
                    value={droneData.model || ''}
                    onChange={(e) => handleChange('model', e.target.value)}
                    placeholder="Enter Drone Name"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Manufacturer (optional)</label>
                  <input
                    type="text"
                    value={droneData.manufacturer || ''}
                    onChange={(e) => handleChange('manufacturer', e.target.value)}
                    placeholder="Manufacturer"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Drone Type</label>
                  <select
                    value={droneData.type || 'photography'}
                    onChange={(e) => handleChange('type', e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  >
                    <option value="photography">Photography</option>
                    <option value="sport">Sport</option>
                    <option value="freestyle">Freestyle</option>
                    <option value="another">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Description</label>
                  <textarea
                    value={droneData.description || ''}
                    onChange={(e) => handleChange('description', e.target.value)}
                    placeholder="Enter drone description"
                    rows="3"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  ></textarea>
                </div>
              </div>
            </div>

            {/* Physical Characteristics */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold mb-3 text-primary">Physical Characteristics</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Weight Override (g)</label>
                  <input
                    type="number"
                    value={droneData.total_weight || ''}
                    onChange={(e) => handleChange('total_weight', e.target.value)}
                    placeholder="Auto calculated if left empty"
                    min="0"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  />
                  <p className="text-xs text-gray-500 mt-1">Leave empty to use auto-calculated weight</p>
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Max Speed (km/h)</label>
                  <input
                    type="number"
                    value={droneData.max_speed || ''}
                    onChange={(e) => handleChange('max_speed', e.target.value)}
                    placeholder="Estimated max speed"
                    min="0"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Flight Time (minutes)</label>
                  <input
                    type="number"
                    value={droneData.flight_duration || ''}
                    onChange={(e) => handleChange('flight_duration', e.target.value)}
                    placeholder="Estimated flight time"
                    min="0"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Control Range (meters)</label>
                  <input
                    type="number"
                    value={droneData.control_range || ''}
                    onChange={(e) => handleChange('control_range', e.target.value)}
                    placeholder="Maximum control distance"
                    min="0"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Maximum Altitude (meters)</label>
                  <input
                    type="number"
                    value={droneData.max_altitude || ''}
                    onChange={(e) => handleChange('max_altitude', e.target.value)}
                    placeholder="Maximum flying height"
                    min="0"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  />
                </div>
              </div>
            </div>

            {/* Image Gallery Management */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold mb-3 text-primary">Image Gallery</h3>

              <div className="gallery-thumbnails flex flex-wrap gap-3 mb-3">
                {/* Image thumbnails */}
                {droneData.images && droneData.images.map((image, index) => (
                  <div key={index} className="relative w-20 h-20 border rounded group">
                    <img
                      src={typeof image === 'string' ? image : image.image}
                      alt={`Drone thumbnail ${index}`}
                      className="w-full h-full object-cover rounded"
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <button
                        onClick={() => onImageRemove(index)}
                        className="text-white hover:text-red-400"
                        aria-label="Remove image"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                ))}

                {/* Upload new image button */}
                <label className="w-20 h-20 border-2 border-dashed border-gray-300 rounded flex flex-col items-center justify-center cursor-pointer hover:border-primary transition-colors">
                  <FontAwesomeIcon icon={faImage} className="text-gray-400 mb-1" />
                  <span className="text-xs text-gray-500">Add</span>
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleImageChange}
                  />
                </label>
              </div>

              <p className="text-xs text-gray-500">Upload images of your drone (max 5MB each)</p>
            </div>

            {/* Document Upload */}
            <div>
              <h3 className="text-sm font-semibold mb-3 text-primary">Documents</h3>

              <label className="block border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-primary transition-colors">
                <FontAwesomeIcon icon={faFileUpload} className="text-gray-400 text-2xl mb-2" />
                <p className="text-sm text-gray-600">Drag & drop files here or click to browse</p>
                <p className="text-xs text-gray-500 mt-1">PDF, DOC, TXT files up to 10MB</p>
                <input
                  type="file"
                  className="hidden"
                  onChange={handleDocumentChange}
                />
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Component Details Panel */}
      {!isDetailsVisible && selectedComponent && componentType && (
        <div className="bg-white rounded-3xl shadow-sm overflow-hidden">
          <div className="py-4 px-6 border-b border-gray-100 font-semibold text-primary">
            Component Preview
          </div>

          <div className="p-6 text-center text-gray-500">
            <p className="mb-3">This is a preview of the selected component. In the full implementation, this would display the component details.</p>
            <p className="font-medium text-primary">
              {selectedComponent.manufacturer} {selectedComponent.model}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

DronePropertiesPanel.propTypes = {
  droneData: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired,
  onImageAdd: PropTypes.func.isRequired,
  onImageRemove: PropTypes.func.isRequired,
  selectedComponent: PropTypes.object,
  componentType: PropTypes.string
};

export default DronePropertiesPanel;