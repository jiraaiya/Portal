import axios from "axios";

const API_URL = "http://localhost:8000"; // Backend URL

// Fetch all Jira issues
export const getJiraIssues = async () => {
  const response = await axios.get(`${API_URL}/dashboard`);
  return response.data;
};

// Get all available transitions for a given issue key
export const getAvailableTransitions = async (issueKey) => {
  try {
    const response = await axios.get(`${API_URL}/transitions/${issueKey}`);
    return response.data.transitions;  // Return the transitions list
  } catch (error) {
    console.error("Error fetching transitions:", error);
    throw error;  // You may want to handle this error further in the UI
  }
};

// Perform the issue transition by passing the issue key and transition ID
export const performTransition = async (issueKey, transitionId) => {
  try {
    const response = await axios.post(`${API_URL}/transition/${issueKey}`, {
      "transitionId": transitionId  // The transition ID to perform the transition
    });
    return response.data; // Return the response from backend if needed
  } catch (error) {
    console.error("Error performing transition:", error);
    throw error;  // Handle this error in the UI
  }
};

// Get a single Jira issue by key
export const getSingleIssue = async (issueKey) => {
  try {
    const response = await axios.get(`${API_URL}/issues/${issueKey}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching issue:", error);
    throw error;
  }
};

