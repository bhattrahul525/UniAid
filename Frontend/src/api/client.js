import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
});

api.interceptors.request.use((config) => {
  const storedAuth = localStorage.getItem("auth");
  const token = storedAuth ? JSON.parse(storedAuth).token : null;

  if (token) {
    config.headers.Authorization = token;
  }

  config.headers["Ngrok-Skip-Browser-Warning"] = "true";

  return config;
});

export default api;