import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
// import { authenticateUser } from "../api/jira";
import axios from "axios";

const OAuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [processingToken, setProcessingToken] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const handleCallback = async () => {
      // Prevent multiple simultaneous token processing
      if (processingToken) {
        return;
      }

      try {
        setProcessingToken(true);
        
        // Get the authorization code from URL parameters
        const params = new URLSearchParams(location.search);
        const code = params.get("code");
        const error = params.get("error");
        const errorDescription = params.get("error_description");
        const osDestination = params.get("os_destination");

        // If we have an os_destination parameter, extract the code from it
        let authCode = code;
        if (!authCode && osDestination) {
          try {
            const destinationUrl = new URL(osDestination);
            authCode = destinationUrl.searchParams.get("code");
          } catch (e) {
            console.error("Error parsing os_destination:", e);
            setError("Failed to parse authorization code");
            navigate("/login");
            return;
          }
        }

        // Check if we've already processed this code
        const tokenKey = `token_${authCode}`;
        const tokenProcessed = sessionStorage.getItem(tokenKey);
        
        if (tokenProcessed) {
          navigate("/dashboard");
          return;
        }

        // Check if we've already processed this code in localStorage (persistent check)
        const processedCode = localStorage.getItem("processed_auth_code");
        if (processedCode === authCode) {
          navigate("/dashboard");
          return;
        }

        if (error) {
          console.error("OAuth error:", error, errorDescription);
          setError(`OAuth error: ${error} - ${errorDescription}`);
          navigate("/login");
          return;
        }

        if (!authCode) {
          console.error("No authorization code received");
          setError("No authorization code received");
          navigate("/login");
          return;
        }

        // Mark this code as being processed to prevent duplicate processing
        sessionStorage.setItem(tokenKey, "processing");
        
        // Exchange the authorization code for an access token
        const response = await axios.post(
          "http://localhost:8000/auth/callback",
          { code: authCode },
          {
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            },
            withCredentials: true
          }
        );

        const { access_token, refresh_token, expires_in, scope, token_type, user } = response.data;

        if (!access_token) {
          console.error("No access token in response");
          setError("No access token in response");
          navigate("/login");
          return;
        }

        // Save tokens to localStorage
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("refresh_token", refresh_token);
        localStorage.setItem("token_expires_at", Date.now() + expires_in * 1000);
        localStorage.setItem("token_scope", scope);
        localStorage.setItem("token_type", token_type);

        // Save user information
        if (user) {
          localStorage.setItem("user_name", user.name);
          localStorage.setItem("user_email", user.email);
          localStorage.setItem("user_account_id", user.accountId);
        }

        // Mark this code as processed in both session and local storage
        sessionStorage.setItem(tokenKey, "processed");
        localStorage.setItem("processed_auth_code", authCode);

        // Dispatch an event to notify that auth state has changed
        window.dispatchEvent(new Event("authStateChanged"));

        // Redirect to dashboard
        navigate("/dashboard");
      } catch (error) {
        console.error("Error in OAuth callback:", error);
        if (error.response) {
          console.error("Error response:", {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          });
          setError(`Server error: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
        } else {
          setError(`Network error: ${error.message}`);
        }
        navigate("/login");
      } finally {
        setProcessingToken(false);
      }
    };

    // Only run the callback if we're not already processing a token
    if (!processingToken) {
      handleCallback();
    }
    
    // Cleanup function to handle component unmounting
    return () => {};
  }, [navigate, location, processingToken]);

  // If there's an error, display it
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">Error: {error}</div>
          <button 
            onClick={() => navigate("/login")}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Return to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-4 text-gray-600">در حال تکمیل فرآیند ورود...</p>
      </div>
    </div>
  );
};

export default OAuthCallback;