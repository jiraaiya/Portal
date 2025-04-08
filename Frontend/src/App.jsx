import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";
import Finance from "./pages/Finance";
import OAuthCallback from "./pages/OAuthCallback";
import Login from "./pages/Login";
import Reports from "./pages/Reports";
import { AuthProvider, useAuth } from "./context/AuthContext";

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

// Layout component for authenticated pages
const AuthenticatedLayout = ({ children }) => {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">
        <Topbar />
        <div className="main-content">
          {children}
        </div>
      </div>
    </div>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/auth/callback" element={<OAuthCallback />} />
          
          {/* Protected routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AuthenticatedLayout>
                  <Dashboard />
                </AuthenticatedLayout>
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/finance"
            element={
              <ProtectedRoute>
                <AuthenticatedLayout>
                  <Finance />
                </AuthenticatedLayout>
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/reports"
            element={
              <ProtectedRoute>
                <AuthenticatedLayout>
                  <Reports />
                </AuthenticatedLayout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;