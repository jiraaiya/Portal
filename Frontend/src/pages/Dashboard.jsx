import { useEffect, useState } from "react";
import { getJiraIssues } from "../api/jira";
import JiraTable from "../components/JiraTable";

const Dashboard = () => {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchIssues = () => {
    setLoading(true);
    getJiraIssues()
      .then((data) => {
        setIssues(data.issues);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
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
    fetchIssues(); // Fetch issues on component mount
  }, []);

  return (
    <div className="p-4">
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
