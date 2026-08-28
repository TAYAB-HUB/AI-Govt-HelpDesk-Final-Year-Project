import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Card, Button, StatusStamp, PriorityTag, inputClass } from "../components/ui";

const STATUS_OPTIONS = ["open", "in_progress", "resolved", "closed"];

export default function TicketDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [ticket, setTicket] = useState(null);
  const [comment, setComment] = useState("");
  const [statusChange, setStatusChange] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function load() {
    const t = await api.getTicket(id);
    setTicket(t);
  }

  useEffect(() => { load(); }, [id]);

  async function handleAddComment(e) {
    e.preventDefault();
    if (!comment.trim() && !statusChange) return;
    setSubmitting(true);
    setError("");
    try {
      const updated = await api.addComment(id, {
        body: comment || `Status changed to ${statusChange}`,
        status_change_to: statusChange || null,
      });
      setTicket(updated);
      setComment("");
      setStatusChange("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (!ticket) return <p style={{ color: "var(--ink-soft)" }}>Loading…</p>;

  const canChangeStatus = user?.role !== "employee";

  return (
    <div className="max-w-2xl">
      <div className="flex items-center gap-2 mb-1">
        <span className="font-mono text-xs" style={{ color: "var(--ink-soft)" }}>#{ticket.id}</span>
        <PriorityTag priority={ticket.priority} />
        <StatusStamp status={ticket.status} />
      </div>
      <h1 className="font-display text-2xl mb-1">{ticket.subject}</h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink-soft)" }}>{ticket.category}</p>

      <Card className="p-5 mb-6">
        <p className="text-sm whitespace-pre-wrap">{ticket.description}</p>
      </Card>

      <h2 className="font-display text-lg mb-3">Timeline</h2>
      <div className="space-y-3 mb-6">
        {ticket.comments.length === 0 && (
          <p className="text-sm" style={{ color: "var(--ink-soft)" }}>No updates yet.</p>
        )}
        {ticket.comments.map((c) => (
          <Card key={c.id} className="p-4">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-mono" style={{ color: "var(--ink-soft)" }}>
                {new Date(c.created_at).toLocaleString()}
              </span>
              {c.status_change_to && <StatusStamp status={c.status_change_to} />}
            </div>
            <p className="text-sm">{c.body}</p>
          </Card>
        ))}
      </div>

      <Card className="p-5">
        <form onSubmit={handleAddComment}>
          <textarea
            className={inputClass + " mb-3"}
            rows={3}
            placeholder="Add an update or comment…"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
          {canChangeStatus && (
            <select className={inputClass + " mb-3"} value={statusChange} onChange={(e) => setStatusChange(e.target.value)}>
              <option value="">No status change</option>
              {STATUS_OPTIONS.map((s) => <option key={s} value={s}>{s.replace("_", " ")}</option>)}
            </select>
          )}
          {error && <div className="text-sm mb-3" style={{ color: "var(--danger)" }}>{error}</div>}
          <Button type="submit" disabled={submitting}>{submitting ? "Posting…" : "Post update"}</Button>
        </form>
      </Card>
    </div>
  );
}
