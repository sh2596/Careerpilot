// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import JobsList from "./pages/JobsList";
import CreateJob from "./pages/CreateJob";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/jobs" element={<JobsList />} />
          <Route path="/jobs/new" element={<CreateJob />} />
          <Route path="/" element={<JobsList />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
