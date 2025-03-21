import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { hasDetails, hasDocuments } from '../../utils/componentDetailUtils';


/**
 * Container component for detail page tabs
 * Handles tab switching and conditional rendering based on available data
 *
 * @param {Object} props Component properties
 * @param {Object} props.item Component data to display
 * @param {string} props.componentType Type of component (antennas, cameras, etc.)
 * @param {string} props.themeColor Theme color for styling
 * @param {React.ReactNode} props.descriptionTab Description tab content
 * @param {React.ReactNode} props.specificationsTab Specifications tab content
 * @param {React.ReactNode} props.detailsTab Details tab content
 * @param {React.ReactNode} props.documentsTab Documents tab content
 */
const TabContainer = ({
  item,
  componentType,
  themeColor,
  descriptionTab,
  specificationsTab,
  detailsTab,
  documentsTab
}) => {
  const [activeTab, setActiveTab] = useState('description');
  const [availableTabs, setAvailableTabs] = useState([]);

  // Determine which tabs should be available based on the data
  useEffect(() => {
    if (!item) return;

    const tabs = [
      { id: 'description', label: 'Description', available: true },
      { id: 'specs', label: 'Specifications', available: true }
    ];

    // Add details tab if the component has details
    if (hasDetails(item, componentType)) {
      tabs.push({ id: 'details', label: 'Details', available: true });
    }

    // Add documents tab if the component has documents
    if (hasDocuments(item)) {
      tabs.push({ id: 'documents', label: 'Documents', available: true });
    }

    setAvailableTabs(tabs);

    // If the current active tab is not available, switch to the first available tab
    if (!tabs.some(tab => tab.id === activeTab)) {
      setActiveTab(tabs[0].id);
    }
  }, [item, componentType, activeTab]);

  // Handle tab switching
  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
  };

  // Get the content for the active tab
  const getTabContent = () => {
    switch (activeTab) {
      case 'description':
        return descriptionTab;
      case 'specs':
        return specificationsTab;
      case 'details':
        return detailsTab;
      case 'documents':
        return documentsTab;
      default:
        return null;
    }
  };

  return (
    <div>
      {/* Tab navigation */}
      <div className="bg-white rounded-3xl shadow-sm mb-6 flex overflow-hidden">
        {availableTabs.map(tab => (
          <button
            key={tab.id}
            className={`flex-1 py-4 px-6 font-medium transition-colors ${
              activeTab === tab.id
                ? `text-${themeColor} border-b-3 border-${themeColor} bg-${themeColor} bg-opacity-5`
                : 'text-gray-600 hover:bg-gray-50'
            }`}
            onClick={() => handleTabClick(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="tab-content">
        {getTabContent()}
      </div>
    </div>
  );
};

TabContainer.propTypes = {
  item: PropTypes.object.isRequired,
  componentType: PropTypes.string.isRequired,
  themeColor: PropTypes.string.isRequired,
  descriptionTab: PropTypes.node,
  specificationsTab: PropTypes.node,
  detailsTab: PropTypes.node,
  documentsTab: PropTypes.node,
};

export default TabContainer;