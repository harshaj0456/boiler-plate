import apiClient from "./client";

export const authApi = {
  login: (payload) => apiClient.post("/auth/login", payload),

  register: (payload) =>
    apiClient.post("/auth/register", payload),

  me: () => apiClient.get("/auth/me"),
};

export function setAccessToken(token) {
  if (token) {
    localStorage.setItem("access_token", token);
  }
}

export function getAccessToken() {
  return localStorage.getItem("access_token");
}

export function clearAccessToken() {
  localStorage.removeItem("access_token");
}