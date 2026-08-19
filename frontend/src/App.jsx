import { Navigate, Route, Routes } from "react-router-dom";

import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import FeaturePage from "./pages/FeaturePage";
import NotFound from "./pages/NotFound";
import Layout from "./layouts/Layout";

export default function App() {
  return (
    <Routes>
      {/* Auth pages — NO application navbar */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />

      {/* Main application — navbar/layout */}
      <Route element={<Layout />}>
        <Route path="/home" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/feature" element={<FeaturePage />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
