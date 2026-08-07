import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Card, Button, StatusStamp, PriorityTag, inputClass } from "../components/ui";

const STATUS_FILTERS = ["", "open", "in_progress", "resolved", "closed"];

export default function TicketsPage() {
  const { user } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.listTickets(status || undefined).then(setTickets).finally(() => setLoading(false));
  }, [status]);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl">
          {user?.role === "employee" ? "My tickets" : "Tickets"}
        </h1>
        <div className="flex gap-2 items-center">
          <select className={inputClass + " w-40"} value={status} onChange={(e) => setStatus(e.target.value)}>
            {STATUS_FILTERS.map((s) => (
              <option key={s} value={s}>{s ? s.replace("_", " ") : "All statuses"}</option>
            ))}
          </select>
          {user?.role === "employee" && (
            <Link to="/tickets/new"><Button>+ New ticket</Button></Link>
          )}
        </div>
      </div>

      {loading ? (
        <p style={{ color: "var(--ink-soft)" }}>Loading…</p>
      ) : tickets.length === 0 ? (
        <Card className="p-8 text-center">
          <p style={{ color: "var(--ink-soft)" }}>No tickets here yet.</p>
        </Card>
      ) : (
        <div className="space-y-3">
          {tickets.map((t) => (
            <Link key={t.id} to={`/tickets/${t.id}`}>
              <Card className="p-4 hover:shadow-md transition-shadow flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-xs" style={{ color: "var(--ink-soft)" }}>#{t.id}</span>
                    <PriorityTag priority={t.priority} />
                    <span className="text-xs" style={{ color: "var(--ink-soft)" }}>{t.category}</span>
                  </div>
                  <div className="font-medium text-sm">{t.subject}</div>
                </div>
                <StatusStamp status={t.status} />
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
