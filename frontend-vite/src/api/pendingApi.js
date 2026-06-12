// =======================================================================
// File: src/api/pendingApi.js
// =======================================================================
import { handleAuthError } from "../utils/authErrorHandler";
import { API_BASE_URL } from "./apiConfig";
const BASE = `${API_BASE_URL}/person_pending`;

function getAuthHeaders(extraHeaders = {}) {
  const token = localStorage.getItem("token");

  return {
    ...extraHeaders,
    Authorization: `Bearer ${token}`,
  };
}

function handle401(res) {
  if (res.status === 401) {
    handleAuthError({ response: { status: 401 } });
    return true;
  }

  return false;
}

// 🟦 1) Lấy danh sách pending
export async function getPendingList() {
  const res = await fetch(BASE, {
    headers: getAuthHeaders(),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không lấy được danh sách pending");
  return await res.json();
}

// 🟦 2) Lấy chi tiết 1 pending
export async function getPendingDetail(id) {
  const res = await fetch(`${BASE}/${id}`, {
    headers: getAuthHeaders(),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không lấy được chi tiết pending");
  return await res.json();
}

// 🟩 3) Cập nhật pending
export async function updatePending(id, payload) {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: getAuthHeaders({
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không cập nhật được pending");
  return await res.json();
}

// 🟩 4) Duyệt pending
export async function approvePending(id) {
  const res = await fetch(`${BASE}/approve/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không duyệt được pending");
  return await res.json();
}

// 🟥 5) Hủy duyệt
export async function cancelPending(id) {
  const res = await fetch(`${BASE}/cancel/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không thể hủy duyệt");
  return await res.json();
}

// 🗑 6) Xóa pending
export async function deletePending(id) {
  const res = await fetch(`${BASE}/delete/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không thể xóa pending");
  return await res.json();
}

