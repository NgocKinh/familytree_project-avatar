import { handleAuthError } from "./authErrorHandler";
import { API_BASE_URL } from "../api/apiConfig";

export async function apiClient(path, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    ...(options.headers || {}),
  };

  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    handleAuthError({ response: { status: 401 } });
    throw new Error("Phiên đăng nhập đã hết hạn hoặc không hợp lệ");
  }

  return res;
}