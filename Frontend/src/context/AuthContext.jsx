import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated on initial load
    const checkAuth = () => {
      const token = localStorage.getItem('access_token');
      setIsAuthenticated(!!token);
      setLoading(false);
    };

    checkAuth();

    // Listen for auth state changes
    const handleAuthChange = () => {
      checkAuth();
    };

    window.addEventListener('authStateChanged', handleAuthChange);

    return () => {
      window.removeEventListener('authStateChanged', handleAuthChange);
    };
  }, []);

  const login = () => {
    window.location.href = 'http://localhost:8000/auth/login';
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token_expires_at');
    setIsAuthenticated(false);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);