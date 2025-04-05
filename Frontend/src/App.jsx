import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";
import Finance from "./pages/Finance";
import OAuthCallback from "./pages/OAuthCallback";
// import CreateTicket from "./pages/CreateTicket";
import Reports from "./pages/Reports"; // You can create this later

const App = () => {
  return (
    <Router>
      <div className="flex">
        <Sidebar />
        <div className="flex-1">
          <Topbar />
          <div className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/finance" element={<Finance />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/auth/callback" element={<OAuthCallback />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;

