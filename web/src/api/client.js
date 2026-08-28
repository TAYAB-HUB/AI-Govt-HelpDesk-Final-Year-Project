const BASE_URL = import.meta.env.VITE_API_BASE_URL !== undefined 
  ? import.meta.env.VITE_API_BASE_URL 
  : (import.meta.env.MODE === "production" ? "" : "http://localhost:8000");

function getToken() {
  return localStorage.getItem("helpdesk_token");
}

async function request(path, { method = "GET", body, params, isForm = false } = {}) {
  let url = `${BASE_URL}${path}`;
  if (params) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null)
    ).toString();
    if (qs) url += `?${qs}`;
  }

  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (!isForm && body !== undefined) headers["Content-Type"] = "application/json";

  const resp = await fetch(url, {
    method,
    headers,
    body: isForm ? body : body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (resp.status === 204) return null;

  let data = null;
  try {
    data = await resp.json();
  } catch {
    data = null;
  }

  if (!resp.ok) {
    const message = data?.detail
      ? Array.isArray(data.detail)
        ? data.detail.map((d) => d.msg).join(", ")
        : data.detail
      : `Request failed (${resp.status})`;
    throw new Error(message);
  }
  return data;
}

export const api = {
  // auth
  login: (email, password) => request("/api/auth/login", { method: "POST", body: { email, password } }),
  register: (payload) => request("/api/auth/register", { method: "POST", body: payload }),
  me: () => request("/api/auth/me"),

  // departments
  listDepartments: () => request("/api/departments"),
  createDepartment: (payload) => request("/api/departments", { method: "POST", body: payload }),

  // documents
  listDocuments: (department_id) => request("/api/documents", { params: { department_id } }),
  uploadDocument: (department_id, title, file) => {
    const form = new FormData();
    form.append("file", file);
    return request(`/api/documents/upload?department_id=${department_id}&title=${encodeURIComponent(title)}`, {
      method: "POST",
      body: form,
      isForm: true,
    });
  },
  deleteDocument: (id) => request(`/api/documents/${id}`, { method: "DELETE" }),

  // chat
  askChat: (department_id, question) => request("/api/chat/ask", { method: "POST", body: { department_id, question } }),
  chatHistory: (department_id) => request("/api/chat/history", { params: { department_id } }),
  sendFeedback: (chat_log_id, vote) => request("/api/chat/feedback", { method: "POST", body: { chat_log_id, vote } }),

  // tickets
  createTicket: (payload) => request("/api/tickets", { method: "POST", body: payload }),
  listTickets: (status) => request("/api/tickets", { params: { status } }),
  getTicket: (id) => request(`/api/tickets/${id}`),
  addComment: (id, payload) => request(`/api/tickets/${id}/comments`, { method: "POST", body: payload }),
  assignTicket: (id, assigned_to_id) => request(`/api/tickets/${id}/assign`, { method: "POST", body: { assigned_to_id } }),

  // dashboard
  analytics: (department_id) => request("/api/dashboard/analytics", { params: { department_id } }),

  // admin
  auditLogs: (limit = 100) => request("/api/admin/audit-logs", { params: { limit } }),
  listUsers: (department_id) => request("/api/admin/users", { params: { department_id } }),
  changeRole: (userId, role) => request(`/api/admin/users/${userId}/role?role=${role}`, { method: "PATCH" }),
  toggleActive: (userId) => request(`/api/admin/users/${userId}/toggle-active`, { method: "PATCH" }),
};

export function setToken(token) {
  localStorage.setItem("helpdesk_token", token);
}
export function clearToken() {
  localStorage.removeItem("helpdesk_token");
}
export { getToken };
