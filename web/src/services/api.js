import axios from 'axios';

const configuredApiUrl = import.meta.env.VITE_API_BASE_URL;
const isProduction = import.meta.env.MODE === 'production';

const api = axios.create({
  // A deployed frontend must use its hosted API, never the visitor's localhost.
  baseURL: configuredApiUrl || (isProduction ? '' : 'http://localhost:8000'),
  headers: {
    'Content-Type': 'application/json',
  },
});

export const backendIsConfigured = Boolean(configuredApiUrl) || !isProduction;
export const backendSetupMessage =
  'The helpdesk service is still being connected. Please try again shortly.';

export const createEmployee = (employee) => api.post('/admin/employees', employee);

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
