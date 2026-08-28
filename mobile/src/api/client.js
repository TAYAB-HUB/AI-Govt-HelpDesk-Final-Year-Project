import AsyncStorage from "@react-native-async-storage/async-storage";

const BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL || "http://localhost:8000";
const TOKEN_KEY = "helpdesk_token";

export async function getToken() {
  return AsyncStorage.getItem(TOKEN_KEY);
}
export async function setToken(token) {
  await AsyncStorage.setItem(TOKEN_KEY, token);
}
export async function clearToken() {
  await AsyncStorage.removeItem(TOKEN_KEY);
}

async function request(path, { method = "GET", body, params } = {}) {
  let url = `${BASE_URL}${path}`;
  if (params) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null)
    ).toString();
    if (qs) url += `?${qs}`;
  }

  const headers = { "Content-Type": "application/json" };
  const token = await getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const resp = await fetch(url, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
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
  login: (email, password) => request("/api/auth/login", { method: "POST", body: { email, password } }),
  me: () => request("/api/auth/me"),
  listDepartments: () => request("/api/departments"),
  askChat: (department_id, question) =>
    request("/api/chat/ask", { method: "POST", body: { department_id, question } }),
  chatHistory: (department_id) => request("/api/chat/history", { params: { department_id } }),
  createTicket: (payload) => request("/api/tickets", { method: "POST", body: payload }),
  listTickets: () => request("/api/tickets"),
  getTicket: (id) => request(`/api/tickets/${id}`),
};
