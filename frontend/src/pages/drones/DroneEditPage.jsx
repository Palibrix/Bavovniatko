import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import DroneCreateTemplate from '../../components/templates/DroneCreateTemplate';
import { dronesApi } from '../../services/api';
import { ROUTES } from '../../routes';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import ErrorMessage from '../../components/common/ErrorMessage';

const DroneEditPage = () => {
  const { id } = useParams();
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [drone, setDrone] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDrone = async () => {
      if (!id) return;

      try {
        setLoading(true);
        const data = await dronesApi.getDroneById(id);

        // Check if user is authorized to edit this drone
        if (user && data.user && data.user.id !== user.id) {
          setError("You don't have permission to edit this drone");
          return;
        }

        setDrone(data);
      } catch (err) {
        console.error("Error fetching drone:", err);
        setError("Failed to load drone data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (!authLoading && isAuthenticated) {
      fetchDrone();
    }
  }, [id, user, authLoading, isAuthenticated]);

  // Show loading state
  if (authLoading || loading) {
    return (
      <div className="w-full h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="w-[92%] max-w-[1400px] mx-auto px-4 py-8">
        <ErrorMessage
          message={error}
          onRetry={() => navigate(ROUTES.BUILDS.DRONES.LIST)}
        />
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    navigate(ROUTES.AUTH, { state: { from: window.location.pathname } });
    return null;
  }

  return <DroneCreateTemplate isEditMode={true} initialDrone={drone} />;
};

export default DroneEditPage;