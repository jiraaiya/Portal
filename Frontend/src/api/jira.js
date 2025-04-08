import axios from "axios";

const API_URL = "http://localhost:8000"; // Backend URL

// Create an axios instance with default config
const api = axios.create({
  baseURL: API_URL,
});

// Add a request interceptor to add the auth token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If the error is due to an expired token and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) {
          // No refresh token available, redirect to login
          window.location.href = "/login";
          return Promise.reject(error);
        }

        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, expires_in } = response.data;
        localStorage.setItem("access_token", access_token);
        if (expires_in) {
          localStorage.setItem("token_expires_at", Date.now() + expires_in * 1000);
        }

        // Retry the original request with the new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails, redirect to login
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Fetch all Jira issues
export const getJiraIssues = async (jql_query = "") => {
  const response = await api.get(`/dashboard?jql_query=${encodeURIComponent(jql_query)}`);
  return response.data;
};

// Get all available transitions for a given issue key
export const getAvailableTransitions = async (issueKey) => {
  try {
    const response = await api.get(`/transitions/${issueKey}`);
    return response.data.transitions;
  } catch (error) {
    console.error("Error fetching transitions:", error);
    throw error;
  }
};

// Perform the issue transition by passing the issue key and transition ID
export const performTransition = async (issueKey, transitionId) => {
  try {
    const response = await api.post(`/transition/${issueKey}`, {
      transitionId: transitionId,
    });
    return response.data;
  } catch (error) {
    console.error("Error performing transition:", error);
    throw error;
  }
};

// Get a single Jira issue by key
export const getSingleIssue = async (issueKey) => {
  try {
    const response = await api.get(`/issues/${issueKey}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching issue:", error);
    throw error;
  }
};