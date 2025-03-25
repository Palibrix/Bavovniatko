import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import { useAuth } from '../../context/AuthContext';

/**
 * Protected route component that redirects to login if not authenticated
 */
const ProtectedRoute = ({ children, loginPath = '/auth' }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // If still loading auth state, show nothing yet
  if (loading) {
    return <div className="w-full h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>;
  }

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    return <Navigate to={loginPath} state={{ from: location }} replace />;
  }

  // If authenticated, render the protected component
  return children;
};

ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired,
  loginPath: PropTypes.string
};

export default ProtectedRoute;