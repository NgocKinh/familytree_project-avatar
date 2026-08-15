// src/api/apiConfig.js
// ===============================
// 🔹 Cấu hình API dùng chung cho toàn project
// ===============================

// Tự động nhận môi trường (development / production)
export const isDev = import.meta.env.MODE === "development";

// Backend URLs

const configuredApiBaseUrl =
  import.meta.env.VITE_API_BASE_URL?.trim();

if (!configuredApiBaseUrl && !isDev) {
  throw new Error(
    "Missing VITE_API_BASE_URL. Configure the Railway backend URL before deployment."
  );
}

export const API_FASTAPI =
  configuredApiBaseUrl || "http://127.0.0.1:8000/api";

export const API_BASE_URL = API_FASTAPI;

// Hàm tiện ích để tạo URL động (nếu muốn)
export const makeApiUrl = (endpoint) => {
  const url = `${API_BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;

  return url;
};