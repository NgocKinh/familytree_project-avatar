// ===============================================================
// File: userApi.js
// Mô tả:
//   - API client cho Authentication V2 - User Management
//   - Tất cả request đều dùng JWT token
// ===============================================================
import { API_BASE_URL } from "./apiConfig";
const API_BASE = `${API_BASE_URL}/users`;

function getAuthHeaders() {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

export async function getUsers() {
  const res = await fetch(`${API_BASE}/`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  if (!res.ok) {
    throw new Error("Không tải được danh sách user");
  }

  return await res.json();
}

export async function createUser(data) {
  const res = await fetch(`${API_BASE}/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Không tạo được user");
  }

  return await res.json();
}

export async function updateUser(userId, data) {
  const res = await fetch(`${API_BASE}/${userId}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Không cập nhật được user");
  }

  return await res.json();
}

export async function lockUser(userId) {
  const res = await fetch(`${API_BASE}/${userId}/lock`, {
    method: "PUT",
    headers: getAuthHeaders(),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Không khóa được user");
  }

  return await res.json();
}

export async function unlockUser(userId) {
  const res = await fetch(`${API_BASE}/${userId}/unlock`, {
    method: "PUT",
    headers: getAuthHeaders(),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Không mở khóa được user");
  }

  return await res.json();
}

export async function resetPassword(userId, password) {
  const res = await fetch(`${API_BASE}/${userId}/reset-password`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify({ password }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Không reset được password");
  }

  return await res.json();
}