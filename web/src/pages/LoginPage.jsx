import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Card, Field, inputClass, Button } from "../components/ui";

const DEMO_LOGINS = [
  { role: "Employee", email: "employee@demo.gov.in" },
  { role: "Officer", email: "officer@demo.gov.in" },
  { role: "Dept Admin", email: "deptadmin@demo.gov.in" },
  { role: "Super Admin", email: "superadmin@demo.gov.in" },
];

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("Demo@1234");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--navy)" }}>
      <div className="w-full max-w-4xl grid grid-cols-2 rounded-md overflow-hidden shadow-xl">
        <div className="p-10 text-white flex flex-col justify-between" style={{ background: "var(--navy-soft)" }}>
          <div>
            <div className="font-display text-2xl leading-tight mb-2">
              AI-Based Multi-Department<br />Helpdesk
            </div>
            <p className="text-sm opacity-70 leading-relaxed">
              Document-grounded answers and ticket tracking for HR, Finance, IT,
              Pension, and Administration — academic prototype, not an official
              government system.
            </p>
          </div>
          <div className="font-mono text-xs opacity-50 mt-10">
            DEMO LOGINS (password: Demo@1234)
            <ul className="mt-2 space-y-1 opacity-80">
              {DEMO_LOGINS.map((d) => (
                <li key={d.email}>
                  <button
                    type="button"
                    className="underline hover:opacity-100"
                    onClick={() => setEmail(d.email)}
                  >
                    {d.role}: {d.email}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <Card className="rounded-none border-0 p-10">
          <h1 className="font-display text-xl mb-6">Sign in</h1>
          <form onSubmit={handleSubmit}>
            <Field label="Email">
              <input className={inputClass} type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </Field>
            <Field label="Password">
              <input className={inputClass} type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </Field>
            {error && <div className="text-sm mb-4" style={{ color: "var(--danger)" }}>{error}</div>}
            <Button type="submit" disabled={loading} className="w-full">
              {loading ? "Signing in…" : "Sign in"}
            </Button>
          </form>
          <p className="text-sm mt-5" style={{ color: "var(--ink-soft)" }}>
            New employee?{" "}
            <Link to="/register" className="underline" style={{ color: "var(--teal)" }}>
              Register here
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
