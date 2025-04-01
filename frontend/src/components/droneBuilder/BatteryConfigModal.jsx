import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faSpinner, faTimes} from '@fortawesome/free-solid-svg-icons';
import { getEntityThemeClass } from '../../utils/themeUtils';

/**
 * Modal for configuring a custom battery
 */
const BatteryConfigModal = ({ isOpen, onClose, onSave, initialData = {}, isSaving = false, saveError = null }) => {
  const themeClass = getEntityThemeClass('propulsion');

  // Battery form data
  const [batteryData, setBatteryData] = useState({
    manufacturer: initialData.manufacturer || '',
    type: initialData.type || 'LIPO',
    series: initialData.series || 4,
    parallels: initialData.parallels || 1,
    size: initialData.size || '18650',
    capacity: initialData.capacity || 1500,
    voltage: initialData.voltage || 14.8,
    discharge_current: initialData.discharge_current || 75,
    charge_current: initialData.charge_current || 3,
    connector_type: initialData.connector_type || 'XT60',
    balancer: initialData.balancer || 'JST XH-5 pin',
    weight: initialData.weight || 165,
    length: initialData.length || 72,
    height: initialData.height || 35,
    width: initialData.width || 25
  });

  // Handle input changes
  const handleChange = (field, value) => {
    setBatteryData({
      ...batteryData,
      [field]: value
    });
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(batteryData);
    onClose();
  };

  // If modal is not open, don't render anything
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center bg-black bg-opacity-50">
      <div className="relative bg-white rounded-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="p-5 border-b border-gray-200 flex justify-between items-center sticky top-0 bg-white z-10">
          <h2 className={`text-xl font-semibold ${themeClass.text}`}>Configure Battery</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-xl"
            aria-label="Close"
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="p-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Battery Type */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Battery Type</label>
              <select
                value={batteryData.type}
                onChange={(e) => handleChange('type', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              >
                <option value="LIPO">LiPo</option>
                <option value="LI_ION">Li-Ion</option>
                <option value="LIHV">LiHV</option>
                <option value="ANOTHER">Other</option>
              </select>
            </div>

            {/* Manufacturer */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Manufacturer (optional)</label>
              <input
                type="text"
                value={batteryData.manufacturer}
                onChange={(e) => handleChange('manufacturer', e.target.value)}
                placeholder="Manufacturer"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
              />
            </div>

            {/* Cells in series */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Cells (S)</label>
              <input
                type="number"
                value={batteryData.series}
                onChange={(e) => handleChange('series', parseInt(e.target.value, 10))}
                min="1"
                max="12"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Cells in parallel */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Parallels (P)</label>
              <input
                type="number"
                value={batteryData.parallels}
                onChange={(e) => handleChange('parallels', parseInt(e.target.value, 10))}
                min="1"
                max="12"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Battery size */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Cell Size</label>
              <input
                type="text"
                value={batteryData.size}
                onChange={(e) => handleChange('size', e.target.value)}
                placeholder="e.g. 18650"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Capacity */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Capacity (mAh)</label>
              <input
                type="number"
                value={batteryData.capacity}
                onChange={(e) => handleChange('capacity', parseInt(e.target.value, 10))}
                min="100"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Voltage */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Voltage (V)</label>
              <input
                type="number"
                value={batteryData.voltage}
                onChange={(e) => handleChange('voltage', parseFloat(e.target.value))}
                min="2"
                max="50"
                step="0.1"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Discharge current */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Discharge Current (C)</label>
              <input
                type="number"
                value={batteryData.discharge_current}
                onChange={(e) => handleChange('discharge_current', parseInt(e.target.value, 10))}
                min="1"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Charge current */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Charge Current (C)</label>
              <input
                type="number"
                value={batteryData.charge_current}
                onChange={(e) => handleChange('charge_current', parseInt(e.target.value, 10))}
                min="1"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Weight */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Weight (g)</label>
              <input
                type="number"
                value={batteryData.weight}
                onChange={(e) => handleChange('weight', parseInt(e.target.value, 10))}
                min="1"
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
              />
            </div>

            {/* Connector type */}
            <input
                type="text"
                value={batteryData.connector_type}
                onChange={(e) => handleChange('connector_type', e.target.value)}
                placeholder="e.g. XT60, XT30, EC3, etc."
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                required
            />

            {/* Balancer */}
            <div>
              <label className="block text-sm text-gray-600 mb-1">Balancer Connector</label>
              <input
                  type="text"
                  value={batteryData.balancer}
                  onChange={(e) => handleChange('balancer', e.target.value)}
                  placeholder="e.g. JST XH-5 pin"
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
              />
            </div>
          </div>

          {/* Dimensions section */}
          <div className="mt-5">
            <h3 className="text-sm font-semibold mb-3 text-primary">Dimensions</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Length (mm)</label>
                <input
                  type="number"
                  value={batteryData.length}
                  onChange={(e) => handleChange('length', parseFloat(e.target.value))}
                  min="1"
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  required
                />
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Height (mm)</label>
                <input
                  type="number"
                  value={batteryData.height}
                  onChange={(e) => handleChange('height', parseFloat(e.target.value))}
                  min="1"
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  required
                />
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Width (mm)</label>
                <input
                  type="number"
                  value={batteryData.width}
                  onChange={(e) => handleChange('width', parseFloat(e.target.value))}
                  min="1"
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  required
                />
              </div>
            </div>
          </div>

          {/* Footer with actions */}
          <div className="mt-8 flex justify-end gap-3">
            {saveError && (
              <div className="mr-auto text-red-600 text-sm">
                Error: {saveError}
              </div>
            )}
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 font-medium transition-colors"
              disabled={isSaving}
            >
              Cancel
            </button>
            <button
              type="submit"
              className={`px-5 py-2 ${themeClass.bg} hover:opacity-90 text-white rounded-lg font-medium transition-opacity ${isSaving ? 'opacity-70 cursor-not-allowed' : ''}`}
              disabled={isSaving}
            >
              {isSaving ? (
                <>
                  <FontAwesomeIcon icon={faSpinner} className="animate-spin mr-2" />
                  Saving...
                </>
              ) : (
                'Save Battery & Continue'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

BatteryConfigModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
  initialData: PropTypes.object,
  isSaving: PropTypes.bool,
  saveError: PropTypes.string
};

export default BatteryConfigModal;