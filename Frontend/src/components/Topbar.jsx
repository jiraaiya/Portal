import React from "react";
import { useAuth } from "../context/AuthContext";

const Topbar = () => {
  const { logout } = useAuth();

  return (
    <div className="bg-cyan-500 shadow-md p-2 flex justify-between items-center">
      <h1 className="text-xl font-bold flex items-center">پرتال سازمانی</h1>
      <div className="flex items-center">
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