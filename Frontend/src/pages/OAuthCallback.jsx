import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const OAuthCallback = () => {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const handleOAuthCallback = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get("code");
      const error = urlParams.get("error");
      const errorDescription = urlParams.get("error_description");

      if (error) {
        setError(`OAuth Error: ${error} - ${errorDescription || "No description provided"}`);
        setLoading(false);
        return;
      }

      if (!code) {
        setError("Authorization code not received from Jira");
        setLoading(false);
        return;
      }

      try {
        console.log("Exchanging authorization code for access token...");
        const response = await axios.get(`http://localhost:8000/auth/callback?code=${code}`);
        const { access_token, refresh_token, expires_in } = response.data;

        if (!access_token) {
          throw new Error("No access token received from server");
        }

        // Save tokens in localStorage
        localStorage.setItem("access_token", access_token);
        if (refresh_token) {
          localStorage.setItem("refresh_token", refresh_token);
        }
        if (expires_in) {
          localStorage.setItem("token_expires_at", Date.now() + expires_in * 1000);
        }

        // Set authentication state
        window.dispatchEvent(new Event('authStateChanged'));

        console.log("Successfully authenticated with Jira");
        navigate("/");
      } catch (err) {
        console.error("OAuth error:", err);
        const errorMessage = err.response?.data?.detail || err.message || "Failed to authenticate with Jira";
        setError(`Authentication Error: ${errorMessage}`);
        setLoading(false);
      }
    };

    handleOAuthCallback();
  }, [navigate]);

  return (
    <div className="p-4 text-center">
      {loading ? (
        <div className="flex flex-col items-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
          <p>Authenticating with Jira...</p>
        </div>
      ) : error ? (
        <div className="text-red-600">
          <p className="font-bold">Authentication Error</p>
          <p>{error}</p>
          <button
            onClick={() => window.location.href = "/login"}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Return to Login
          </button>
        </div>
      ) : null}
    </div>
  );
};

export default OAuthCallback;