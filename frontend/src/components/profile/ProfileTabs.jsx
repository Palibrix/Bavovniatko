import React, { useState } from 'react';
import PropTypes from 'prop-types';
import ListsTab from './tabs/ListsTab';
import DronesTab from './tabs/DronesTab';
import SuggestionsTab from './tabs/SuggestionsTab';

const ProfileTabs = ({ profileData }) => {
  const [activeTab, setActiveTab] = useState('lists');

  const tabs = [
    { id: 'lists', label: 'My Lists' },
    { id: 'drones', label: 'My Drones' },
    { id: 'suggestions', label: 'My Suggestions' }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'lists':
        return <ListsTab profileData={profileData} />;
      case 'drones':
        return <DronesTab profileData={profileData} />;
      case 'suggestions':
        return <SuggestionsTab profileData={profileData} />;
      default:
        return <ListsTab profileData={profileData} />;
    }
  };

  return (
    <div>
      {/* Tab Navigation */}
      <div className="mb-8">
        <div className="bg-white rounded-xl shadow-sm flex overflow-x-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`flex-1 min-w-[120px] py-4 px-6 font-medium text-center whitespace-nowrap transition-colors relative ${
                activeTab === tab.id
                  ? 'text-secondary'
                  : 'text-primary hover:bg-gray-50'
              }`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
              {activeTab === tab.id && (
                <span className="absolute bottom-0 left-[20%] right-[20%] h-0.75 bg-secondary rounded-t-sm" />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div>
        {renderTabContent()}
      </div>
    </div>
  );
};

ProfileTabs.propTypes = {
  profileData: PropTypes.object.isRequired
};

export default ProfileTabs;