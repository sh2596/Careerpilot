// src/pages/UploadResume.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function UploadResume() {
  const [file, setFile] = useState(null);
  const [parsed, setParsed] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await api.post("/resumes/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setParsed(res.data.parsed);
    } catch (err) {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Upload Resume</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-4"
        />
        <button
          type="submit"
          disabled={!file || loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
        >
          {loading ? "Uploading..." : "Upload & Parse"}
        </button>
      </form>

      {parsed && (
        <div className="mt-6 p-4 border rounded bg-white">
          <h3 className="text-xl font-semibold mb-2">Parsed Resume</h3>
          <p>
            <strong>Name:</strong> {parsed.name || "—"}
          </p>
          <p>
            <strong>Email:</strong> {parsed.email || "—"}
          </p>
          <p>
            <strong>Phone:</strong> {parsed.phone || "—"}
          </p>
          <p>
            <strong>Skills:</strong> {parsed.skills?.join(", ") || "—"}
          </p>
        </div>
      )}
    </div>
  );
}
