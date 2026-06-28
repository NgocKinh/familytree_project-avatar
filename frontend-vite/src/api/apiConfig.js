// src/api/apiConfig.js
// ===============================
// 🔹 Cấu hình API dùng chung cho toàn project
// ===============================

// Tự động nhận môi trường (development / production)
export const isDev = import.meta.env.MODE === "development";

// Backend URLs

export const API_FASTAPI =
  import.meta.env.VITE_API_BASE_URL ||
  "https://dynamic-kindness-production-4485.up.railway.app/api";

export const API_BASE_URL = API_FASTAPI;

// Hàm tiện ích để tạo URL động (nếu muốn)
export const makeApiUrl = (endpoint) => {
  const url = `${API_BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;
  console.log("🔗 makeApiUrl:", url);
  return url;
};