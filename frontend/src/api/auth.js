// src/api/auth.js

let accessToken = null;

export const setAccessToken = (token) => {
  accessToken = token;
  if (token) {
    localStorage.setItem("access_token", token);
  }
};

export const getAccessToken = () => accessToken || localStorage.getItem("access_token");

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const authApi = {
  login: async (data) => {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return response.json();
  },

  register: async (data) => {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return response.json();
  },

  logout: async () => {
    const response = await fetch(`${API_URL}/api/auth/logout`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${getAccessToken()}`
      }
    });
    setAccessToken(null);
    return response.json();
  }
};