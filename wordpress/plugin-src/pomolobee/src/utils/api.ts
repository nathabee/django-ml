// src/utils/api.ts
import axios from "axios";

function getApiBase(): string {
  // comes from your plugin’s wp_localize_script
  const raw = (window as any)?.pomolobeeSettings?.apiUrl || "http://localhost:8001/api";
  return raw.replace(/\/+$/, ""); // strip trailing slash
}

export const api = axios.create({
  baseURL: getApiBase(),
  timeout: 15000,
});

// Attach token on the fly
export function authHeaders(token: string | null) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}
