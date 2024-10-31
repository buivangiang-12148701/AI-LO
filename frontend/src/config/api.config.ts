export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
};

export const API_ENDPOINTS = {
  chat: "/api/chat",
  menu: "/api/menu",
  train: "/api/train",
  dishes: "/api/dishes",
  categories: "/api/categories",
};
