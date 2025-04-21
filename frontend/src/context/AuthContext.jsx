import React, { createContext, useState, useEffect, useCallback, useContext } from 'react';
import { authApi, usersApi } from '../services/api';

// Create the context
const AuthContext = createContext();

/**
 * Authentication provider component
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Helper function to fetch user profile data
  const fetchUserProfile = async () => {
    try {
      const userData = await usersApi.getCurrentUserProfile();
      // Set user with id and username from profile data
      setUser({
        id: userData.id,
        username: userData.username
      });
      return userData;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      throw error;
    }
  };

  // Initialize: check if user is already logged in
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (authApi.isAuthenticated()) {
          try {
            // Verify token validity
            await authApi.verifyToken();

            // Fetch user profile to get ID and other data
            await fetchUserProfile();
          } catch (error) {
            // Token invalid - try to refresh
            try {
              await authApi.refreshToken();
              // After refresh, fetch user data
              await fetchUserProfile();
            } catch (refreshError) {
              // Refresh failed - user needs to login again
              authApi.logout();
              setUser(null);
            }
          }
        }
      } catch (e) {
        console.error('Auth initialization error:', e);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  // Login function
  const login = useCallback(async (credentials) => {
    setLoading(true);
    setError(null);

    try {
      const response = await authApi.login(credentials);
      // Save username for display (as fallback)
      localStorage.setItem('username', credentials.username);

      // Fetch user profile to get ID
      await fetchUserProfile();

      return response;
    } catch (e) {
      setError(e.message || 'Login failed');
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  // Register function
  const register = useCallback(async (userData) => {
    setLoading(true);
    setError(null);

    try {
      const response = await authApi.register(userData);
      return response;
    } catch (e) {
      setError(e.message || 'Registration failed');
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  // Logout function
  const logout = useCallback(async () => {
    setLoading(true);

    try {
      await authApi.logout();
      localStorage.removeItem('username');
      setUser(null);
    } catch (e) {
      console.error('Logout error:', e);
    } finally {
      setLoading(false);
    }
  }, []);

  // Create the context value object
  const value = {
    user,
    isAuthenticated: !!user,
    loading,
    error,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to use the auth context
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;