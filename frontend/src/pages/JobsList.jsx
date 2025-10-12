// src/pages/JobsList.jsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function JobsList() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    // Mock data for Day 1 — replace with API call later
    setJobs([
      {
        id: 1,
        title: "Frontend Developer",
        company: "TechCorp",
        status: "Applied",
      },
      {
        id: 2,
        title: "React Engineer",
        company: "StartupXYZ",
        status: "Interview",
      },
    ]);
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">My Applications</h1>
        <Link
          to="/jobs/new"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + Add Job
        </Link>
      </div>
      <div className="space-y-4">
        {jobs.map((job) => (
          <div key={job.id} className="p-4 border rounded shadow">
            <h3 className="text-xl font-semibold">{job.title}</h3>
            <p className="text-gray-600">{job.company}</p>
            <span className="inline-block mt-2 px-2 py-1 text-xs font-semibold text-white bg-gray-500 rounded">
              {job.status}
            </span>
          </div>
        ))}
        {jobs.length === 0 && <p>No jobs added yet.</p>}
      </div>
    </div>
  );
}
