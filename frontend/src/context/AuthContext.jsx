import { createContext, useContext, useMemo, useState } from 'react';
import { authApi } from '../services/api';
const AuthContext = createContext(null);
export function AuthProvider({ children }) { const [token, setToken] = useState(() => localStorage.getItem('vocalize_token')); const [authError, setAuthError] = useState('');
  const finish = (value) => { localStorage.setItem('vocalize_token', value); setToken(value); setAuthError(''); };
  const login = async (email, password) => { try { finish((await authApi.login({ email, password })).data.access_token); } catch (e) { setAuthError(e.response?.data?.detail || 'Unable to sign in'); throw e; } };
  const register = async (email, password) => { try { finish((await authApi.register({ email, password })).data.access_token); } catch (e) { setAuthError(e.response?.data?.detail || 'Unable to create account'); throw e; } };
  const logout = () => { localStorage.removeItem('vocalize_token'); setToken(null); };
  const value = useMemo(() => ({ token, isAuthenticated: Boolean(token), login, register, logout, authError }), [token, authError]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
