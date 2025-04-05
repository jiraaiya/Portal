import React, { useState } from "react";
import { getAvailableTransitions, performTransition, getSingleIssue } from "../api/jira"; // Importing from api/jira

const JiraTable = ({ issueData, onUpdateIssue }) => {
  const [transitions, setTransitions] = useState([]);
  const [selectedIssueKey, setSelectedIssueKey] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch available transitions for a given issue
  const fetchTransitions = async (issueKey) => {
    setLoading(true);
    try {
      const availableTransitions = await getAvailableTransitions(issueKey); // Get transitions from API
      setTransitions(availableTransitions);
      setSelectedIssueKey(issueKey);
      setShowModal(true);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching transitions", err);
      setError("خطا در دریافت انتقال‌ها");
      setLoading(false);
    }
  };

  // Perform the issue transition by passing the transitionId
  const handleTransitionSelect = async (transitionId) => {
    try {
      console.log('Starting transition with:', { issueKey: selectedIssueKey, transitionId });
      await performTransition(selectedIssueKey, transitionId); // Perform the transition
      console.log(`Successfully transitioned issue: ${selectedIssueKey}`);
      setShowModal(false); // Close modal

      // Refetch the updated issue data after transition
      console.log('Fetching updated issue data for:', selectedIssueKey);
      const updatedIssue = await getSingleIssue(selectedIssueKey);
      console.log('Received updated issue data:', updatedIssue);
      
      // Update the specific row with the updated issue data
      console.log('Updating issue in table with:', { key: selectedIssueKey, data: updatedIssue });
      onUpdateIssue(selectedIssueKey, updatedIssue);
    } catch (err) {
      console.error("Error performing transition", err);
      console.log('Error details:', { 
        message: err.message,
        issueKey: selectedIssueKey,
        transitionId 
      });
    }
  };

  return (
    <div className="overflow-x-auto shadow-md border border-gray-200 rounded-lg bg-white text-sm">
      <table className="w-full border-collapse text-right rtl">
        <thead className="bg-gray-100 text-gray-700 font-bold">
          <tr>
            <th className="px-6 py-4 border-b">کلید</th>
            <th className="px-6 py-4 border-b">خلاصه</th>
            <th className="px-6 py-4 border-b">وضعیت</th>
            <th className="px-6 py-4 border-b">مسئول</th>
            <th className="px-6 py-4 border-b">انتقال</th>
          </tr>
        </thead>
        <tbody>
          {issueData.map((issue) => (
            <tr key={issue.key} className="hover:bg-gray-50 transition">
              <td className="px-6 py-3 border-b">{issue.key}</td>
              <td className="px-6 py-3 border-b">{issue.summary}</td>
              <td className="px-6 py-3 border-b">{issue.status}</td>
              <td className="px-6 py-3 border-b">{issue.assignee}</td>
              <td className="px-6 py-3 border-b">
                <button
                  onClick={() => fetchTransitions(issue.key)} // Fetch transitions when clicked
                  className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition duration-200"
                >
                  انتقال
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal to show transitions */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h2 className="text-lg font-bold mb-4">انتقال وظیفه</h2>
            {loading && <p>در حال بارگذاری...</p>}
            {error && <p className="text-red-500">{error}</p>}
            <div className="space-y-3">
              {transitions.map((transition) => (
                <button
                  key={transition.id}
                  onClick={() => handleTransitionSelect(transition.id)} // Select the transition
                  className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition duration-200"
                >
                  {transition.name}
                </button>
              ))}
            </div>
            <button
              onClick={() => setShowModal(false)}
              className="mt-4 w-full bg-gray-400 text-white py-2 rounded-lg hover:bg-gray-500 transition duration-200"
            >
              بستن
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default JiraTable;
