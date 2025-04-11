import React, { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const Topbar = () => {
  const { logout } = useAuth();
  const [userName, setUserName] = useState("");

  useEffect(() => {
    // Get username from localStorage
    const name = localStorage.getItem("user_name") || "کاربر";
    setUserName(name);
  }, []);

  return (
    <div className="bg-cyan-500 shadow-md p-2 flex justify-between items-center">
      <h1 className="text-xl font-bold flex items-center">پرتال سازمانی</h1>
      <div className="flex items-center gap-3">
        <span className="text-white font-medium">
          {userName}
        </span>
        <button
          onClick={logout}
          className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition duration-200"
        >
          خروج
        </button>
      </div>
    </div>
  );
};

export default Topbar;