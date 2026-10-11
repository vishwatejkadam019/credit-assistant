import axios from "axios";

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000" });

api.interceptors.request.use((c) => {
  const t = localStorage.getItem("token");
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});
api.interceptors.response.use((r) => r, (e) => {
  if (e.response?.status === 401 && localStorage.getItem("token")) {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
  return Promise.reject(e);
});

export const errMsg = (e) => {
  const d = e.response?.data?.detail;
  if (Array.isArray(d)) return d.map((x) => x.msg).join(". ");
  return d || "Could not reach the server. Check your connection and try again.";
};
export const inr = (n) =>
  new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(n);
export default api;
