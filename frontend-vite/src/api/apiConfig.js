// src/api/apiConfig.js
// ===============================
// 🔹 Cấu hình API dùng chung cho toàn project
// ===============================

// Tự động nhận môi trường (development / production)
export const isDev = import.meta.env.MODE === "development";

// Backend URLs

export const API_FASTAPI =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000/api";

export const API_BASE_URL = API_FASTAPI;


// Hàm tiện ích để tạo URL động (nếu muốn)
export const makeApiUrl = (endpoint) =>
  `${API_BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;
