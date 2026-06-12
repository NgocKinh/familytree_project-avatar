// =============================================================
// File: src/api/personDetailApi.js (v1.5 – FULL, CLEAN, READY)
// Mô tả:
//   - Gọi API chi tiết thành viên
//   - Đồng bộ endpoint: /api/person/detail
//   - Hỗ trợ GET / POST / PUT
//   - Có alias getPersonDetail để PersonDetailForm dùng
// =============================================================
import { handleAuthError } from "../utils/authErrorHandler";
const BASE_URL = "http://localhost:8000/api/person";
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
// -------------------------------------------------------------
// 🔹 Lấy chi tiết 1 person theo ID
// -------------------------------------------------------------
export async function getPersonDetailById(personId) {
  const res = await fetch(`${BASE_URL}/${personId}`, {
    headers: getAuthHeaders(),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không thể tải dữ liệu chi tiết");
  return res.json();
}

// -------------------------------------------------------------
// ⭐ Alias cho PersonDetailForm (đang gọi getPersonDetail)
// -------------------------------------------------------------
export const getPersonDetail = getPersonDetailById;

// -------------------------------------------------------------
// 🔹 Thêm mới chi tiết (ADD)
// -------------------------------------------------------------
export async function addPersonDetail(payload) {
  const res = await fetch(`${BASE_URL}`, {
    method: "POST",
    headers: getAuthHeaders({
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không thể thêm chi tiết");
  return res.json();
}

// -------------------------------------------------------------
// 🔹 Cập nhật chi tiết (UPDATE)
// -------------------------------------------------------------
export async function updatePersonDetail(personId, payload) {
  const res = await fetch(`${BASE_URL}/${personId}`, {
    method: "PUT",
    headers: getAuthHeaders({
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  });

  if (handle401(res)) return;

  if (!res.ok) throw new Error("Không thể cập nhật chi tiết");
  return res.json();
}


