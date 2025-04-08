import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Login = () => {
  const navigate = useNavigate();
  const { isAuthenticated, login } = useAuth();

  useEffect(() => {
    // Redirect to dashboard if already authenticated
    if (isAuthenticated) {
      navigate("/");
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold text-center mb-6">پرتال سازمانی</h1>
        <p className="text-gray-600 text-center mb-8">
          لطفا برای استفاده لاگین کنید
        </p>
        
        <button
          onClick={login}
          className="w-full py-3 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-200 flex items-center justify-center"
        >
          لاگین با جیرا
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-5 w-5 mr-2" 
            viewBox="0 0 24 24" 
            fill="currentColor"
          >
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default Login;