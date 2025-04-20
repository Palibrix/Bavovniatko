import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { usersApi } from '../../services/api';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import ErrorMessage from '../../components/common/ErrorMessage';
import ProfileInfo from '../../components/profile/ProfileInfo';
import ProfileTabs from '../../components/profile/ProfileTabs';

const ProfilePage = () => {
  const { id } = useParams();
  const { user: authUser } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCurrentUser, setIsCurrentUser] = useState(false);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);
        setError(null);

        let userId = id;
        // If no ID specified or ID is 'me', use the current user
        if (!userId || userId === 'me') {
          setIsCurrentUser(true);
          // Fetch current user profile
          const data = await usersApi.getCurrentUserProfile();
          setProfileData(data);
        } else {
          // Check if this is the current user's profile
          setIsCurrentUser(userId === authUser?.id || userId === 'me');
          // Fetch specified user profile
          const data = await usersApi.getUserProfile(userId);
          setProfileData(data);
        }
      } catch (err) {
        console.error('Error fetching profile:', err);
        setError(err.message || 'Failed to load profile');
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, [id, authUser]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!profileData) {
    return <ErrorMessage message="User not found" />;
  }

  return (
    <div className="w-[90%] max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-primary relative pb-2 mb-8">
        {isCurrentUser ? 'My Profile' : `${profileData.username}'s Profile`}
        <span className="absolute bottom-0 left-0 w-14 h-1 bg-secondary"></span>
      </h1>

      <ProfileInfo
        profileData={profileData}
        isCurrentUser={isCurrentUser}
        onProfileUpdate={(updatedData) => setProfileData(updatedData)}
      />

      <ProfileTabs
        profileData={profileData}
        isCurrentUser={isCurrentUser}
        userId={profileData.id}
      />
    </div>
  );
};

export default ProfilePage;