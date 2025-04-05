import React from "react";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <a href="/">Dashboard</a>
      <a href="/create-ticket">Create Ticket</a>
      <a href="/reports">Reports</a>
      {/* More menu items will be added here dynamically */}
    </div>
  );
};

export default Sidebar;
