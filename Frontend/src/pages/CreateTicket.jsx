import { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000"; // Backend API URL

const CreateTicket = () => {
  const [formData, setFormData] = useState({
    projectKey: "",
    summary: "",
    description: "",
    issueType: "Task",
  });

  const [status, setStatus] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/jira/create-issue`, formData);
      setStatus({ type: "success", message: `Issue Created: ${response.data.key}` });
    } catch (error) {
      setStatus({ type: "error", message: "Failed to create issue" });
    }
  };

  return (
    <div className="p-4 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">Create Jira Ticket</h1>

      {status && (
        <div className={`p-2 mb-4 ${status.type === "success" ? "bg-green-200" : "bg-red-200"}`}>
          {status.message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label>
          Project Key:
          <input type="text" name="projectKey" value={formData.projectKey} onChange={handleChange} required className="border p-2 w-full" />
        </label>

        <label>
          Summary:
          <input type="text" name="summary" value={formData.summary} onChange={handleChange} required className="border p-2 w-full" />
        </label>

        <label>
          Description:
          <textarea name="description" value={formData.description} onChange={handleChange} required className="border p-2 w-full" />
        </label>

        <label>
          Issue Type:
          <select name="issueType" value={formData.issueType} onChange={handleChange} className="border p-2 w-full">
            <option value="Task">Task</option>
            <option value="Bug">Bug</option>
            <option value="Story">Story</option>
          </select>
        </label>

        <button type="submit" className="bg-blue-500 text-white p-2">Create Ticket</button>
      </form>
    </div>
  );
};

export default CreateTicket;
