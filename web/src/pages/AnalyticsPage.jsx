import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { api } from "../api/client";
import { Card } from "../components/ui";

const COLORS = ["#17233f", "#127a6b", "#b8791e", "#b4432f", "#6b7280"];

export default function AnalyticsPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.analytics().then(setData);
  }, []);

  if (!data) return <p style={{ color: "var(--ink-soft)" }}>Loading…</p>;

  const statusData = Object.entries(data.tickets_by_status).map(([status, count]) => ({ status, count }));
  const categoryData = Object.entries(data.tickets_by_category).map(([name, value]) => ({ name, value }));

  return (
    <div>
      <h1 className="font-display text-2xl mb-6">Analytics</h1>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <Card className="p-5">
          <div className="text-3xl font-display">{data.total_tickets}</div>
          <div className="text-sm" style={{ color: "var(--ink-soft)" }}>Total tickets</div>
        </Card>
        <Card className="p-5">
          <div className="text-3xl font-display">{data.total_documents}</div>
          <div className="text-sm" style={{ color: "var(--ink-soft)" }}>Documents in knowledge base</div>
        </Card>
        <Card className="p-5">
          <div className="text-3xl font-display">{data.total_chats}</div>
          <div className="text-sm" style={{ color: "var(--ink-soft)" }}>Chatbot questions asked</div>
        </Card>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-8">
        <Card className="p-5">
          <h2 className="font-display text-lg mb-4">Tickets by status</h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--line)" />
              <XAxis dataKey="status" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="count" fill="var(--teal)" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card className="p-5">
          <h2 className="font-display text-lg mb-4">Tickets by category</h2>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={categoryData} dataKey="value" nameKey="name" outerRadius={80} label={{ fontSize: 11 }}>
                {categoryData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <Card className="p-5">
        <h2 className="font-display text-lg mb-4">Most common employee questions</h2>
        {data.common_questions.length === 0 ? (
          <p className="text-sm" style={{ color: "var(--ink-soft)" }}>No chat history yet.</p>
        ) : (
          <ol className="space-y-2">
            {data.common_questions.map((q, i) => (
              <li key={i} className="text-sm flex gap-2">
                <span className="font-mono" style={{ color: "var(--ink-soft)" }}>{i + 1}.</span>
                {q}
              </li>
            ))}
          </ol>
        )}
      </Card>
    </div>
  );
}
