import axios from "axios";

const API_URL = "http://localhost:8000";

export const getJiraIssues = async (jql) => {
  try {
    const response = await axios.get(`${API_URL}/jira/issues`, { params: { jql } });
    return response.data;
  } catch (error) {
    console.error("Error fetching Jira issues:", error);
    return [];
  }
};
