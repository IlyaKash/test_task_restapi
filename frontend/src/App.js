import React from "react";
import { Routes, Route } from "react-router-dom";
import DevicesPage from "./pages/DevicesPage";
import DeviceDetailPage from "./pages/DeviceDetailPage";
import StatsPage from "./pages/StatsPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<DevicesPage />} />
      <Route path="/device/:id" element={<DeviceDetailPage />} />
      <Route path="/statistics" element={<StatsPage />} />
    </Routes>
  );
}
