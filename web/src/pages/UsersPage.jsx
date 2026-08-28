import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Card } from "../components/ui";

const ROLES = ["employee", "officer", "dept_admin", "super_admin"];

export default function UsersPage() {
  const [users, setUsers] = useState([]);

  async function load() {
    setUsers(await api.listUsers());
  }

  useEffect(() => { load(); }, []);

  async function handleRoleChange(userId, role) {
    await api.changeRole(userId, role);
    load();
  }

  async function handleToggleActive(userId) {
    await api.toggleActive(userId);
    load();
  }

  return (
    <div>
      <h1 className="font-display text-2xl mb-6">Users</h1>
      <Card className="overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b" style={{ borderColor: "var(--line)", color: "var(--ink-soft)" }}>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3">Role</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-b last:border-0" style={{ borderColor: "var(--line)" }}>
                <td className="px-4 py-3">{u.full_name}</td>
                <td className="px-4 py-3 font-mono text-xs">{u.email}</td>
                <td className="px-4 py-3">
                  <select
                    className="border rounded-sm px-2 py-1 text-xs"
                    style={{ borderColor: "var(--line)" }}
                    value={u.role}
                    onChange={(e) => handleRoleChange(u.id, e.target.value)}
                  >
                    {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
                  </select>
                </td>
                <td className="px-4 py-3">
                  <span style={{ color: u.is_active ? "var(--teal)" : "var(--danger)" }}>
                    {u.is_active ? "Active" : "Disabled"}
                  </span>
                </td>
                <td className="px-4 py-3 text-right">
                  <button className="text-xs underline" onClick={() => handleToggleActive(u.id)}>
                    {u.is_active ? "Disable" : "Enable"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
