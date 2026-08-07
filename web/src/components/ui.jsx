export function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-white rounded-md border border-[var(--line)] shadow-sm ${className}`}
      style={{ background: "var(--paper-raised)" }}
    >
      {children}
    </div>
  );
}

export function Button({ children, variant = "primary", className = "", ...props }) {
  const base = "px-4 py-2 rounded-sm text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed";
  const variants = {
    primary: "text-white",
    secondary: "border",
    ghost: "hover:bg-black/5",
  };
  const style =
    variant === "primary"
      ? { background: "var(--navy)" }
      : variant === "secondary"
      ? { borderColor: "var(--line)", color: "var(--ink)" }
      : {};
  return (
    <button className={`${base} ${variants[variant]} ${className}`} style={style} {...props}>
      {children}
    </button>
  );
}

export function StatusStamp({ status }) {
  const map = {
    open: { color: "var(--amber)" },
    in_progress: { color: "var(--teal)" },
    resolved: { color: "var(--navy)" },
    closed: { color: "var(--ink-soft)" },
  };
  const style = map[status] || { color: "var(--ink-soft)" };
  return <span className="stamp" style={style}>{status?.replace("_", " ")}</span>;
}

export function PriorityTag({ priority }) {
  const map = {
    low: "var(--ink-soft)",
    medium: "var(--amber)",
    high: "var(--danger)",
    urgent: "var(--danger)",
  };
  return (
    <span
      className="font-mono text-xs uppercase tracking-wide px-2 py-0.5 rounded-sm border"
      style={{ color: map[priority] || "var(--ink-soft)", borderColor: map[priority] || "var(--line)" }}
    >
      {priority}
    </span>
  );
}

export function Field({ label, children }) {
  return (
    <label className="block mb-4">
      <span className="block text-sm font-medium mb-1" style={{ color: "var(--ink-soft)" }}>{label}</span>
      {children}
    </label>
  );
}

export const inputClass =
  "w-full px-3 py-2 rounded-sm border border-[var(--line)] bg-white focus:outline-none focus:ring-2 focus:ring-[var(--teal)] text-sm";
