import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const NAV_BY_ROLE = {
  employee: [
    { to: "/chat", label: "Ask a question" },
    { to: "/tickets", label: "My tickets" },
  ],
  officer: [
    { to: "/tickets", label: "Assigned tickets" },
  ],
  dept_admin: [
    { to: "/tickets", label: "Department tickets" },
    { to: "/documents", label: "Documents" },
    { to: "/analytics", label: "Analytics" },
    { to: "/users", label: "Officers" },
  ],
  super_admin: [
    { to: "/tickets", label: "All tickets" },
    { to: "/documents", label: "Documents" },
    { to: "/departments", label: "Departments" },
    { to: "/users", label: "Users" },
    { to: "/analytics", label: "Analytics" },
    { to: "/audit-log", label: "Audit log" },
  ],
};

const ROLE_LABEL = {
  employee: "Employee",
  officer: "Department Officer",
  dept_admin: "Department Admin",
  super_admin: "Super Admin",
};

export default function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const links = NAV_BY_ROLE[user?.role] || [];

  return (
    <div className="flex min-h-screen">
      <aside
        className="w-60 shrink-0 flex flex-col justify-between"
        style={{ background: "var(--navy)", color: "#fff" }}
      >
        <div>
          <div className="px-5 py-6 border-b border-white/10">
            <div className="font-display text-lg leading-tight">Government<br />Helpdesk</div>
            <div className="text-xs opacity-60 mt-1 font-mono">ACADEMIC PROTOTYPE</div>
          </div>
          <nav className="px-3 py-4 flex flex-col gap-1">
            {links.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                className={({ isActive }) =>
                  `px-3 py-2 rounded-sm text-sm transition-colors ${
                    isActive ? "bg-white/15 font-medium" : "hover:bg-white/5 opacity-85"
                  }`
                }
              >
                {l.label}
              </NavLink>
            ))}
          </nav>
        </div>
        <div className="px-5 py-5 border-t border-white/10 text-sm">
          <div className="font-medium">{user?.full_name}</div>
          <div className="text-xs opacity-60 mb-3">{ROLE_LABEL[user?.role]}</div>
          <button
            onClick={() => {
              logout();
              navigate("/login");
            }}
            className="text-xs underline opacity-80 hover:opacity-100"
          >
            Sign out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto" style={{ background: "var(--paper)" }}>
        <div className="max-w-5xl mx-auto px-8 py-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
