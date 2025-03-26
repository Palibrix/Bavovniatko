import React, { useState } from 'react';
import PropTypes from 'prop-types';
import EditProfileModal from './EditProfileModal';

const ProfileInfo = ({ profileData, isCurrentUser, onProfileUpdate }) => {
  const [showEditModal, setShowEditModal] = useState(false);

  const handleEditProfile = () => {
    setShowEditModal(true);
  };

  const handleModalClose = () => {
    setShowEditModal(false);
  };

  return (
    <div className="bg-white rounded-3xl shadow-sm overflow-hidden border-t-4 border-t-secondary mb-8">
      <div className="p-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2">
            <h2 className="text-xl font-semibold text-primary mb-6">Account Information</h2>

            <div className="space-y-4">
              <div>
                <div className="text-gray-500 text-sm mb-1">Username</div>
                <div className="font-semibold text-primary">{profileData.username}</div>
              </div>

              <div>
                <div className="text-gray-500 text-sm mb-1">Name</div>
                <div className="font-semibold text-primary">
                  {profileData.profile?.first_name} {profileData.profile?.last_name}
                </div>
              </div>

              <div>
                <div className="text-gray-500 text-sm mb-1">Email</div>
                <div className="font-semibold text-primary">{profileData.email}</div>
              </div>
            </div>

            {isCurrentUser && (
              <div className="mt-6">
                <button
                  onClick={handleEditProfile}
                  className="px-4 py-2 bg-secondary text-white rounded-lg hover:bg-opacity-90 transition-colors"
                >
                  Edit Profile
                </button>
              </div>
            )}
          </div>

          <div>
            {/* Future place for stats or profile image */}
          </div>
        </div>
      </div>

      {showEditModal && (
        <EditProfileModal
          profileData={profileData}
          onClose={handleModalClose}
          onSave={onProfileUpdate}
        />
      )}
    </div>
  );
};

ProfileInfo.propTypes = {
  profileData: PropTypes.object.isRequired,
  isCurrentUser: PropTypes.bool.isRequired,
  onProfileUpdate: PropTypes.func
};

export default ProfileInfo;