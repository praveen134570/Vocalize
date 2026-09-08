import axios from 'axios';

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const api = axios.create({ baseURL: API_URL });
api.interceptors.request.use((config) => { const token = localStorage.getItem('vocalize_token'); if (token) config.headers.Authorization = `Bearer ${token}`; return config; });
export const authApi = { register: (data) => api.post('/auth/register', data), login: (data) => api.post('/auth/login', data) };
export const speechApi = { voices: () => api.get('/api/voices'), generate: (data) => api.post('/api/tts', data), history: () => api.get('/api/history') };
export const parseUpload = (file) => { const form = new FormData(); form.append('file', file); return api.post('/api/parse-file', form); };
export default api;
