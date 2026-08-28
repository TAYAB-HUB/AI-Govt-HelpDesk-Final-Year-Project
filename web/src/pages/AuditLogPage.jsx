import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Card } from "../components/ui";

export default function AuditLogPage() {
  const [logs, setLogs] = useState([]);

  useEffect(() => { api.auditLogs(200).then(setLogs); }, []);

  return (
    <div>
      <h1 className="font-display text-2xl mb-6">Audit log</h1>
      <Card className="overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b" style={{ borderColor: "var(--line)", color: "var(--ink-soft)" }}>
              <th className="px-4 py-3">Time</th>
              <th className="px-4 py-3">Actor</th>
              <th className="px-4 py-3">Action</th>
              <th className="px-4 py-3">Target</th>
              <th className="px-4 py-3">Detail</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((l) => (
              <tr key={l.id} className="border-b last:border-0" style={{ borderColor: "var(--line)" }}>
                <td className="px-4 py-3 font-mono text-xs whitespace-nowrap">
                  {new Date(l.created_at).toLocaleString()}
                </td>
                <td className="px-4 py-3 font-mono text-xs">{l.actor_id ?? "—"}</td>
                <td className="px-4 py-3">
                  <span className="font-mono text-xs px-2 py-0.5 rounded-sm" style={{ background: "var(--teal-soft)", color: "var(--teal)" }}>
                    {l.action}
                  </span>
                </td>
                <td className="px-4 py-3 text-xs">{l.target_type} {l.target_id ? `#${l.target_id}` : ""}</td>
                <td className="px-4 py-3 text-xs" style={{ color: "var(--ink-soft)" }}>{l.detail}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
