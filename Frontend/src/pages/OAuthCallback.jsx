import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
// import { authenticateUser } from "../api/jira";
import axios from "axios";

const OAuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Get the authorization code from URL parameters
        const params = new URLSearchParams(location.search);
        const code = params.get("code");
        const error = params.get("error");
        const errorDescription = params.get("error_description");
        const osDestination = params.get("os_destination");

        console.log("OAuth callback received:", {
          code: code ? "Present" : "Missing",
          error,
          errorDescription,
          osDestination,
        });

        // If we have an os_destination parameter, extract the code from it
        let authCode = code;
        if (!authCode && osDestination) {
          try {
            const destinationUrl = new URL(osDestination);
            authCode = destinationUrl.searchParams.get("code");
            console.log("Extracted code from os_destination:", authCode);
          } catch (e) {
            console.error("Error parsing os_destination:", e);
          }
        }

        // Check if we've already processed this code
        const processedCode = localStorage.getItem("processed_auth_code");
        if (processedCode === authCode) {
          console.log("This authorization code has already been processed");
          navigate("/dashboard");
          return;
        }

        if (error) {
          console.error("OAuth error:", error, errorDescription);
          navigate("/login");
          return;
        }

        if (!authCode) {
          console.error("No authorization code received");
          navigate("/login");
          return;
        }

        // Exchange the authorization code for an access token
        const response = await axios.get(`http://localhost:8000/auth/callback?code=${authCode}`, {
          headers: {
            'Accept': 'application/json'
          }
        });
        console.log("Authentication response:", response.data);
        // console.log("Token response:", response.data);

        const { access_token, refresh_token, expires_in, scope, token_type, user } = response.data;

        if (!access_token) {
          console.error("No access token in response");
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

        // Mark this code as processed
        localStorage.setItem("processed_auth_code", authCode);

        // Verify tokens are saved
        console.log("Tokens saved to localStorage:", {
          access_token: localStorage.getItem("access_token") ? "Present" : "Missing",
          refresh_token: localStorage.getItem("refresh_token") ? "Present" : "Missing",
          expires_at: localStorage.getItem("token_expires_at") ? "Present" : "Missing",
          user_name: localStorage.getItem("user_name") || "Not available",
        });

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
        }
        navigate("/login");
      }
    };

    handleCallback();
  }, [navigate, location]);

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