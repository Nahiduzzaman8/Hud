// src/App.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login"; // create this next
// import Dashboard from "./components/Dashboard"; // example protected page

function App() {
  return (
    <Routes>
      {/* Default route */}
      <Route path="/" element={<Navigate to="/signup" />} />

      {/* Public pages */}
      <Route
        path="/signup"
        element={<Signup onLoginRedirect={() => window.location.href = "/login"} />}
      />
      <Route path="/login" element={<Login />} />

      {/* Protected page example
      <Route path="/dashboard" element={<Dashboard />} /> */}
    </Routes>
  );
}

export default App;
