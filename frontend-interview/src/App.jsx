import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AccessibilityProvider } from './context/AccessibilityContext';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import SetupPage from './pages/SetupPage';
import RoomPage from './pages/RoomPage';
import ReportPage from './pages/ReportPage';

export default function App() {
  return (
    <AccessibilityProvider>
      <BrowserRouter>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/setup" element={<SetupPage />} />
              <Route path="/interview/:id" element={<RoomPage />} />
              <Route path="/report/:id" element={<ReportPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </AccessibilityProvider>
  );
}
