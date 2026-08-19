import { api } from "./client";

// Replace these examples with your hackathon's real endpoints.
export const exampleApi = {
  getItems: async () => (await api.get("/items")).data,
  getItem: async (id) => (await api.get(`/items/${id}`)).data,
  createItem: async (payload) => (await api.post("/items", payload)).data,
  updateItem: async (id, payload) => (await api.put(`/items/${id}`, payload)).data,
  deleteItem: async (id) => (await api.delete(`/items/${id}`)).data,
};
