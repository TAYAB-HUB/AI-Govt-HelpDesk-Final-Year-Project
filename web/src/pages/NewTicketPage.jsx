import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Card, Field, inputClass, Button } from "../components/ui";

const CATEGORIES = [
  "HR - Leave", "HR - Recruitment", "HR - Appraisal",
  "Finance - Payroll", "Finance - Reimbursement", "Finance - Procurement",
  "IT - Hardware", "IT - Software", "IT - Network", "IT - Asset Request",
  "Pension - PPO", "Pension - Commutation",
  "Administration - Maintenance", "Administration - Travel", "Other",
];

export default function NewTicketPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const preset = location.state || {};
  const [departments, setDepartments] = useState([]);
  const [form, setForm] = useState({
    department_id: preset.department_id || user?.department_id || "",
    category: CATEGORIES[0],
    subject: preset.subject || "",
    description: "",
    priority: "medium",
    origin_chat_log_id: preset.origin_chat_log_id || null,
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.listDepartments().then(setDepartments);
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const ticket = await api.createTicket({ ...form, department_id: Number(form.department_id) });
      navigate(`/tickets/${ticket.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl">
      <h1 className="font-display text-2xl mb-6">Raise a ticket</h1>
      <Card className="p-6">
        <form onSubmit={handleSubmit}>
          <Field label="Department">
            <select className={inputClass} required value={form.department_id}
              onChange={(e) => setForm({ ...form, department_id: e.target.value })}>
              <option value="">Select department</option>
              {departments.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
            </select>
          </Field>
          <Field label="Category">
            <select className={inputClass} value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}>
              {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </Field>
          <Field label="Subject">
            <input className={inputClass} required value={form.subject}
              onChange={(e) => setForm({ ...form, subject: e.target.value })} />
          </Field>
          <Field label="Description">
            <textarea className={inputClass} rows={5} required value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })} />
          </Field>
          <Field label="Priority">
            <select className={inputClass} value={form.priority}
              onChange={(e) => setForm({ ...form, priority: e.target.value })}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </Field>
          {error && <div className="text-sm mb-4" style={{ color: "var(--danger)" }}>{error}</div>}
          <Button type="submit" disabled={loading}>{loading ? "Submitting…" : "Submit ticket"}</Button>
        </form>
      </Card>
    </div>
  );
}
