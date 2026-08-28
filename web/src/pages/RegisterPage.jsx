import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Card, Field, inputClass, Button } from "../components/ui";

export default function RegisterPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [departments, setDepartments] = useState([]);
  const [form, setForm] = useState({ full_name: "", email: "", password: "", department_id: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Public department list for signup; falls back silently if not reachable pre-auth.
    api.listDepartments().then(setDepartments).catch(() => {});
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.register({
        ...form,
        department_id: form.department_id ? Number(form.department_id) : null,
        role: "employee",
      });
      await login(form.email, form.password);
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--navy)" }}>
      <Card className="w-full max-w-md p-10">
        <h1 className="font-display text-xl mb-1">Employee registration</h1>
        <p className="text-sm mb-6" style={{ color: "var(--ink-soft)" }}>
          New accounts are created with the Employee role. Ask your Department
          Admin to grant elevated access if needed.
        </p>
        <form onSubmit={handleSubmit}>
          <Field label="Full name">
            <input className={inputClass} required value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          </Field>
          <Field label="Email">
            <input className={inputClass} type="email" required value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })} />
          </Field>
          <Field label="Password">
            <input className={inputClass} type="password" required value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })} />
          </Field>
          <Field label="Department">
            <select className={inputClass} required value={form.department_id}
              onChange={(e) => setForm({ ...form, department_id: e.target.value })}>
              <option value="">Select a department</option>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </Field>
          {error && <div className="text-sm mb-4" style={{ color: "var(--danger)" }}>{error}</div>}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Creating account…" : "Create account"}
          </Button>
        </form>
        <p className="text-sm mt-5" style={{ color: "var(--ink-soft)" }}>
          Already have an account?{" "}
          <Link to="/login" className="underline" style={{ color: "var(--teal)" }}>Sign in</Link>
        </p>
      </Card>
    </div>
  );
}
