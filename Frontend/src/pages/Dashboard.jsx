import { useEffect, useState } from "react";
import { getJiraIssues } from "../api/jira";
import JiraTable from "../components/JiraTable";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();
  const [userName, setUserName] = useState("");

  const fetchIssues = () => {
    setLoading(true);
    getJiraIssues("status is not EMPTY")
      .then((data) => {
        setIssues(data.issues);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        
        // Check if the error is due to authentication
        if (err.response && err.response.status === 401) {
          console.log("Authentication error, redirecting to login");
          navigate("/login");
          return;
        }
        
        setError("خطا در دریافت اطلاعات");
        setLoading(false);
      });
  };

  const updateIssueData = (issueKey, updatedIssue) => {
    setIssues((prevIssues) =>
      prevIssues.map((issue) =>
        issue.key === issueKey ? { ...issue, ...updatedIssue } : issue
      )
    );
  };

  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated) {
      console.log("User not authenticated, redirecting to login");
      navigate("/login");
      return;
    }
    
    fetchIssues(); // Fetch issues on component mount
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    // Get user name from localStorage
    const name = localStorage.getItem("user_name");
    if (name) {
      setUserName(name);
    }
  }, []);

  return (


      <div className="max-w-7xl mx-2 py-0 sm:px-8 lg:px-8">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-bold">داشبورد</h1>
          <button
            onClick={fetchIssues}  // Trigger refresh
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition duration-200"
          >
            تازه‌سازی
          </button>
        </div>

        {loading && <p>در حال بارگذاری...</p>}
        {error && <p className="text-red-500">{error}</p>}

        {/* Multiple JiraTables */}
        {!loading && !error && (
          <JiraTable issueData={issues} onUpdateIssue={updateIssueData} />
        )}
      </div>

  );
};

export default Dashboard;
