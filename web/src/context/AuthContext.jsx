import { createContext, useContext, useEffect, useState } from "react";
import { api, setToken, clearToken, getToken } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function bootstrap() {
      if (getToken()) {
        try {
          const me = await api.me();
          setUser(me);
        } catch {
          clearToken();
        }
      }
      setLoading(false);
    }
    bootstrap();
  }, []);

  async function login(email, password) {
    const data = await api.login(email, password);
    setToken(data.access_token);
    const me = await api.me();
    setUser(me);
    return me;
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
