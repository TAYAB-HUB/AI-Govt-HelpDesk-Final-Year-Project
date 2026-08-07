import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import AppShell from "./layouts/AppShell";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ChatPage from "./pages/ChatPage";
import TicketsPage from "./pages/TicketsPage";
import NewTicketPage from "./pages/NewTicketPage";
import TicketDetailPage from "./pages/TicketDetailPage";
import DocumentsPage from "./pages/DocumentsPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import UsersPage from "./pages/UsersPage";
import DepartmentsPage from "./pages/DepartmentsPage";
import AuditLogPage from "./pages/AuditLogPage";

function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="p-10 text-sm">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
}

function HomeRedirect() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (user.role === "employee") return <Navigate to="/chat" replace />;
  return <Navigate to="/tickets" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
            <Route path="/" element={<HomeRedirect />} />
            <Route path="/chat" element={<ProtectedRoute roles={["employee"]}><ChatPage /></ProtectedRoute>} />
            <Route path="/tickets" element={<TicketsPage />} />
            <Route path="/tickets/new" element={<ProtectedRoute roles={["employee"]}><NewTicketPage /></ProtectedRoute>} />
            <Route path="/tickets/:id" element={<TicketDetailPage />} />
            <Route
              path="/documents"
              element={<ProtectedRoute roles={["dept_admin", "super_admin"]}><DocumentsPage /></ProtectedRoute>}
            />
            <Route
              path="/analytics"
              element={<ProtectedRoute roles={["dept_admin", "super_admin", "officer"]}><AnalyticsPage /></ProtectedRoute>}
            />
            <Route
              path="/users"
              element={<ProtectedRoute roles={["dept_admin", "super_admin"]}><UsersPage /></ProtectedRoute>}
            />
            <Route
              path="/departments"
              element={<ProtectedRoute roles={["super_admin"]}><DepartmentsPage /></ProtectedRoute>}
            />
            <Route
              path="/audit-log"
              element={<ProtectedRoute roles={["super_admin"]}><AuditLogPage /></ProtectedRoute>}
            />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
