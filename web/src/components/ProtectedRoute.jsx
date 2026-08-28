import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="p-8 font-mono text-sm text-[var(--ink-soft)]">Loading...</div>;
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (roles && !roles.includes(user.role) && user.role !== "super_admin") {
    return <Navigate to="/" replace />;
  }
  return children;
}
