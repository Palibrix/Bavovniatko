
import React from 'react';
import { useAuth } from '../../context/AuthContext';
import DroneCreateTemplate from '../../components/templates/DroneCreateTemplate';
import { Navigate, useLocation } from 'react-router-dom';
import { ROUTES } from '../../routes';

/**
 * Page component for drone creation
 */
const DroneCreatePage = () => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="w-full h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to={ROUTES.AUTH} state={{ from: location }} replace />;
  }

  return <DroneCreateTemplate />;
};

export default DroneCreatePage;