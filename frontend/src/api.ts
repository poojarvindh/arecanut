// In the browser dev server, relative "/api" works via the Vite proxy.
// Packaged into the Android app there's no dev-server proxy, so the mobile
// build is compiled with VITE_API_BASE pointing at the backend's real host.
const BASE = import.meta.env.VITE_API_BASE || "/api";
const TOKEN_KEY = "gt_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}
export function setToken(token: string | null) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

// Fired whenever a request comes back 401 so the app can force a re-login.
export const AUTH_EVENT = "gt-auth-expired";

async function req(path: string, options?: RequestInit) {
  const token = getToken();
  const res = await fetch(`${BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...options,
  });
  if (res.status === 401) {
    setToken(null);
    window.dispatchEvent(new Event(AUTH_EVENT));
    throw new Error("Session expired — please log in again.");
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  login: (username: string, password: string) =>
    req("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) }),
  me: () => req("/auth/me"),
  districts: () => req("/masters/districts"),
  talukas: (district: string) => req(`/masters/talukas?district=${encodeURIComponent(district)}`),
  villages: (district: string, taluka: string) =>
    req(`/masters/villages?district=${encodeURIComponent(district)}&taluka=${encodeURIComponent(taluka)}`),
  villagesFlat: (): Promise<{ village: string; taluka: string; district: string }[]> => req("/masters/villages-flat"),
  societies: () => req("/masters/societies"),
  crops: () => req("/masters/crops"),
  schemes: () => req("/masters/schemes"),
  machines: () => req("/masters/machines"),
  options: (listCode: string) => req(`/masters/options?list_code=${encodeURIComponent(listCode)}`),
  lookupFarmer: (q: string) => req(`/farmer-master/lookup?q=${encodeURIComponent(q)}`),
  listSurveys: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return req(`/surveys${qs}`);
  },
  getSurvey: (id: number) => req(`/surveys/${id}`),
  createSurvey: (data: any) => req("/surveys", { method: "POST", body: JSON.stringify(data) }),
  updateSurvey: (id: number, data: any) => req(`/surveys/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteSurvey: (id: number) => req(`/surveys/${id}`, { method: "DELETE" }),
  dashboardKpis: () => req("/dashboard/kpis"),
  yieldBenchmarks: () => req("/dashboard/yield-benchmarks"),
};
