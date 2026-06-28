// =======================================================
// File: src/api/personApi.js (v7.0-FINAL-STABLE-FASTAPI)
// Mô tả:
//   - Đồng bộ hoàn toàn với FastAPI
//   - Giữ nguyên cấu trúc file cũ
//   - Không phá UI hiện tại
// =======================================================
import axios from "axios";
import { handleAuthError } from "../utils/authErrorHandler";
import { API_BASE_URL } from "./apiConfig";
// ============================================
// BASE URL
// ============================================
// ❌ Flask (không dùng nữa)
// const PERSON_URL = "http://127.0.0.1:5000/api/person";

// ✅ FastAPI
const API_URL = `${API_BASE_URL}/person`;
const AVATAR_URL = `${API_BASE_URL}/avatar/upload`;
const BACKEND_BASE_URL = API_BASE_URL.replace("/api", "");
// ============================================
// LẤY DANH SÁCH PERSON
// ============================================
export const getPersonList = async () => {
  try {

    const res = await axios.get(`${API_URL}/`, {
      timeout: 5000,
      params: { include_hidden: true },
    });

    // ✅ tương thích cả format cũ và mới
    if (Array.isArray(res.data)) return res.data;
    if (res.data?.persons) return res.data.persons;
    if (res.data?.data) return res.data.data;

    return [];
  } catch (err) {
    if (handleAuthError(err)) {
      return [];
    }
    console.error("❌ API ERROR:", err);

    // 🔁 retry 1 lần
    try {
      const res = await axios.get(`${API_URL}/`, {
        timeout: 5000,
        params: { include_hidden: true },
      });

      if (Array.isArray(res.data)) return res.data;
      if (res.data?.persons) return res.data.persons;
      if (res.data?.data) return res.data.data;

      return [];
    } catch (err2) {
      if (handleAuthError(err2)) {
        return [];
      }
      console.error("💥 RETRY FAIL:", err2);
      return [];
    }
  }
};

// Alias cũ
export const getAllPersons = getPersonList;

// ============================================
// SOFT DELETE (tạm giữ nếu backend chưa đổi)
// ============================================
export const softDeletePerson = async (id) => {
  try {
    return await axios.put(`${API_URL}/delete_soft/${id}`);
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }

    throw err;
  }
};

// ============================================
// RESTORE
// ============================================
export const restorePerson = async (id) => {
  try {
    return await axios.put(`${API_URL}/restore/${id}`);
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }

    throw err;
  }
};

// ============================================
// HARD DELETE
// ============================================
export const hardDeletePerson = async (id) => {
  try {
    return await axios.delete(`${API_URL}/delete_permanent/${id}`);
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }

    throw err;
  }
};

// ============================================
// GET DETAIL
// ============================================
export const getPersonById = async (id) => {
  try {
    const res = await axios.get(`${API_URL}/${id}`);
    return res.data;
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }
    console.error(`❌ Lỗi khi lấy chi tiết ID=${id}:`, err);
    throw err;
  }
};

// ============================================
// CREATE PERSON
// ============================================
export const addPerson = async (data) => {
  try {
    const res = await axios.post(`${API_URL}`, data, {
      headers: { "Content-Type": "application/json" },
    });
    return res.data;
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }
  
    console.error("❌ Lỗi thêm người mới:", err);
    throw err;
  }
};

// ============================================
// UPDATE PERSON
// ============================================
export const updatePerson = async (id, data) => {
  try {
    const res = await axios.put(`${API_URL}/${id}`, data, {
      headers: { "Content-Type": "application/json" },
    });
    return res.data;
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }
    console.error(`❌ Lỗi cập nhật ID=${id}:`, err);
    throw err;
  }
};

// ============================================
// CHECK DUPLICATE
// ============================================
export const checkDuplicatePerson = async (data) => {
  const res = await axios.post(`${API_URL}/check_duplicate`, data);
  return res.data;
};

// ============================================
// UPLOAD AVATAR
// ============================================
export const uploadAvatar = async (personId, file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await axios.post(`${AVATAR_URL}/${personId}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return res.data;
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }
    console.error("❌ Lỗi upload avatar:", err);
    throw err;
  }
};

// ============================================
// GET AVATAR URL (ANTI CACHE)
// ============================================
export const getAvatarURL = (person) => {
  if (!person) return "";

  const id = person.id || person.person_id;
  const gender = person.gender || "other";

  // ưu tiên avatar thật
  return `${BACKEND_BASE_URL}/static/avatars/${id}.jpg?t=${Date.now()}`;
};
// ============================================
// GET PERSON FAMILY OVERVIEW
// ============================================
export const getPersonFamilyOverview = async (personId) => {
  try {
    const res = await axios.get(
      `${API_BASE_URL}/parent_child/person/${personId}/family`
    );

    return res.data;
  } catch (err) {
    if (handleAuthError(err)) {
      return null;
    }

    console.error(`❌ Lỗi lấy gia đình trực hệ ID=${personId}:`, err);
    return null;
  }
};