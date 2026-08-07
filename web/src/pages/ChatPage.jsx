import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Card, Button, inputClass } from "../components/ui";

export default function ChatPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [departments, setDepartments] = useState([]);
  const [departmentId, setDepartmentId] = useState("");
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    api.listDepartments().then((depts) => {
      setDepartments(depts);
      if (user?.department_id) setDepartmentId(String(user.department_id));
      else if (depts.length) setDepartmentId(String(depts[0].id));
    });
  }, [user]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleAsk(e) {
    e.preventDefault();
    if (!question.trim() || !departmentId) return;
    const q = question;
    setQuestion("");
    setAsking(true);
    setMessages((m) => [...m, { role: "user", text: q }]);
    try {
      const resp = await api.askChat(Number(departmentId), q);
      setMessages((m) => [...m, { role: "assistant", ...resp }]);
    } catch (err) {
      setMessages((m) => [...m, { role: "assistant", answer: `Error: ${err.message}`, sources: [] }]);
    } finally {
      setAsking(false);
    }
  }

  async function handleFeedback(chat_log_id, vote, idx) {
    try {
      await api.sendFeedback(chat_log_id, vote);
      setMessages((m) => m.map((msg, i) => (i === idx ? { ...msg, feedbackGiven: vote } : msg)));
    } catch {
      /* non-critical */
    }
  }

  function raiseTicket(originChatLogId, presetQuestion) {
    navigate("/tickets/new", {
      state: { department_id: Number(departmentId), origin_chat_log_id: originChatLogId, subject: presetQuestion },
    });
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex items-center justify-between mb-4">
        <h1 className="font-display text-2xl">Ask the helpdesk</h1>
        <select
          className={inputClass + " w-56"}
          value={departmentId}
          onChange={(e) => { setDepartmentId(e.target.value); setMessages([]); }}
        >
          {departments.map((d) => (
            <option key={d.id} value={d.id}>{d.name}</option>
          ))}
        </select>
      </div>

      <Card className="flex-1 overflow-y-auto scrollbar-thin p-6 mb-4">
        {messages.length === 0 && (
          <p className="text-sm" style={{ color: "var(--ink-soft)" }}>
            Ask about leave, payroll, IT issues, pension, or office admin rules for the
            selected department. Answers are grounded in approved documents, with sources shown below each answer.
          </p>
        )}
        <div className="space-y-5">
          {messages.map((m, i) =>
            m.role === "user" ? (
              <div key={i} className="flex justify-end">
                <div className="rounded-md px-4 py-2 max-w-lg text-sm text-white" style={{ background: "var(--navy)" }}>
                  {m.text}
                </div>
              </div>
            ) : (
              <div key={i} className="max-w-2xl">
                <div className="rounded-md px-4 py-3 text-sm border" style={{ borderColor: "var(--line)", background: "var(--paper-raised)" }}>
                  <p className="whitespace-pre-wrap">{m.answer}</p>

                  {m.sources?.length > 0 && (
                    <>
                      <hr className="ledger-divider" />
                      <div className="space-y-1">
                        {m.sources.map((s, si) => (
                          <div key={si} className="text-xs flex gap-2" style={{ color: "var(--ink-soft)" }}>
                            <span className="font-mono shrink-0" style={{ color: "var(--teal)" }}>[{si + 1}]</span>
                            <span><strong>{s.document_title}</strong> — {(s.score * 100).toFixed(0)}% match</span>
                          </div>
                        ))}
                      </div>
                    </>
                  )}

                  {m.suggest_ticket && (
                    <div className="mt-3 pt-3 border-t flex items-center justify-between" style={{ borderColor: "var(--line)" }}>
                      <span className="text-xs" style={{ color: "var(--amber)" }}>
                        Low confidence — you may want a human to help.
                      </span>
                      <Button variant="secondary" onClick={() => raiseTicket(m.chat_log_id, messages[i - 1]?.text)}>
                        Raise a ticket
                      </Button>
                    </div>
                  )}
                </div>
                {m.chat_log_id && (
                  <div className="flex gap-2 mt-1.5 ml-1">
                    <button
                      onClick={() => handleFeedback(m.chat_log_id, "up", i)}
                      className="text-xs"
                      style={{ color: m.feedbackGiven === "up" ? "var(--teal)" : "var(--ink-soft)" }}
                    >
                      👍 Helpful
                    </button>
                    <button
                      onClick={() => handleFeedback(m.chat_log_id, "down", i)}
                      className="text-xs"
                      style={{ color: m.feedbackGiven === "down" ? "var(--danger)" : "var(--ink-soft)" }}
                    >
                      👎 Not helpful
                    </button>
                  </div>
                )}
              </div>
            )
          )}
          <div ref={bottomRef} />
        </div>
      </Card>

      <form onSubmit={handleAsk} className="flex gap-2">
        <input
          className={inputClass}
          placeholder="e.g. How many days of earned leave do I get?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={asking}
        />
        <Button type="submit" disabled={asking || !question.trim()}>
          {asking ? "Thinking…" : "Ask"}
        </Button>
      </form>
    </div>
  );
}
