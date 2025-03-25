import React, { createContext, useState, useEffect, useCallback, useContext } from 'react';
import { authApi } from '../services/api';

// Create the context
const AuthContext = createContext();

/**
 * Authentication provider component
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize: check if user is already logged in
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (authApi.isAuthenticated()) {
          try {
            // Verify token validity
            await authApi.verifyToken();

            // Here we would normally fetch user profile data
            // For now, we'll just set a basic user object based on JWT
            setUser({ username: localStorage.getItem('username') || 'User' });
          } catch (error) {
            // Token invalid - try to refresh
            try {
              await authApi.refreshToken();
              setUser({ username: localStorage.getItem('username') || 'User' });
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
      // Save username for display
      localStorage.setItem('username', credentials.username);
      setUser({ username: credentials.username });
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