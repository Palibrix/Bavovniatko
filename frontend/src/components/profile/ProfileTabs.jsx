import React, { useState } from 'react';
import PropTypes from 'prop-types';
import ListsTab from './tabs/ListsTab';
import DronesTab from './tabs/DronesTab';
import SuggestionsTab from './tabs/SuggestionsTab';

const ProfileTabs = ({ profileData, isCurrentUser, userId }) => {
  const [activeTab, setActiveTab] = useState('drones');

  // Only show certain tabs for the user's own profile
  const tabs = [
    { id: 'drones', label: `${isCurrentUser ? 'My' : `${profileData.username}'s`} Drones`, always: true },
    { id: 'lists', label: 'My Lists', onlyForCurrentUser: true },
    { id: 'suggestions', label: 'My Suggestions', onlyForCurrentUser: true }
  ].filter(tab => tab.always || (tab.onlyForCurrentUser && isCurrentUser));

  const renderTabContent = () => {
    switch (activeTab) {
      case 'lists':
        return <ListsTab profileData={profileData} />;
      case 'drones':
        return <DronesTab
                 profileData={profileData}
                 userId={userId}
                 isCurrentUser={isCurrentUser}
               />;
      case 'suggestions':
        return <SuggestionsTab profileData={profileData} />;
      default:
        return <DronesTab
                 profileData={profileData}
                 userId={userId}
                 isCurrentUser={isCurrentUser}
               />;
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
  profileData: PropTypes.object.isRequired,
  isCurrentUser: PropTypes.bool,
  userId: PropTypes.oneOfType([PropTypes.string, PropTypes.number])
};

ProfileTabs.defaultProps = {
  isCurrentUser: false
};

export default ProfileTabs;