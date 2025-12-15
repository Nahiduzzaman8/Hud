// src/App.jsx
import { Routes, Route, Navigate } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Dashboard from "./components/dashboard/Dashboard";

function App() {
  return (
    <Routes>
      {/* Default */}
      <Route path="/" element={<Navigate to="/login" />} />

      {/* Public routes */}
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />

      {/* Protected route */}
      <Route path="/dashboard" element={<Dashboard />} />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

export default App;
