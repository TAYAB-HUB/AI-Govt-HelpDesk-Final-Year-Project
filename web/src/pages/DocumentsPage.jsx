import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Card, Button, Field, inputClass } from "../components/ui";

export default function DocumentsPage() {
  const { user } = useAuth();
  const [departments, setDepartments] = useState([]);
  const [departmentId, setDepartmentId] = useState("");
  const [documents, setDocuments] = useState([]);
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.listDepartments().then((depts) => {
      setDepartments(depts);
      const initial = user?.department_id ? String(user.department_id) : String(depts[0]?.id || "");
      setDepartmentId(initial);
    });
  }, [user]);

  useEffect(() => {
    if (departmentId) api.listDocuments(Number(departmentId)).then(setDocuments);
  }, [departmentId]);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file || !title) return;
    setUploading(true);
    setError("");
    try {
      await api.uploadDocument(Number(departmentId), title, file);
      setTitle("");
      setFile(null);
      e.target.reset();
      api.listDocuments(Number(departmentId)).then(setDocuments);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(docId) {
    if (!confirm("Remove this document from the knowledge base?")) return;
    await api.deleteDocument(docId);
    setDocuments((docs) => docs.filter((d) => d.id !== docId));
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl">Documents</h1>
        <select className={inputClass + " w-56"} value={departmentId} onChange={(e) => setDepartmentId(e.target.value)}>
          {departments.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
      </div>

      <Card className="p-5 mb-6">
        <h2 className="font-display text-lg mb-3">Upload a new document</h2>
        <form onSubmit={handleUpload} className="flex flex-col gap-3 sm:flex-row sm:items-end">
          <Field label="Title">
            <input className={inputClass} required value={title} onChange={(e) => setTitle(e.target.value)} />
          </Field>
          <Field label="File (PDF, TXT, or MD)">
            <input className={inputClass} type="file" accept=".pdf,.txt,.md" required
              onChange={(e) => setFile(e.target.files[0])} />
          </Field>
          <Button type="submit" disabled={uploading} className="whitespace-nowrap">
            {uploading ? "Ingesting…" : "Upload & ingest"}
          </Button>
        </form>
        {error && <div className="text-sm mt-3" style={{ color: "var(--danger)" }}>{error}</div>}
      </Card>

      <div className="space-y-2">
        {documents.map((d) => (
          <Card key={d.id} className="p-4 flex items-center justify-between">
            <div>
              <div className="font-medium text-sm">{d.title}</div>
              <div className="text-xs font-mono" style={{ color: "var(--ink-soft)" }}>
                {d.filename} · {d.chunk_count} chunks · {d.source_type}
              </div>
            </div>
            <button
              onClick={() => handleDelete(d.id)}
              className="text-xs underline"
              style={{ color: "var(--danger)" }}
            >
              Remove
            </button>
          </Card>
        ))}
        {documents.length === 0 && (
          <p className="text-sm" style={{ color: "var(--ink-soft)" }}>No documents in this department yet.</p>
        )}
      </div>
    </div>
  );
}
