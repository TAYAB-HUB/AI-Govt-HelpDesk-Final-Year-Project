import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import EmployeeDashboard from './pages/EmployeeDashboard';
import OfficerDashboard from './pages/OfficerDashboard';
import DeptAdminDashboard from './pages/DeptAdminDashboard';
import SuperAdminDashboard from './pages/SuperAdminDashboard';
import ChatPage from './pages/ChatPage';
import TicketsPage from './pages/TicketsPage';
import TicketDetailPage from './pages/TicketDetailPage';

const queryClient = new QueryClient();

// Protected Route Component
function ProtectedRoute({ children, allowedRoles }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" />;
  }

  return children;
}

// Dashboard Router
function DashboardRouter() {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" />;

  switch (user.role) {
    case 'Employee':
      return <EmployeeDashboard />;
    case 'Officer':
      return <OfficerDashboard />;
    case 'DeptAdmin':
      return <DeptAdminDashboard />;
    case 'SuperAdmin':
      return <SuperAdminDashboard />;
    default:
      return <Navigate to="/login" />;
  }
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            <Route path="/" element={
              <ProtectedRoute>
                <DashboardRouter />
              </ProtectedRoute>
            } />
            
            <Route path="/chat" element={
              <ProtectedRoute allowedRoles={['Employee', 'Officer', 'DeptAdmin', 'SuperAdmin']}>
                <ChatPage />
              </ProtectedRoute>
            } />
            
            <Route path="/tickets" element={
              <ProtectedRoute>
                <TicketsPage />
              </ProtectedRoute>
            } />
            
            <Route path="/tickets/:id" element={
              <ProtectedRoute>
                <TicketDetailPage />
              </ProtectedRoute>
            } />
          </Routes>
          <Toaster position="top-right" />
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;