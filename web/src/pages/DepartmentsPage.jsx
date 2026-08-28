import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Card, Field, inputClass, Button } from "../components/ui";

export default function DepartmentsPage() {
  const [departments, setDepartments] = useState([]);
  const [form, setForm] = useState({ name: "", code: "", description: "" });
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => { api.listDepartments().then(setDepartments); }, []);

  async function handleCreate(e) {
    e.preventDefault();
    setError("");
    setCreating(true);
    try {
      await api.createDepartment(form);
      setForm({ name: "", code: "", description: "" });
      api.listDepartments().then(setDepartments);
    } catch (err) {
      setError(err.message);
    } finally {
      setCreating(false);
    }
  }

  return (
    <div>
      <h1 className="font-display text-2xl mb-6">Departments</h1>

      <Card className="p-5 mb-6">
        <h2 className="font-display text-lg mb-3">Add a department</h2>
        <form onSubmit={handleCreate} className="grid grid-cols-3 gap-3 items-end">
          <Field label="Name">
            <input className={inputClass} required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          </Field>
          <Field label="Code">
            <input className={inputClass} required value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value.toUpperCase() })} />
          </Field>
          <Field label="Description">
            <input className={inputClass} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          </Field>
          <div className="col-span-3">
            {error && <div className="text-sm mb-2" style={{ color: "var(--danger)" }}>{error}</div>}
            <Button type="submit" disabled={creating}>{creating ? "Creating…" : "Create department"}</Button>
          </div>
        </form>
      </Card>

      <div className="space-y-2">
        {departments.map((d) => (
          <Card key={d.id} className="p-4">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs px-2 py-0.5 rounded-sm" style={{ background: "var(--teal-soft)", color: "var(--teal)" }}>
                {d.code}
              </span>
              <span className="font-medium text-sm">{d.name}</span>
            </div>
            {d.description && <p className="text-sm mt-1" style={{ color: "var(--ink-soft)" }}>{d.description}</p>}
          </Card>
        ))}
      </div>
    </div>
  );
}
